"""
API Configuration for External Service Integrations
This file contains configuration for various APIs used in skill-based recommendations.
"""

import os
from django.conf import settings

# API Configuration for External Learning Platforms
API_CONFIG = {
    # Coursera API Configuration
    'COURSERA': {
        'API_KEY': os.environ.get('COURSERA_API_KEY', 'your_coursera_api_key_here'),
        'BASE_URL': 'https://api.coursera.org/api/courses.v1',
        'ENDPOINTS': {
            'courses': '/courses',
            'search': '/search',
            'categories': '/categories'
        }
    },
    
    # Udemy API Configuration
    'UDEMY': {
        'API_KEY': os.environ.get('UDEMY_API_KEY', 'your_udemy_api_key_here'),
        'CLIENT_ID': os.environ.get('UDEMY_CLIENT_ID', 'your_udemy_client_id_here'),
        'CLIENT_SECRET': os.environ.get('UDEMY_CLIENT_SECRET', 'your_udemy_client_secret_here'),
        'BASE_URL': 'https://www.udemy.com/api-2.0',
        'ENDPOINTS': {
            'courses': '/courses',
            'search': '/courses/search',
            'categories': '/categories'
        }
    },
    
    # LinkedIn Learning API Configuration
    'LINKEDIN_LEARNING': {
        'API_KEY': os.environ.get('LINKEDIN_LEARNING_API_KEY', 'your_linkedin_learning_api_key_here'),
        'CLIENT_ID': os.environ.get('LINKEDIN_CLIENT_ID', 'your_linkedin_client_id_here'),
        'CLIENT_SECRET': os.environ.get('LINKEDIN_CLIENT_SECRET', 'your_linkedin_client_secret_here'),
        'BASE_URL': 'https://api.linkedin.com/v2',
        'ENDPOINTS': {
            'courses': '/learning/courses',
            'search': '/learning/search',
            'categories': '/learning/categories'
        }
    },
    
    # edX API Configuration
    'EDX': {
        'API_KEY': os.environ.get('EDX_API_KEY', 'your_edx_api_key_here'),
        'BASE_URL': 'https://api.edx.org/catalog/v1',
        'ENDPOINTS': {
            'courses': '/catalogs',
            'search': '/catalogs/search',
            'categories': '/catalogs/categories'
        }
    },
    
    # YouTube Learning API Configuration
    'YOUTUBE': {
        'API_KEY': os.environ.get('YOUTUBE_API_KEY', 'your_youtube_api_key_here'),
        'BASE_URL': 'https://www.googleapis.com/youtube/v3',
        'ENDPOINTS': {
            'search': '/search',
            'playlists': '/playlists',
            'videos': '/videos'
        }
    },
    
    # Certification APIs
    'CERTIFICATION': {
        'SERVSAFE': {
            'API_KEY': os.environ.get('SERVSAFE_API_KEY', 'your_servsafe_api_key_here'),
            'BASE_URL': 'https://api.servsafe.com/v1',
            'ENDPOINTS': {
                'certifications': '/certifications',
                'courses': '/courses'
            }
        },
        'ACF': {
            'API_KEY': os.environ.get('ACF_API_KEY', 'your_acf_api_key_here'),
            'BASE_URL': 'https://api.acfchefs.org/v1',
            'ENDPOINTS': {
                'certifications': '/certifications',
                'programs': '/programs'
            }
        },
        'PHCC': {
            'API_KEY': os.environ.get('PHCC_API_KEY', 'your_phcc_api_key_here'),
            'BASE_URL': 'https://api.phccweb.org/v1',
            'ENDPOINTS': {
                'certifications': '/certifications',
                'apprenticeships': '/apprenticeships'
            }
        },
        'NECA': {
            'API_KEY': os.environ.get('NECA_API_KEY', 'your_neca_api_key_here'),
            'BASE_URL': 'https://api.necanet.org/v1',
            'ENDPOINTS': {
                'certifications': '/certifications',
                'training': '/training'
            }
        }
    },
    
    # Community Resource APIs
    'COMMUNITY': {
        'FOOD_BANKS': {
            'API_KEY': os.environ.get('FOOD_BANKS_API_KEY', 'your_food_banks_api_key_here'),
            'BASE_URL': 'https://api.feedingamerica.org/v1',
            'ENDPOINTS': {
                'locations': '/locations',
                'services': '/services'
            }
        },
        'HEALTH_CLINICS': {
            'API_KEY': os.environ.get('HEALTH_CLINICS_API_KEY', 'your_health_clinics_api_key_here'),
            'BASE_URL': 'https://api.healthcare.gov/v1',
            'ENDPOINTS': {
                'providers': '/providers',
                'services': '/services'
            }
        },
        'LEGAL_AID': {
            'API_KEY': os.environ.get('LEGAL_AID_API_KEY', 'your_legal_aid_api_key_here'),
            'BASE_URL': 'https://api.legalaid.org/v1',
            'ENDPOINTS': {
                'services': '/services',
                'providers': '/providers'
            }
        }
    }
}

