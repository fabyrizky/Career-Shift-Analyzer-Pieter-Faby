import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_TITLE = "Career Shift to Future STEM Industry"
APP_ICON = "🚀"
VERSION = "1.0.0"

# STEM Fields Data
STEM_FIELDS = {
    'AI & Machine Learning': {
        'icon': '🤖',
        'growth': '+25%',
        'avg_salary': 145000,
        'description': 'Build intelligent systems'
    },
    'Data Science': {
        'icon': '📊', 
        'growth': '+18%',
        'avg_salary': 125000,
        'description': 'Extract insights from data'
    },
    'Cybersecurity': {
        'icon': '🔒',
        'growth': '+15%', 
        'avg_salary': 110000,
        'description': 'Protect digital assets'
    },
    'Cloud Computing': {
        'icon': '☁️',
        'growth': '+28%',
        'avg_salary': 135000,
        'description': 'Scale applications globally'
    }
}

# Scoring weights
SCORING_WEIGHTS = {
    "current_skills_match": 0.35,
    "transferable_skills": 0.25,
    "learning_curve": 0.20,
    "market_demand": 0.20
}
