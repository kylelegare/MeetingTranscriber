import os
import base64
import streamlit as st
from transcribe import transcribe_audio, meeting_minutes, save_as_docx

st.markdown("<h1 style='text-align: center;'>GPT-4 Powered Meeting Transcriber and Summarizer</h1>", unsafe_allow_html=True)

st.markdown("""
Drop in your audio or video file and after it's finished you'll have a word doc with:
* Meeting summary
* Key points
* Action items
* Sentiment Analysis
""")

# Put your secret key in the Streamlit secrets.toml
my_secret = st.secrets["OPENAI_API_KEY"]

# Create a file uploader for audio files
uploaded_file = st.file_uploader("Upload audio", type=['mp3', 'wav', 'm4a', 'webm', 'mp4', 'mpga', 'mpeg'])

# Process the uploaded file
if uploaded_file is not None:
  # Save the uploaded file temporarily
  audio_file_path = 'uploaded_audio.' + uploaded_file.type.split('/')[1]
  with open(audio_file_path, 'wb') as f:
    f.write(uploaded_file.getbuffer())

  # Transcribe the audio and get meeting minutes
  transcription = transcribe_audio(audio_file_path)
  minutes = meeting_minutes(transcription)

  # Generate the docx file
  docx_filename = 'meeting_minutes.docx'
  save_as_docx(minutes, docx_filename)

  # Provide a link to download the docx file
  def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
      data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

  st.markdown(get_binary_file_downloader_html(docx_filename, 'Meeting Summary'), unsafe_allow_html=True)
