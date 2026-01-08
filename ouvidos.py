import faster_whisper
import speech_recognition as sr
import os

ID_MICROFONE = 27

class Ouvidos:
  def __init__(self):
    print("🧠 Carregando Ouvidos (Whisper)...")
    self.modelo = faster_whisper.WhisperModel("base", device="cpu", compute_type="int8")

  def ouvir(self):
    reconhecer = sr.Recognizer()
    with sr.Microphone(device_index=ID_MICROFONE) as source:
      reconhecer.adjust_for_ambient_noise(source, duration=0.5)
      print("Ouvindo...", flush=True)

      try:
        audio = reconhecer.listen(source, timeout=10, phrase_time_limit=10)

        with open("temp_mic.wav", "wb") as f:
          f.write(audio.get_wav_data())

        segmentos, _ = self.modelo.transcribe("temp_mic.wav", language="pt")
        texto_transcrito = ""

        for segmento in segmentos:
          texto_transcrito += segmento.text
        
        return texto_transcrito
      
      except sr.WaitTimeoutError:
        return "" # Não falou nada
      
      except Exception as e:
        print(f"Erro ao ouvir: {e}")
        return ""
      

      