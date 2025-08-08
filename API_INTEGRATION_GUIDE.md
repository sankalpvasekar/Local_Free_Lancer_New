# API Integration Guide for Skill-Based Recommendations

This guide explains how to integrate external APIs for skill-based recommendations, certification links, and online learning resources in the Local Free-Lancer platform.

## 🌟 Overview

The platform integrates with multiple external APIs to provide personalized skill development recommendations, certification programs, and online learning resources based on user skills and preferences.

## 🔧 API Configuration

### Environment Variables Setup

Add the following environment variables to your `.env` file:

```bash
# Learning Platform APIs
COURSERA_API_KEY=your_coursera_api_key_here
UDEMY_API_KEY=your_udemy_api_key_here
UDEMY_CLIENT_ID=your_udemy_client_id_here
UDEMY_CLIENT_SECRET=your_udemy_client_secret_here
LINKEDIN_LEARNING_API_KEY=your_linkedin_learning_api_key_here
LINKEDIN_CLIENT_ID=your_linkedin_client_id_here
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret_here
EDX_API_KEY=your_edx_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# Certification APIs
SERVSAFE_API_KEY=your_servsafe_api_key_here
ACF_API_KEY=your_acf_api_key_here
PHCC_API_KEY=your_phcc_api_key_here
NECA_API_KEY=your_neca_api_key_here

# Community Resource APIs
FOOD_BANKS_API_KEY=your_food_banks_api_key_here
HEALTH_CLINICS_API_KEY=your_health_clinics_api_key_here
LEGAL_AID_API_KEY=your_legal_aid_api_key_here
```

## 📚 Learning Platform APIs

### 1. Coursera API

**Purpose**: Course recommendations and learning paths

**Setup**:

