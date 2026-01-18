import customtkinter as ctk
import threading
import cerebro, voz
from ouvidos import Ouvidos
import re
from ferramentas import ver_hora, verificar_clima

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HUD(ctk.CTk):
  def __init__(self):
    super().__init__()

    # Remove Barra de títulos e define a posição da janela
    self.overrideredirect(True)
    self.geometry("300x170+1000+50")
    self.resizable(False, False)
    # Efeito de Transparência
    self.COR_TRANSPARENTE = "#000001"
    self.wm_attributes("-transparentcolor", self.COR_TRANSPARENTE)
    self.configure(fg_color=self.COR_TRANSPARENTE)
    # Definindo o frame que vai segurar tudo
    self.container = ctk.CTkFrame(self, fg_color=self.COR_TRANSPARENTE)
    self.container.pack(expand=True, fill="both")
    # Desenho do "Olho"
    self.nucleo_visual = ctk.CTkCanvas(
      self.container, 
      width=50, 
      height=50, 
      bg=self.COR_TRANSPARENTE, 
      highlightthickness=0
    )
    self.nucleo_visual.create_oval(2, 2, 48, 48, outline="#333333", width=2)
    self.circulo_id = self.nucleo_visual.create_oval(8, 8, 42, 42, fill="#333333", outline="")
    self.nucleo_visual.pack(pady=(10, 5))
    # Texto Informando o Status
    self.label_status = ctk.CTkLabel(
      self.container, 
      text="SISTEMAS OFFLINE", 
      font=("Roboto Mono", 12, "bold"),
      text_color="gray"
    )
    self.label_status.pack(pady=0)
    # Texto do Usuário
    self.user_text = ctk.CTkLabel(
      self.container,
      text="...",
      font=("Arial", 10),
      text_color="#888888"
    )
    self.user_text.pack(pady=5)
    # Botão de Inicio
    self.btn_iniciar = ctk.CTkButton(
      self.container, 
      text="ATIVAR", 
      command=self.start_thread,
      width=100,
      height=50,
      fg_color="#222222",
      hover_color="#444444",
      font=("Roboto", 12, "bold")
    )
    self.btn_iniciar.pack(pady=5)
    # Habilidade de Arrastar
    self.bind("<Button-1>", self.comecar_arrastar)
    self.bind("<B1-Motion>", self.arrastar_janela)
    self.running = False

  def comecar_arrastar(self, event):
    self.x_mouse = event.x
    self.y_mouse = event.y
    
  def arrastar_janela(self, event):
    x_tela = event.x_root
    y_tela = event.y_root
    novo_x = x_tela - self.x_mouse
    novo_y = y_tela - self.y_mouse
    self.geometry(f"+{novo_x}+{novo_y}")

  def update_visual(self, cor_nucleo, texto_status, cor_texto="white"):
    self.nucleo_visual.itemconfig(self.circulo_id, fill=cor_nucleo)
    self.label_status.configure(text=texto_status, text_color=cor_texto)

  def start_thread(self):
     if not self.running:
      self.running = True
      self.btn_iniciar.pack_forget()

      t = threading.Thread(target=self.main_loop)
      t.daemon = True
      t.start()

  def main_loop(self):
        
    self.update_visual("orange", "INICIALIZANDO...", "orange")
    try:
      jarvis_ouvidos = Ouvidos()
    except Exception as e:
      self.update_visual("red", "ERRO MIC", "red")
      self.user_text.configure(text=str(e)[:30])
      return

    # Inicialização Completa
    self.update_visual("#00ff00", "COLETANDO DADOS...", "#00ff00")

    # Protocolo Inicial --------------------------
    try:
      hora_atual = ver_hora.invoke({})
      clima_atual = verificar_clima.invoke({"cidade": "Camaquã"})

      texto_prompt = (
        f"Gere uma saudação curta, sarcástica e executiva para o Mestre Kelvin. "
        f"Dados atuais: {hora_atual} e {clima_atual}. "
        f"NÃO pesquise nada, apenas monte a frase."
      )

      saudacao = cerebro.pensar(texto_prompt)
      voz.falar(saudacao)

    except Exception as e:
      print(f"Erro no protocolo matinal: {e}")
      voz.falar("Sistemas online. Erro ao gerar relatório matinal.")
    
    # Palavras de ativação locais
    WAKE_WORDS = ["edith", "edit", "jarvis", "sexta"]

    # Loop Principal ----------------------
    while self.running:
      self.update_visual("cyan", "ESCUTANDO...", "cyan")
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
          self.update_visual("#ff00ff", "PROCESSANDO...", "#ff00ff")
          resposta = cerebro.pensar(texto_usuario)

          self.update_visual("#00ff00", "FALANDO...", "#00ff00")
          voz.falar(resposta)

          self.user_text.configure(text="...")
        else:
          self.user_text.configure(text=f"(Ignorado)")
          self.update_visual("#555555", "AGUARDANDO...", "gray")

if __name__ == "__main__":
    app = HUD()
    app.mainloop()