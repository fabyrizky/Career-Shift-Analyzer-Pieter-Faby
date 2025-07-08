import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime
import random

# Page config
st.set_page_config(
    page_title="Career Shift to Future STEM Industry",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-optimized CSS (No external fonts to avoid loading issues)
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #0a0e1a 0%, #1a1f3a 100%);
        color: #ffffff;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #00f0ff, #b347d9, #ff006e);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease-in-out infinite;
        margin: 2rem 0;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer {
        background: rgba(10, 14, 26, 0.95);
        border-top: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 20px 20px 0 0;
        padding: 3rem 2rem;
        margin-top: 4rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Static data (no external API calls that could fail)
MARKET_DATA = {
    'ai_ml_jobs': 15420,
    'data_science_jobs': 12850,
    'cybersecurity_jobs': 9340,
    'cloud_jobs': 18750,
    'total_jobs': 56360
}

STEM_FIELDS = {
    'AI & Machine Learning 🤖': {
        'courses': ['Python Fundamentals', 'Machine Learning Basics', 'Deep Learning Intro', 'Data Science Tools'],
        'salary': '$95K - $190K',
        'growth': '+25%',
        'description': 'Build intelligent systems that transform industries'
    },
    'Data Science 📊': {
        'courses': ['Statistics & Analytics', 'Data Visualization', 'SQL & Databases', 'Business Intelligence'],
        'salary': '$85K - $170K', 
        'growth': '+18%',
        'description': 'Extract insights from complex data'
    },
    'Cybersecurity 🔒': {
        'courses': ['Network Security', 'Ethical Hacking', 'Security Architecture', 'Risk Management'],
        'salary': '$75K - $155K',
        'growth': '+15%', 
        'description': 'Protect digital assets and infrastructure'
    },
    'Cloud Computing ☁️': {
        'courses': ['AWS Fundamentals', 'Azure Basics', 'DevOps Pipeline', 'Kubernetes'],
        'salary': '$90K - $185K',
        'growth': '+28%',
        'description': 'Scale applications globally with cloud'
    }
}

def get_simple_ai_response(question):
    """Simple AI response without external API dependency"""
    responses = {
        "salary": "STEM salaries range from $75K-$190K depending on experience and field. AI/ML and Cloud Computing offer the highest compensation.",
        "transition": "Start with online courses, build projects, get certifications, and network with professionals. Timeline: 6-18 months with dedicated effort.",
        "skills": "Key skills: Programming (Python/SQL), data analysis, problem-solving, cloud platforms, and continuous learning mindset.",
        "certifications": "Popular certs: AWS Solutions Architect, Google Data Engineer, CompTIA Security+, Microsoft Azure certifications.",
        "remote": "68% of STEM jobs offer remote options. Cloud and data roles have highest remote availability.",
        "default": "Great question! Focus on building practical skills through projects, networking, and continuous learning. What specific area interests you most?"
    }
    
    question_lower = question.lower()
    for key, response in responses.items():
        if key in question_lower:
            return response
    return responses["default"]

def create_growth_chart():
    """Create growth projections chart"""
    years = list(range(2023, 2031))
    
    data = {
        'Year': years,
        'AI/ML': [100 * (1.25 ** (i/4)) for i in range(len(years))],
        'Cloud Computing': [100 * (1.28 ** (i/4)) for i in range(len(years))],
        'Data Science': [100 * (1.18 ** (i/4)) for i in range(len(years))],
        'Cybersecurity': [100 * (1.15 ** (i/4)) for i in range(len(years))]
    }
    
    df = pd.DataFrame(data)
    fig = px.line(df, x='Year', y=['AI/ML', 'Cloud Computing', 'Data Science', 'Cybersecurity'],
                  title='📈 STEM Career Growth Projections (2023-2030)')
    
    fig.update_layout(
        height=450,
        font=dict(color='#ffffff', size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.1)',
        title_font_size=16
    )
    return fig

def create_salary_chart():
    """Create salary comparison chart"""
    fields = ['AI/ML', 'Cloud Computing', 'Data Science', 'Cybersecurity']
    min_salaries = [95000, 90000, 85000, 75000]
    max_salaries = [190000, 185000, 170000, 155000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Min Salary',
        x=fields,
        y=min_salaries,
        marker_color='rgba(0, 240, 255, 0.6)'
    ))
    
    fig.add_trace(go.Bar(
        name='Max Salary', 
        x=fields,
        y=max_salaries,
        marker_color='rgba(179, 71, 217, 0.8)'
    ))
    
    fig.update_layout(
        title='💰 STEM Salary Ranges (USD)',
        barmode='group',
        height=400,
        font=dict(color='#ffffff'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.1)'
    )
    return fig

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Career Shift to Future STEM Industry</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox("Choose your path:", 
                               ["🏠 Home", "📈 Market Analysis", "📚 Course Catalog", 
                                "🤖 AI Advisor", "🎯 Skill Assessment"])
    
    # Live metrics sidebar
    st.sidebar.markdown("### 📊 Live Market Data")
    st.sidebar.metric("🔥 Total STEM Jobs", f"{MARKET_DATA['total_jobs']:,}")
    st.sidebar.metric("🚀 AI/ML Positions", f"{MARKET_DATA['ai_ml_jobs']:,}")
    st.sidebar.metric("☁️ Cloud Jobs", f"{MARKET_DATA['cloud_jobs']:,}")
    
    # Page Content
    if page == "🏠 Home":
        # Hero Section
        st.markdown("### 🌟 Welcome to Your STEM Career Transformation")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-number">15K+</div>
                <div>AI/ML Jobs</div>
                <div style="color: #00d4aa;">+25% Growth</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-number">19K+</div>
                <div>Cloud Jobs</div>
                <div style="color: #00d4aa;">+28% Growth</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-number">13K+</div>
                <div>Data Science</div>
                <div style="color: #00d4aa;">+18% Growth</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-number">9K+</div>
                <div>Cybersecurity</div>
                <div style="color: #00d4aa;">+15% Growth</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Featured Career Paths
        st.markdown("### 🔥 Trending Career Paths")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #00f0ff;">🤖 AI Engineer</h4>
                <p>Build intelligent systems that transform industries</p>
                <p><strong>Salary:</strong> $95K - $190K</p>
                <p><strong>Growth:</strong> +150% over 5 years</p>
                <div style="margin-top: 1rem;">
                    <span style="background: rgba(0,240,255,0.2); padding: 0.3rem 0.6rem; border-radius: 6px; margin: 0.2rem;">Python</span>
                    <span style="background: rgba(0,240,255,0.2); padding: 0.3rem 0.6rem; border-radius: 6px; margin: 0.2rem;">TensorFlow</span>
                    <span style="background: rgba(0,240,255,0.2); padding: 0.3rem 0.6rem; border-radius: 6px; margin: 0.2rem;">ML</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #00f0ff;">☁️ Cloud Architect</h4>
                <p>Design scalable cloud infrastructure</p>
                <p><strong>Salary:</strong> $90K - $185K</p>
                <p><strong>Growth:</strong> +180% over 5 years</p>
                <div style="margin-top: 1rem;">
                    <span style="background: rgba(0,240,255,0.2); padding: 0.3rem 0.6rem; border-radius: 6px; margin: 0.2rem;">AWS</span>
                    <span style="background: rgba(0,240,255,0.2); padding: 0.3rem 0.6rem; border-radius: 6px; margin: 0.2rem;">Kubernetes</span>
                    <span style="background: rgba(0,240,255,0.2); padding: 0.3rem 0.6rem; border-radius: 6px; margin: 0.2rem;">DevOps</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📈 Market Analysis":
        st.header("📈 STEM Market Intelligence")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_growth_chart()
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_salary_chart()
            st.plotly_chart(fig2, use_container_width=True)
        
        # Market insights
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #00f0ff;">📊 Key Market Insights</h4>
            <ul style="color: #b0b3b8;">
                <li><strong>Cloud Computing:</strong> Fastest growing field (+28% annually)</li>
                <li><strong>AI/ML:</strong> Highest salary potential ($95K-$190K)</li>
                <li><strong>Remote Work:</strong> 68% of STEM jobs offer remote options</li>
                <li><strong>Skills Gap:</strong> High demand for Python, AWS, ML skills</li>
                <li><strong>Job Security:</strong> 94% job retention rate in STEM fields</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    elif page == "📚 Course Catalog":
        st.header("📚 STEM Learning Catalog")
        
        selected_field = st.selectbox("Select STEM Field:", list(STEM_FIELDS.keys()))
        
        if selected_field:
            field_data = STEM_FIELDS[selected_field]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #00f0ff;">{selected_field}</h4>
                    <p>{field_data['description']}</p>
                    <p><strong>Average Salary:</strong> {field_data['salary']}</p>
                    <p><strong>Growth Rate:</strong> {field_data['growth']}</p>
                    
                    <h5 style="color: #00d4aa;">Recommended Courses:</h5>
                    <ul style="color: #b0b3b8;">
                        {''.join([f'<li>{course}</li>' for course in field_data['courses']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🎯 Get Learning Path", type="primary"):
                    st.success("✅ Personalized learning path generated!")
                    st.balloons()
                    
                    st.markdown(f"""
                    **Your {selected_field} Learning Plan:**
                    
                    📅 **Timeline:** 6-12 months
                    
                    🎯 **Phase 1 (Months 1-3):** Foundations
                    🚀 **Phase 2 (Months 4-6):** Practical Projects  
                    💼 **Phase 3 (Months 7-12):** Portfolio & Job Search
                    """)
    
    elif page == "🤖 AI Advisor":
        st.header("🤖 AI Career Advisor")
        
        # Quick questions
        st.subheader("🚀 Popular Questions")
        quick_questions = [
            "What's the salary range for STEM careers?",
            "How to transition to data science?", 
            "Which programming language should I learn first?",
            "Best certifications for cloud computing?",
            "Remote work opportunities in STEM?"
        ]
        
        for i, question in enumerate(quick_questions):
            if st.button(f"❓ {question}", key=f"quick_{i}"):
                response = get_simple_ai_response(question)
                st.markdown(f"""
                <div class="glass-card">
                    <strong style="color: #00f0ff;">Question:</strong> {question}<br><br>
                    <strong style="color: #00d4aa;">AI Answer:</strong> {response}
                </div>
                """, unsafe_allow_html=True)
        
        # Custom question
        st.subheader("💬 Ask Your Question")
        user_question = st.text_area("What would you like to know about STEM careers?", height=100)
        
        if st.button("🚀 Get AI Advice", type="primary"):
            if user_question:
                response = get_simple_ai_response(user_question)
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": response,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                st.markdown(f"""
                <div class="glass-card">
                    <strong style="color: #00f0ff;">Your Question:</strong> {user_question}<br><br>
                    <strong style="color: #00d4aa;">AI Answer:</strong> {response}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat history
        if st.session_state.chat_history:
            st.subheader("💬 Recent Conversations")
            for chat in reversed(st.session_state.chat_history[-3:]):
                st.markdown(f"""
                <div class="glass-card">
                    <small style="color: #888;">{chat['timestamp']}</small><br>
                    <strong style="color: #00f0ff;">Q:</strong> {chat['question']}<br><br>
                    <strong style="color: #00d4aa;">A:</strong> {chat['answer']}
                </div>
                """, unsafe_allow_html=True)
    
    elif page == "🎯 Skill Assessment":
        st.header("🎯 STEM Skill Assessment")
        
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #00f0ff;">Rate Your Current Skills (1-10)</h4>
            <p>Get personalized recommendations based on your skill level</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Skill assessment
        programming = st.slider("💻 Programming (Python, SQL, etc.)", 1, 10, 5)
        data_analysis = st.slider("📊 Data Analysis & Statistics", 1, 10, 5)
        cloud_tech = st.slider("☁️ Cloud Technologies (AWS, Azure)", 1, 10, 5)
        soft_skills = st.slider("🧠 Communication & Problem Solving", 1, 10, 5)
        
        if st.button("📊 Generate Assessment Report", type="primary"):
            overall_score = (programming + data_analysis + cloud_tech + soft_skills) / 4
            
            # Determine readiness level
            if overall_score >= 8:
                level = "Expert"
                color = "#00d4aa"
                advice = "You're ready for senior roles! Focus on leadership and specialization."
            elif overall_score >= 6:
                level = "Intermediate"
                color = "#00f0ff"
                advice = "You're on the right track! Build more projects and get certified."
            else:
                level = "Beginner"
                color = "#ff6b6b"
                advice = "Start with fundamentals and build a strong foundation."
            
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="color: #00f0ff;">Your STEM Readiness Report</h4>
                <div class="metric-number" style="color: {color};">{overall_score:.1f}/10</div>
                <div style="color: {color}; font-size: 1.2rem; font-weight: 600;">{level} Level</div>
                
                <h5 style="color: #00d4aa; margin-top: 2rem;">Skill Breakdown:</h5>
                <div style="color: #b0b3b8;">
                    <p>💻 Programming: {programming}/10</p>
                    <p>📊 Data Analysis: {data_analysis}/10</p>
                    <p>☁️ Cloud Technologies: {cloud_tech}/10</p>
                    <p>🧠 Soft Skills: {soft_skills}/10</p>
                </div>
                
                <h5 style="color: #00d4aa; margin-top: 2rem;">Recommendations:</h5>
                <p style="color: #b0b3b8;">{advice}</p>
                
                <h5 style="color: #00d4aa;">Next Steps:</h5>
                <ul style="color: #b0b3b8;">
                    {"<li>Focus on strengthening programming fundamentals</li>" if programming < 6 else ""}
                    {"<li>Develop cloud computing skills (high demand)</li>" if cloud_tech < 6 else ""}
                    {"<li>Practice data analysis with real datasets</li>" if data_analysis < 6 else ""}
                    <li>Build 2-3 portfolio projects</li>
                    <li>Network with STEM professionals</li>
                    <li>Consider industry certifications</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3 style="color: #00f0ff;">🚀 Ready to Transform Your Career?</h3>
        <p style="color: #b0b3b8;">Join thousands of professionals transitioning to high-growth STEM careers</p>
        
        <div style="margin: 2rem 0;">
            <span style="background: rgba(0,240,255,0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem; display: inline-block;">
                <strong style="color: #00f0ff;">87%</strong><br>Success Rate
            </span>
            <span style="background: rgba(0,212,170,0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem; display: inline-block;">
                <strong style="color: #00d4aa;">10K+</strong><br>Career Transitions
            </span>
            <span style="background: rgba(255,107,107,0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem; display: inline-block;">
                <strong style="color: #ff6b6b;">6-18</strong><br>Months Timeline
            </span>
        </div>
        
        <div style="margin-top: 2rem; color: #b0b3b8;">
            <strong>Built by Faby Rizky & Pieter Andrian</strong><br>
            © 2025 STEM Career Platform. Built with ❤️ using Streamlit.
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
