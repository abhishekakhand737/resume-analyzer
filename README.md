# 🎯 ResumeIQ — AI Resume Analyzer

AI-powered resume analyzer built with Streamlit + Claude API.

## Features
- 📄 PDF Resume Upload
- 🤖 Claude AI Analysis
- 📊 Overall / ATS / Impact / Completeness Scores
- 💼 Job Description Match Score
- 🛠 Skills Extraction
- ✅ Strengths & Improvements
- 🤖 ATS Optimization Tips

## Setup & Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. Run App
```bash
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add `ANTHROPIC_API_KEY` in **Secrets** section:
   ```
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Deploy! 🚀

## Project Structure
```
resume_analyzer/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md          # This file
```
