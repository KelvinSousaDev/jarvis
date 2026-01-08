from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

print("🧠 Conectando ao Cérebro Local...")

sistema = SystemMessage(
    content="""
    Você é Alfred, um mordomo inteligente e sarcástico (estilo Jarvis).
    IMPORTANTE: Suas respostas devem ser CURTAS (máximo de 2 frases).
    Não use emojis. Fale como se estivesse conversando por voz.
    """
)

llm = ChatOllama(model="llama3.2",temperature=0.5)

def pensar(texto_usuario):
  mensagens = [
        sistema,
        HumanMessage(content=texto_usuario)
    ]
  resposta = llm.invoke(mensagens)
  return resposta.content