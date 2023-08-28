# Installation
# !pip install --upgrade --quiet pip
# !pip install --quiet git+https://github.com/huggingface/transformers.git datasets[audio]
# !pip install scipy

from transformers import MusicgenForConditionalGeneration
from transformers import AutoProcessor
import torch
import scipy
import re

def audioGen(text):
    text = re.findall(r'"([^"]*)"', text)[0]
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    sampling_rate = model.config.audio_encoder.sampling_rate

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model.to(device)

    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")

    inputs = processor(
        # text=["This playful tune features a bouncy, upbeat rhythm that captures the mischievous energy of a llama munching on flowers in a garden. The melody is lighthearted and whimsical, with a touch of mischief and mayhem thrown in for good measure. Imagine a jaunty flute or recorder solo, accompanied by a bouncy piano or accordion, with a sprinkle of silly sound effects to capture the llama's antics. The chorus might feature a fun, repetitive phrase like 'Llama, llama, eating all my flowers!' to emphasize the silly situation. Overall, 'The Llama's Garden Jig' is a fun and frolicksome tune that will put a smile on your face and transport you to a sunny, whimsical world of garden adventures"],
        text=[text],
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=256)

    scipy.io.wavfile.write("musicgen_out_Llama.wav", rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
    music_path = 'musicgen_out_Llama.wav'
    
    print("MusicGen -> Completion:\n")
    
    return music_path   