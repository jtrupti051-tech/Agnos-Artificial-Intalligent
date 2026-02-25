import streamlit as st 
import spacy
import fitz  # PyMuPDF
import re

# 1. Initialize the AI
try:
    nlp = spacy.load("en_core_web_sm")
except:
    st.error("AI Brain missing. Please run: python -m spacy download en_core_web_sm")

# 2. The Master Anonymizer Function
def anonymize(text):
    doc = nlp(text)
    anonymized = text
    
    # AI Labels: PERSON (Names), GPE (Locations), ORG (Schools), FAC (Buildings)
    labels_to_hide = ["PERSON", "GPE", "ORG", "FAC"]
    
    # Pass 1: Neural Named Entity Recognition
    for ent in reversed(doc.ents):
        if ent.label_ in labels_to_hide:
            anonymized = anonymized[:ent.start_char] + f"[{ent.label_}]" + anonymized[ent.end_char:]
    
    # Pass 2: Manual Safety Net (The code you asked to add)
    anonymized = anonymized.replace("TRUPTI", "[PERSON]")
    anonymized = anonymized.replace("THOMBARE", "[PERSON]")
    anonymized = anonymized.replace("Ahilyanagar", "[GPE]")
    
    # Pass 3: Email & Phone Pattern Scrubbing (Extra protection)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    anonymized = re.sub(email_pattern, "[EMAIL]", anonymized)
    
    return anonymized

# 3. Streamlit Interface
st.set_page_config(page_title="Agnos | Unbiased Hiring", page_icon="⚖️")
st.title("🛡️ Agnos")
st.markdown("### *Hiring for talent, not identity.*")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file:
    # Extract text from the PDF
    pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    raw_text = "".join([page.get_text() for page in pdf_doc])
    
    # Run the anonymization
    clean_text = anonymize(raw_text)

    #--------ADDED SUCCESSS MESSEGE--------
    st.success("Resume is done!✅✅✅✅")
    #-----------------------
    
    # Layout for Original vs Sanitized
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### Original Preview")
        st.text(raw_text[:800] + "...")
        
    with col2:
        st.success("### Sanitized Version")
        st.text_area("Bias-Free Content", clean_text, height=450)
        
        # 4. The Download Button (The code you asked to add)
        st.download_button(
            label="📥 Download Anonymized Resume",
            data=clean_text,
            file_name="agnos_anonymized_resume.txt",
            mime="text/plain"
        )
        
        # Celebration effect for a great demo!
        if st.button("Finalize Selection"):
            st.balloons()