1. Register at [Coursera for Business](https://www.coursera.org/business)
2. Get API credentials from your dashboard
3. Add to environment variables

**Usage**:

```python
from freelancer_platform.api_config import get_api_config

coursera_config = get_api_config('COURSERA')
api_key = coursera_config['API_KEY']
base_url = coursera_config['BASE_URL']
```

**Endpoints**:

- `/courses` - Get available courses
- `/search` - Search courses by keywords
- `/categories` - Get course categories

### 2. Udemy API

**Purpose**: Professional development courses

**Setup**:

1. Create a Udemy instructor account
2. Generate API credentials
3. Add to environment variables

**Usage**:

```python
udemy_config = get_api_config('UDEMY')
api_key = udemy_config['API_KEY']
client_id = udemy_config['CLIENT_ID']
client_secret = udemy_config['CLIENT_SECRET']
```

**Endpoints**:

- `/courses` - Get course listings
- `/courses/search` - Search courses
- `/categories` - Get course categories

### 3. LinkedIn Learning API

**Purpose**: Professional skills development

**Setup**:

1. Register for LinkedIn Learning API access
2. Create a LinkedIn application
3. Get OAuth credentials

**Usage**:

```python
linkedin_config = get_api_config('LINKEDIN_LEARNING')
api_key = linkedin_config['API_KEY']
client_id = linkedin_config['CLIENT_ID']
client_secret = linkedin_config['CLIENT_SECRET']
```

**Endpoints**:

- `/learning/courses` - Get learning courses
- `/learning/search` - Search learning content
- `/learning/categories` - Get learning categories

### 4. edX API

**Purpose**: University-level courses and certificates

**Setup**:

1. Register for edX API access
2. Generate API key
3. Add to environment variables

**Usage**:

```python
edx_config = get_api_config('EDX')
api_key = edx_config['API_KEY']
base_url = edx_config['BASE_URL']
```

### 5. YouTube Learning API

**Purpose**: Free educational content and tutorials

**Setup**:

1. Create a Google Cloud project
2. Enable YouTube Data API v3
3. Generate API key

**Usage**:

```python
youtube_config = get_api_config('YOUTUBE')
api_key = youtube_config['API_KEY']
base_url = youtube_config['BASE_URL']
```

## 🏆 Certification APIs

### 1. ServSafe API

**Purpose**: Food safety certifications

**Setup**:

1. Contact ServSafe for API access
2. Get API credentials
3. Add to environment variables

**Usage**:

```python
servsafe_config = get_api_config('CERTIFICATION')['SERVSAFE']
api_key = servsafe_config['API_KEY']
base_url = servsafe_config['BASE_URL']
```

### 2. American Culinary Federation (ACF) API

**Purpose**: Culinary arts certifications

**Setup**:

1. Contact ACF for API access
2. Get API credentials
3. Add to environment variables

### 3. Plumbing-Heating-Cooling Contractors (PHCC) API

**Purpose**: Plumbing certifications

**Setup**:

1. Contact PHCC for API access
2. Get API credentials
3. Add to environment variables

### 4. National Electrical Contractors Association (NECA) API

**Purpose**: Electrical certifications

**Setup**:

1. Contact NECA for API access
2. Get API credentials
3. Add to environment variables

## 🏥 Community Resource APIs

### 1. Food Banks API

**Purpose**: Local food assistance resources

**Setup**:

1. Contact Feeding America for API access
2. Get API credentials
3. Add to environment variables

### 2. Health Clinics API

**Purpose**: Free and low-cost healthcare resources

**Setup**:

1. Contact healthcare.gov for API access
2. Get API credentials
3. Add to environment variables

### 3. Legal Aid API

**Purpose**: Free legal assistance resources

**Setup**:

1. Contact legal aid organizations for API access
2. Get API credentials
3. Add to environment variables

## 🔄 API Integration Implementation

### 1. API Views

The platform includes three main API endpoints:

```python
# Skill-based course recommendations
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def skill_recommendations_api(request):
    # Implementation for course recommendations

# Certification program links
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def certification_links_api(request):
    # Implementation for certification links

# Online learning resources
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def online_learning_links_api(request):
    # Implementation for learning resources
```

### 2. Helper Functions

```python
def get_skill_recommendations_from_api(skill_type, user_skills, api_key, user_profile):
    """Get skill-based course recommendations from external APIs"""
    # Implementation for fetching recommendations

def get_certification_links_from_api(skill_type, user_skills, api_key, user_profile):
    """Get certification program links from external APIs"""
    # Implementation for fetching certifications

def get_online_learning_links_from_api(skill_type, user_skills, api_keys, user_profile):
    """Get online learning resources from multiple platforms"""
    # Implementation for fetching learning resources
```

### 3. Frontend Integration

The frontend uses JavaScript to call these APIs:

```javascript
// Get skill recommendations
async function getSkillRecommendations(skillType) {
    const response = await fetch('/api/skill-recommendations/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            skill_type: skillType,
            user_skills: userSkills,
            api_key: API_CONFIG.COURSERA_API_KEY
        })
    });
    
    const data = await response.json();
    displaySkillRecommendations(data.recommendations);
}
```

## 🎯 Skill Categories

The platform supports the following skill categories with specific API integrations:

### Cooking Skills

- **Platforms**: Coursera, Udemy, LinkedIn Learning, edX
- **Certifications**: ServSafe, ACF
- **Resources**: YouTube, Community

### Plumbing Skills

- **Platforms**: Udemy, LinkedIn Learning, YouTube
- **Certifications**: PHCC, State Licensing
- **Resources**: YouTube, Community

### Electrical Skills

- **Platforms**: Coursera, Udemy, LinkedIn Learning
- **Certifications**: NECA, State Licensing
- **Resources**: YouTube, Community

### Other Skills

- Cleaning, Carpentry, Painting, Gardening
- Mechanical, Tailoring, Salon/Beauty

## ⚡ Rate Limiting

The platform implements rate limiting for API calls:

```python
RATE_LIMITS = {
    'coursera': {'requests_per_minute': 60, 'requests_per_day': 1000},
    'udemy': {'requests_per_minute': 30, 'requests_per_day': 500},
    'linkedin_learning': {'requests_per_minute': 20, 'requests_per_day': 300},
    'edx': {'requests_per_minute': 40, 'requests_per_day': 800},
    'youtube': {'requests_per_minute': 100, 'requests_per_day': 10000}
}
```

## 💾 Caching

API responses are cached to improve performance:

```python
CACHE_CONFIG = {
    'skill_recommendations': 3600,  # 1 hour
    'certification_links': 7200,    # 2 hours
    'online_learning_links': 1800,  # 30 minutes
    'community_resources': 86400    # 24 hours
}
```

## 🚀 Production Deployment

### 1. Environment Setup

```bash
# Set environment variables
export COURSERA_API_KEY="your_actual_api_key"
export UDEMY_API_KEY="your_actual_api_key"
# ... other API keys

# Or use a .env file
source .env
```

### 2. API Key Management

- Store API keys securely in environment variables
- Use different keys for development and production
- Rotate API keys regularly
- Monitor API usage and costs

### 3. Error Handling

```python
ERROR_MESSAGES = {
    'api_unavailable': 'The learning platform is temporarily unavailable. Please try again later.',
    'rate_limit_exceeded': 'Too many requests. Please wait a moment and try again.',
    'invalid_api_key': 'API configuration error. Please contact support.',
    'no_results': 'No recommendations found for your skills. Try broadening your search.',
    'network_error': 'Network error. Please check your connection and try again.'
}
```

### 4. Monitoring

- Monitor API response times
- Track API usage and costs
- Set up alerts for API failures
- Log API errors for debugging

## 🔒 Security Considerations

1. **API Key Protection**: Never commit API keys to version control
2. **Rate Limiting**: Implement proper rate limiting to avoid API abuse
3. **Input Validation**: Validate all user inputs before making API calls
4. **Error Handling**: Handle API errors gracefully without exposing sensitive information
5. **HTTPS**: Always use HTTPS for API communications

## 📊 Testing

### 1. Unit Tests

```python
def test_skill_recommendations_api():
    """Test skill recommendations API endpoint"""
    # Test implementation

def test_certification_links_api():
    """Test certification links API endpoint"""
    # Test implementation

def test_online_learning_links_api():
    """Test online learning links API endpoint"""
    # Test implementation
```

### 2. Integration Tests

```python
def test_api_integration():
    """Test integration with external APIs"""
    # Test implementation
```

## 🆘 Troubleshooting

### Common Issues

1. **API Key Invalid**: Check environment variables and API key validity
2. **Rate Limit Exceeded**: Implement proper rate limiting and caching
3. **Network Errors**: Check internet connection and API endpoint availability
4. **Authentication Errors**: Verify OAuth credentials and tokens

### Debug Mode

Enable debug mode to see detailed API responses:

```python
DEBUG = True  # In settings.py
```

## 📞 Support

For API integration support:

- **Email**: <api-support@localfreelancer.com>
- **Documentation**: Check individual API provider documentation
- **Community**: Join our developer community for help

## 🎯 Next Steps

1. **Get API Keys**: Register for the APIs you want to integrate
2. **Set Environment Variables**: Add API keys to your environment
3. **Test Integration**: Test the API endpoints with sample data
4. **Deploy**: Deploy to production with proper error handling
5. **Monitor**: Set up monitoring and alerting for API usage

---

**Local Free-Lancer** - Empowering communities through skill development and API integration.
