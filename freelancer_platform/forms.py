from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Job, Application, JobRequest, WorkExample

class UserRegistrationForm(UserCreationForm):
    USER_TYPES = [
        ('freelancer', 'Freelancer'),
        ('recruiter', 'Job Recruiter'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.Select(attrs={'class': 'form-select'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': 'form-control'})

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'category', 'company_name', 'location', 'salary_min', 'salary_max', 'required_skills', 'duration_months']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'required_skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'proposed_rate']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'proposed_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class JobRequestForm(forms.ModelForm):
    selected_work_examples = forms.ModelMultipleChoiceField(
        queryset=WorkExample.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        help_text="Select your previous work samples to showcase your skills"
    )
    
    class Meta:
        model = JobRequest
        fields = ['cover_letter', 'cover_letter_audio', 'proposal_type', 'proposed_rate', 'proposed_duration', 'selected_work_examples', 'certificates']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Explain why you are the best fit for this job... You can also record audio below.'
            }),
            'cover_letter_audio': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'audio/*',
                'data-audio-recorder': 'true'
            }),
            'proposal_type': forms.Select(attrs={'class': 'form-select'}),
            'proposed_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'proposed_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'certificates': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        freelancer = kwargs.pop('freelancer', None)
        super().__init__(*args, **kwargs)
        
        if freelancer:
            # Set the queryset for work examples to only show the freelancer's examples
            self.fields['selected_work_examples'].queryset = WorkExample.objects.filter(freelancer=freelancer)
        
        # Add help text for proposal fields
        self.fields['proposal_type'].help_text = "Choose how you want to charge for this job"
        self.fields['proposed_rate'].help_text = "Your proposed rate per unit (month/day/hour)"
        self.fields['proposed_duration'].help_text = "Duration in the selected unit"
        self.fields['certificates'].help_text = "Upload relevant certificates (optional)"

class FreelancerProfileForm(forms.ModelForm):
    selected_skills = forms.MultipleChoiceField(
        choices=UserProfile.SKILL_CATEGORIES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'skills', 'selected_skills', 'experience_years', 'hourly_rate', 'bio', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter additional skills (comma-separated)'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'data-max-size': '5242880',  # 5MB in bytes
                'onchange': 'previewImage(this)'
            }),
        }
    
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        
        # Only validate if this is a new file upload (not an existing file)
        if profile_picture and hasattr(profile_picture, 'content_type'):
            # This is a new uploaded file
            # Check file size (5MB limit)
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise forms.ValidationError("Profile picture must be less than 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if profile_picture.content_type not in allowed_types:
                raise forms.ValidationError("Please upload a valid image file (JPG, PNG, or GIF).")
        
        return profile_picture

class WorkExampleForm(forms.ModelForm):
    class Meta:
        model = WorkExample
        fields = ['title', 'description', 'work_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'work_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        } 