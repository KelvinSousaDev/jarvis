from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from ferramentas import ver_hora, abrir_programa, pesquisar_internet, monitorar_sistema, controlar_midia, ler_memoria, salvar_memoria, tocar_youtube, verificar_clima, controlar_sistema, consultar_vigilante, analisar_tendencia, ver_tela


print("🧠 Conectando ao Cérebro Local...")

PERSONALIDADE = """
Você é a SEXTA-FEIRA (ou E.D.I.T.H.), uma inteligência artificial avançada criada por Kelvin.
Sua personalidade é feminina, eficiente, profissional e levemente sarcástica.

CONTEXTO CRÍTICO (MEMÓRIA):
Você possui acesso a dados pessoais sobre o Kelvin logo abaixo. 
USE ESSES DADOS. Se o usuário perguntar algo que está na memória, responda com base nela.

REGRAS DE OURO:
1. Respostas curtas e diretas (máximo 3 frases).
2. NÃO use emojis.
3. FERRAMENTA 'salvar_memoria': Use APENAS se o usuário disser explicitamente "anote", "lembre-se", "salve isso". NÃO use para salvar sua própria descrição.
4. QUESTÕES DE IDENTIDADE: Se perguntarem "quem é você", "qual seu nome" ou "quem te criou", NÃO USE NENHUMA FERRAMENTA. Responda imediatamente com seu conhecimento interno.
5. PROIBIDO pesquisar na internet sobre "Edith", "Sexta-Feira", "Jarvis" ou "Kelvin". Você já sabe quem são.
"""

llm = ChatOllama(model="qwen2.5:7b",temperature=0.1)

lista_ferramentas = [
  ver_hora, abrir_programa, pesquisar_internet, monitorar_sistema, controlar_midia, ler_memoria, salvar_memoria,
  tocar_youtube, verificar_clima, controlar_sistema, consultar_vigilante, analisar_tendencia, ver_tela
  ]
llm_com_ferramentas = llm.bind_tools(lista_ferramentas)

mapa_funcoes = {
  "ver_hora": ver_hora,
  "abrir_programa": abrir_programa,
  "pesquisar_internet": pesquisar_internet,
  "monitorar_sistema": monitorar_sistema,
  "controlar_midia": controlar_midia,
  "ler_memoria": ler_memoria,
  "salvar_memoria": salvar_memoria,
  "tocar_youtube": tocar_youtube,
  "verificar_clima": verificar_clima,
  "controlar_sistema": controlar_sistema,
  "consultar_vigilante": consultar_vigilante,
  "analisar_tendencia": analisar_tendencia,
  "ver_tela": ver_tela
}

ferramentas_imediatas = ["abrir_programa", "controlar_midia", "tocar_youtube", "salvar_memoria", "controlar_sistema"]

def pensar(texto_usuario):
  try:
    memoria_atual = ler_memoria.invoke({})
  except:
    memoria_atual = "Memória vazia ou inacessível."

  prompt_sistema = f"{PERSONALIDADE}\n\nMEMÓRIA DE LONGO PRAZO (O que você sabe sobre o Kelvin):\n{memoria_atual}"
  mensagem_sistema = SystemMessage(content=prompt_sistema)

  mensagens = [mensagem_sistema, HumanMessage(content=texto_usuario)]
  resposta = llm_com_ferramentas.invoke(mensagens)

  if resposta.tool_calls:
    print(f"🔧 IA solicitou: {resposta.tool_calls}")

    dados_brutos = ""

    for ferramenta in resposta.tool_calls:
      nome_ferramenta = ferramenta["name"]
      argumentos = ferramenta["args"]

      if nome_ferramenta in mapa_funcoes:
        print(f"⚙️ Executando: {nome_ferramenta}...")
        funcao_real = mapa_funcoes[nome_ferramenta]
        resultado = funcao_real.invoke(argumentos)

        if nome_ferramenta in ferramentas_imediatas:
          return str(resultado)

        dados_brutos += str(resultado) + ". "

    print(f"🔍 Dados crus recebidos: {dados_brutos}")
    novo_prompt = f"""
        O usuário perguntou: '{texto_usuario}'
        A ferramenta trouxe estes dados técnicos: {dados_brutos}
        MISSÃO: Use os dados acima para responder a pergunta do usuário de forma natural, falada e curta.
      """
    
    resposta_final = llm.invoke([mensagem_sistema, HumanMessage(content=novo_prompt)])
    return resposta_final.content
      
  return resposta.content