from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
import os
import re, json as pyjson
from .models import UserProfile, Job, Application, JobRequest, WorkExample
from .forms import UserRegistrationForm, JobForm, ApplicationForm, JobRequestForm, FreelancerProfileForm, WorkExampleForm
from .ai_utils import get_skill_recommendations, get_similar_skills, get_job_matching_score
from .api_config import get_api_config, get_skill_config, is_api_enabled

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyB4Owr1pklmI7WZUE5PqM07HGGZ3drBjRE')

def fetch_gemini_resources(skills, resource_type, api_key=GEMINI_API_KEY):
    prompt = (
        f"Suggest 3-5 high-quality, up-to-date online resources (links/tools/videos) for {resource_type} "
        f"that would help a freelancer with these skills: {', '.join(skills) if skills else 'general skills'}. "
        "For each resource, provide exactly this JSON format: {{\"title\": \"Resource Name\", \"description\": \"Brief description\", \"type\": \"Tool/Video/Article\", \"url\": \"https://example.com\"}}. "
        "Return as a JSON array of these objects."
    )
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params={"key": api_key},
            json={
                "contents": [{"parts": [{"text": prompt}]}]
            },
            timeout=20
        )
        data = response.json()
        
        if 'candidates' not in data or not data['candidates']:
            print(f"Gemini API error: {data}")
            return []
            
        text = data['candidates'][0]['content']['parts'][0]['text']
        
        # Try to extract JSON from the response
        try:
            # Look for JSON array in the response
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                return pyjson.loads(match.group(0))
            
            # If no array found, try to parse the entire response
            return pyjson.loads(text)
        except pyjson.JSONDecodeError:
            # If JSON parsing fails, return fallback resources
            print(f"Failed to parse Gemini response: {text}")
            return get_fallback_resources(resource_type)
            
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return get_fallback_resources(resource_type)

def get_fallback_resources(resource_type):
    """Provide fallback resources when Gemini API fails"""
    fallback_resources = {
        'financial support and planning': [
            {
                'title': 'Financial Planning for Freelancers',
                'description': 'Comprehensive guide to managing finances as a freelancer',
                'type': 'Tool',
                'url': 'https://www.mint.com/freelancer-finances'
            },
            {
                'title': 'Budget Management App',
                'description': 'Free budgeting tool for independent workers',
                'type': 'Tool',
                'url': 'https://www.youneedabudget.com'
            }
        ],
        'community support and networking': [
            {
                'title': 'Local Freelancer Community',
                'description': 'Connect with other freelancers in your area',
                'type': 'Community',
                'url': 'https://www.meetup.com/freelancers'
            },
            {
                'title': 'Professional Networking Platform',
                'description': 'Build your professional network',
                'type': 'Platform',
                'url': 'https://www.linkedin.com'
            }
        ],
        'legal support and worker rights': [
            {
                'title': 'Freelancer Legal Rights',
                'description': 'Information about your rights as a freelancer',
                'type': 'Information',
                'url': 'https://www.freelancersunion.org/rights'
            },
            {
                'title': 'Free Legal Aid Directory',
                'description': 'Find free legal assistance in your area',
                'type': 'Directory',
                'url': 'https://www.lawhelp.org'
            }
        ],
        'health and wellness support': [
            {
                'title': 'Healthcare for Freelancers',
                'description': 'Health insurance options for independent workers',
                'type': 'Information',
                'url': 'https://www.healthcare.gov/freelancers'
            },
            {
                'title': 'Mental Health Resources',
                'description': 'Free mental health support for freelancers',
                'type': 'Support',
                'url': 'https://www.crisistextline.org'
            }
        ],
        'emergency assistance and crisis support': [
            {
                'title': 'Emergency Assistance Hotline',
                'description': '24/7 emergency support for freelancers',
                'type': 'Hotline',
                'url': 'tel:1-800-273-8255'
            },
            {
                'title': 'Local Food Bank Directory',
                'description': 'Find food assistance in your area',
                'type': 'Directory',
                'url': 'https://www.feedingamerica.org/find-your-local-foodbank'
            }
        ]
    }
    
    return fallback_resources.get(resource_type, [
        {
            'title': 'General Resource',
            'description': 'Resource for freelancers',
            'type': 'Resource',
            'url': 'https://www.example.com'
        }
    ])

