# Here we are importing the necessary functions from elevenlabs library.
from elevenlabs import generate, set_api_key     # voices, play
from elevenlabs.api import History
import os


# Here we are setting up the ElevenLabs API key.
# os.environ['ELEVENLABS_API_KEY'] = 'a77232a2653ddfkjff03fgluasfc1f2'
# set_api_key(os.environ.get("ELEVENLABS_API_KEY"))

# Here we are creating a function to generate audio for podcast with premade voices. This voices are already trained and default in ElevenLabs.
def with_premade_voice(prompt, elevenlabs_api_key):
    
    os.environ['ELEVENLABS_API_KEY'] = f'{elevenlabs_api_key}'
    set_api_key(os.environ.get("ELEVENLABS_API_KEY"))
    audio_path = f'Nicole_whisper.mp3'

    audio = generate(
        text=prompt,
        voice='Nicole',
        model="eleven_monolingual_v1"
    )

    try:
        with open(audio_path, 'wb') as f:
            f.write(audio)

        print("ElevenLabs -> Completion:\n")
        return audio_path
    
    except Exception as e:
        print(e)

        return ""
    
# with_premade_voice(prompt="Theres llama")