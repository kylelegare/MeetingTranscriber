import os
import streamlit as st
from transcribe import transcribe_audio, meeting_minutes, save_as_docx

# Put your secret key in the Streamlit secrets.toml
my_secret = st.secrets["OPENAI_API_KEY"]

# Create a file uploader for audio files
uploaded_file = st.file_uploader("Upload audio",
                                 type=['mp3', 'wav'],
                                 max_upload_size=26214400)  # max 25 MB

# Process the uploaded file
if uploaded_file is not None:
  # Save the uploaded file temporarily
  audio_file_path = 'uploaded_audio.mp3'
  with open(audio_file_path, 'wb') as f:
    f.write(uploaded_file.getbuffer())

  # Transcribe the audio and get meeting minutes
  transcription = transcribe_audio(audio_file_path)
  minutes = meeting_minutes(transcription)

  # Generate the docx file
  docx_filename = 'meeting_minutes.docx'
  save_as_docx(minutes, docx_filename)

  # Provide a link to download the docx file
  st.markdown(f"[Download the meeting minutes]({docx_filename})")
