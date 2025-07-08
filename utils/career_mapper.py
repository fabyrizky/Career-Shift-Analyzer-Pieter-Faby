"""
Career Mapper Module
Maps current career to potential future STEM careers
"""

import pandas as pd
from typing import Dict, List, Tuple
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import FUTURE_INDUSTRIES

class CareerMapper:
    def __init__(self):
        """Initialize career mapper with transition data"""
        self.transition_matrix = self._build_transition_matrix()
        self.career_paths = self._define_career_paths()
        
    def _build_transition_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Build transition probability matrix between careers
        Higher score = easier transition
        """
        return {
            # From Traditional Roles
            "accountant": {
                "AI": 0.6,  # Data analysis skills transfer
                "BLOCKCHAIN": 0.8,  # DeFi, crypto accounting
                "CYBERSECURITY": 0.5,  # Compliance, risk management
                "BIOTECH": 0.4,  # Financial analysis in biotech
                "AGRITECH": 0.5,  # AgTech business analysis
                "AQUATECH": 0.4,  # Marine business management
                "SPACETECH": 0.3,  # Space industry finance
                "RENEWABLE": 0.6   # Energy economics
            },
            "software_developer": {
                "AI": 0.9,  # Natural progression
                "BLOCKCHAIN": 0.85,  # Smart contract development
                "CYBERSECURITY": 0.8,  # Security development
                "BIOTECH": 0.7,  # Bioinformatics
                "AGRITECH": 0.75,  # AgTech software
                "AQUATECH": 0.7,  # Marine tech systems
                "SPACETECH": 0.8,  # Space software systems
                "RENEWABLE": 0.75  # Energy management systems
            },
            "data_analyst": {
                "AI": 0.95,  # Direct path to ML/AI
                "BLOCKCHAIN": 0.7,  # Blockchain analytics
                "CYBERSECURITY": 0.75,  # Security analytics
                "BIOTECH": 0.85,  # Biostatistics
                "AGRITECH": 0.8,  # Precision agriculture
                "AQUATECH": 0.75,  # Marine data analysis
                "SPACETECH": 0.7,  # Space data analysis
                "RENEWABLE": 0.8   # Energy data analytics
            },
            "engineer": {
                "AI": 0.7,  # AI/ML engineering
                "BLOCKCHAIN": 0.6,  # Infrastructure
                "CYBERSECURITY": 0.65,  # Security engineering
                "BIOTECH": 0.7,  # Biomedical engineering
                "AGRITECH": 0.85,  # Agricultural engineering
                "AQUATECH": 0.8,  # Marine engineering
                "SPACETECH": 0.9,  # Aerospace engineering
                "RENEWABLE": 0.95  # Energy engineering
            },
            "teacher": {
                "AI": 0.5,  # EdTech, AI training
                "BLOCKCHAIN": 0.4,  # Blockchain education
                "CYBERSECURITY": 0.5,  # Security awareness training
                "BIOTECH": 0.5,  # Science education
                "AGRITECH": 0.6,  # Agricultural education
                "AQUATECH": 0.5,  # Marine science education
                "SPACETECH": 0.5,  # STEM education
                "RENEWABLE": 0.6   # Sustainability education
            },
            "healthcare_professional": {
                "AI": 0.7,  # Medical AI
                "BLOCKCHAIN": 0.5,  # Healthcare blockchain
                "CYBERSECURITY": 0.6,  # Healthcare security
                "BIOTECH": 0.95,  # Natural fit
                "AGRITECH": 0.4,  # Food safety
                "AQUATECH": 0.5,  # Marine biotechnology
                "SPACETECH": 0.6,  # Space medicine
                "RENEWABLE": 0.4   # Environmental health
            },
            "marketing_professional": {
                "AI": 0.6,  # AI marketing tools
                "BLOCKCHAIN": 0.7,  # Crypto marketing
                "CYBERSECURITY": 0.5,  # Security marketing
                "BIOTECH": 0.6,  # Biotech marketing
                "AGRITECH": 0.7,  # AgTech marketing
                "AQUATECH": 0.6,  # Marine industry marketing
                "SPACETECH": 0.6,  # Space industry marketing
                "RENEWABLE": 0.7   # Green energy marketing
            },
            "researcher": {
                "AI": 0.85,  # AI research
                "BLOCKCHAIN": 0.7,  # Blockchain research
                "CYBERSECURITY": 0.7,  # Security research
                "BIOTECH": 0.9,  # Biotech research
                "AGRITECH": 0.85,  # Agricultural research
                "AQUATECH": 0.85,  # Marine research
                "SPACETECH": 0.9,  # Space research
                "RENEWABLE": 0.85  # Energy research
            }
        }
    
    def _define_career_paths(self) -> Dict[str, List[Dict[str, str]]]:
        """Define specific career transition paths with milestones"""
        return {
            "accountant_to_blockchain": [
                {
                    "step": 1,
                    "title": "Learn Blockchain Fundamentals",
                    "duration": "2-3 months",
                    "skills": ["Blockchain basics", "Cryptocurrency", "DeFi concepts"],
                    "resources": ["Blockchain Council", "Coursera Blockchain Specialization"]
                },
                {
                    "step": 2,
                    "title": "Master Smart Contracts",
                    "duration": "3-4 months",
                    "skills": ["Solidity", "Web3.js", "Smart contract auditing"],
                    "resources": ["CryptoZombies", "Ethereum.org tutorials"]
                },
                {
                    "step": 3,
                    "title": "Specialize in DeFi/Crypto Accounting",
                    "duration": "2-3 months",
                    "skills": ["DeFi protocols", "Crypto taxation", "Blockchain analytics"],
                    "resources": ["DeFi courses", "Crypto accounting certifications"]
                }
            ],
            "developer_to_ai": [
                {
                    "step": 1,
                    "title": "Foundation in ML/AI",
                    "duration": "3-4 months",
                    "skills": ["Python", "Machine Learning basics", "Statistics"],
                    "resources": ["Andrew Ng's ML Course", "Fast.ai"]
                },
                {
                    "step": 2,
                    "title": "Deep Learning & Specialization",
                    "duration": "4-6 months",
                    "skills": ["TensorFlow/PyTorch", "Neural Networks", "Computer Vision/NLP"],
                    "resources": ["Deep Learning Specialization", "PyTorch tutorials"]
                },
                {
                    "step": 3,
                    "title": "Industry Application",
                    "duration": "3-4 months",
                    "skills": ["MLOps", "Model deployment", "AI ethics"],
                    "resources": ["Google Cloud AI", "AWS ML Certification"]
                }
            ],
            "analyst_to_biotech": [
                {
                    "step": 1,
                    "title": "Biology & Bioinformatics Basics",
                    "duration": "3-4 months",
                    "skills": ["Molecular biology", "Genetics", "Bioinformatics tools"],
                    "resources": ["Coursera Bioinformatics", "edX Biology courses"]
                },
                {
                    "step": 2,
                    "title": "Computational Biology",
                    "duration": "4-5 months",
                    "skills": ["R/Python for biology", "Genomic data analysis", "Biostatistics"],
                    "resources": ["Bioconductor", "Rosalind platform"]
                },
                {
                    "step": 3,
                    "title": "Industry Specialization",
                    "duration": "3-4 months",
                    "skills": ["Clinical data analysis", "Drug discovery", "Precision medicine"],
                    "resources": ["Industry internships", "Biotech bootcamps"]
                }
            ]
        }
    
    def map_career_transition(self, current_role: str, target_industry: str) -> Dict:
        """
        Map career transition from current role to target industry
        
        Args:
            current_role: Current job role
            target_industry: Target STEM industry
            
        Returns:
            Transition analysis with score, path, and recommendations
        """
        # Normalize inputs
        current_role = current_role.lower().replace(" ", "_")
        
        # Get transition score
        transition_score = self._calculate_transition_score(current_role, target_industry)
        
        # Get transition difficulty
        difficulty = self._get_transition_difficulty(transition_score)
        
        # Get recommended path
        path_key = f"{current_role}_to_{target_industry.lower()}"
        specific_path = self.career_paths.get(path_key, self._generate_generic_path(current_role, target_industry))
        
        # Get transferable skills
        transferable_skills = self._identify_transferable_skills(current_role, target_industry)
        
        # Get skill gaps
        skill_gaps = self._identify_skill_gaps(current_role, target_industry)
        
        return {
            "transition_score": transition_score,
            "difficulty": difficulty,
            "estimated_duration": self._estimate_duration(difficulty),
            "career_path": specific_path,
            "transferable_skills": transferable_skills,
            "skill_gaps": skill_gaps,
            "success_factors": self._get_success_factors(current_role, target_industry),
            "potential_roles": self._get_potential_roles(target_industry)
        }
    
    def _calculate_transition_score(self, current_role: str, target_industry: str) -> float:
        """Calculate transition feasibility score (0-1)"""
        # Get base score from transition matrix
        if current_role in self.transition_matrix:
            base_score = self.transition_matrix[current_role].get(target_industry, 0.5)
        else:
            # Default score for unknown roles
            base_score = 0.5
        
        # Apply modifiers based on market demand and growth
        market_modifier = self._get_market_modifier(target_industry)
        
        final_score = base_score * market_modifier
        return min(max(final_score, 0.0), 1.0)
    
    def _get_transition_difficulty(self, score: float) -> str:
        """Categorize transition difficulty based on score"""
        if score >= 0.8:
            return "Easy"
        elif score >= 0.6:
            return "Moderate"
        elif score >= 0.4:
            return "Challenging"
        else:
            return "Very Challenging"
    
    def _estimate_duration(self, difficulty: str) -> str:
        """Estimate transition duration based on difficulty"""
        duration_map = {
            "Easy": "6-9 months",
            "Moderate": "9-12 months",
            "Challenging": "12-18 months",
            "Very Challenging": "18-24 months"
        }
        return duration_map.get(difficulty, "12-18 months")
    
    def _generate_generic_path(self, current_role: str, target_industry: str) -> List[Dict]:
        """Generate generic career transition path"""
        industry_info = FUTURE_INDUSTRIES.get(target_industry, {})
        key_skills = industry_info.get("key_skills", [])
        
        return [
            {
                "step": 1,
                "title": f"Learn {industry_info.get('name', target_industry)} Fundamentals",
                "duration": "2-3 months",
                "skills": key_skills[:3] if key_skills else ["Industry basics"],
                "resources": ["Online courses", "Industry documentation", "YouTube tutorials"]
            },
            {
                "step": 2,
                "title": "Develop Core Technical Skills",
                "duration": "4-6 months",
                "skills": key_skills[3:6] if len(key_skills) > 3 else ["Technical skills"],
                "resources": ["Specialized courses", "Bootcamps", "Certifications"]
            },
            {
                "step": 3,
                "title": "Build Portfolio & Network",
                "duration": "3-4 months",
                "skills": ["Project development", "Industry networking", "Portfolio building"],
                "resources": ["GitHub projects", "LinkedIn networking", "Industry meetups"]
            }
        ]
    
    def _identify_transferable_skills(self, current_role: str, target_industry: str) -> List[str]:
        """Identify skills that transfer from current role to target industry"""
        # Define transferable skills by role
        role_skills = {
            "accountant": ["analytical thinking", "attention to detail", "data analysis", 
                          "financial modeling", "compliance", "risk assessment"],
            "software_developer": ["programming", "problem solving", "system design", 
                                 "debugging", "version control", "agile methodology"],
            "data_analyst": ["data visualization", "statistical analysis", "SQL", 
                           "reporting", "critical thinking", "pattern recognition"],
            "engineer": ["technical problem solving", "project management", "mathematics",
                        "system optimization", "technical documentation", "CAD skills"],
            "teacher": ["communication", "presentation skills", "curriculum development",
                       "mentoring", "patience", "adaptability"],
            "healthcare_professional": ["attention to detail", "ethics", "research skills",
                                      "patient care", "documentation", "teamwork"],
            "marketing_professional": ["communication", "market analysis", "creativity",
                                     "digital marketing", "brand management", "analytics"],
            "researcher": ["research methodology", "data analysis", "scientific writing",
                         "hypothesis testing", "literature review", "experimentation"]
        }
        
        current_skills = role_skills.get(current_role, ["problem solving", "communication"])
        
        # Industry-agnostic transferable skills
        universal_skills = ["problem solving", "communication", "teamwork", "adaptability"]
        
        return list(set(current_skills + universal_skills))
    
    def _identify_skill_gaps(self, current_role: str, target_industry: str) -> List[str]:
        """Identify skills needed for target industry"""
        industry_info = FUTURE_INDUSTRIES.get(target_industry, {})
        required_skills = industry_info.get("key_skills", [])
        
        # Get current role's typical skills
        current_skills = self._get_role_technical_skills(current_role)
        
        # Find gaps
        skill_gaps = [skill for skill in required_skills if skill.lower() not in 
                     [s.lower() for s in current_skills]]
        
        return skill_gaps[:6]  # Return top 6 gaps
    
    def _get_role_technical_skills(self, role: str) -> List[str]:
        """Get typical technical skills for a role"""
        role_tech_skills = {
            "accountant": ["Excel", "QuickBooks", "SQL", "Financial Analysis"],
            "software_developer": ["Python", "JavaScript", "Git", "APIs", "Databases"],
            "data_analyst": ["SQL", "Python", "Tableau", "Excel", "Statistics"],
            "engineer": ["CAD", "MATLAB", "Project Management", "Technical Drawing"],
            "teacher": ["Curriculum Design", "Assessment", "Educational Technology"],
            "healthcare_professional": ["Clinical Skills", "Medical Knowledge", "EMR Systems"],
            "marketing_professional": ["SEO", "Google Analytics", "Social Media", "CRM"],
            "researcher": ["Research Methods", "Statistical Analysis", "Academic Writing"]
        }
        
        return role_tech_skills.get(role, [])
    
    def _get_market_modifier(self, industry: str) -> float:
        """Get market demand modifier for industry"""
        # Market growth rates (simplified)
        market_modifiers = {
            "AI": 1.3,  # High growth
            "BLOCKCHAIN": 1.2,
            "CYBERSECURITY": 1.25,
            "BIOTECH": 1.15,
            "AGRITECH": 1.1,
            "AQUATECH": 1.05,
            "SPACETECH": 1.15,
            "RENEWABLE": 1.2
        }
        return market_modifiers.get(industry, 1.0)
    
    def _get_success_factors(self, current_role: str, target_industry: str) -> List[str]:
        """Get key success factors for transition"""
        return [
            "Strong commitment to continuous learning",
            "Building a portfolio of relevant projects",
            "Networking within the target industry",
            "Obtaining industry-recognized certifications",
            "Finding a mentor in the target field",
            "Starting with transitional roles or freelance projects"
        ]
    
    def _get_potential_roles(self, industry: str) -> List[str]:
        """Get potential job roles in target industry"""
        industry_roles = {
            "AI": ["ML Engineer", "Data Scientist", "AI Researcher", "ML Ops Engineer", 
                   "Computer Vision Engineer", "NLP Engineer"],
            "BLOCKCHAIN": ["Blockchain Developer", "Smart Contract Developer", "DeFi Analyst",
                          "Crypto Security Specialist", "Blockchain Architect", "Web3 Developer"],
            "CYBERSECURITY": ["Security Analyst", "Penetration Tester", "Security Engineer",
                             "SOC Analyst", "Security Architect", "Incident Response Specialist"],
            "BIOTECH": ["Bioinformatician", "Clinical Data Analyst", "Biotech Researcher",
                        "Genomics Specialist", "Biostatistician", "Medical Device Engineer"],
            "AGRITECH": ["Precision Agriculture Specialist", "AgTech Developer", "Farm Data Analyst",
                         "Sustainable Agriculture Consultant", "IoT Agriculture Engineer"],
            "AQUATECH": ["Aquaculture Systems Engineer", "Marine Biologist", "Aquatech Data Analyst",
                         "Sustainable Fisheries Manager", "Marine Biotechnologist"],
            "SPACETECH": ["Satellite Engineer", "Space Systems Analyst", "Mission Planner",
                         "Spacecraft Software Developer", "Remote Sensing Specialist"],
            "RENEWABLE": ["Renewable Energy Engineer", "Energy Data Analyst", "Solar/Wind Technician",
                         "Energy Storage Specialist", "Grid Integration Engineer", "Sustainability Analyst"]
        }
        
        return industry_roles.get(industry, ["Industry Specialist", "Technical Analyst", "Project Manager"])
