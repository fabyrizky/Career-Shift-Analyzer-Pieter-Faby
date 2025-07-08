# Career Shift to Future STEM Industry 🚀

> AI-powered career transition analyzer helping professionals transition to future STEM industries like AI, Blockchain, Cybersecurity, BioTech, AgriTech, AquaTech, SpaceTech, and Renewable Energy.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.29.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **🔍 Skill Analysis**: Intelligent extraction and categorization of your current skills using NLP
- **🎯 Career Mapping**: Personalized career transition paths to future STEM industries
- **📊 Readiness Score**: Comprehensive assessment of your readiness for career transition
- **📚 Learning Paths**: Curated learning resources and skill development roadmaps
- **💼 Industry Insights**: Real-time market trends and salary projections
- **🗺️ Visual Analytics**: Interactive charts and visualizations for better decision-making

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/career_shift_analyzer.git
cd career_shift_analyzer
```

2. **Create a virtual environment** (recommended)
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

4. **Download spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
career_shift_analyzer/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── config.py                   # Configuration settings
├── .gitignore                 # Git ignore file
│
├── data/                      # Data files
│   ├── industry_skills.csv    # Industry skill requirements
│   ├── course_catalog.csv     # Learning resources catalog
│   └── ...                    # Additional data files
│
├── utils/                     # Core utilities
│   ├── __init__.py
│   ├── career_mapper.py       # Career transition mapping
│   ├── skill_extractor.py     # NLP-based skill extraction
│   ├── readiness_score.py     # Readiness calculation
│   └── ...                    # Additional utilities
│
├── components/                # UI components
│   ├── __init__.py
│   ├── ui_components.py       # Reusable UI elements
│   └── visualizations.py      # Chart components
│
└── tests/                     # Unit tests
    └── ...
```

## 🎯 Target Industries

1. **AI & Machine Learning** 🤖
   - Machine Learning Engineer
   - Data Scientist
   - AI Researcher
   - Computer Vision Engineer

2. **Blockchain & Web3** ⛓️
   - Blockchain Developer
   - Smart Contract Developer
   - DeFi Analyst
   - Web3 Developer

3. **Cybersecurity** 🔒
   - Security Analyst
   - Penetration Tester
   - Security Architect
   - SOC Analyst

4. **BioTech & HealthTech** 🧬
   - Bioinformatician
   - Clinical Data Analyst
   - Genomics Specialist
   - Biostatistician

5. **Agriculture & FoodTech** 🌾
   - Precision Agriculture Specialist
   - AgTech Developer
   - Sustainability Consultant
   - IoT Agriculture Engineer

6. **Aquaculture & Marine Tech** 🐟
   - Aquaculture Systems Engineer
   - Marine Biologist
   - Marine Biotechnologist
   - Aquatech Data Analyst

7. **SpaceTech & Exploration** 🚀
   - Satellite Engineer
   - Space Systems Analyst
   - Mission Planner
   - Remote Sensing Specialist

8. **New & Renewable Energy** ♻️
   - Renewable Energy Engineer
   - Energy Data Analyst
   - Grid Integration Engineer
   - Sustainability Analyst

## 💡 How It Works

### 1. **Skill Extraction**
The app uses Natural Language Processing (NLP) to extract and categorize skills from your input:
- Technical skills (programming languages, frameworks, tools)
- Domain skills (industry-specific knowledge)
- Soft skills (communication, leadership, problem-solving)

### 2. **Career Mapping**
Based on your current role and skills, the system:
- Calculates transition feasibility scores
- Identifies transferable skills
- Maps optimal career paths
- Estimates transition duration

### 3. **Readiness Assessment**
Comprehensive scoring based on:
- Current skills match (35%)
- Transferable skills (25%)
- Learning curve (20%)
- Market demand (20%)

### 4. **Learning Path Generation**
Personalized recommendations including:
- Priority skills to develop
- Curated course suggestions
- Project ideas
- Certification paths

## 🛠️ Configuration

Edit `config.py` to customize:
- Industry definitions and skills
- Scoring weights
- UI colors and themes
- Learning platform URLs

## 📊 Data Sources

- **Industry Skills**: Curated from O*NET, LinkedIn, and industry reports
- **Course Catalog**: Aggregated from Coursera, Udemy, edX, and other platforms
- **Market Data**: Based on Bureau of Labor Statistics and industry trends

## 🔧 Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
flake8 .
```

### Adding New Industries
1. Update `FUTURE_INDUSTRIES` in `config.py`
2. Add industry skills to `data/industry_skills.csv`
3. Update career mapping in `utils/career_mapper.py`

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- NLP powered by [spaCy](https://spacy.io/)
- Visualizations using [Plotly](https://plotly.com/)
- Icons from [Emoji](https://emojipedia.org/)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/career_shift_analyzer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/career_shift_analyzer/discussions)
- **Email**: your.email@example.com

## 🚀 Deployment

### Deploy to Streamlit Cloud (Recommended)

1. **Fork this repository** to your GitHub account

2. **Prepare your repository:**
   - Ensure all files are committed
   - Check that `requirements.txt` is up to date
   - Verify `packages.txt` exists (for system dependencies)

3. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Click "New app"
   - Connect your GitHub account
   - Select your forked repository
   - Set branch to `main`
   - Set main file path to `app.py`
   - Click "Deploy"

4. **Troubleshooting Deployment:**
   - If you see "Error installing requirements", check the logs
   - Common issues:
     - Missing system dependencies: Add to `packages.txt`
     - Version conflicts: Update `requirements.txt`
     - Import errors: Check file paths and `__init__.py` files

### Deploy to Heroku

1. **Create required files:**

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

2. **Deploy to Heroku:**
```bash
heroku create your-app-name
heroku buildpacks:add --index 1 heroku/python
git push heroku main
```

### Local Development

For local development with all features:
```bash
# Install development dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the app
streamlit run app.py
```

## 🌟 Future Enhancements

- [ ] AI-powered chat assistant for career guidance
- [ ] Integration with job boards and LinkedIn
- [ ] Advanced skill matching using transformer models
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] API for third-party integrations

---

**Made with ❤️ for career changers worldwide**

*Remember: The best time to plant a tree was 20 years ago. The second best time is now. Start your STEM career journey today!* 🌱
