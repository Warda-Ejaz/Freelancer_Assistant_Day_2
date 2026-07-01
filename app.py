import streamlit as st
import pandas as pd
import plotly.express as px
import time
import re 

st.set_page_config(page_title="AI Freelancer Assistant Pro", layout="wide", page_icon="🤖")

st.markdown("""
<style>
    .stButton>button { border-radius: 10px; background-color: #4F46E5; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
</style>
""", unsafe_allow_html=True)

if 'proposals' not in st.session_state: st.session_state.proposals = []
if 'cover_letters' not in st.session_state: st.session_state.cover_letters = []
if 'ai_credits' not in st.session_state: st.session_state.ai_credits = 150

def generate_ai_text(prompt_type, inputs):
    time.sleep(0.8) 
    if prompt_type == "proposal":
        return f"**Proposal for {inputs['project_title']}**\n\nDear {inputs['client_name']},\nI specialize in {inputs['skills']}. I can deliver this for ${inputs['budget']} within 2 weeks.\n\nBest, Warda"
    else:
        return f"**Cover Letter for {inputs['job_title']}**\n\nDear Hiring Team at {inputs['company']},\nWith {inputs['experience']} years exp in AI, I am a strong fit for this role.\n\nSincerely, Warda"

def clean_filename(name): 
    name = name.strip()
    if not name: name = "document"
    return re.sub(r'[^A-Za-z0-9]+', '_', name) 

st.title("🤖 AI Freelancer Assistant Pro")
st.caption("Day 2 Submission | Proposal & Cover Letter Module")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📄 Proposal Generator", "✉️ Cover Letter"])

with tab1:
    st.subheader("Key Performance Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Proposals Generated", len(st.session_state.proposals), delta=len(st.session_state.proposals) if len(st.session_state.proposals) > 0 else None)
    c2.metric("Cover Letters Generated", len(st.session_state.cover_letters), delta=len(st.session_state.cover_letters) if len(st.session_state.cover_letters) > 0 else None)
    c3.metric("AI Credits Left", st.session_state.ai_credits)

    if len(st.session_state.proposals) > 0 or len(st.session_state.cover_letters) > 0:
        data = pd.DataFrame({
            "Type": ["Proposals"] * len(st.session_state.proposals) + ["Cover Letters"] * len(st.session_state.cover_letters)
        })
        fig = px.histogram(data, x="Type", title='Documents Generated Today', color="Type")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Generate your first document to see analytics here.")

with tab2:
    st.subheader("AI Proposal Generator")
    with st.form("p_form", clear_on_submit=False): 
        c1, c2 = st.columns(2)
        cname = c1.text_input("Client Name", placeholder="e.g. ABC Corp")
        ptitle = c2.text_input("Project Title", placeholder="e.g. E-commerce AI Bot")
        skills = st.text_input("Your Skills", placeholder="Python, LangChain, AI")
        budget = st.slider("Budget $", 50, 5000, 500)
        
        if st.form_submit_button("✨ Generate AI Proposal", use_container_width=True):
            if st.session_state.ai_credits > 0 and ptitle and cname: 
                res = generate_ai_text("proposal", {"client_name":cname, "project_title":ptitle, "skills":skills, "budget":budget})
                st.session_state.proposals.append(res)
                st.session_state.ai_credits -= 10
                st.success("Proposal Generated Successfully!")
                st.code(res, language="markdown")
                clean_name = clean_filename(ptitle) 
                st.download_button("📥 Download .txt", res, f"proposal_{clean_name}.txt")
            else:
                st.error("Please fill Client Name & Project Title. AI Credits checked.")

with tab3:
    st.subheader("AI Cover Letter Generator")
    with st.form("c_form", clear_on_submit=False): 
        c1, c2 = st.columns(2)
        jtitle = c1.text_input("Job Title", placeholder="AI Engineer")
        company = c2.text_input("Company", placeholder="Meta")
        exp = st.number_input("Years of Experience", 0, 20, 2)
        
        if st.form_submit_button("✨ Generate AI Cover Letter", use_container_width=True):
            if st.session_state.ai_credits > 0 and jtitle and company: 
                res = generate_ai_text("cover", {"job_title":jtitle, "company":company, "experience":exp})
                st.session_state.cover_letters.append(res)
                st.session_state.ai_credits -= 5
                st.success("Cover Letter Generated Successfully!")
                st.code(res, language="markdown")
                clean_name = clean_filename(company) 
                st.download_button("📥 Download .txt", res, f"coverletter_{clean_name}.txt")
            else:
                st.error("Please fill Job Title & Company. AI Credits checked.")
