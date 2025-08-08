<<<<<<< HEAD
# Local_FreeLancer
=======
# Local Free-Lancer Platform

A Django-based freelancer platform focused on reducing poverty through local economic empowerment. This platform connects local workers with job opportunities, providing resources and support to help communities thrive.

## 🌟 Project Overview

Local Free-Lancer is dedicated to addressing poverty through local economic empowerment. Our platform connects skilled local workers with job opportunities, helping communities thrive and individuals achieve financial independence.

### Key Features

- **Local Community Focus**: Connect with workers and opportunities in your own community
- **Poverty Reduction**: Directly addresses poverty by creating sustainable employment opportunities
- **AI-Powered Matching**: Advanced algorithms match workers with the best opportunities
- **Resource Support**: Comprehensive community resources and support systems
- **Separate Dashboards**: Different interfaces for job recruiters and local workers
- **Multi-language Support**: Available in English, Hindi, and Marathi

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Local_Free_Lancer
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - The admin panel is available at `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

```
Local_Free_Lancer/
├── poverty_freelancer/          # Django project settings
│   ├── settings.py              # Project configuration
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py                  # WSGI configuration
├── freelancer_platform/         # Main application
│   ├── models.py                # Database models
│   ├── views.py                 # View functions
│   ├── forms.py                 # Form definitions
│   ├── urls.py                  # App URL routing
│   └── ai_utils.py              # AI recommendation utilities
├── templates/                   # HTML templates
│   └── freelancer_platform/     # App-specific templates
├── static/                      # Static files (CSS, JS, images)
├── media/                       # User-uploaded files
├── manage.py                    # Django management script
└── requirements.txt             # Python dependencies
```

## 🎯 User Types

### Local Workers (Freelancers)

- Find local job opportunities
- Build professional profiles
- Access community resources
- Get skill development support
- Receive AI-powered job recommendations

### Job Recruiters

- Post job opportunities
- Connect with local talent
- Support community development
- Manage applications
- Contribute to poverty reduction

## 🔧 Key Features

### Home Page

- Poverty-focused messaging and community impact
- Separate registration options for workers and recruiters
- Impact statistics and community benefits
- Multi-language support

### User Dashboards

- **Freelancer Dashboard**: Job opportunities, applications, profile management
- **Recruiter Dashboard**: Posted jobs, applications, job management
- **Resources Section**: Community support, skill development, financial assistance

### AI Job Recommendations

- Skill-based job matching
- Personalized recommendations
- Community resource recommendations

### Community Resources

- Skill development programs
- Financial support resources
- Health and wellness programs
- Legal assistance
- Emergency support
- Community groups and mentorship

## 🌐 Multi-language Support

The platform supports multiple languages:

- English (en)
- Hindi (हिंदी)
- Marathi (मराठी)

Language switching is available throughout the application.

## 🛠️ Technology Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production)
- **AI/ML**: Custom recommendation algorithms
- **File Storage**: Local file system (development), AWS S3 (production)

## 📊 Database Models

### Core Models

- **UserProfile**: Extended user profiles with skills and preferences
- **Job**: Job postings with categories and requirements
- **Application**: Job applications from workers
- **JobRequest**: Detailed job requests with proposals
- **WorkExample**: Portfolio items and work samples

### Key Features

- Skill categorization and matching
- Proposal management
- Work example portfolios
- Application tracking
- Community resource management

## 🚀 Deployment

### Production Setup

1. **Environment Variables**

   ```bash
   export DEBUG=False
   export SECRET_KEY='your-secret-key'
   export ALLOWED_HOSTS='your-domain.com'
   ```

2. **Database Setup**

   ```bash
   # For PostgreSQL
   pip install psycopg2-binary
   ```

3. **Static Files**

   ```bash
   python manage.py collectstatic
   ```

4. **Web Server**
   - Use Gunicorn or uWSGI
   - Configure Nginx as reverse proxy
   - Set up SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Tailwind CSS for the beautiful styling system
- Local communities for inspiration and feedback
- Contributors and supporters of poverty reduction initiatives

## 📞 Support

For support and questions:

- Email: <support@localfreelancer.com>
- Phone: +1 (555) 123-4567
- Address: Local Community Center

## 🎯 Mission

Our mission is to reduce poverty through local economic empowerment by connecting talent with opportunity, providing resources and support to help communities thrive.

---

**Local Free-Lancer** - Empowering communities through local work opportunities.
>>>>>>> 8269074 (Initial commit)
