import os
import streamlit as st
import fitz  # PyMuPDF
import requests
import re
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]


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

# Streamlit UI (Clean)
st.set_page_config(page_title="Fact Checker", layout="wide")

st.title("Fact Checking System")
st.write("Upload a PDF document to extract factual claims and verify them using live web search.")

uploaded_file = st.file_uploader("Upload PDF file", type="pdf")

# Session state
if "claims" not in st.session_state:
    st.session_state.claims = ""
if "results" not in st.session_state:
    st.session_state.results = []

# --------- FUNCTIONS ---------

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

def clean_text(text):
    text = re.sub(r'(?<=\w)\s+(?=\w)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def call_openrouter(prompt):
    data = {
        "model": CURRENT_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(OPENROUTER_URL, headers=HEADERS, json=data)

    try:
        result = response.json()
    except:
        return "API returned invalid JSON."

    if "choices" not in result:
        return f"OpenRouter Error: {result}"

    raw_text = result["choices"][0]["message"]["content"]
    return clean_text(raw_text)

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

    st.subheader("Extracted PDF Text")
    st.text_area("Document Content", pdf_text, height=250)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Extract Claims"):
            with st.spinner("Extracting claims..."):
                st.session_state.claims = extract_claims(pdf_text)

    with col2:
        if st.button("Clear Results"):
            st.session_state.claims = ""
            st.session_state.results = []

    if st.session_state.claims:
        st.subheader("Extracted Claims")
        st.text(st.session_state.claims)

if st.session_state.claims:
    if st.button("Verify Claims"):
        results = []
        claims_list = [c.strip() for c in st.session_state.claims.split("\n") if c.strip()]

        progress_bar = st.progress(0)

        for i, claim in enumerate(claims_list):
            with st.spinner(f"Verifying: {claim[:60]}"):
                search_results = tavily.search(query=claim, max_results=3)

                evidence = "\n".join(
                    [r["content"] for r in search_results["results"]]
                )

                verdict = judge_claim(claim, evidence)
                results.append((claim, verdict))

            progress_bar.progress((i + 1) / len(claims_list))

        st.session_state.results = results

if st.session_state.results:
    st.subheader("Fact Check Results")

    for i, (claim, verdict) in enumerate(st.session_state.results, 1):
        with st.expander(f"Claim {i}"):
            st.markdown(f"**Claim:** {claim}")
            st.markdown(f"**Verdict:** {verdict}")