# Skill Categories for API Integration
SKILL_CATEGORIES = {
    'cooking': {
        'keywords': ['cooking', 'culinary', 'food preparation', 'kitchen', 'chef'],
        'platforms': ['coursera', 'udemy', 'linkedin_learning', 'edx'],
        'certifications': ['servsafe', 'acf'],
        'resources': ['youtube', 'community']
    },
    'plumbing': {
        'keywords': ['plumbing', 'pipe fitting', 'water systems', 'drainage'],
        'platforms': ['udemy', 'linkedin_learning', 'youtube'],
        'certifications': ['phcc', 'state_licensing'],
        'resources': ['youtube', 'community']
    },
    'electrical': {
        'keywords': ['electrical', 'wiring', 'electrical systems', 'electrical safety'],
        'platforms': ['coursera', 'udemy', 'linkedin_learning'],
        'certifications': ['neca', 'state_licensing'],
        'resources': ['youtube', 'community']
    },
    'cleaning': {
        'keywords': ['cleaning', 'housekeeping', 'janitorial', 'sanitation'],
        'platforms': ['udemy', 'linkedin_learning', 'youtube'],
        'certifications': ['general'],
        'resources': ['youtube', 'community']
    },
    'carpentry': {
        'keywords': ['carpentry', 'woodworking', 'construction', 'building'],
        'platforms': ['udemy', 'linkedin_learning', 'youtube'],
        'certifications': ['general'],
        'resources': ['youtube', 'community']
    },
    'painting': {
        'keywords': ['painting', 'decorating', 'interior design', 'color'],
        'platforms': ['udemy', 'linkedin_learning', 'youtube'],
        'certifications': ['general'],
        'resources': ['youtube', 'community']
    },
    'gardening': {
        'keywords': ['gardening', 'landscaping', 'horticulture', 'plants'],
        'platforms': ['coursera', 'udemy', 'linkedin_learning', 'youtube'],
        'certifications': ['general'],
        'resources': ['youtube', 'community']
    },
    'mechanical': {
        'keywords': ['mechanical', 'repair', 'maintenance', 'automotive'],
        'platforms': ['udemy', 'linkedin_learning', 'youtube'],
        'certifications': ['general'],
        'resources': ['youtube', 'community']
    },
    'tailoring': {
        'keywords': ['tailoring', 'sewing', 'fashion', 'textiles'],
        'platforms': ['udemy', 'linkedin_learning', 'youtube'],
        'certifications': ['general'],
        'resources': ['youtube', 'community']
    },
    'salon': {
        'keywords': ['beauty', 'salon', 'cosmetology', 'hair styling'],
        'platforms': ['udemy', 'linkedin_learning', 'youtube'],
        'certifications': ['general'],
        'resources': ['youtube', 'community']
    }
}

# API Rate Limiting Configuration
RATE_LIMITS = {
    'coursera': {'requests_per_minute': 60, 'requests_per_day': 1000},
    'udemy': {'requests_per_minute': 30, 'requests_per_day': 500},
    'linkedin_learning': {'requests_per_minute': 20, 'requests_per_day': 300},
    'edx': {'requests_per_minute': 40, 'requests_per_day': 800},
    'youtube': {'requests_per_minute': 100, 'requests_per_day': 10000}
}

# Cache Configuration for API Responses
CACHE_CONFIG = {
    'skill_recommendations': 3600,  # 1 hour
    'certification_links': 7200,    # 2 hours
    'online_learning_links': 1800,  # 30 minutes
    'community_resources': 86400    # 24 hours
}

# Error Messages for API Failures
ERROR_MESSAGES = {
    'api_unavailable': 'The learning platform is temporarily unavailable. Please try again later.',
    'rate_limit_exceeded': 'Too many requests. Please wait a moment and try again.',
    'invalid_api_key': 'API configuration error. Please contact support.',
    'no_results': 'No recommendations found for your skills. Try broadening your search.',
    'network_error': 'Network error. Please check your connection and try again.'
}

def get_api_config(service):
    """Get API configuration for a specific service"""
    return API_CONFIG.get(service, {})

def get_skill_config(skill):
    """Get configuration for a specific skill"""
    return SKILL_CATEGORIES.get(skill, SKILL_CATEGORIES.get('general', {}))

def is_api_enabled(service):
    """Check if an API service is enabled"""
    config = get_api_config(service)
    return bool(config.get('API_KEY') and config.get('API_KEY') != f'your_{service.lower()}_api_key_here')

def get_enabled_apis():
    """Get list of enabled APIs"""
    return [service for service in API_CONFIG.keys() if is_api_enabled(service)] 