import edge_tts
import asyncio
import pygame
import os

VOZ = "pt-BR-AntonioNeural"

async def gerar_audio(texto):
  comunicacao = edge_tts.Communicate(texto, VOZ)
  await comunicacao.save("fala_temp.mp3")

def tocar_audio():
  pygame.mixer.init()
  pygame.mixer.music.load("fala_temp.mp3")
  pygame.mixer.music.play()

  while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

  pygame.mixer.music.unload()
  pygame.mixer.quit()
  
def falar(texto):
  asyncio.run(gerar_audio(texto))
  tocar_audio()