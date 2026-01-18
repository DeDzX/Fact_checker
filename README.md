# Fact_checker
This project is a simple web-based fact checking system that helps verify factual claims found in PDF documents. The user uploads a PDF, the system extracts key claims, searches the web for evidence, and then checks whether those claims are accurate using an AI language model.

## Project Overview

This project is a simple web-based fact checking system that helps verify factual claims found in PDF documents. The user uploads a PDF, the system extracts key claims, searches the web for evidence, and then checks whether those claims are accurate using an AI language model.

The goal of this project is to show how AI and live web search can be combined to assist with information verification.

---

## How It Works

The system follows a step-by-step process:

1. **Upload a PDF file**
   The user uploads a document through the web interface.

2. **Text extraction**
   The content of the PDF is extracted using a PDF reading library.

3. **Claim extraction**
   An AI model identifies factual claims such as numbers, dates, and specific statements from the text.

4. **Web search for evidence**
   Each claim is searched online using a web search API to collect supporting or contradicting information.

5. **Claim verification**
   The claim and the evidence are analysed by the AI model, which classifies the claim as:

   * Verified
   * Inaccurate
   * False
   * Insufficient Evidence

6. **Results display**
   The final verdict and explanation are shown to the user in a clean and readable format.

---

## Technologies Used

* **Python** – Main programming language
* **Streamlit** – Web interface
* **PyMuPDF (fitz)** – PDF text extraction
* **OpenRouter API** – Access to Meta Llama 3 AI model
* **Tavily API** – Live web search
* **Requests** – API communication
* **dotenv** – Environment variable management

---

## Installation Guide

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd fact_checker_app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Required Libraries

```bash
pip install streamlit pymupdf requests python-dotenv tavily-python
```

### 4. Create a `.env` File

Add your API keys in a file named `.env`:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
TAVILY_API_KEY=xxxxxxxxxxxxxxxx
```

---

## Running the Application

```bash
streamlit run app.py
```

A local URL will appear in the terminal. Open it in your browser.

---

## How to Use the App

1. Upload a PDF file
2. Click **Extract Claims**
3. Review the extracted claims
4. Click **Verify Claims**
5. View the results for each claim

Each claim is shown with a short explanation of whether it is verified or not.

---

## Key Features

* Automatic claim detection from PDFs
* Live web-based evidence retrieval
* AI-powered verification
* Simple and clean interface
* Expandable result sections
* Error handling for API issues

---
## Conclusion

This project demonstrates how AI and web search can be used together to analyse factual information in documents. It provides a practical example of building a simple fact checking tool with real-world applications in research, journalism, and education.

---
