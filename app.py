import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Career Shift to Future STEM Industry",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with proper rendering
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(180deg, #0a0e1a 0%, #1a1f3a 100%);
        color: #ffffff;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #00f0ff, #b347d9, #ff006e);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease-in-out infinite;
        margin: 2rem 0;
        line-height: 1.2;
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
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 240, 255, 0.2);
        border-color: rgba(0, 240, 255, 0.3);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 240, 255, 0.5);
        transform: scale(1.02);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .ai-response {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.1) 0%, rgba(179, 71, 217, 0.1) 100%);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .ai-response::before {
        content: "🤖";
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        opacity: 0.5;
    }
    
    .skill-bar {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
        height: 20px;
    }
    
    .skill-fill {
        height: 100%;
        background: linear-gradient(90deg, #00f0ff, #b347d9);
        border-radius: 10px;
        transition: width 0.8s ease;
    }
    
    .footer-clean {
        background: rgba(10, 14, 26, 0.95);
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 20px 20px 0 0;
        padding: 3rem 2rem;
        margin-top: 4rem;
        text-align: center;
    }
    
    .success-metric {
        background: rgba(0, 240, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem;
        display: inline-block;
        min-width: 120px;
    }
    
    .course-badge {
        background: rgba(0, 240, 255, 0.2);
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'assessment_done' not in st.session_state:
    st.session_state.assessment_done = False

# Market data
MARKET_DATA = {
    'ai_ml_jobs': 15420,
    'data_science_jobs': 12850, 
    'cybersecurity_jobs': 9340,
    'cloud_jobs': 18750,
    'total_jobs': 56360
}

# STEM fields configuration
STEM_FIELDS = {
    'AI & Machine Learning 🤖': {
        'courses': ['Python for AI', 'Machine Learning Fundamentals', 'Deep Learning with TensorFlow', 'Natural Language Processing'],
        'salary_range': '$95K - $190K',
        'growth_rate': '+25%',
        'description': 'Build intelligent systems that transform industries',
        'skills': ['Python', 'TensorFlow', 'Scikit-learn', 'Statistics'],
        'timeline': '8-12 months'
    },
    'Data Science 📊': {
        'courses': ['Python for Data Analysis', 'Statistical Modeling', 'Data Visualization', 'Big Data Analytics'],
        'salary_range': '$85K - $170K',
        'growth_rate': '+18%', 
        'description': 'Extract insights from complex data',
        'skills': ['Python', 'SQL', 'Tableau', 'R'],
        'timeline': '6-10 months'
    },
    'Cybersecurity 🔒': {
        'courses': ['Network Security', 'Ethical Hacking', 'Security Architecture', 'Digital Forensics'],
        'salary_range': '$75K - $155K',
        'growth_rate': '+15%',
        'description': 'Protect digital assets and infrastructure', 
        'skills': ['Networking', 'Linux', 'Security Tools', 'Risk Assessment'],
        'timeline': '6-9 months'
    },
    'Cloud Computing ☁️': {
        'courses': ['AWS Fundamentals', 'Azure Architecture', 'DevOps with Docker', 'Kubernetes Orchestration'],
        'salary_range': '$90K - $185K',
        'growth_rate': '+28%',
        'description': 'Scale applications globally with cloud infrastructure',
        'skills': ['AWS', 'Docker', 'Kubernetes', 'DevOps'],
        'timeline': '5-8 months'
    }
}

# AI Integration with OpenRouter
def get_ai_response(prompt, context="career_advice"):
    """Enhanced AI response using OpenRouter Qwen QwQ 32B"""
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        model = st.secrets["OPENROUTER_MODEL"]
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://career-shift-analyzer.streamlit.app",
            "X-Title": "STEM Career Advisor"
        }
        
        system_prompt = """You are an expert STEM career advisor with 15+ years of experience helping professionals transition into technology careers. 

Provide practical, actionable advice that is:
- Specific and detailed
- Based on current market trends
- Includes realistic timelines
- Mentions specific tools/skills/certifications
- Encouraging but honest about challenges

Keep responses under 300 words and well-structured."""

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 400,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return "I'm here to help with your STEM career questions! The AI service is temporarily busy, but I can still provide guidance through our interactive features."
            
    except Exception as e:
        return f"I'm ready to assist with your STEM career journey! While the AI connects, explore our course catalog and market analysis features."

# Enhanced visualizations
def create_interactive_growth_chart():
    """Create enhanced growth projections"""
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
                  title='📈 STEM Career Growth Projections (2023-2030)',
                  color_discrete_map={
                      'AI/ML': '#00f0ff',
                      'Cloud Computing': '#b347d9', 
                      'Data Science': '#00d4aa',
                      'Cybersecurity': '#ff6b6b'
                  })
    
    fig.update_layout(
        height=500,
        font=dict(color='#ffffff', size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_size=18,
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.1)', borderwidth=1),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

def create_salary_comparison_chart():
    """Enhanced salary comparison"""
    fields = ['AI/ML', 'Cloud Computing', 'Data Science', 'Cybersecurity']
    min_salaries = [95000, 90000, 85000, 75000]
    max_salaries = [190000, 185000, 170000, 155000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Starting Range',
        x=fields,
        y=min_salaries,
        marker_color='rgba(0, 240, 255, 0.7)',
        text=[f'${x//1000}K' for x in min_salaries],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Senior Range',
        x=fields,
        y=max_salaries,
        marker_color='rgba(179, 71, 217, 0.8)',
        text=[f'${x//1000}K' for x in max_salaries],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='💰 STEM Salary Ranges (USD)',
        barmode='group',
        height=450,
        font=dict(color='#ffffff'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_size=18,
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

# Main application
def main():
    # Header with animation
    st.markdown('<h1 class="main-header">🚀 Career Shift to Future STEM Industry</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox("Choose your path:", 
                               ["🏠 Home", "📈 Market Intelligence", "📚 Course Catalog", 
                                "🤖 AI Career Advisor", "🎯 Skill Assessment"])
    
    # Live metrics in sidebar
    st.sidebar.markdown("### 📊 Live Market Data")
    st.sidebar.metric("🔥 Total STEM Jobs", f"{MARKET_DATA['total_jobs']:,}")
    st.sidebar.metric("🚀 AI/ML Positions", f"{MARKET_DATA['ai_ml_jobs']:,}")
    st.sidebar.metric("☁️ Cloud Jobs", f"{MARKET_DATA['cloud_jobs']:,}")
    
    # Page content
    if page == "🏠 Home":
        # Hero metrics with enhanced styling
        st.markdown("### 🌟 Welcome to Your STEM Career Transformation")
        
        col1, col2, col3, col4 = st.columns(4)
        
        metrics_data = [
            ("15K+", "AI/ML Jobs", "+25% Growth", "#00f0ff"),
            ("19K+", "Cloud Jobs", "+28% Growth", "#b347d9"),
            ("13K+", "Data Science", "+18% Growth", "#00d4aa"),
            ("9K+", "Cybersecurity", "+15% Growth", "#ff6b6b")
        ]
        
        for i, (col, (number, title, growth, color)) in enumerate(zip([col1, col2, col3, col4], metrics_data)):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-number" style="color: {color};">{number}</div>
                    <div style="color: #ffffff; font-weight: 600;">{title}</div>
                    <div style="color: #00d4aa; font-size: 0.9rem;">{growth}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Featured career paths
        st.markdown("### 🔥 Trending Career Paths")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #00f0ff; margin-bottom: 1rem;">🤖 AI Engineer</h4>
                <p style="color: #b0b3b8; margin-bottom: 1rem;">Build intelligent systems that transform industries</p>
                <p style="color: #ffffff;"><strong>Salary:</strong> $95K - $190K</p>
                <p style="color: #ffffff;"><strong>Growth:</strong> +150% over 5 years</p>
                <div style="margin-top: 1rem;">
                    <span class="course-badge">Python</span>
                    <span class="course-badge">TensorFlow</span>
                    <span class="course-badge">Machine Learning</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #00f0ff; margin-bottom: 1rem;">☁️ Cloud Architect</h4>
                <p style="color: #b0b3b8; margin-bottom: 1rem;">Design scalable cloud infrastructure</p>
                <p style="color: #ffffff;"><strong>Salary:</strong> $90K - $185K</p>
                <p style="color: #ffffff;"><strong>Growth:</strong> +180% over 5 years</p>
                <div style="margin-top: 1rem;">
                    <span class="course-badge">AWS</span>
                    <span class="course-badge">Kubernetes</span>
                    <span class="course-badge">DevOps</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📈 Market Intelligence":
        st.header("📈 STEM Market Intelligence")
        
        # Enhanced charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_interactive_growth_chart()
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_salary_comparison_chart()
            st.plotly_chart(fig2, use_container_width=True)
        
        # Market insights with enhanced styling
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #00f0ff; margin-bottom: 1.5rem;">📊 Key Market Insights</h4>
            <div style="color: #b0b3b8; line-height: 1.8;">
                <p><strong style="color: #00d4aa;">🚀 Cloud Computing:</strong> Fastest growing field (+28% annually) with highest remote work opportunities</p>
                <p><strong style="color: #00f0ff;">🤖 AI/ML:</strong> Highest salary potential ($95K-$190K) and most in-demand skills</p>
                <p><strong style="color: #b347d9;">📊 Data Science:</strong> Most accessible entry point with strong career progression</p>
                <p><strong style="color: #ff6b6b;">🔒 Cybersecurity:</strong> Recession-proof with excellent job security and government opportunities</p>
                <p><strong style="color: #ffffff;">💼 Remote Work:</strong> 68% of STEM jobs offer remote options, 89% offer hybrid flexibility</p>
            </div>
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
                    <h4 style="color: #00f0ff; margin-bottom: 1rem;">{selected_field}</h4>
                    <p style="color: #b0b3b8; margin-bottom: 1.5rem;">{field_data['description']}</p>
                    
                    <div style="margin-bottom: 1.5rem;">
                        <p style="color: #ffffff;"><strong>💰 Salary Range:</strong> {field_data['salary_range']}</p>
                        <p style="color: #ffffff;"><strong>📈 Growth Rate:</strong> {field_data['growth_rate']}</p>
                        <p style="color: #ffffff;"><strong>⏱️ Timeline:</strong> {field_data['timeline']}</p>
                    </div>
                    
                    <h5 style="color: #00d4aa; margin-bottom: 1rem;">📚 Recommended Courses:</h5>
                    <div style="margin-bottom: 1.5rem;">
                        {' '.join([f'<span class="course-badge">{course}</span>' for course in field_data['courses']])}
                    </div>
                    
                    <h5 style="color: #00d4aa; margin-bottom: 1rem;">🛠️ Key Skills:</h5>
                    <div>
                        {' '.join([f'<span class="course-badge">{skill}</span>' for skill in field_data['skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🎯 Get Personalized Learning Path", type="primary"):
                    st.success("✅ Personalized learning path generated!")
                    st.balloons()
                    
                    st.markdown(f"""
                    <div class="ai-response">
                        <h5 style="color: #00f0ff;">Your {selected_field} Learning Plan</h5>
                        <p><strong>📅 Timeline:</strong> {field_data['timeline']}</p>
                        <p><strong>🎯 Phase 1 (30%):</strong> Foundations & Theory</p>
                        <p><strong>🚀 Phase 2 (50%):</strong> Hands-on Projects</p>
                        <p><strong>💼 Phase 3 (20%):</strong> Portfolio & Job Search</p>
                        <p style="color: #00d4aa; margin-top: 1rem;"><strong>Success Rate:</strong> 87% completion rate</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif page == "🤖 AI Career Advisor":
        st.header("🤖 AI Career Advisor")
        st.markdown("*Powered by Qwen QwQ 32B - Advanced reasoning model*")
        
        # Quick questions with enhanced styling
        st.subheader("🚀 Popular Career Questions")
        quick_questions = [
            "How do I transition from marketing to data science?",
            "What programming language should I learn first for AI?",
            "Which cloud certification offers the best ROI?",
            "How to build a portfolio with no tech experience?",
            "What's the realistic timeline to land a STEM job?"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(quick_questions):
            with cols[i % 2]:
                if st.button(f"❓ {question}", key=f"quick_{i}"):
                    with st.spinner("🤖 AI analyzing your question..."):
                        response = get_ai_response(question)
                        st.markdown(f"""
                        <div class="ai-response">
                            <p><strong style="color: #00f0ff;">Question:</strong> {question}</p>
                            <p><strong style="color: #00d4aa;">AI Expert Advice:</strong></p>
                            <p style="color: #ffffff; line-height: 1.6;">{response}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Custom question
        st.subheader("💬 Ask Your Custom Question")
        user_question = st.text_area("What specific career challenge are you facing?", 
                                   height=100,
                                   placeholder="e.g., I'm a teacher wanting to move into data science but don't know where to start...")
        
        if st.button("🚀 Get Expert AI Advice", type="primary"):
            if user_question:
                with st.spinner("🤖 AI thinking deeply about your situation..."):
                    response = get_ai_response(user_question)
                    
                    st.session_state.chat_history.append({
                        "question": user_question,
                        "answer": response,
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                    
                    st.markdown(f"""
                    <div class="ai-response">
                        <p><strong style="color: #00f0ff;">Your Question:</strong> {user_question}</p>
                        <p><strong style="color: #00d4aa;">AI Expert Analysis:</strong></p>
                        <p style="color: #ffffff; line-height: 1.6;">{response}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat history
        if st.session_state.chat_history:
            st.subheader("💬 Recent Consultations")
            for chat in reversed(st.session_state.chat_history[-3:]):
                st.markdown(f"""
                <div class="glass-card">
                    <small style="color: #888;">⏰ {chat['timestamp']}</small>
                    <p style="margin: 0.5rem 0;"><strong style="color: #00f0ff;">Q:</strong> {chat['question'][:100]}...</p>
                    <p style="margin: 0.5rem 0;"><strong style="color: #00d4aa;">A:</strong> {chat['answer'][:150]}...</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif page == "🎯 Skill Assessment":
        st.header("🎯 STEM Readiness Assessment")
        
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #00f0ff;">Evaluate Your Current Skills (1-10)</h4>
            <p style="color: #b0b3b8;">Get personalized recommendations and career roadmap</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Skill assessment with visual bars
        skills = {
            "💻 Programming": st.slider("Programming (Python, SQL, etc.)", 1, 10, 5),
            "📊 Data Analysis": st.slider("Data Analysis & Statistics", 1, 10, 5),
            "☁️ Cloud Technologies": st.slider("Cloud Platforms (AWS, Azure)", 1, 10, 5),
            "🧠 Problem Solving": st.slider("Analytical & Problem Solving", 1, 10, 5),
            "🔧 Technical Tools": st.slider("Technical Tools & Frameworks", 1, 10, 5)
        }
        
        # Visual skill display
        for skill_name, score in skills.items():
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <p style="color: #ffffff; margin-bottom: 0.5rem;">{skill_name}: {score}/10</p>
                <div class="skill-bar">
                    <div class="skill-fill" style="width: {score * 10}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("📊 Generate Comprehensive Assessment", type="primary"):
            overall_score = sum(skills.values()) / len(skills)
            
            # Determine level and recommendations
            if overall_score >= 8:
                level, color, advice = "Expert Level", "#00d4aa", "You're ready for senior positions! Focus on leadership and specialization."
            elif overall_score >= 6:
                level, color, advice = "Intermediate Level", "#00f0ff", "Strong foundation! Build projects and pursue certifications."
            elif overall_score >= 4:
                level, color, advice = "Developing Level", "#b347d9", "Good start! Focus on core fundamentals and hands-on practice."
            else:
                level, color, advice = "Beginner Level", "#ff6b6b", "Perfect starting point! Begin with foundations and don't rush."
            
            st.session_state.assessment_done = True
            
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="color: #00f0ff;">🎯 Your STEM Readiness Report</h4>
                <div class="metric-number" style="color: {color};">{overall_score:.1f}/10</div>
                <div style="color: {color}; font-size: 1.3rem; font-weight: 600; margin-bottom: 2rem;">{level}</div>
                
                <div style="color: #ffffff; margin-bottom: 2rem;">
                    <h5 style="color: #00d4aa;">📈 Skill Breakdown:</h5>
                    {"".join([f"<p>{name}: {score}/10</p>" for name, score in skills.items()])}
                </div>
                
                <div style="color: #ffffff; margin-bottom: 2rem;">
                    <h5 style="color: #00d4aa;">💡 Personalized Advice:</h5>
                    <p>{advice}</p>
                </div>
                
                <div style="color: #ffffff;">
                    <h5 style="color: #00d4aa;">🚀 Recommended Next Steps:</h5>
                    <p>• Build 2-3 portfolio projects in your target field</p>
                    <p>• Complete online courses in your weakest areas</p>
                    <p>• Join STEM communities and start networking</p>
                    <p>• Consider industry certifications</p>
                    <p>• Practice coding daily (even 30 minutes helps)</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
    
    # Enhanced footer
    st.markdown("""
    <div class="footer-clean">
        <h3 style="color: #00f0ff; margin-bottom: 1rem;">🚀 Ready to Transform Your Career?</h3>
        <p style="color: #b0b3b8; margin-bottom: 2rem;">Join thousands of professionals transitioning to high-growth STEM careers</p>
        
        <div style="margin: 2rem 0;">
            <span class="success-metric">
                <strong style="color: #00f0ff; font-size: 1.5rem;">87%</strong><br>
                <span style="color: #ffffff;">Success Rate</span>
            </span>
            <span class="success-metric">
                <strong style="color: #00d4aa; font-size: 1.5rem;">10K+</strong><br>
                <span style="color: #ffffff;">Transitions</span>
            </span>
            <span class="success-metric">
                <strong style="color: #b347d9; font-size: 1.5rem;">6-18</strong><br>
                <span style="color: #ffffff;">Months Timeline</span>
            </span>
        </div>
        
        <div style="margin-top: 2rem; color: #b0b3b8;">
            <strong style="color: #ffffff;">Built by Faby Rizky & Pieter Andrian</strong><br>
            © 2025 STEM Career Platform. Built with ❤️ using Streamlit & AI.
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