def home(request):
    """Home page with login/register options"""
    return render(request, 'freelancer_platform/home.html')

def register(request):
    """User registration with user type selection"""
    # Get user type from URL parameter
    user_type = request.GET.get('type', '')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                user_profile = UserProfile.objects.create(
                    user=user,
                    user_type=form.cleaned_data['user_type'],
                    phone=form.cleaned_data.get('phone', ''),
                    address=form.cleaned_data.get('address', ''),
                )
                login(request, user)
                
                # Customize success message based on user type
                if user_profile.user_type == 'freelancer':
                    messages.success(request, f'Account created successfully! Welcome to Local Free-Lancer. Start finding job opportunities and building your career.')
                else:
                    messages.success(request, f'Account created successfully! Welcome to Local Free-Lancer. Start posting jobs and connecting with local talent.')
                
                return redirect('dashboard')
    else:
        # Pre-populate user type if provided in URL
        initial_data = {}
        if user_type in ['freelancer', 'recruiter']:
            initial_data['user_type'] = user_type
        
        form = UserRegistrationForm(initial=initial_data)
    
    return render(request, 'freelancer_platform/register.html', {'form': form, 'user_type': user_type})

def user_login(request):
    """User login"""
    # Get user type from URL parameter for display purposes
    user_type = request.GET.get('type', '')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Customize welcome message based on user type
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.user_type == 'freelancer':
                    messages.success(request, f'Welcome back, {user.username}! Ready to find your next opportunity?')
                else:
                    messages.success(request, f'Welcome back, {user.username}! Ready to connect with local talent?')
            except UserProfile.DoesNotExist:
                messages.success(request, f'Welcome back, {user.username}!')
            
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'freelancer_platform/login.html', {'user_type': user_type})

