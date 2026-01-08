import cerebro
from ouvidos import Ouvidos
import voz

def iniciar_jarvis():
  print("Inicializando...")

  jarvis_ouvidos = Ouvidos()

  voz.falar("Sistemas online. Ao seu dispor, mestre.")

  while True:
    print("Aguardando comando...")

    texto_usuario = jarvis_ouvidos.ouvir()

    if texto_usuario:
      print(f"👤 Mestre: {texto_usuario}")

      print("🧠 Processando...")
      resposta_jarvis = cerebro.pensar(texto_usuario)

      print(f"Jarvis: {resposta_jarvis}")
      voz.falar(resposta_jarvis)

if __name__ == "__main__":
  iniciar_jarvis()