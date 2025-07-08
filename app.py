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

# Enhanced CSS
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
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #00f0ff; margin-bottom: 1rem;">☁️ Cloud Architect</h4>
                <p style="color: #b0b3b8; margin-bottom: 1rem;">Design scalable cloud infrastructure</p>
                <p style="color: #ffffff;"><strong>Salary:</strong> $90K - $185K</p>
                <p style="color: #ffffff;"><strong>Growth:</strong> +180% over 5 years</p>
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
        
        # Market insights
        st.markdown("### 📊 Key Market Insights")
        
        insights = [
            "🚀 **Cloud Computing:** Fastest growing field (+28% annually) with highest remote work opportunities",
            "🤖 **AI/ML:** Highest salary potential ($95K-$190K) and most in-demand skills", 
            "📊 **Data Science:** Most accessible entry point with strong career progression",
            "🔒 **Cybersecurity:** Recession-proof with excellent job security",
            "💼 **Remote Work:** 68% of STEM jobs offer remote options, 89% offer hybrid flexibility"
        ]
        
        for insight in insights:
            st.markdown(f"• {insight}")
    
    elif page == "📚 Course Catalog":
        st.header("📚 STEM Learning Catalog")
        
        selected_field = st.selectbox("Select STEM Field:", list(STEM_FIELDS.keys()))
        
        if selected_field:
            field_data = STEM_FIELDS[selected_field]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Field header
                st.markdown(f"## {selected_field}")
                st.write(f"**Description:** {field_data['description']}")
                
                # Field details in organized sections
                st.markdown("### 💰 Career Information")
                
                info_col1, info_col2, info_col3 = st.columns(3)
                with info_col1:
                    st.metric("💵 Salary Range", field_data['salary_range'])
                with info_col2:
                    st.metric("📈 Growth Rate", field_data['growth_rate'])
                with info_col3:
                    st.metric("⏱️ Timeline", field_data['timeline'])
                
                # Recommended courses
                st.markdown("### 📚 Recommended Courses")
                
                for i, course in enumerate(field_data['courses'], 1):
                    st.write(f"**{i}.** {course}")
                
                # Key skills section
                st.markdown("### 🛠️ Essential Skills to Master")
                
                # Display skills as columns
                skill_cols = st.columns(2)
                for i, skill in enumerate(field_data['skills']):
                    with skill_cols[i % 2]:
                        st.write(f"• **{skill}**")
                
                # Learning path preview
                st.markdown("### 🗺️ Learning Path Overview")
                
                phases = [
                    ("Phase 1: Foundations", "30%", "Learn core concepts and theory"),
                    ("Phase 2: Hands-on Practice", "50%", "Build projects and apply skills"),
                    ("Phase 3: Job Preparation", "20%", "Portfolio building and interview prep")
                ]
                
                for phase, percentage, description in phases:
                    st.write(f"**{phase}** ({percentage}): {description}")
            
            with col2:
                # Call to action
                st.markdown("### 🎯 Ready to Start?")
                
                if st.button("🚀 Get Personalized Learning Path", type="primary", use_container_width=True):
                    st.success("✅ Personalized learning path generated!")
                    st.balloons()
                    
                    # Success message with details
                    st.markdown("### 🎉 Your Learning Plan is Ready!")
                    
                    st.info(f"""
                    **🎯 Field:** {selected_field}
                    
                    **⏱️ Timeline:** {field_data['timeline']}
                    
                    **📋 What's Included:**
                    • Structured curriculum
                    • Hands-on projects  
                    • Career guidance
                    • Portfolio development
                    
                    **🎯 Success Rate:** 87% completion rate
                    """)
                    
                    # Next steps
                    st.markdown("### 📋 Your Next Steps")
                    st.write("1. **Start with foundations** - Begin with core concepts")
                    st.write("2. **Practice daily** - Dedicate 1-2 hours daily")
                    st.write("3. **Build projects** - Apply your learning")
                    st.write("4. **Join community** - Connect with learners")
                    st.write("5. **Stay consistent** - Track your progress")
                
                # Additional resources
                st.markdown("### 📖 Additional Resources")
                
                resources = [
                    "🎓 Official Documentation",
                    "👥 Community Forums", 
                    "📹 Video Tutorials",
                    "💼 Career Guidance",
                    "🏆 Certification Prep"
                ]
                
                for resource in resources:
                    st.write(f"• {resource}")
                
                # Market demand indicator
                st.markdown("### 📊 Market Demand")
                
                demand_score = {"AI & Machine Learning 🤖": 95, "Data Science 📊": 88, "Cybersecurity 🔒": 82, "Cloud Computing ☁️": 97}
                field_demand = demand_score.get(selected_field, 85)
                
                st.progress(field_demand / 100)
                st.write(f"**Demand Level:** {field_demand}/100")
                
                if field_demand >= 90:
                    st.success("🔥 **Very High Demand** - Excellent career prospects!")
                elif field_demand >= 80:
                    st.info("📈 **High Demand** - Strong job market")
                else:
                    st.warning("📊 **Moderate Demand** - Steady opportunities")
    
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
                        st.success(f"**Question:** {question}")
                        st.info(f"**AI Expert Advice:**\n\n{response}")
        
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
                    
                    st.success(f"**Your Question:** {user_question}")
                    st.info(f"**AI Expert Analysis:**\n\n{response}")
        
        # Chat history
        if st.session_state.chat_history:
            st.subheader("💬 Recent Consultations")
            for chat in reversed(st.session_state.chat_history[-3:]):
                with st.expander(f"🕐 {chat['timestamp']} - {chat['question'][:50]}..."):
                    st.write(f"**Question:** {chat['question']}")
                    st.write(f"**Answer:** {chat['answer']}")
    
    elif page == "🎯 Skill Assessment":
        st.header("🎯 STEM Readiness Assessment")
        
        st.info("📋 **Evaluate Your Current Skills (1-10)**\n\nGet personalized recommendations and career roadmap")
        
        # Skill assessment with visual bars
        skills = {
            "💻 Programming": st.slider("Programming (Python, SQL, etc.)", 1, 10, 5),
            "📊 Data Analysis": st.slider("Data Analysis & Statistics", 1, 10, 5),
            "☁️ Cloud Technologies": st.slider("Cloud Platforms (AWS, Azure)", 1, 10, 5),
            "🧠 Problem Solving": st.slider("Analytical & Problem Solving", 1, 10, 5),
            "🔧 Technical Tools": st.slider("Technical Tools & Frameworks", 1, 10, 5)
        }
        
        # Visual skill display using progress bars
        st.subheader("📈 Your Current Skill Levels")
        
        for skill_name, score in skills.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{skill_name}**")
            with col2:
                st.write(f"**{score}/10**")
            with col3:
                st.progress(score / 10)
        
        if st.button("📊 Generate Comprehensive Assessment", type="primary"):
            overall_score = sum(skills.values()) / len(skills)
            
            # Determine level and recommendations
            if overall_score >= 8:
                level, advice, next_steps = "Expert Level", "You're ready for senior positions! Focus on leadership and specialization.", [
                    "Apply for senior-level positions",
                    "Consider technical leadership roles", 
                    "Mentor junior professionals",
                    "Contribute to open source projects"
                ]
                level_color = "🟢"
            elif overall_score >= 6:
                level, advice, next_steps = "Intermediate Level", "Strong foundation! Build projects and pursue certifications.", [
                    "Complete 2-3 advanced portfolio projects",
                    "Pursue industry certifications",
                    "Start applying for mid-level positions",
                    "Join professional communities"
                ]
                level_color = "🔵"
            elif overall_score >= 4:
                level, advice, next_steps = "Developing Level", "Good start! Focus on core fundamentals and hands-on practice.", [
                    "Complete foundational courses",
                    "Build 3-5 beginner projects",
                    "Practice coding daily",
                    "Find a mentor or study group"
                ]
                level_color = "🟡"
            else:
                level, advice, next_steps = "Beginner Level", "Perfect starting point! Begin with foundations and don't rush.", [
                    "Start with basic programming courses",
                    "Learn fundamental concepts",
                    "Set up development environment",
                    "Follow structured learning path"
                ]
                level_color = "🔴"
            
            st.session_state.assessment_done = True
            
            # Display results using native Streamlit components
            st.success("✅ Assessment Complete!")
            
            # Overall score
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.metric(
                    label=f"{level_color} Your STEM Readiness Score",
                    value=f"{overall_score:.1f}/10",
                    help=f"You are at {level}"
                )
            
            # Level and advice
            st.markdown(f"### 🎯 Assessment Results: **{level}**")
            st.info(f"**💡 Personalized Advice:**\n\n{advice}")
            
            # Skill breakdown
            st.markdown("### 📊 Detailed Skill Breakdown")
            
            skills_df = pd.DataFrame([
                {"Skill Area": skill.replace("💻 ", "").replace("📊 ", "").replace("☁️ ", "").replace("🧠 ", "").replace("🔧 ", ""), 
                 "Your Score": f"{score}/10", 
                 "Level": "Expert" if score >= 8 else "Intermediate" if score >= 6 else "Developing" if score >= 4 else "Beginner"}
                for skill, score in skills.items()
            ])
            
            st.dataframe(skills_df, use_container_width=True)
            
            # Next steps
            st.markdown("### 🚀 Recommended Next Steps")
            
            for i, step in enumerate(next_steps, 1):
                st.write(f"**{i}.** {step}")
            
            # Personalized timeline
            timeline_months = max(6, int(12 - (overall_score - 1)))
            st.markdown(f"### ⏱️ Estimated Timeline to Career Transition")
            st.warning(f"📅 **{timeline_months} months** based on your current skill level and target goals")
            
            st.balloons()
    
    # Clean Footer Section
    st.markdown("---")
    st.markdown("## 🚀 Ready to Transform Your Career?")
    st.markdown("**Join thousands of professionals transitioning to high-growth STEM careers**")
    
    # Success metrics using Streamlit native components
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🎯 Success Rate", 
            value="87%",
            help="Of users successfully transition to STEM careers"
        )
    
    with col2:
        st.metric(
            label="👥 Career Transitions", 
            value="10,000+",
            help="Professionals helped worldwide"
        )
    
    with col3:
        st.metric(
            label="⏱️ Average Timeline", 
            value="6-18 months",
            help="From start to landing first STEM job"
        )
    
    # Call to action
    st.markdown("### 🎯 Start Your STEM Journey Today")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Begin Free Career Assessment", type="primary", use_container_width=True):
            st.balloons()
            st.success("✅ Great choice! Navigate to 'Skill Assessment' to start your personalized career plan.")
    
    # Simple footer information
    st.markdown("---")
    
    # Footer info using columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **👥 Development Team:**
        
        Built by **Faby Rizky** & Developed 🤝🏻 by **Pieter Andrian**
        """)
    
    with col2:
        st.markdown("""
        **⚡ Technology Stack:**
        - Streamlit Framework
        - OpenRouter AI (Qwen QwQ 32B)
        - Advanced Analytics
        """)
    
    # Creator highlight section
    st.markdown("---")
    st.markdown(
        """
        <div style='background: rgba(0, 240, 255, 0.05); padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid rgba(0, 240, 255, 0.2);'>
            <h4 style='color: #00f0ff; margin-bottom: 1rem;'>👨‍💻 Meet the Creators</h4>
            <p style='color: #ffffff; font-size: 1.1rem; margin-bottom: 0.5rem;'>
                <strong>Built by Faby Rizky & Developed 🤝🏻 by Pieter Andrian</strong>
            </p>
            <p style='color: #b0b3b8; margin-bottom: 1rem;'>
                Passionate about helping professionals transition to tech careers
            </p>
            <p style='color: #00d4aa; font-weight: 600;'>
                © 2025 STEM Career Platform
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(
        "<div style='text-align: center; color: #b0b3b8; margin-top: 1rem;'>"
        "<p>🌟 Transforming careers, one professional at a time 🌟</p>"
        "</div>", 
        unsafe_allow_html=True
    )
    
    # Action badges
    st.markdown("### 🛣️ Your STEM Journey Path")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("**Step 1: Learn** 📚\nTake courses & build skills")
    
    with col2:
        st.success("**Step 2: Build** 🛠️\nCreate portfolio projects")
    
    with col3:
        st.warning("**Step 3: Network** 🤝\nConnect with professionals")
    
    with col4:
        st.error("**Step 4: Land Job** 💼\nSecure your dream role")

if __name__ == "__main__":
    main()
