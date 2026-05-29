import streamlit as st
import PyPDF2
import io
import json
from groq import Groq

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeIQ — AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0a0a0f;
    color: #e8e6f0;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1200px; margin: auto; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed22, #2563eb22);
    border: 1px solid #7c3aed55;
    color: #a78bfa;
    padding: 0.3rem 1rem;
    border-radius: 100px;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    font-weight: 500;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #fff 30%, #a78bfa 70%, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero p {
    color: #9ca3af;
    font-size: 1.1rem;
    max-width: 500px;
    margin: 0 auto 2rem;
    line-height: 1.6;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 0.6rem;
}

.score-card {
    background: #111118;
    border: 1px solid #1f1f35;
    border-radius: 14px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.score-num {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.score-label {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.result-block {
    background: #111118;
    border: 1px solid #1f1f35;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.result-block h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.result-block ul {
    list-style: none;
    padding: 0;
}
.result-block ul li {
    padding: 0.4rem 0;
    border-bottom: 1px solid #1a1a28;
    font-size: 0.9rem;
    color: #c4c4d4;
    line-height: 1.5;
}
.result-block ul li:last-child { border-bottom: none; }
.result-block ul li::before {
    content: '▸ ';
    color: #7c3aed;
    font-size: 0.75rem;
}

.skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.skill-tag {
    background: #1a1a2e;
    border: 1px solid #2d2d4a;
    color: #a78bfa;
    padding: 0.25rem 0.8rem;
    border-radius: 100px;
    font-size: 0.78rem;
}
.skill-tag.match {
    background: #14381a;
    border-color: #22c55e44;
    color: #4ade80;
}
.skill-tag.missing {
    background: #3b1515;
    border-color: #ef444444;
    color: #f87171;
}

.prog-bar-wrap {
    background: #1a1a28;
    border-radius: 100px;
    height: 8px;
    margin: 0.4rem 0 1rem;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #7c3aed, #2563eb);
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    padding: 0.8rem 2.5rem !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    width: 100% !important;
}

.stTextArea textarea {
    background: #0f0f1a !important;
    border: 1px solid #2d2d4a !important;
    color: #e8e6f0 !important;
    border-radius: 10px !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #111118 !important;
    border-radius: 10px !important;
    gap: 4px !important;
    padding: 4px !important;
    border: 1px solid #1f1f35 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed22, #2563eb22) !important;
    color: #a78bfa !important;
    border: 1px solid #7c3aed44 !important;
}

.divider {
    border: none;
    border-top: 1px solid #1f1f35;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ──────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception:
        return None


def analyze_resume(resume_text: str, job_description: str = "") -> dict:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    jd_section = ""
    if job_description.strip():
        jd_section = f"""
Also, the user has provided this Job Description to match against:
---
{job_description}
---
Calculate a job_match_score (0-100) based on how well the resume matches this JD.
List matched_skills (skills in resume that JD needs) and missing_skills (skills JD needs but resume lacks).
"""

    prompt = f"""You are an expert HR consultant and career coach. Analyze this resume carefully.

RESUME:
---
{resume_text}
---
{jd_section}

Return ONLY a valid JSON object (no markdown, no backticks, no extra text) with this exact structure:
{{
  "overall_score": 75,
  "ats_score": 70,
  "impact_score": 65,
  "completeness_score": 80,
  "job_match_score": null,
  "candidate_name": "John Doe",
  "current_role": "Software Engineer",
  "years_experience": "3 years",
  "top_skills": ["Python", "JavaScript", "React", "SQL", "Git", "Docker", "AWS", "REST APIs"],
  "matched_skills": [],
  "missing_skills": [],
  "strengths": [
    "Strong technical background with diverse skill set",
    "Clear progression of responsibilities shown",
    "Quantified achievements with metrics",
    "Good project diversity"
  ],
  "improvements": [
    "Add more quantifiable achievements",
    "Include a professional summary at the top",
    "Add LinkedIn and GitHub profile links",
    "Use stronger action verbs throughout"
  ],
  "ats_issues": [
    "Avoid tables and columns - ATS cannot parse them",
    "Use standard section headings like Experience, Education, Skills",
    "Include keywords from job descriptions you are targeting"
  ],
  "summary": "A skilled professional with solid experience in the field. Shows consistent growth and technical competency across multiple roles.",
  "best_fit_roles": ["Software Engineer", "Backend Developer", "Full Stack Developer"]
}}

Now analyze the actual resume above and return real JSON based on it."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    # Find JSON object
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        raw = raw[start:end]
    return json.loads(raw)


def score_color(score):
    if score >= 80:
        return "#4ade80"
    elif score >= 60:
        return "#facc15"
    elif score >= 40:
        return "#fb923c"
    else:
        return "#f87171"


def render_score_card(label, score, color=None):
    c = color or score_color(score)
    st.markdown(f"""
    <div class="score-card">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{c};"></div>
        <div class="score-num" style="color:{c};">{score}</div>
        <div class="score-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_progress(label, score):
    color = score_color(score)
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="font-size:0.85rem; color:#9ca3af;">{label}</span>
        <span style="font-size:0.85rem; font-weight:600; color:{color};">{score}/100</span>
    </div>
    <div class="prog-bar-wrap">
        <div class="prog-bar-fill" style="width:{score}%; background:{color};"></div>
    </div>
    """, unsafe_allow_html=True)


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Groq AI (Free)</div>
    <h1>ResumeIQ</h1>
    <p>Upload your resume and get instant AI-powered analysis, ATS score, and actionable improvements.</p>
</div>
""", unsafe_allow_html=True)

# ─── Inputs ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-label">📄 Upload Resume (PDF)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Resume", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}** uploaded!")

with col2:
    st.markdown('<div class="section-label">💼 Job Description (Optional)</div>', unsafe_allow_html=True)
    job_desc = st.text_area(
        "JD",
        placeholder="Paste job description here to get a match % score...",
        height=140,
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button("🎯 Analyze Resume", use_container_width=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─── Analysis ─────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not uploaded_file:
        st.error("⚠️ Please upload a PDF resume first!")
    else:
        with st.spinner("🤖 AI is analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if not resume_text or len(resume_text) < 100:
                st.error("❌ Could not extract text. Make sure it's not a scanned image PDF.")
            else:
                try:
                    result = analyze_resume(resume_text, job_desc)
                    st.session_state["result"] = result
                    st.session_state["has_jd"] = bool(job_desc.strip())
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")

# ─── Results ──────────────────────────────────────────────────────────────────
if "result" in st.session_state:
    r = st.session_state["result"]
    has_jd = st.session_state.get("has_jd", False)

    # Candidate Banner
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #111118, #16161f);
                border: 1px solid #2d2d4a; border-radius: 16px;
                padding: 1.5rem 2rem; margin-bottom: 1.5rem;">
        <div style="font-size:3rem; margin-bottom:0.5rem;">👤</div>
        <div style="font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:800; color:#fff;">
            {r.get('candidate_name', 'N/A')}
        </div>
        <div style="color:#a78bfa; font-size:0.95rem; margin-top:0.2rem;">
            {r.get('current_role', 'N/A')} &nbsp;•&nbsp; {r.get('years_experience', 'N/A')} experience
        </div>
        <div style="color:#6b7280; font-size:0.85rem; margin-top:0.5rem; max-width:600px;">
            {r.get('summary', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Score Cards
    num_scores = 5 if (has_jd and r.get("job_match_score") is not None) else 4
    cols = st.columns(num_scores)
    scores = [
        ("Overall", r.get("overall_score", 0), None),
        ("ATS Score", r.get("ats_score", 0), None),
        ("Impact", r.get("impact_score", 0), None),
        ("Completeness", r.get("completeness_score", 0), None),
    ]
    if has_jd and r.get("job_match_score") is not None:
        scores.append(("Job Match", r.get("job_match_score", 0), "#60a5fa"))

    for col, (label, score, accent) in zip(cols, scores):
        with col:
            render_score_card(label, score, accent)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    tabs = st.tabs(["📊 Score Breakdown", "🛠 Skills", "✅ Strengths & Tips", "🤖 ATS Tips"])

    with tabs[0]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown("<br>", unsafe_allow_html=True)
            render_progress("Overall Score", r.get("overall_score", 0))
            render_progress("ATS Friendliness", r.get("ats_score", 0))
            render_progress("Impact & Language", r.get("impact_score", 0))
            render_progress("Section Completeness", r.get("completeness_score", 0))
            if has_jd and r.get("job_match_score") is not None:
                render_progress("Job Match", r.get("job_match_score", 0))
        with c2:
            best_roles = r.get("best_fit_roles", [])
            if best_roles:
                st.markdown(f"""
                <div class="result-block">
                    <h3>🎯 Best Fit Roles</h3>
                    <ul>{''.join(f"<li>{role}</li>" for role in best_roles)}</ul>
                </div>
                """, unsafe_allow_html=True)

    with tabs[1]:
        top_skills = r.get("top_skills", [])
        st.markdown('<div class="section-label">🔧 Skills Found in Resume</div>', unsafe_allow_html=True)
        tags = "".join(f'<span class="skill-tag">{s}</span>' for s in top_skills)
        st.markdown(f'<div class="skill-tags">{tags}</div>', unsafe_allow_html=True)

        if has_jd:
            matched = r.get("matched_skills", [])
            missing = r.get("missing_skills", [])
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="section-label">✅ Matched Skills</div>', unsafe_allow_html=True)
                t = "".join(f'<span class="skill-tag match">{s}</span>' for s in matched) or "<span style='color:#6b7280;font-size:0.85rem;'>None found</span>"
                st.markdown(f'<div class="skill-tags">{t}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="section-label">❌ Missing Skills</div>', unsafe_allow_html=True)
                t = "".join(f'<span class="skill-tag missing">{s}</span>' for s in missing) or "<span style='color:#6b7280;font-size:0.85rem;'>Great match!</span>"
                st.markdown(f'<div class="skill-tags">{t}</div>', unsafe_allow_html=True)

    with tabs[2]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            strengths = r.get("strengths", [])
            st.markdown(f"""
            <div class="result-block">
                <h3>💪 Strengths</h3>
                <ul>{''.join(f"<li>{s}</li>" for s in strengths)}</ul>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            improvements = r.get("improvements", [])
            st.markdown(f"""
            <div class="result-block">
                <h3>🔧 Areas to Improve</h3>
                <ul>{''.join(f"<li>{i}</li>" for i in improvements)}</ul>
            </div>
            """, unsafe_allow_html=True)

    with tabs[3]:
        ats_issues = r.get("ats_issues", [])
        st.markdown(f"""
        <div class="result-block">
            <h3>🤖 ATS Optimization Tips</h3>
            <p style="font-size:0.82rem; color:#6b7280; margin-bottom:1rem;">
                ATS systems filter resumes before a human reads them. Here's how to pass them:
            </p>
            <ul>{''.join(f"<li>{issue}</li>" for issue in ats_issues)}</ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding:2rem 0 1rem; color:#374151; font-size:0.8rem;">
        ResumeIQ &nbsp;•&nbsp; Powered by Groq AI (Free) &nbsp;•&nbsp; Built with Streamlit
    </div>
    """, unsafe_allow_html=True)
