from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]['xvector']).unsqueeze(0)

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
inputs = processor(text = 'An example', return_tensors='pt')

vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

speech = model.generate_speech(inputs['input_ids'], speaker_embeddings, vocoder=vocoder)

sf.write("test", speech.numpy(), samplerate=16_000)