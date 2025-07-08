"""
Reusable UI Components for Streamlit App
"""

import streamlit as st
from typing import List, Dict, Optional
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import FUTURE_INDUSTRIES, UI_CONFIG
except ImportError:
    # Fallback values if config not accessible
    FUTURE_INDUSTRIES = {}
    UI_CONFIG = {
        "primary_color": "#1E88E5",
        "secondary_color": "#FFC107",
        "success_color": "#4CAF50",
        "warning_color": "#FF9800",
        "danger_color": "#F44336"
    }

def render_header():
    """Render application header"""
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Career Shift to Future STEM Industry</h1>
        <p>AI-powered career transition analyzer for emerging tech industries</p>
    </div>
    """, unsafe_allow_html=True)

def render_industry_card(industry_key: str, industry_info: Dict):
    """Render an industry information card"""
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<h1 style='text-align: center;'>{industry_info['icon']}</h1>", 
                       unsafe_allow_html=True)
        with col2:
            st.subheader(industry_info['name'])
            st.caption(industry_info['description'])
            
            # Display key skills as tags
            skills_html = " ".join([f"<span style='background-color: #e0e0e0; padding: 4px 8px; "
                                  f"border-radius: 4px; margin: 2px; display: inline-block; "
                                  f"font-size: 0.8em;'>{skill}</span>" 
                                  for skill in industry_info['key_skills'][:5]])
            st.markdown(skills_html, unsafe_allow_html=True)
        
        st.markdown("---")

def render_progress_bar(label: str, value: float, color: str = "#1E88E5"):
    """Render a custom progress bar"""
    st.markdown(f"""
    <div style="margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>{label}</span>
            <span>{value:.0f}%</span>
        </div>
        <div style="width: 100%; background-color: #e0e0e0; border-radius: 10px; height: 20px;">
            <div style="width: {value}%; background-color: {color}; 
                        border-radius: 10px; height: 100%; 
                        transition: width 0.5s ease-in-out;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_skill_input_section() -> Dict:
    """Render skill input section and return user inputs"""
    st.subheader("📝 Tell us about yourself")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_role = st.text_input("Current Role/Job Title", 
                                    placeholder="e.g., Software Developer, Accountant")
        experience_years = st.number_input("Years of Experience", 
                                         min_value=0, max_value=50, value=3)
        education_level = st.selectbox("Highest Education Level",
                                     ["High School", "Associate Degree", "Bachelor's Degree", 
                                      "Master's Degree", "PhD"])
    
    with col2:
        # Multi-line text input for skills
        skills_text = st.text_area("Your Skills (one per line or comma-separated)",
                                  placeholder="Python\nData Analysis\nProject Management\n...",
                                  height=150)
        
        certifications = st.text_area("Certifications (optional)",
                                    placeholder="AWS Certified\nPMP\n...",
                                    height=70)
    
    # Projects section
    st.subheader("🚀 Projects & Experience")
    projects = st.text_area("Describe your projects (optional)",
                          placeholder="1. Built a web application using React and Node.js\n"
                                    "2. Analyzed sales data using Python and created dashboards\n"
                                    "3. Led a team of 5 developers...",
                          height=100)
    
    return {
        "current_role": current_role,
        "experience_years": experience_years,
        "education_level": education_level,
        "skills_text": skills_text,
        "certifications": certifications.split('\n') if certifications else [],
        "projects": projects.split('\n') if projects else []
    }

def render_industry_selector() -> str:
    """Render industry selection and return selected industry"""
    st.subheader("🎯 Select Your Target Industry")
    
    # Create columns for industry cards
    cols = st.columns(2)
    selected_industry = None
    
    for i, (key, info) in enumerate(FUTURE_INDUSTRIES.items()):
        with cols[i % 2]:
            if st.button(f"{info['icon']} {info['name']}", 
                        key=f"industry_{key}",
                        use_container_width=True):
                selected_industry = key
    
    # Alternative: Radio button selection
    if not selected_industry:
        industry_names = [f"{info['icon']} {info['name']}" 
                         for info in FUTURE_INDUSTRIES.values()]
        selected_index = st.radio("Or select from list:", 
                                 industry_names, 
                                 horizontal=True,
                                 label_visibility="collapsed")
        
        # Map back to industry key
        for key, info in FUTURE_INDUSTRIES.items():
            if f"{info['icon']} {info['name']}" == selected_index:
                selected_industry = key
                break
    
    return selected_industry

