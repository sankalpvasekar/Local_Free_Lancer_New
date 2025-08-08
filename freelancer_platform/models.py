from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    USER_TYPES = [
        ('freelancer', 'Freelancer'),
        ('recruiter', 'Job Recruiter'),
    ]
    
    SKILL_CATEGORIES = [
        ('cooking', 'Cooking'),
        ('salon', 'Salon/Beauty'),
        ('mechanical', 'Mechanical'),
        ('tailoring', 'Tailoring'),
        ('wireman', 'Electrical/Wiring'),
        ('cleaning', 'Cleaning'),
        ('plumbing', 'Plumbing'),
        ('carpentry', 'Carpentry'),
        ('painting', 'Painting'),
        ('gardening', 'Gardening'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="Comma-separated list of skills")
    selected_skills = models.JSONField(default=list, blank=True, help_text="Selected skills from categories")
    experience_years = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50)])
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    
    def get_selected_skills_display(self):
        """Return selected skills as readable text"""
        if self.selected_skills:
            skill_names = [dict(UserProfile.SKILL_CATEGORIES)[skill] for skill in self.selected_skills if skill in dict(UserProfile.SKILL_CATEGORIES)]
            return ', '.join(skill_names)
        return ""
    
    def save(self, *args, **kwargs):
        # Delete old profile picture if a new one is being uploaded
        if self.pk:  # Only for existing instances
            try:
                old_instance = UserProfile.objects.get(pk=self.pk)
                if old_instance.profile_picture and self.profile_picture and old_instance.profile_picture != self.profile_picture:
                    # Delete the old file
                    old_instance.profile_picture.delete(save=False)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

class WorkExample(models.Model):
    WORK_TYPES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('vr_video', 'VR Video'),
    ]
    
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='work_examples')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    work_type = models.CharField(max_length=10, choices=WORK_TYPES)
    file = models.FileField(upload_to='work_examples/', help_text="Upload photos, videos, or VR videos")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.freelancer.user.username} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']

class Job(models.Model):
    JOB_CATEGORIES = [
        ('cooking', 'Cooking'),
        ('salon', 'Salon/Beauty'),
        ('mechanical', 'Mechanical'),
        ('tailoring', 'Tailoring'),
        ('wireman', 'Electrical/Wiring'),
        ('cleaning', 'Cleaning'),
        ('plumbing', 'Plumbing'),
        ('carpentry', 'Carpentry'),
        ('painting', 'Painting'),
        ('gardening', 'Gardening'),
        ('other', 'Other'),
    ]
    
    JOB_STATUS = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('assigned', 'Assigned'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=JOB_CATEGORIES)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    required_skills = models.TextField()
    duration_months = models.IntegerField(default=1, help_text="Duration in months")
    status = models.CharField(max_length=15, choices=JOB_STATUS, default='open')
    recruiter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posted_jobs')
    assigned_freelancer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.expires_at and self.duration_months:
            from datetime import datetime, timedelta
            self.expires_at = datetime.now() + timedelta(days=self.duration_months * 30)
        super().save(*args, **kwargs)
    
    def can_be_deleted(self):
        """
        Check if the job can be deleted by the recruiter.
        Jobs can be deleted if:
        1. No job requests have been approved yet
        2. OR the job period has expired
        """
        from django.utils import timezone
        
        # Check if any job request has been approved
        has_approved_request = self.job_requests.filter(status='approved').exists()
        
        # Check if job period has expired
        is_expired = self.expires_at and timezone.now() > self.expires_at
        
        # Can be deleted if no approved requests OR job has expired
        return not has_approved_request or is_expired
    
    def get_deletion_status(self):
        """
        Get a human-readable status about job deletion
        """
        from django.utils import timezone
        
        if self.can_be_deleted():
            if self.expires_at and timezone.now() > self.expires_at:
                return "Job period expired - can be deleted"
            else:
                return "No approved requests - can be deleted"
        else:
            return "Has approved requests - cannot be deleted until job period ends"

class Application(models.Model):
    APPLICATION_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField()
    proposed_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=APPLICATION_STATUS, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job', 'freelancer']
    
    def __str__(self):
        return f"{self.freelancer.user.username} - {self.job.title}"

class JobRequest(models.Model):
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    PROPOSAL_TYPE = [
        ('monthly', 'Monthly'),
        ('daily', 'Daily'),
        ('hourly', 'Hourly'),
        ('fixed', 'Fixed Project'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_requests')
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_requests')
    
    # Cover letter with microphone input support
    cover_letter = models.TextField(blank=True, null=True, help_text="Your proposal message. You can also record audio.")
    cover_letter_audio = models.FileField(upload_to='job_requests/audio/', blank=True, null=True, help_text="Record your cover letter via microphone")
    
    # Proposal details
    proposal_type = models.CharField(max_length=10, choices=PROPOSAL_TYPE, default='monthly')
    proposed_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Your proposed rate")
    proposed_duration = models.IntegerField(blank=True, null=True, help_text="Duration in the selected unit (months/days/hours)")
    
    # Work examples and certificates
    selected_work_examples = models.ManyToManyField(WorkExample, blank=True, help_text="Select your previous work samples")
    certificates = models.FileField(upload_to='job_requests/certificates/', blank=True, null=True, help_text="Upload relevant certificates")
    
    status = models.CharField(max_length=15, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job', 'freelancer']
    
    def __str__(self):
        return f"{self.freelancer.user.username} - {self.job.title}"
    
    def get_proposal_display(self):
        """Get formatted proposal rate display"""
        if self.proposal_type == 'monthly':
            return f"₹{self.proposed_rate}/month for {self.proposed_duration} months"
        elif self.proposal_type == 'daily':
            return f"₹{self.proposed_rate}/day for {self.proposed_duration} days"
        elif self.proposal_type == 'hourly':
            return f"₹{self.proposed_rate}/hour for {self.proposed_duration} hours"
        else:
            return f"₹{self.proposed_rate} (fixed project)"
