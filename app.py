# Import from standard library
import os
import logging
from moviepy.editor import AudioFileClip, CompositeAudioClip
# Import from 3rd party libraries
import streamlit as st

# Import modules from the local package
from _langchain import get_response
from _elevenlabs import with_premade_voice
from audioGen import audioGen

def generate_podcast_text(prompt):
    return get_response(STORY_LINES=prompt)

def overlay_music(audio_path, music_path):
    # Open the first audio file
    audio = AudioFileClip(rf'{audio_path}')

    # Open the second audio file
    music = AudioFileClip(rf'{music_path}')

    # Combine the two audio files
    combined_audio = CompositeAudioClip([audio, music])
    combined_audio.write_audiofile(r'combined_3.wav', fps=44100)
    combined_path = r'combined_3.wav'
    return combined_path

def generate_podcast(prompt, elevenlabs_api_key):

    if prompt == "":
        st.session_state.text_error = "Please enter a prompt."
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            g_podcast = generate_podcast_text(prompt=prompt)

            st.session_state.podcast_generate = (g_podcast)
            
    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            music_path = audioGen(text=st.session_state.podcast_generate)   # This takes the response from the LLM and generates a background music for the storyline.
            audio_path = with_premade_voice(prompt=prompt, elevenlabs_api_key=elevenlabs_api_key )  # This takes the response from the LLM and generates a voice to read out the storyline.
            audio_path = r'ElevenLabsNicole.wav'
            combined_path = overlay_music(audio_path=audio_path, music_path=music_path)  # This takes the both of the audio files and combines them into one audio file.
            if music_path != "":
                st.session_state.output_file_path = combined_path

def generate_podcast_demo(prompt):

    if prompt == "":
        st.session_state.text_error = "Please enter a prompt."
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            g_podcast = generate_podcast_text(prompt=prompt)

            st.session_state.podcast_generate = (g_podcast)
            
    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            music_path = audioGen(text=st.session_state.podcast_generate)   # This takes the response from the LLM and generates a background music for the storyline.
            # audio_path = with_premade_voice(prompt=prompt, elevenlabs_api_key=elevenlabs_api_key )  # This takes the response from the LLM and generates a voice to read out the storyline.
            audio_path = r'C:\Users\Administrator\Documents\Python\Llama2Hackathon\ElevenLabsNicole.wav'
            combined_path = overlay_music(audio_path=audio_path, music_path=music_path)  # This takes the both of the audio files and combines them into one audio file.
            if music_path != "":
                st.session_state.output_file_path = combined_path


# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Configure Streamlit page and state
st.set_page_config(page_title="QuakeAI", page_icon="🎧")

# Store the initial value of widgets in session state
if "podcast_generate" not in st.session_state:
    st.session_state.podcast_generate = ""

if "output_file_path" not in st.session_state:
    st.session_state.output_file_path = ""

if "input_file_path" not in st.session_state:
    st.session_state.input_file_path = ""

if "text_error" not in st.session_state:
    st.session_state.text_error = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    
# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Give a title to the app
st.title("Eleven Labs + Llama2 + Musicgen")

# Give a description to the app
st.markdown(
    "This is a demo of QuakeAI for the llama 2 hackathon with clarifai"
)

# # Create a column layout to make UX better.
# col1, col2 = st.columns(2)

# # First one is for Twitch channel name: `Ex. lablabai`.
# with col1:
#     twitch_channel = st.text_input(label="Twitch channel", placeholder="Ex. lablabai")

# # Second one is for manual storyline input: `There's a llama in my garden. It's eating all my flowers. I'm going to call the police.`.
# with col2:
#     # manual_storyline = st.text_input(label="manual storyline input", placeholder="Ex. There's a llama...")
#     st.button(
#         label="Generate Story through Twitch",  # name on the button
#         help="Click to generate story",  # hint text (on hover)
#         key="generate_story_twitch",  # key to be used for the button
#         type="primary",  # red default streamlit button
#         on_click=get_response,  # function to be called on click
#         args=(twitch_channel),  # arguments to be passed to the function
#     )

# Get ElevenLabs API key from user
with st.sidebar:
    elevenlabs_api_key = st.text_input("ElevenLabs API key", value="", type="password")
    st.caption("*If you don't have an ElevenLabs API key, get it [here](https://elevenlabs.io/).*")

# Create a text area to describe actual podcast topic, information or brief explanation.
prompt = st.text_input(label="Story info", placeholder="Ex. There's a llama...")
# Create a column layout to make UX better.
col3, col4 = st.columns(2) 

with col3:
    st.button(
    label="Generate Story through Text Input Demo",  # name on the button
    help="Click to generate story",  # hint text (on hover)
    key="generate_story_user_demo",  # key to be used for the button
    type="secondary",  # red default streamlit button
    on_click=generate_podcast_demo,  # function to be called on click
    args=[prompt],  # arguments to be passed to the function
    )
# Create a button to generate podcast.
with col4:
    if st.button(
        label="Generate Story through Text Input",  # name on the button
        help="Click to generate story",  # hint text (on hover)
        key="generate_story_user",  # key to be used for the button
        type="primary",  # red default streamlit button
        on_click=generate_podcast,  # function to be called on click
        args=[prompt, elevenlabs_api_key],  # arguments to be passed to the function
        ):
        # Validate inputs
        if not elevenlabs_api_key.strip():
            st.error("Please provide the missing ElevenLabs API.")
    
    
# Shows loading icon while podcast and audio are being generated
text_spinner_placeholder = st.empty()

# Shows error message if any error occurs
if st.session_state.text_error:
    st.error(st.session_state.text_error)


# Output generated podcast transcription
if st.session_state.podcast_generate:
    st.markdown("""---""")
    st.subheader("Read Music Description")
    st.text_area(label="You may read Music Description while audio being generated.", value=st.session_state.podcast_generate,)


# Output generated podcast audio
if st.session_state.output_file_path:
    st.markdown("""---""")
    st.subheader("Listen to The Story")

    with open(st.session_state.output_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    st.audio(audio_bytes, format='audio/mp3', start_time=0)
    

       