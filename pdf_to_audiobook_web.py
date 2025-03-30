import streamlit as st
import PyPDF2
import pyttsx3
import tempfile
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Streamlit App UI
st.title("📖 PDF to Audiobook 🎧")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Speed Control
speed = st.slider("Select Speech Speed", min_value=50, max_value=300, value=150, step=10)

if uploaded_file:
    st.success("PDF Uploaded Successfully!")
    
    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = " ".join([pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages)) if pdf_reader.pages[i].extract_text()])

    if text:
        st.text_area("Extracted Text:", text, height=200)

        # Play Audio Button
        if st.button("🎧 Listen to Audiobook"):
            engine.setProperty('rate', speed)
            engine.say(text)
            engine.runAndWait()
            st.success("Playing Audiobook...")

        # Save as MP3 Button
        if st.button("💾 Download Audiobook (MP3)"):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            engine.save_to_file(text, temp_file.name)
            engine.runAndWait()
            
            # Provide download link
            with open(temp_file.name, "rb") as file:
                st.download_button(label="Download MP3", data=file, file_name="audiobook.mp3", mime="audio/mp3")
            
            # Cleanup temp file
            os.remove(temp_file.name)

    else:
        st.error("No text found in the PDF! Try another file.")
