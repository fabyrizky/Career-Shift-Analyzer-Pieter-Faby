"""
Advanced Visualization Components
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import FUTURE_INDUSTRIES
except ImportError:
    # Fallback if config not accessible
    FUTURE_INDUSTRIES = {}

def create_radar_chart(scores: Dict[str, float], title: str = "Skills Assessment") -> go.Figure:
    """Create a radar chart for multi-dimensional scoring"""
    
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Score',
        line_color='#1E88E5',
        fillcolor='rgba(30, 136, 229, 0.3)'
    ))
    
    # Add reference line at 50%
    fig.add_trace(go.Scatterpolar(
        r=[50] * len(categories),
        theta=categories,
        fill='toself',
        name='Industry Average',
        line_color='#FFC107',
        fillcolor='rgba(255, 193, 7, 0.1)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=title
    )
    
    return fig

def create_transition_sankey(current_role: str, target_industry: str, 
                           transition_paths: List[Dict]) -> go.Figure:
    """Create a Sankey diagram showing career transition paths"""
    
    # Define nodes
    nodes = [current_role]
    for path in transition_paths:
        nodes.extend([step['title'] for step in path])
    nodes.append(f"{target_industry} Professional")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_nodes = []
    for node in nodes:
        if node not in seen:
            seen.add(node)
            unique_nodes.append(node)
    
    # Create links
    source = []
    target = []
    value = []
    
    # Link from current role to first steps
    for i, path in enumerate(transition_paths):
        if path:
            source.append(0)  # Current role index
            target.append(unique_nodes.index(path[0]['title']))
            value.append(10)
    
    # Link between steps
    for path in transition_paths:
        for i in range(len(path) - 1):
            source.append(unique_nodes.index(path[i]['title']))
            target.append(unique_nodes.index(path[i + 1]['title']))
            value.append(10)
    
    # Link to final role
    for path in transition_paths:
        if path:
            source.append(unique_nodes.index(path[-1]['title']))
            target.append(len(unique_nodes) - 1)
            value.append(10)
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=unique_nodes,
            color=["#4CAF50"] + ["#2196F3"] * (len(unique_nodes) - 2) + ["#9C27B0"]
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color="rgba(33, 150, 243, 0.3)"
        )
    )])
    
    fig.update_layout(
        title="Career Transition Pathways",
        font_size=12,
        height=400
    )
    
    return fig

def create_skill_heatmap(user_skills: List[str], industry_requirements: Dict[str, List[str]]) -> go.Figure:
    """Create a heatmap showing skill matches across industries"""
    
    industries = list(industry_requirements.keys())
    all_skills = set()
    for skills in industry_requirements.values():
        all_skills.update(skills)
    all_skills = sorted(list(all_skills))
    
    # Create matrix
    matrix = []
    for industry in industries:
        row = []
        for skill in all_skills:
            if skill in user_skills and skill in industry_requirements[industry]:
                row.append(2)  # User has skill and it's required
            elif skill in industry_requirements[industry]:
                row.append(1)  # Required but user doesn't have
            else:
                row.append(0)  # Not required
        matrix.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=all_skills,
        y=industries,
        colorscale=[[0, '#f5f5f5'], [0.5, '#FFE082'], [1, '#4CAF50']],
        text=[[f"{'✓' if val == 2 else '✗' if val == 1 else ''}" for val in row] for row in matrix],
        texttemplate="%{text}",
        textfont={"size": 12},
        showscale=False
    ))
    
    fig.update_layout(
        title="Skill Match Across Industries",
        xaxis_title="Skills",
        yaxis_title="Industries",
        height=400
    )
    
    fig.update_xaxis(tickangle=-45)
    
    return fig

def create_timeline_chart(milestones: List[Dict]) -> go.Figure:
    """Create a timeline visualization for career transition milestones"""
    
    if not milestones:
        fig = go.Figure()
        fig.add_annotation(
            text="No timeline data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )
        return fig
    
    # Prepare data
    dates = []
    labels = []
    colors = []
    
    start_date = pd.Timestamp.now()
    for i, milestone in enumerate(milestones):
        duration_months = int(milestone.get('duration', '3').split('-')[0])
        date = start_date + pd.DateOffset(months=duration_months * (i + 1))
        dates.append(date)
        labels.append(milestone.get('title', f'Step {i+1}'))
        colors.append('#1E88E5' if i % 2 == 0 else '#FFC107')
    
    fig = go.Figure()
    
    # Add timeline line
    fig.add_trace(go.Scatter(
        x=dates,
        y=[1] * len(dates),
        mode='lines',
        line=dict(color='#E0E0E0', width=4),
        showlegend=False
    ))
    
    # Add milestone points
    fig.add_trace(go.Scatter(
        x=dates,
        y=[1] * len(dates),
        mode='markers+text',
        marker=dict(size=20, color=colors),
        text=labels,
        textposition="top center",
        showlegend=False
    ))
    
    fig.update_layout(
        title="Career Transition Timeline",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickformat='%b %Y'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0.5, 1.5]
        ),
        height=300,
        margin=dict(t=50, b=50)
    )
    
    return fig

def create_salary_projection(current_salary: float, industry: str) -> go.Figure:
    """Create salary projection chart"""
    
    # Industry salary multipliers (simplified)
    multipliers = {
        "AI": 1.5,
        "BLOCKCHAIN": 1.4,
        "CYBERSECURITY": 1.35,
        "BIOTECH": 1.3,
        "AGRITECH": 1.2,
        "AQUATECH": 1.15,
        "SPACETECH": 1.4,
        "RENEWABLE": 1.25
    }
    
    multiplier = multipliers.get(industry, 1.3)
    years = list(range(6))
    
    # Current path projection (3% annual increase)
    current_path = [current_salary * (1.03 ** year) for year in years]
    
    # New industry path (higher growth)
    new_path = [current_salary]  # Start same
    for year in range(1, 6):
        if year == 1:
            new_path.append(current_salary * 0.9)  # Initial dip
        else:
            new_path.append(current_salary * multiplier * (1.06 ** (year - 1)))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=current_path,
        mode='lines+markers',
        name='Current Career Path',
        line=dict(color='#FF9800', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=new_path,
        mode='lines+markers',
        name=f'{industry} Career Path',
        line=dict(color='#4CAF50', width=3)
    ))
    
    fig.update_layout(
        title="Projected Salary Progression",
        xaxis_title="Years",
        yaxis_title="Annual Salary ($)",
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_industry_demand_chart() -> go.Figure:
    """Create industry demand comparison chart"""
    
    industries = list(FUTURE_INDUSTRIES.keys())
    demand_scores = [85, 78, 82, 75, 70, 65, 72, 80]  # Sample demand scores
    growth_rates = [25, 20, 22, 18, 15, 12, 16, 19]   # Sample growth rates
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Market Demand',
        x=industries,
        y=demand_scores,
        marker_color='#2196F3',
        yaxis='y',
        offsetgroup=1
    ))
    
    fig.add_trace(go.Bar(
        name='Growth Rate (%)',
        x=industries,
        y=growth_rates,
        marker_color='#4CAF50',
        yaxis='y2',
        offsetgroup=2
    ))
    
    fig.update_layout(
        title="Industry Demand & Growth Rates",
        xaxis=dict(title="Industry"),
        yaxis=dict(title="Market Demand Score", side="left"),
        yaxis2=dict(title="5-Year Growth Rate (%)", overlaying="y", side="right"),
        barmode='group',
        height=400
    )
    
    return fig

def create_learning_progress_chart(completed: int, total: int) -> go.Figure:
    """Create a circular progress chart"""
    
    percentage = (completed / total * 100) if total > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Learning Progress"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#4CAF50"},
            'steps': [
                {'range': [0, 25], 'color': "#FFEBEE"},
                {'range': [25, 50], 'color': "#FFF3E0"},
                {'range': [50, 75], 'color': "#E8F5E9"},
                {'range': [75, 100], 'color': "#C8E6C9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_skill_network_graph(skills: List[str], connections: Dict[str, List[str]]) -> go.Figure:
    """Create a network graph showing skill relationships"""
    
    # Create edges
    edge_trace = []
    for skill, related in connections.items():
        if skill in skills:
            for related_skill in related:
                if related_skill in skills:
                    x0, y0 = np.random.rand(2)
                    x1, y1 = np.random.rand(2)
                    edge_trace.append(go.Scatter(
                        x=[x0, x1, None],
                        y=[y0, y1, None],
                        mode='lines',
                        line=dict(width=1, color='#888'),
                        hoverinfo='none'
                    ))
    
    # Create nodes
    node_trace = go.Scatter(
        x=[np.random.rand() for _ in skills],
        y=[np.random.rand() for _ in skills],
        mode='markers+text',
        text=skills,
        textposition="top center",
        marker=dict(
            size=20,
            color='#1E88E5',
            line=dict(width=2, color='white')
        )
    )
    
    fig = go.Figure(data=edge_trace + [node_trace])
    
    fig.update_layout(
        title="Skill Network",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400
    )
    
    return fig
