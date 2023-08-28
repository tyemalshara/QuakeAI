from moviepy.editor import AudioFileClip, CompositeAudioClip

# Erstellen Sie eine neue Klasse, die von CompositeAudioClip erbt
# class MyCompositeAudioClip(CompositeAudioClip):
#     def __init__(self, clips):
#         super().__init__(clips)
#         self.fps = 44100

# Open the first audio file
audio1 = AudioFileClip(r'C:\Users\Administrator\Documents\Python\Llama2Hackathon\ElevenLabsNicole.wav')

# Open the second audio file
audio2 = AudioFileClip(r'C:\Users\Administrator\Documents\Python\Llama2Hackathon\musicgen_out_Llama.wav')

# Combine the two audio files
combined_audio = CompositeAudioClip([audio1, audio2])
combined_audio.write_audiofile(r'C:\Users\Administrator\Documents\Python\Llama2Hackathon\combined_2.wav', fps=44100)