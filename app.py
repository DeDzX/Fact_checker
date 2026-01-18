import os
import streamlit as st
import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables (still fine for local use)
load_dotenv()

# Use Streamlit secrets for deployment
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY")

# OpenRouter API config
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Fact Checker AI"
}

# Free Meta Llama 3 model
CURRENT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# Tavily client
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# Streamlit UI
st.set_page_config(page_title="Fact Checker AI", layout="wide")
st.title("Fact-Checking Web App")
st.write(f"Verifying claims using **Meta Llama 3** + **Live Web Search**")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# Session state
if "claims" not in st.session_state:
    st.session_state.claims = ""

if "results" not in st.session_state:
    st.session_state.results = []

# --------- FUNCTIONS ---------

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

def call_openrouter(prompt):
    data = {
        "model": CURRENT_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(OPENROUTER_URL, headers=HEADERS, json=data)
    
    if response.status_code != 200:
        return f"API Error: {response.text}"
    
    return response.json()["choices"][0]["message"]["content"]

def extract_claims(text):
    prompt = f"""
Extract factual claims (numbers, dates, statistics, named facts) from this text.
Return each claim on a new line.

TEXT:
{text}
"""
    return call_openrouter(prompt)

def judge_claim(claim, evidence):
    prompt = f"""
Claim: {claim}

Evidence:
{evidence}

Classify the claim as:
- Verified
- Inaccurate
- False
- Insufficient Evidence

Give a short explanation.
"""
    return call_openrouter(prompt)

# --------- APP LOGIC ---------

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    st.subheader("📄 PDF Content")
    st.text_area("Extracted Text", pdf_text, height=200)

    if st.button("🔍 Extract Claims"):
        with st.spinner("Extracting claims..."):
            st.session_state.claims = extract_claims(pdf_text)

        st.subheader("📝 Extracted Claims")
        st.text(st.session_state.claims)

if st.session_state.claims:
    if st.button("✅ Verify Claims"):
        results = []
        claims_list = [c.strip() for c in st.session_state.claims.split("\n") if c.strip()]

        progress_bar = st.progress(0)

        for i, claim in enumerate(claims_list):
            with st.spinner(f"Verifying: {claim[:60]}..."):
                search_results = tavily.search(query=claim, max_results=3)

                evidence = "\n".join(
                    [r["content"] for r in search_results["results"]]
                )

                verdict = judge_claim(claim, evidence)
                results.append((claim, verdict))

            progress_bar.progress((i + 1) / len(claims_list))

        st.session_state.results = results

if st.session_state.results:
    st.subheader("📊 Fact Check Results")

    for claim, verdict in st.session_state.results:
        with st.expander(f"Claim: {claim[:100]}..."):
            st.markdown(f"**Verdict:**\n\n{verdict}")