def render_readiness_gauge(score: float, title: str = "Overall Readiness"):
    """Render a gauge chart for readiness score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': get_score_color(score)},
            'steps': [
                {'range': [0, 20], 'color': "lightgray"},
                {'range': [20, 40], 'color': "#FFE0B2"},
                {'range': [40, 60], 'color': "#FFCC80"},
                {'range': [60, 80], 'color': "#FFB74D"},
                {'range': [80, 100], 'color': "#4CAF50"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def render_skill_gap_chart(current_skills: List[str], required_skills: List[str]):
    """Render skill gap visualization"""
    all_skills = list(set(current_skills + required_skills))
    
    current_values = [1 if skill in current_skills else 0 for skill in all_skills]
    required_values = [1 if skill in required_skills else 0 for skill in all_skills]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current Skills',
        x=all_skills,
        y=current_values,
        marker_color='#4CAF50'
    ))
    
    fig.add_trace(go.Bar(
        name='Required Skills',
        x=all_skills,
        y=required_values,
        marker_color='#FF9800',
        opacity=0.6
    ))
    
    fig.update_layout(
        title="Skill Gap Analysis",
        xaxis_title="Skills",
        yaxis_title="Skill Level",
        barmode='overlay',
        height=400
    )
    
    return fig

def render_career_path_timeline(career_path: List[Dict]):
    """Render career transition timeline"""
    if not career_path:
        st.info("No specific career path available")
        return
    
    for i, step in enumerate(career_path):
        col1, col2 = st.columns([1, 5])
        
        with col1:
            st.markdown(f"""
            <div style="background-color: {UI_CONFIG['primary_color']}; 
                        color: white; 
                        border-radius: 50%; 
                        width: 50px; 
                        height: 50px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        font-size: 1.5em; 
                        font-weight: bold;">
                {step['step']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### {step['title']}")
            st.caption(f"Duration: {step['duration']}")
            
            # Skills to learn
            st.markdown("**Skills to develop:**")
            skills_html = " ".join([f"<span style='background-color: #e3f2fd; "
                                  f"padding: 4px 8px; border-radius: 4px; "
                                  f"margin: 2px; display: inline-block;'>{skill}</span>" 
                                  for skill in step['skills']])
            st.markdown(skills_html, unsafe_allow_html=True)
            
            # Resources
            if 'resources' in step:
                with st.expander("📚 Recommended Resources"):
                    for resource in step['resources']:
                        st.write(f"- {resource}")
        
        if i < len(career_path) - 1:
            st.markdown("""
            <div style="width: 2px; 
                        height: 30px; 
                        background-color: #e0e0e0; 
                        margin-left: 25px;"></div>
            """, unsafe_allow_html=True)

def render_recommendations(recommendations: List[str]):
    """Render recommendations in a nice format"""
    st.subheader("💡 Personalized Recommendations")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div style="background-color: #f5f5f5; 
                    padding: 15px; 
                    border-left: 4px solid {UI_CONFIG['primary_color']}; 
                    margin-bottom: 10px;
                    border-radius: 5px;">
            <strong>{i}.</strong> {rec}
        </div>
        """, unsafe_allow_html=True)

def render_learning_resources(industry: str, skills_to_learn: List[str]):
    """Render learning resources section"""
    st.subheader("📚 Learning Resources")
    
    # Import here to avoid circular import
    try:
        from config import LEARNING_PLATFORMS
    except ImportError:
        LEARNING_PLATFORMS = {
            "coursera": "https://www.coursera.org/search?query=",
            "udemy": "https://www.udemy.com/courses/search/?q=",
            "edx": "https://www.edx.org/search?q="
        }
    
    tabs = st.tabs(list(LEARNING_PLATFORMS.keys()))
    
    for i, (platform, base_url) in enumerate(LEARNING_PLATFORMS.items()):
        with tabs[i]:
            st.write(f"Search for courses on {platform.title()}:")
            
            # Create search links for top skills
            for skill in skills_to_learn[:5]:
                search_url = f"{base_url}{skill.replace(' ', '+')}"
                st.markdown(f"- [{skill}]({search_url})")

def get_score_color(score: float) -> str:
    """Get color based on score value"""
    if score >= 80:
        return UI_CONFIG['success_color']
    elif score >= 60:
        return UI_CONFIG['secondary_color']
    elif score >= 40:
        return UI_CONFIG['warning_color']
    else:
        return UI_CONFIG['danger_color']

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>Built with ❤️ using Streamlit | 
        <a href="https://github.com/yourusername/career-shift-analyzer" target="_blank">GitHub</a> | 
        <a href="https://linkedin.com/in/yourprofile" target="_blank">LinkedIn</a></p>
        <p style="font-size: 0.8em;">© 2024 Career Shift Analyzer. 
        Educational purpose only.</p>
    </div>
    """, unsafe_allow_html=True)
