import customtkinter as ctk
import threading
import cerebro, voz
from ouvidos import Ouvidos
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class IAGUI(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.title("F.R.I.D.A.Y - Interface Neural")
    self.geometry("400x450")
    self.resizable(False, False)
    self.status_dot = ctk.CTkLabel(
      self, 
      text="●", 
      font=("Arial", 140), 
      text_color="#555555"
    )
    self.status_dot.pack(pady=(50, 20))

    self.status_text = ctk.CTkLabel(
      self, 
      text="SISTEMAS OFFLINE", 
      font=("Roboto Mono", 18, "bold")
    )
    self.status_text.pack(pady=10)

    self.user_text = ctk.CTkLabel(
      self,
      text="...",
      font=("Arial", 12),
      text_color="gray"
    )
    self.user_text.pack(pady=5)

    self.btn_iniciar = ctk.CTkButton(
      self, 
      text="INICIAR PROTOCOLO", 
      command=self.start_thread,
      width=200,
      height=40,
      font=("Arial", 14, "bold")
    )
    self.btn_iniciar.pack(pady=40)

    self.running = False

  def start_thread(self):
     if not self.running:
      self.running = True
      self.btn_iniciar.configure(state="disabled", text="SISTEMAS ONLINE", fg_color="green")

      t = threading.Thread(target=self.main_loop)
      t.daemon = True
      t.start()
  
  def update_status(self, color, text):
     self.status_dot.configure(text_color=color)
     self.status_text.configure(text=text)

  def main_loop(self):
        
    self.update_status("orange", "CARREGANDO...")
    try:
      jarvis_ouvidos = Ouvidos()
    except Exception as e:
      self.update_status("red", "ERRO DE MICROFONE")
      self.user_text.configure(text=str(e))
      return

    # Inicialização Completa
    self.update_status("#00ff00", "ONLINE")
    voz.falar("Interface visual conectada.")
    
    # Palavras de ativação locais
    WAKE_WORDS = ["edith", "edit" "jarvis", "sexta"]
    
    while self.running:
      self.update_status("white", "OUVINDO AMBIENTE...")
      texto_usuario = jarvis_ouvidos.ouvir()

      if texto_usuario:
        t_low = texto_usuario.lower()
        texto_limpo = re.sub(r'[^a-z0-9]', ' ', t_low)
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
        ativou = False
        
        for w in WAKE_WORDS:
          if w in texto_limpo:
            ativou = True
            print(f"✅ ATIVOU: '{w}' encontrado em '{texto_limpo}'")
            break
          
        if ativou:
          self.user_text.configure(text=f'"{texto_usuario}"')
          self.update_status("cyan", "PROCESSANDO...")
          resposta = cerebro.pensar(texto_usuario)

          self.update_status("purple", "FALANDO...")
          voz.falar(resposta)
        else:
          self.user_text.configure(text=f"(Ignorado: {texto_usuario})")
          self.update_status("gray", "AGUARDANDO...")

if __name__ == "__main__":
    app = IAGUI()
    app.mainloop()