from pydub import AudioSegment

audio_path = r"C:\Users\Administrator\Documents\Python\Llama2Hackathon\ElevenLabsNicole.wav"
music_path = r"C:\Users\Administrator\Documents\Python\Llama2Hackathon\musicgen_out_Llama.wav"

def overlay_music(audio_path, music_path):
    # Load audio files
    audio = AudioSegment.from_wav(audio_path)
    music = AudioSegment.from_wav(music_path)

    # Overlay audio files
    combined = audio.overlay(music)

    # Export combined audio file
    combined.export("combined.wav", format="wav")

overlay_music(audio_path=audio_path, music_path=music_path)
# print(combined_path)