"""
Readiness Score Calculator
Calculates individual readiness score for transitioning to future STEM industries
"""

import numpy as np
from typing import Dict, List, Tuple
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import FUTURE_INDUSTRIES, SCORING_WEIGHTS

class ReadinessCalculator:
    def __init__(self):
        """Initialize readiness calculator"""
        self.weights = SCORING_WEIGHTS
        self.industry_requirements = self._load_industry_requirements()
        
    def _load_industry_requirements(self) -> Dict[str, Dict]:
        """Load specific requirements for each industry"""
        return {
            "AI": {
                "essential_skills": ["Python", "Machine Learning", "Mathematics", "Statistics"],
                "preferred_skills": ["TensorFlow", "PyTorch", "Deep Learning", "NLP", "Computer Vision"],
                "experience_level": "intermediate",
                "education_preference": "technical",
                "project_importance": 0.9
            },
            "BLOCKCHAIN": {
                "essential_skills": ["Programming", "Cryptography", "Distributed Systems"],
                "preferred_skills": ["Solidity", "Web3", "Smart Contracts", "DeFi", "Ethereum"],
                "experience_level": "intermediate",
                "education_preference": "technical",
                "project_importance": 0.85
            },
            "CYBERSECURITY": {
                "essential_skills": ["Networking", "Security Fundamentals", "Linux", "Python"],
                "preferred_skills": ["Penetration Testing", "SIEM", "Cloud Security", "Cryptography"],
                "experience_level": "intermediate",
                "education_preference": "technical",
                "project_importance": 0.8
            },
            "BIOTECH": {
                "essential_skills": ["Biology", "Data Analysis", "Research Methods"],
                "preferred_skills": ["Bioinformatics", "Genomics", "R/Python", "Lab Techniques"],
                "experience_level": "advanced",
                "education_preference": "scientific",
                "project_importance": 0.7
            },
            "AGRITECH": {
                "essential_skills": ["Agriculture Knowledge", "Data Analysis", "IoT"],
                "preferred_skills": ["Precision Agriculture", "GIS", "Sustainability", "Automation"],
                "experience_level": "intermediate",
                "education_preference": "mixed",
                "project_importance": 0.75
            },
            "AQUATECH": {
                "essential_skills": ["Marine Science", "Data Analysis", "Environmental Science"],
                "preferred_skills": ["Aquaculture Systems", "Water Quality", "IoT", "Sustainability"],
                "experience_level": "intermediate",
                "education_preference": "scientific",
                "project_importance": 0.7
            },
            "SPACETECH": {
                "essential_skills": ["Engineering", "Mathematics", "Physics", "Programming"],
                "preferred_skills": ["Aerospace Engineering", "Systems Engineering", "MATLAB", "Simulation"],
                "experience_level": "advanced",
                "education_preference": "engineering",
                "project_importance": 0.85
            },
            "RENEWABLE": {
                "essential_skills": ["Engineering", "Energy Systems", "Mathematics"],
                "preferred_skills": ["Solar/Wind Technology", "Grid Systems", "Energy Storage", "Sustainability"],
                "experience_level": "intermediate",
                "education_preference": "engineering",
                "project_importance": 0.8
            }
        }
    
    def calculate_readiness_score(self, user_profile: Dict, target_industry: str) -> Dict:
        """
        Calculate comprehensive readiness score
        
        Args:
            user_profile: User's profile with skills, experience, education
            target_industry: Target STEM industry
            
        Returns:
            Detailed readiness assessment
        """
        # Extract user information
        user_skills = user_profile.get("skills", {})
        experience_years = user_profile.get("experience_years", 0)
        education_level = user_profile.get("education_level", "")
        current_role = user_profile.get("current_role", "")
        projects = user_profile.get("projects", [])
        certifications = user_profile.get("certifications", [])
        
        # Calculate component scores
        skill_match_score = self._calculate_skill_match(user_skills, target_industry)
        experience_score = self._calculate_experience_score(experience_years, current_role, target_industry)
        education_score = self._calculate_education_score(education_level, target_industry)
        project_score = self._calculate_project_score(projects, target_industry)
        certification_score = self._calculate_certification_score(certifications, target_industry)
        
        # Calculate learning curve score
        learning_curve_score = self._calculate_learning_curve(user_skills, target_industry)
        
        # Calculate market readiness
        market_readiness = self._calculate_market_readiness(target_industry)
        
        # Weighted final score
        final_score = (
            skill_match_score * self.weights["current_skills_match"] +
            experience_score * self.weights["transferable_skills"] +
            learning_curve_score * self.weights["learning_curve"] +
            market_readiness * self.weights["market_demand"]
        )
        
        # Additional factors
        bonus_score = (education_score + project_score + certification_score) / 3 * 0.1
        final_score = min(final_score + bonus_score, 1.0)
        
        # Generate readiness level
        readiness_level = self._get_readiness_level(final_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            skill_match_score, experience_score, learning_curve_score, 
            user_skills, target_industry
        )
        
        # Time to readiness estimate
        time_to_ready = self._estimate_time_to_readiness(final_score, learning_curve_score)
        
        return {
            "overall_score": round(final_score * 100, 1),
            "readiness_level": readiness_level,
            "component_scores": {
                "skill_match": round(skill_match_score * 100, 1),
                "experience": round(experience_score * 100, 1),
                "education": round(education_score * 100, 1),
                "projects": round(project_score * 100, 1),
                "certifications": round(certification_score * 100, 1),
                "learning_curve": round(learning_curve_score * 100, 1),
                "market_readiness": round(market_readiness * 100, 1)
            },
            "time_to_ready": time_to_ready,
            "recommendations": recommendations,
            "strengths": self._identify_strengths(user_profile, target_industry),
            "gaps": self._identify_gaps(user_skills, target_industry),
            "next_steps": self._generate_next_steps(final_score, target_industry)
        }
    
    def _calculate_skill_match(self, user_skills: Dict, industry: str) -> float:
        """Calculate skill match score"""
        requirements = self.industry_requirements.get(industry, {})
        essential_skills = requirements.get("essential_skills", [])
        preferred_skills = requirements.get("preferred_skills", [])
        
        # Flatten user skills
        all_user_skills = []
        for category, skills in user_skills.items():
            all_user_skills.extend([s.lower() for s in skills])
        
        # Check essential skills (60% weight)
        essential_match = sum(1 for skill in essential_skills if skill.lower() in all_user_skills)
        essential_score = essential_match / len(essential_skills) if essential_skills else 0
        
        # Check preferred skills (40% weight)
        preferred_match = sum(1 for skill in preferred_skills if skill.lower() in all_user_skills)
        preferred_score = preferred_match / len(preferred_skills) if preferred_skills else 0
        
        return essential_score * 0.6 + preferred_score * 0.4
    
    def _calculate_experience_score(self, years: int, current_role: str, industry: str) -> float:
        """Calculate experience relevance score"""
        # Base score from years of experience
        if years >= 10:
            base_score = 0.9
        elif years >= 5:
            base_score = 0.7
        elif years >= 3:
            base_score = 0.5
        elif years >= 1:
            base_score = 0.3
        else:
            base_score = 0.1
        
        # Adjust based on role relevance
        role_relevance = {
            "software_developer": 0.8,
            "data_analyst": 0.75,
            "engineer": 0.7,
            "researcher": 0.65,
            "teacher": 0.4,
            "healthcare_professional": 0.5,
            "accountant": 0.45,
            "marketing_professional": 0.4
        }
        
        relevance_modifier = role_relevance.get(current_role.lower().replace(" ", "_"), 0.5)
        
        return base_score * relevance_modifier
    
    def _calculate_education_score(self, education: str, industry: str) -> float:
        """Calculate education relevance score"""
        requirements = self.industry_requirements.get(industry, {})
        preference = requirements.get("education_preference", "technical")
        
        education_scores = {
            "phd": {"technical": 1.0, "scientific": 1.0, "engineering": 1.0, "mixed": 0.9},
            "masters": {"technical": 0.9, "scientific": 0.9, "engineering": 0.9, "mixed": 0.8},
            "bachelors": {"technical": 0.7, "scientific": 0.7, "engineering": 0.7, "mixed": 0.7},
            "associate": {"technical": 0.5, "scientific": 0.4, "engineering": 0.5, "mixed": 0.5},
            "high_school": {"technical": 0.3, "scientific": 0.2, "engineering": 0.3, "mixed": 0.4}
        }
        
        education_lower = education.lower()
        for edu_level, scores in education_scores.items():
            if edu_level in education_lower:
                return scores.get(preference, 0.5)
        
        return 0.5  # Default score
    
    def _calculate_project_score(self, projects: List[str], industry: str) -> float:
        """Calculate project relevance score"""
        if not projects:
            return 0.0
        
        requirements = self.industry_requirements.get(industry, {})
        importance = requirements.get("project_importance", 0.7)
        
        # Simple heuristic: more projects = higher score
        project_count = len(projects)
        if project_count >= 5:
            base_score = 0.9
        elif project_count >= 3:
            base_score = 0.7
        elif project_count >= 1:
            base_score = 0.4
        else:
            base_score = 0.0
        
        return base_score * importance
    
    def _calculate_certification_score(self, certifications: List[str], industry: str) -> float:
        """Calculate certification relevance score"""
        if not certifications:
            return 0.0
        
        # Industry-relevant certification keywords
        industry_certs = {
            "AI": ["machine learning", "deep learning", "ai", "tensorflow", "aws ml"],
            "BLOCKCHAIN": ["blockchain", "ethereum", "solidity", "web3", "defi"],
            "CYBERSECURITY": ["security+", "cissp", "ceh", "oscp", "ccna security"],
            "BIOTECH": ["bioinformatics", "clinical", "gcp", "biostatistics"],
            "AGRITECH": ["precision agriculture", "iot", "sustainability", "gis"],
            "AQUATECH": ["aquaculture", "marine", "water quality", "environmental"],
            "SPACETECH": ["aerospace", "systems engineering", "satellite", "space"],
            "RENEWABLE": ["renewable energy", "solar", "wind", "energy management", "leed"]
        }
        
        relevant_keywords = industry_certs.get(industry, [])
        cert_text = " ".join(certifications).lower()
        
        matches = sum(1 for keyword in relevant_keywords if keyword in cert_text)
        return min(matches / 3, 1.0)  # Cap at 3 relevant certs
    
    def _calculate_learning_curve(self, user_skills: Dict, industry: str) -> float:
        """Calculate learning curve difficulty (inverse - higher score = easier learning)"""
        requirements = self.industry_requirements.get(industry, {})
        essential_skills = requirements.get("essential_skills", [])
        
        # Flatten user skills
        all_user_skills = []
        for category, skills in user_skills.items():
            all_user_skills.extend([s.lower() for s in skills])
        
        # Check for foundational skills that make learning easier
        foundational_skills = ["programming", "data analysis", "mathematics", "problem solving"]
        foundation_score = sum(1 for skill in foundational_skills if skill in all_user_skills)
        foundation_score = foundation_score / len(foundational_skills)
        
        # Check existing match with essential skills
        skill_match = self._calculate_skill_match(user_skills, industry)
        
        # Learning curve score (higher = easier to learn)
        learning_score = (foundation_score * 0.4 + skill_match * 0.6)
        
        return learning_score
    
    def _calculate_market_readiness(self, industry: str) -> float:
        """Calculate market demand and readiness"""
        # Simplified market scores based on current trends
        market_scores = {
            "AI": 0.95,
            "CYBERSECURITY": 0.9,
            "RENEWABLE": 0.85,
            "BLOCKCHAIN": 0.8,
            "BIOTECH": 0.8,
            "SPACETECH": 0.75,
            "AGRITECH": 0.75,
            "AQUATECH": 0.7
        }
        
        return market_scores.get(industry, 0.7)
    
    def _get_readiness_level(self, score: float) -> str:
        """Convert score to readiness level"""
        if score >= 0.8:
            return "Ready to Transition"
        elif score >= 0.6:
            return "Nearly Ready"
        elif score >= 0.4:
            return "Developing Readiness"
        elif score >= 0.2:
            return "Early Stage"
        else:
            return "Foundation Building"
    
    def _estimate_time_to_readiness(self, overall_score: float, learning_score: float) -> str:
        """Estimate time needed to be ready"""
        # Combine overall readiness and learning ease
        combined_score = (overall_score + learning_score) / 2
        
        if combined_score >= 0.8:
            return "0-3 months"
        elif combined_score >= 0.6:
            return "3-6 months"
        elif combined_score >= 0.4:
            return "6-12 months"
        elif combined_score >= 0.2:
            return "12-18 months"
        else:
            return "18-24 months"
    
    def _generate_recommendations(self, skill_score: float, exp_score: float, 
                                learning_score: float, user_skills: Dict, industry: str) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if skill_score < 0.5:
            recommendations.append("Focus on building essential technical skills through online courses and bootcamps")
        
        if exp_score < 0.5:
            recommendations.append("Gain practical experience through internships, freelance projects, or open-source contributions")
        
        if learning_score < 0.5:
            recommendations.append("Strengthen foundational skills in programming and mathematics")
        
        # Industry-specific recommendations
        requirements = self.industry_requirements.get(industry, {})
        essential_skills = requirements.get("essential_skills", [])
        
        all_user_skills = []
        for category, skills in user_skills.items():
            all_user_skills.extend([s.lower() for s in skills])
        
        missing_essentials = [s for s in essential_skills if s.lower() not in all_user_skills]
        if missing_essentials:
            recommendations.append(f"Priority skills to learn: {', '.join(missing_essentials[:3])}")
        
        recommendations.append("Build a portfolio showcasing relevant projects")
        recommendations.append("Network with professionals in your target industry")
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _identify_strengths(self, user_profile: Dict, industry: str) -> List[str]:
        """Identify user's strengths for the transition"""
        strengths = []
        
        # Check experience
        if user_profile.get("experience_years", 0) >= 5:
            strengths.append("Strong professional experience")
        
        # Check education
        education = user_profile.get("education_level", "").lower()
        if any(level in education for level in ["masters", "phd", "bachelor"]):
            strengths.append("Solid educational background")
        
        # Check relevant skills
        user_skills = user_profile.get("skills", {})
        all_skills = []
        for category, skills in user_skills.items():
            all_skills.extend(skills)
        
        if len(all_skills) > 10:
            strengths.append("Diverse skill set")
        
        # Check projects
        if len(user_profile.get("projects", [])) > 2:
            strengths.append("Proven project experience")
        
        return strengths
    
    def _identify_gaps(self, user_skills: Dict, industry: str) -> List[str]:
        """Identify skill gaps"""
        requirements = self.industry_requirements.get(industry, {})
        essential_skills = requirements.get("essential_skills", [])
        preferred_skills = requirements.get("preferred_skills", [])
        
        all_user_skills = []
        for category, skills in user_skills.items():
            all_user_skills.extend([s.lower() for s in skills])
        
        gaps = []
        
        # Essential skill gaps
        essential_gaps = [s for s in essential_skills if s.lower() not in all_user_skills]
        if essential_gaps:
            gaps.extend([f"Essential: {skill}" for skill in essential_gaps[:3]])
        
        # Preferred skill gaps
        preferred_gaps = [s for s in preferred_skills if s.lower() not in all_user_skills]
        if preferred_gaps:
            gaps.extend([f"Preferred: {skill}" for skill in preferred_gaps[:2]])
        
        return gaps[:5]
    
    def _generate_next_steps(self, score: float, industry: str) -> List[str]:
        """Generate immediate next steps"""
        if score >= 0.8:
            return [
                "Update resume highlighting relevant skills",
                "Apply for entry-level positions in the industry",
                "Join industry-specific communities and forums"
            ]
        elif score >= 0.6:
            return [
                "Complete 1-2 industry-relevant certifications",
                "Build 2-3 portfolio projects",
                "Attend industry meetups and conferences"
            ]
        elif score >= 0.4:
            return [
                "Enroll in comprehensive online courses",
                "Start with beginner projects",
                "Find a mentor in the field"
            ]
        else:
            return [
                "Build foundational skills through MOOCs",
                "Join study groups or bootcamps",
                "Create a structured learning plan"
            ]
