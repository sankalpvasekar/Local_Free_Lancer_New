from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('job/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('job/<int:job_id>/request/', views.request_job, name='request_job'),
    path('job/<int:job_id>/requests/', views.view_job_requests, name='view_job_requests'),
    path('job-request/<int:request_id>/approve/', views.approve_job_request, name='approve_job_request'),
    path('job-request/<int:request_id>/reject/', views.reject_job_request, name='reject_job_request'),
    path('freelancer-profile/', views.freelancer_profile, name='freelancer_profile'),
    path('add-work-example/', views.add_work_example, name='add_work_example'),
    path('delete-work-example/<int:example_id>/', views.delete_work_example, name='delete_work_example'),
    path('skill-based-jobs/', views.skill_based_jobs, name='skill_based_jobs'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    
    # API endpoints for skill-based recommendations
    path('api/skill-recommendations/', views.skill_recommendations_api, name='skill_recommendations_api'),
    path('api/certification-links/', views.certification_links_api, name='certification_links_api'),
    path('api/online-learning-links/', views.online_learning_links_api, name='online_learning_links_api'),
    path('api/financial-resources/', views.financial_resources_api, name='financial_resources_api'),
    path('api/community-resources/', views.community_resources_api, name='community_resources_api'),
    path('api/legal-resources/', views.legal_resources_api, name='legal_resources_api'),
    path('api/health-resources/', views.health_resources_api, name='health_resources_api'),
    path('api/emergency-resources/', views.emergency_resources_api, name='emergency_resources_api'),
] 