@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    """User dashboard based on user type"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        if user_profile.user_type == 'freelancer':
            # Freelancer dashboard
            available_jobs = Job.objects.filter(status='open').exclude(
                applications__freelancer=user_profile
            )
            my_applications = Application.objects.filter(freelancer=user_profile)
            my_job_requests = JobRequest.objects.filter(freelancer=user_profile)
            
            context = {
                'user_profile': user_profile,
                'available_jobs': available_jobs,
                'my_applications': my_applications,
                'my_job_requests': my_job_requests,
            }
            return render(request, 'freelancer_platform/freelancer_dashboard.html', context)
        
        else:
            # Recruiter dashboard
            posted_jobs = Job.objects.filter(recruiter=user_profile)
            active_jobs = posted_jobs.filter(status='open')
            total_applications = Application.objects.filter(job__recruiter=user_profile)
            job_requests = JobRequest.objects.filter(job__recruiter=user_profile)
            
            context = {
                'user_profile': user_profile,
                'posted_jobs': posted_jobs,
                'active_jobs': active_jobs,
                'total_applications': total_applications,
                'job_requests': job_requests,
            }
            return render(request, 'freelancer_platform/recruiter_dashboard.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

# API Views for Skill-Based Recommendations
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def skill_recommendations_api(request):
    """API endpoint for skill-based course recommendations"""
    try:
        data = json.loads(request.body)
        skill_type = data.get('skill_type', 'general')
        user_skills = data.get('user_skills', [])
        api_key = data.get('api_key')
        
        # Get user profile for personalized recommendations
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Mock API response - in production, this would call external APIs
        recommendations = get_skill_recommendations_from_api(skill_type, user_skills, api_key, user_profile)
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def certification_links_api(request):
    """API endpoint for certification program links"""
    try:
        data = json.loads(request.body)
        skill_type = data.get('skill_type', 'general')
        user_skills = data.get('user_skills', [])
        api_key = data.get('api_key')
        
        # Get user profile for personalized recommendations
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Mock API response - in production, this would call external APIs
        certifications = get_certification_links_from_api(skill_type, user_skills, api_key, user_profile)
        
        return JsonResponse({
            'success': True,
            'certifications': certifications
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def online_learning_links_api(request):
    """API endpoint for online learning resources"""
    try:
        data = json.loads(request.body)
        skill_type = data.get('skill_type', 'general')
        user_skills = data.get('user_skills', [])
        api_keys = data.get('api_keys', {})
        
        # Get user profile for personalized recommendations
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Mock API response - in production, this would call external APIs
        resources = get_online_learning_links_from_api(skill_type, user_skills, api_keys, user_profile)
        
        return JsonResponse({
            'success': True,
            'resources': resources
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def financial_resources_api(request):
    try:
        data = json.loads(request.body)
        user_skills = data.get('user_skills', [])
        user_profile = UserProfile.objects.get(user=request.user)
        resources = fetch_gemini_resources(user_skills, 'financial support and planning')
        if not resources:
            resources = [{
                'title': 'General Financial Planning',
                'description': 'Budgeting and financial planning for freelancers.',
                'type': 'Tool',
                'url': 'https://www.example.com/financial-planning',
            }]
        return JsonResponse({'success': True, 'resources': resources})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def community_resources_api(request):
    try:
        data = json.loads(request.body)
        user_skills = data.get('user_skills', [])
        user_profile = UserProfile.objects.get(user=request.user)
        resources = fetch_gemini_resources(user_skills, 'community support and networking')
        if not resources:
            resources = [{
                'title': 'Freelancer Community Forum',
                'description': 'Online forum for all local freelancers.',
                'type': 'Community',
                'url': 'https://www.example.com/freelancer-forum',
            }]
        return JsonResponse({'success': True, 'resources': resources})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def legal_resources_api(request):
    try:
        data = json.loads(request.body)
        user_skills = data.get('user_skills', [])
        user_profile = UserProfile.objects.get(user=request.user)
        resources = fetch_gemini_resources(user_skills, 'legal support and worker rights')
        if not resources:
            resources = [{
                'title': 'Legal Aid for Freelancers',
                'description': 'Free legal advice for local freelancers.',
                'type': 'Legal',
                'url': 'https://www.example.com/legal-aid',
            }]
        return JsonResponse({'success': True, 'resources': resources})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def health_resources_api(request):
    try:
        data = json.loads(request.body)
        user_skills = data.get('user_skills', [])
        user_profile = UserProfile.objects.get(user=request.user)
        resources = fetch_gemini_resources(user_skills, 'health and wellness support')
        if not resources:
            resources = [{
                'title': 'Local Health Center Finder',
                'description': 'Find free and low-cost health clinics near you.',
                'type': 'Health',
                'url': 'https://www.example.com/health-centers',
            }]
        return JsonResponse({'success': True, 'resources': resources})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def emergency_resources_api(request):
    try:
        data = json.loads(request.body)
        user_skills = data.get('user_skills', [])
        user_profile = UserProfile.objects.get(user=request.user)
        resources = fetch_gemini_resources(user_skills, 'emergency assistance and crisis support')
        if not resources:
            resources = [{
                'title': 'Emergency Hotline',
                'description': '24/7 emergency support for freelancers.',
                'type': 'Emergency',
                'url': 'tel:123-456-7890',
            }]
        return JsonResponse({'success': True, 'resources': resources})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Helper functions for API integrations
def get_skill_recommendations_from_api(skill_type, user_skills, api_key, user_profile):
    """Get skill-based course recommendations from external APIs"""
    # This is a mock implementation - in production, you would integrate with:
    # - Coursera API
    # - Udemy API
    # - LinkedIn Learning API
    # - edX API
    
    recommendations = []
    
    # Mock data based on skill type and user skills
    if skill_type == 'general' or 'cooking' in user_skills:
        recommendations.extend([
            {
                'title': 'Professional Cooking Fundamentals',
                'description': 'Learn essential cooking techniques and kitchen management skills',
                'platform': 'Coursera',
                'duration': '8 weeks',
                'level': 'Beginner',
                'url': 'https://www.coursera.org/learn/cooking-fundamentals'
            },
            {
                'title': 'Culinary Arts Certificate Program',
                'description': 'Comprehensive culinary training for professional development',
                'platform': 'edX',
                'duration': '12 weeks',
                'level': 'Intermediate',
                'url': 'https://www.edx.org/learn/culinary-arts'
            }
        ])
    
    if skill_type == 'general' or 'plumbing' in user_skills:
        recommendations.extend([
            {
                'title': 'Basic Plumbing Skills',
                'description': 'Learn essential plumbing techniques and safety procedures',
                'platform': 'Udemy',
                'duration': '6 weeks',
                'level': 'Beginner',
                'url': 'https://www.udemy.com/course/basic-plumbing-skills'
            },
            {
                'title': 'Advanced Plumbing Systems',
                'description': 'Master complex plumbing systems and troubleshooting',
                'platform': 'LinkedIn Learning',
                'duration': '10 weeks',
                'level': 'Advanced',
                'url': 'https://www.linkedin.com/learning/advanced-plumbing-systems'
            }
        ])
    
    if skill_type == 'general' or 'electrical' in user_skills:
        recommendations.extend([
            {
                'title': 'Electrical Wiring Fundamentals',
                'description': 'Learn safe electrical wiring practices and codes',
                'platform': 'Coursera',
                'duration': '8 weeks',
                'level': 'Beginner',
                'url': 'https://www.coursera.org/learn/electrical-wiring'
            },
            {
                'title': 'Advanced Electrical Systems',
                'description': 'Master complex electrical installations and maintenance',
                'platform': 'edX',
                'duration': '12 weeks',
                'level': 'Advanced',
                'url': 'https://www.edx.org/learn/advanced-electrical-systems'
            }
        ])
    
    # Add general skill development courses
    recommendations.extend([
        {
            'title': 'Business Communication Skills',
            'description': 'Improve your professional communication and client interaction',
            'platform': 'LinkedIn Learning',
            'duration': '4 weeks',
            'level': 'All Levels',
            'url': 'https://www.linkedin.com/learning/business-communication'
        },
        {
            'title': 'Customer Service Excellence',
            'description': 'Learn to provide outstanding customer service and build client relationships',
            'platform': 'Udemy',
            'duration': '3 weeks',
            'level': 'All Levels',
            'url': 'https://www.udemy.com/course/customer-service-excellence'
        }
    ])
    
    return recommendations

def get_certification_links_from_api(skill_type, user_skills, api_key, user_profile):
    """Get certification program links from external APIs"""
    # This is a mock implementation - in production, you would integrate with:
    # - Professional certification bodies
    # - Industry-specific certification programs
    # - Government certification programs
    
    certifications = []
    
    # Mock data based on skill type and user skills
    if skill_type == 'general' or 'cooking' in user_skills:
        certifications.extend([
            {
                'title': 'ServSafe Food Handler Certification',
                'description': 'Essential food safety certification for food service workers',
                'provider': 'ServSafe',
                'duration': '2-4 hours',
                'cost': '15',
                'url': 'https://www.servsafe.com/food-handler',
                'enroll_url': 'https://www.servsafe.com/food-handler/enroll'
            },
            {
                'title': 'Culinary Arts Professional Certificate',
                'description': 'Professional certification in culinary arts and kitchen management',
                'provider': 'American Culinary Federation',
                'duration': '6 months',
                'cost': '500',
                'url': 'https://www.acfchefs.org/certification',
                'enroll_url': 'https://www.acfchefs.org/certification/enroll'
            }
        ])
    
    if skill_type == 'general' or 'plumbing' in user_skills:
        certifications.extend([
            {
                'title': 'Plumbing Apprentice Certification',
                'description': 'Entry-level plumbing certification for apprentices',
                'provider': 'Plumbing-Heating-Cooling Contractors Association',
                'duration': '1 year',
                'cost': '300',
                'url': 'https://www.phccweb.org/certification',
                'enroll_url': 'https://www.phccweb.org/certification/enroll'
            },
            {
                'title': 'Journeyman Plumber License',
                'description': 'Professional plumbing license for experienced workers',
                'provider': 'State Licensing Board',
                'duration': '4 years',
                'cost': '200',
                'url': 'https://www.state.gov/plumbing-license',
                'enroll_url': 'https://www.state.gov/plumbing-license/apply'
            }
        ])
    
    if skill_type == 'general' or 'electrical' in user_skills:
        certifications.extend([
            {
                'title': 'Electrical Apprentice Certification',
                'description': 'Entry-level electrical certification for apprentices',
                'provider': 'National Electrical Contractors Association',
                'duration': '1 year',
                'cost': '250',
                'url': 'https://www.necanet.org/certification',
                'enroll_url': 'https://www.necanet.org/certification/enroll'
            },
            {
                'title': 'Journeyman Electrician License',
                'description': 'Professional electrical license for experienced workers',
                'provider': 'State Licensing Board',
                'duration': '4 years',
                'cost': '180',
                'url': 'https://www.state.gov/electrical-license',
                'enroll_url': 'https://www.state.gov/electrical-license/apply'
            }
        ])
    
    # Add general professional certifications
    certifications.extend([
        {
            'title': 'Customer Service Professional Certification',
            'description': 'Professional certification in customer service excellence',
            'provider': 'Customer Service Institute',
            'duration': '3 months',
            'cost': '150',
            'url': 'https://www.csi.org/certification',
            'enroll_url': 'https://www.csi.org/certification/enroll'
        },
        {
            'title': 'Small Business Management Certificate',
            'description': 'Certificate in small business management and entrepreneurship',
            'provider': 'Small Business Administration',
            'duration': '6 months',
            'cost': '100',
            'url': 'https://www.sba.gov/certification',
            'enroll_url': 'https://www.sba.gov/certification/enroll'
        }
    ])
    
    return certifications

def get_online_learning_links_from_api(skill_type, user_skills, api_keys, user_profile):
    """Get online learning resources from multiple platforms"""
    # This is a mock implementation - in production, you would integrate with:
    # - Coursera API
    # - Udemy API
    # - LinkedIn Learning API
    # - YouTube Learning API
    
    resources = {
        'coursera': [],
        'udemy': [],
        'linkedin_learning': [],
        'youtube': []
    }
    
    # Mock data based on skill type and user skills
    if skill_type == 'general' or 'cooking' in user_skills:
        resources['coursera'].extend([
            {
                'title': 'Cooking Fundamentals',
                'description': 'Learn basic cooking techniques and kitchen safety',
                'type': 'Course',
                'duration': '8 weeks',
                'price': 'Free',
                'url': 'https://www.coursera.org/learn/cooking-fundamentals'
            }
        ])
        
        resources['udemy'].extend([
            {
                'title': 'Professional Cooking Masterclass',
                'description': 'Comprehensive cooking course for professional development',
                'type': 'Course',
                'duration': '15 hours',
                'price': '$29.99',
                'url': 'https://www.udemy.com/course/professional-cooking'
            }
        ])
        
        resources['youtube'].extend([
            {
                'title': 'Cooking Basics Playlist',
                'description': 'Free cooking tutorials and tips',
                'type': 'Video Series',
                'duration': '5 hours',
                'price': 'Free',
                'url': 'https://www.youtube.com/playlist?list=cooking-basics'
            }
        ])
    
    if skill_type == 'general' or 'plumbing' in user_skills:
        resources['linkedin_learning'].extend([
            {
                'title': 'Plumbing Essentials',
                'description': 'Essential plumbing skills and safety procedures',
                'type': 'Course',
                'duration': '6 hours',
                'price': 'Free with LinkedIn Premium',
                'url': 'https://www.linkedin.com/learning/plumbing-essentials'
            }
        ])
        
        resources['youtube'].extend([
            {
                'title': 'DIY Plumbing Guide',
                'description': 'Step-by-step plumbing tutorials',
                'type': 'Video Series',
                'duration': '3 hours',
                'price': 'Free',
                'url': 'https://www.youtube.com/playlist?list=diy-plumbing'
            }
        ])
    
    if skill_type == 'general' or 'electrical' in user_skills:
        resources['coursera'].extend([
            {
                'title': 'Electrical Safety Fundamentals',
                'description': 'Learn electrical safety and basic wiring',
                'type': 'Course',
                'duration': '6 weeks',
                'price': 'Free',
                'url': 'https://www.coursera.org/learn/electrical-safety'
            }
        ])
        
        resources['udemy'].extend([
            {
                'title': 'Electrical Wiring Complete Course',
                'description': 'Complete guide to electrical wiring and installation',
                'type': 'Course',
                'duration': '12 hours',
                'price': '$39.99',
                'url': 'https://www.udemy.com/course/electrical-wiring-complete'
            }
        ])
    
    # Add general skill development resources
    resources['linkedin_learning'].extend([
        {
            'title': 'Professional Communication',
            'description': 'Improve your professional communication skills',
            'type': 'Course',
            'duration': '4 hours',
            'price': 'Free with LinkedIn Premium',
            'url': 'https://www.linkedin.com/learning/professional-communication'
        }
    ])
    
    resources['youtube'].extend([
        {
            'title': 'Business Skills for Freelancers',
            'description': 'Essential business skills for independent workers',
            'type': 'Video Series',
            'duration': '2 hours',
            'price': 'Free',
            'url': 'https://www.youtube.com/playlist?list=business-skills-freelancers'
        }
    ])
    
    return resources

@login_required
def post_job(request):
    """Post a new job (recruiter only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'recruiter':
            messages.error(request, 'Only recruiters can post jobs.')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.recruiter = user_profile
                job.save()
                messages.success(request, 'Job posted successfully!')
                return redirect('dashboard')
        else:
            form = JobForm()
        
        return render(request, 'freelancer_platform/post_job.html', {'form': form})
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def job_detail(request, job_id):
    """View job details"""
    job = get_object_or_404(Job, id=job_id)
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check if user has already applied
    has_applied = Application.objects.filter(job=job, freelancer=user_profile).exists()
    
    # Check if user has already requested the job
    has_requested = False
    job_request = None
    if user_profile.user_type == 'freelancer':
        try:
            job_request = JobRequest.objects.get(job=job, freelancer=user_profile)
            has_requested = True
        except JobRequest.DoesNotExist:
            has_requested = False
    
    context = {
        'job': job,
        'user_profile': user_profile,
        'has_applied': has_applied,
        'has_requested': has_requested,
        'job_request': job_request,
    }
    return render(request, 'freelancer_platform/job_detail.html', context)

@login_required
def apply_job(request, job_id):
    """Apply for a job (freelancer only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'freelancer':
            messages.error(request, 'Only freelancers can apply for jobs.')
            return redirect('dashboard')
        
        job = get_object_or_404(Job, id=job_id)
        
        # Check if already applied
        if Application.objects.filter(job=job, freelancer=user_profile).exists():
            messages.warning(request, 'You have already applied for this job.')
            return redirect('job_detail', job_id=job_id)
        
        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.job = job
                application.freelancer = user_profile
                application.save()
                messages.success(request, 'Application submitted successfully!')
                return redirect('dashboard')
        else:
            form = ApplicationForm()
        
        context = {
            'form': form,
            'job': job,
        }
        return render(request, 'freelancer_platform/apply_job.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def view_applications(request, job_id):
    """View applications for a job (recruiter only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'recruiter':
            messages.error(request, 'Only recruiters can view applications.')
            return redirect('dashboard')
        
        job = get_object_or_404(Job, id=job_id, recruiter=user_profile)
        applications = Application.objects.filter(job=job)
        
        context = {
            'job': job,
            'applications': applications,
        }
        return render(request, 'freelancer_platform/view_applications.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def request_job(request, job_id):
    """Request a job assignment (freelancer only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'freelancer':
            messages.error(request, 'Only freelancers can request jobs.')
            return redirect('dashboard')
        
        job = get_object_or_404(Job, id=job_id, status='open')
        
        # Check if already requested
        if JobRequest.objects.filter(job=job, freelancer=user_profile).exists():
            messages.warning(request, 'You have already requested this job.')
            return redirect('job_detail', job_id=job_id)
        
        if request.method == 'POST':
            form = JobRequestForm(request.POST, request.FILES, freelancer=user_profile)
            if form.is_valid():
                job_request = form.save(commit=False)
                job_request.job = job
                job_request.freelancer = user_profile
                job_request.save()
                
                # Save many-to-many relationships
                form.save_m2m()
                
                messages.success(request, 'Job request sent successfully!')
                return redirect('dashboard')
        else:
            form = JobRequestForm(freelancer=user_profile)
        
        context = {
            'form': form,
            'job': job,
        }
        return render(request, 'freelancer_platform/request_job.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def view_job_requests(request, job_id):
    """View job requests for a job (recruiter only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'recruiter':
            messages.error(request, 'Only recruiters can view job requests.')
            return redirect('dashboard')
        
        job = get_object_or_404(Job, id=job_id, recruiter=user_profile)
        job_requests = JobRequest.objects.filter(job=job)
        
        context = {
            'job': job,
            'job_requests': job_requests,
        }
        return render(request, 'freelancer_platform/view_job_requests.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def approve_job_request(request, request_id):
    """Approve a job request (recruiter only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'recruiter':
            messages.error(request, 'Only recruiters can approve job requests.')
            return redirect('dashboard')
        
        job_request = get_object_or_404(JobRequest, id=request_id, job__recruiter=user_profile)
        job = job_request.job
        
        if job.status != 'open':
            messages.error(request, 'This job is no longer available.')
            return redirect('view_job_requests', job_id=job.id)
        
        # Assign the job to the freelancer
        job.assigned_freelancer = job_request.freelancer
        job.status = 'assigned'
        job.save()
        
        # Update the job request status
        job_request.status = 'approved'
        job_request.save()
        
        # Reject all other pending requests for this job
        JobRequest.objects.filter(job=job, status='pending').exclude(id=request_id).update(status='rejected')
        
        messages.success(request, f'Job assigned to {job_request.freelancer.user.get_full_name() or job_request.freelancer.user.username}')
        return redirect('view_job_requests', job_id=job.id)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def reject_job_request(request, request_id):
    """Reject a job request (recruiter only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'recruiter':
            messages.error(request, 'Only recruiters can reject job requests.')
            return redirect('dashboard')
        
        job_request = get_object_or_404(JobRequest, id=request_id, job__recruiter=user_profile)
        job_request.status = 'rejected'
        job_request.save()
        
        messages.success(request, 'Job request rejected.')
        return redirect('view_job_requests', job_id=job_request.job.id)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def freelancer_profile(request):
    """Freelancer profile management"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'freelancer':
            messages.error(request, 'Only freelancers can access this page.')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = FreelancerProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                # Let Django handle the file upload automatically
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('freelancer_profile')
            else:
                # Show form errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            form = FreelancerProfileForm(instance=user_profile)
        
        work_examples = WorkExample.objects.filter(freelancer=user_profile)
        
        context = {
            'form': form,
            'user_profile': user_profile,
            'work_examples': work_examples,
        }
        return render(request, 'freelancer_platform/freelancer_profile.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def add_work_example(request):
    """Add work example (freelancer only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'freelancer':
            messages.error(request, 'Only freelancers can add work examples.')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = WorkExampleForm(request.POST, request.FILES)
            if form.is_valid():
                work_example = form.save(commit=False)
                work_example.freelancer = user_profile
                work_example.save()
                messages.success(request, 'Work example added successfully!')
                return redirect('freelancer_profile')
        else:
            form = WorkExampleForm()
        
        context = {
            'form': form,
        }
        return render(request, 'freelancer_platform/add_work_example.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def delete_work_example(request, example_id):
    """Delete work example (freelancer only)"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'freelancer':
            messages.error(request, 'Only freelancers can delete work examples.')
            return redirect('dashboard')
        
        work_example = get_object_or_404(WorkExample, id=example_id, freelancer=user_profile)
        work_example.delete()
        messages.success(request, 'Work example deleted successfully!')
        return redirect('freelancer_profile')
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def skill_based_jobs(request):
    """Get skill-based job recommendations for freelancers"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'freelancer':
            messages.error(request, 'Only freelancers can access skill-based recommendations.')
            return redirect('dashboard')
        
        # Get freelancer's skills
        freelancer_skills = user_profile.get_skills_list() + user_profile.selected_skills
        
        # Find jobs that match the freelancer's skills
        matching_jobs = []
        for job in Job.objects.filter(status='open'):
            job_skills = [skill.strip().lower() for skill in job.required_skills.split(',')]
            match_score = get_job_matching_score(freelancer_skills, job_skills)
            if match_score >= 5:  # Only show jobs with decent match
                matching_jobs.append({
                    'job': job,
                    'match_score': match_score
                })
        
        # Sort by match score
        matching_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        context = {
            'user_profile': user_profile,
            'matching_jobs': matching_jobs,
        }
        return render(request, 'freelancer_platform/skill_based_jobs.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')

@login_required
def delete_job(request, job_id):
    """Delete a job - only if no approved requests or job period expired"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'recruiter':
            messages.error(request, 'Only recruiters can delete jobs.')
            return redirect('dashboard')
        
        job = get_object_or_404(Job, id=job_id, recruiter=user_profile)
        
        # Check if job can be deleted
        if not job.can_be_deleted():
            messages.error(request, f'Cannot delete this job: {job.get_deletion_status()}')
            return redirect('dashboard')
        
        # Delete the job
        job_title = job.title
        job.delete()
        messages.success(request, f'Job "{job_title}" has been deleted successfully.')
        
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission to delete it.')
    
    return redirect('dashboard')
