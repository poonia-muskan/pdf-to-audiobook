import streamlit as st
import PyPDF2
from gtts import gTTS
import tempfile
import os

# Streamlit App UI
st.title("📖 PDF to Audiobook 🎧")

uploaded_file = st.file_uploader("Upload your PDF 😊", type=["pdf"])

# Speed Control (gtts does not support speed natively)
speed_option = st.radio("Select Speech Speed", ["Slow", "Normal"], index=1)
speed = True if speed_option == "Slow" else False

if uploaded_file:
    st.success("Well done, PDF Uploaded Successfully! <3")

    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    if text:
        st.text_area("Extracted Text:", text, height=200)

        # Generate Audio
        tts = gTTS(text=text, lang="en", slow=speed)

        # Save to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)

        # Play Audio Button
        if st.button("🎧 Listen to Audiobook"):
            st.audio(temp_file.name, format="audio/mp3")

        # Download Audio Button
        with open(temp_file.name, "rb") as file:
            st.download_button(label="💾 Download Audiobook (MP3)", data=file, file_name="audiobook.mp3", mime="audio/mp3")

        # Cleanup temp file
        os.remove(temp_file.name)

    else:
        st.error("No text found in the PDF! Try another file.")
