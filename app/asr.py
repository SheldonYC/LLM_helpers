import streamlit as st
from tempfile import NamedTemporaryFile
from pathlib import Path
from huggingface_hub import InferenceClient

hf_token = st.secrets['HF_TOKEN']['API_KEY']
client = InferenceClient(token=hf_token)
model = 'openai/whisper-large-v3-turbo'
mime_type_map = {
  'wav': 'audio/wav',
  'mp3': 'audio/mpeg'
}
text = ''

def asr(audio_file):
  response = ''
  try :
    audio_file_suffix = Path(audio_file.name).suffix
    # read the file as a temp file and send request to inference endpoints
    with NamedTemporaryFile(suffix=audio_file_suffix) as temp:
      temp.write(audio_file.getvalue())
      temp.seek(0) # clear the temp file
      response = client.automatic_speech_recognition(audio=temp.read(), model=model).text
    return response
  except Exception as e:
    st.error('Oh nyo... an error occurs!', icon='🚨')
    st.exception(e)

intro = '''# ASR (Auto Speech Recognition)
You can upload your audio and let LLM to create transcript with the language spoken in the audio for you!
If you want to use this service, you should follow the steps below:
1. Upload your audio as a file (.mp3 / .wav)
2. Choose the source language of the audio (if you know)
3. Wait for it!'''
st.markdown(intro)

# tabs for different source of audios
upload, microphone = st.tabs(['Upload', 'Record'])

# tab of a audio file uploader
with st.container():
  with upload:
    uploaded_file = st.file_uploader(label='Upload your audio file', key='audio_file_uploader', type=['wav','mp3'])
    if uploaded_file is not None:
      with st.spinner('Wait for response...'):
        text = asr(uploaded_file)

  with microphone:
    recorded_file = st.audio_input('Record an audio of you talking')
    if recorded_file is not None:
      with st.spinner('Wait for response...'):
        text = asr(recorded_file)

  # display the response text with textarea and a copy button
  st.code(body=text,language=None, wrap_lines=True)