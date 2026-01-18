import time
import datetime
from langchain_core.tools import tool
from ddgs import DDGS
import psutil
import pyautogui
import os
import pywhatkit
import requests
from dotenv import load_dotenv
import psycopg2
import statistics
import base64
import json
from io import BytesIO
from PIL import Image


load_dotenv()

@tool
def ver_hora():
  """
    Retorna o horário atual do sistema. Use isso quando o usuário perguntar as horas ou a data de hoje.
  """
  hora_atual = datetime.datetime.now()
  hora_formatada = hora_atual.strftime("%H:%M do dia %d/%m/%Y")
  return hora_formatada

@tool
def abrir_programa(nome_programa: str):
  """
    Abre QUALQUER programa instalado no Windows.
    Use para: 'abrir excel', 'abrir discord', 'abrir steam', 'abrir word'.
  """
  
  try:
    pyautogui.press("win")
    time.sleep(1.0)
    pyautogui.write(nome_programa)
    time.sleep(1.5)
    pyautogui.press("enter")
    return f"Iniciando {nome_programa} via Menu Iniciar."
  
  except Exception as e:
    return f"Erro ao tentar abrir o programa: {e}"


@tool
def pesquisar_internet(pergunta: str):
  """
      Pesquisa informações na internet.
      Use isso para buscar fatos atuais, notícias, clima ou dados que você não sabe.
  """

  with DDGS() as ddgs:
    resultados = ddgs.text(pergunta, max_results=3)
    resposta = ""
    for resultado in resultados:
      titulo = resultado["title"]
      resumo = resultado["body"]
      frase = f"{titulo} - {resumo} \n"
      resposta += frase
    
    return resposta
  
@tool
def monitorar_sistema():
  """
    Verifica o uso atual do sistema (CPU, Memória RAM e Bateria).
    Use isso quando o usuário perguntar: 'Como está o PC?', 'Uso de CPU', 'Memória' ou 'Bateria'.
  """

  uso_cpu = psutil.cpu_percent(interval=1)
  uso_ram = psutil.virtual_memory().percent

  resposta = f"CPU em {uso_cpu}%. Memória RAM em {uso_ram}%."

  bateria = psutil.sensors_battery()
  if bateria:
    resposta += f"Bateria em {bateria.percent}%"
  else:
    resposta += " Ligado na tomada (Sem bateria)."
  return resposta

@tool
def controlar_sistema(comando: str):
  """
    Controla funções do sistema operacional.
    Comandos aceitos: 'desligar', 'reiniciar', 'volume maximo', 'volume mudo', 'aumentar volume', 'diminuir volume'.
  """
  comando = comando.lower().strip()

  if "desligar" in comando:
    os.system("shutdown /s /t 10")
    return "Iniciando sequênmcia de desligamento em 10 segundos"
  
  elif "reiniciar" in comando:
    os.system("shutdown /r /t 10")
    return "Reiniciando sistema em 10 segundos."
  
  elif "mudo" in comando:
    pyautogui.press("volumemute")
    return "Áudio silenciado."
  
  elif "aumentar" in comando:
    for _ in range(5):
      pyautogui.press("volumeup")
    return "Volume aumentado."
  
  elif "diminuir" in comando:
    for _ in range(5):
      pyautogui.press("volumedown")
    return "Volume diminuído."
  
  return "Comando de sistema não reconhecido."

@tool
def controlar_midia(comando: str):
  """
    Controla o player de áudio/vídeo que JÁ ESTÁ ABERTO.
    Use APENAS para comandos de controle: 'pausar', 'retomar' (play), 'proxima', 'anterior'.
    NÃO use isso para buscar músicas novas.
  """

  teclas = {
    "pausar": "playpause",
    "tocar": "playpause",
    "proxima": "nexttrack",
    "anterior": "prevtrack",
  }
  comando_limpo = comando.lower().strip()

  if comando_limpo in teclas:
    pyautogui.press(teclas[comando_limpo])
    return f"Comando de mídia '{comando_limpo}' executado."
  else:
    return f"Comando de mídia '{comando_limpo}' não reconhecido."
  
@tool
def salvar_memoria(texto: str):
  """
    Salva uma informação importante na memória de longo prazo.
    Use isso quando o usuário disser 'anote isso', 'lembre-se que', ou passar uma informação pessoal (senha).
  """

  if not os.path.exists("memoria"):
    os.makedirs("memoria")

  caminho = "memoria/dados.txt"
  data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

  with open(caminho, "a", encoding="utf-8") as arquivo:
    arquivo.write(f"[{data_hora}] {texto}\n")
  return "Informação salva no banco de dados."

@tool
def ler_memoria():
  """
    Lê todas as anotações salvas na memória de longo prazo.
    Use isso quando o usuário perguntar 'o que eu te pedi para lembrar?', 'qual é a senha?', 'o que você sabe sobre mim?'.
  """

  caminho = "memoria/dados.txt"
  if not os.path.exists(caminho):
    return "Minha memória está vazia por enquanto."
  
  with open(caminho, "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
  return conteudo

@tool
def tocar_youtube(video: str):
  """
    Busca e toca um vídeo ou música NOVA no YouTube.
    Use isso quando o usuário disser: 'toque [nome]', 'ouvir [nome]', 'bota [nome]'.
  """

  pywhatkit.playonyt(video)
  return f"Tocando {video} no YouTube."

@tool
def verificar_clima(cidade: str) -> str:
  """
    Verifica o clima atual em uma cidade específica.
  """

  API_KEY = os.getenv("OPENWEATHER_KEY")
  if not API_KEY:
    return "Erro: Chave de API não encontrada no arquivo .env."

  link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric"

  try:
    requisicao = requests.get(link)
    dic_requisicao = requisicao.json()

    if dic_requisicao.get("cod") != 200:
      return f"Erro ao verificar clima: {dic_requisicao.get('message')}"
    
    descricao = dic_requisicao['weather'][0]['description']
    temperatura = dic_requisicao['main']['temp']
    humidade = dic_requisicao['main']['humidity']

    resposta = f"Em {cidade}, o clima está com {descricao}. A temperatura é de {temperatura}°C e a umidade é de {humidade}%."
    return resposta
  
  except Exception as e:
    return f"Erro de conexão: {str(e)}"
  
@tool
def consultar_vigilante(produto: str):
  """
    Busca o preço de um produto monitorado no banco de dados do Vigilante.
    Use quando o usuário perguntar: 'qual o preço do [produto]', 'quanto tá o [produto]', 'veja no vigilante o [produto]'.
  """

  url = os.getenv("DATABASE_URL")
  if not url:
    return "Erro: A variável DATABASE_URL não foi encontrada no .env."
  
  try:
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    # Busca de Dados, limitando somente no produto que perguntou
    query = """
      SELECT dim.loja, dim.nome_produto, f.valor_coletado, f.data_coleta
      FROM dim_produtos as dim
      JOIN fato_precos as f ON dim.id = f.produto_id
      WHERE dim.nome_produto ILIKE %s
      ORDER BY dim.id DESC
      LIMIT 1
    """
    cursor.execute(query, (f"%{produto}%",))
    resultado = cursor.fetchone()
    conn.close()
    # Relatório dos dados recebidos
    if resultado:
      loja, nome_produto, valor_coletado, data_coleta = resultado
      return f"REGISTRO DO VIGILANTE: O produto '{nome_produto}' foi visto no site {loja} por R$ {valor_coletado} em {data_coleta}."
    else:
      return f"Vasculhei o banco de dados e não encontrei nenhum registro recente para '{produto}'."
    
  except Exception as e:
    return f"Erro técnico ao consultar o banco de dados: {str(e)}"

@tool
def analisar_tendencia(produto: str):
  """
    Analisa o histórico de preços de um produto para dizer se está barato ou caro.
    Use quando o usuário perguntar: 'vale a pena comprar [produto]?', 'analise a tendência do [produto]', 'o [produto] está barato?'.
  """
  url = os.getenv("DATABASE_URL")
  if not url:
    return "Erro: Configuração de banco de dados ausente."
  
  try:
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    query = """
      SELECT f.valor_coletado, dim.loja, f.data_coleta
      FROM dim_produtos as dim
      JOIN fato_precos as f ON dim.id = f.produto_id
      WHERE dim.nome_produto ILIKE %s
      ORDER BY f.data_coleta DESC
      LIMIT 30
    """
    cursor.execute(query, (f"%{produto}%",))
    resultados = cursor.fetchall()
    conn.close
    if not resultados:
      return f"Não tenho dados históricos suficientes sobre '{produto}' para uma análise."
    # Processamento dos dados recebidos
    precos = [float(linha[0]) for linha in resultados]
    preco_atual = precos[0]
    preco_medio = statistics.mean(precos)
    menor_preco = min(precos)
    maior_preco = max(precos)
    # Análise de tendência
    diferenca = preco_atual - preco_medio
    porcentagem = (diferenca / preco_medio) * 100

    if porcentagem < -10:
      conselho = "Oportunidade EXCELENTE. O preço caiu muito."
    elif porcentagem < 0:
      conselho = "Bom momento. Está levemente abaixo da média."
    else:
      conselho = "Cuidado. O preço está acima da média histórica."
    
    relatorio = (
      f"ANÁLISE DE MERCADO PARA '{produto.upper()}':\n"
      f"- Preço Atual: R$ {preco_atual:.2f}\n"
      f"- Média Histórica: R$ {preco_medio:.2f}\n"
      f"- Menor Preço Já Visto: R$ {menor_preco:.2f}\n"
      f"VEREDITO: {conselho} (Variação de {porcentagem:.1f}%)"
    )
    return relatorio
  
  except Exception as e:
    return f"Erro ao calcular tendências: {str(e)}"
  
@tool
def ver_tela(pergunta: str):
  """
    Captura a tela atual, REDIMENSIONA e envia para o LLaVA analisar.
    Use quando o usuário disser: 'o que você está vendo?', 'descreva minha tela', 'leia isso'.
    O parâmetro 'pergunta' deve ser o que o usuário quer saber sobre a imagem (ex: 'Descreva a imagem', 'Qual o erro no código?').
  """

  print("👁️ Capturando a tela para análise...")

  try:
    screenshot = pyautogui.screenshot()
    screenshot.thumbnail((800, 800))

    buffered = BytesIO()
    screenshot.save(buffered, format="JPEG", quality=80)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    url = "http://localhost:11434/api/generate"
    payload = {
      "model": "llava",
      "prompt": pergunta if len(pergunta) > 5 else "Descreva detalhadamente o que você vê nesta imagem da tela.",
      "stream": False,
      "images": [img_str]
    }
    print("🧠 Enviando para o Lobo Visual (LLaVA)...")

    response = requests.post(url, json=payload)
    if response.status_code == 200:
      resultado = response.json()
      descricao = resultado.get("response", "Sem resposta visual.")
      
      if not descricao or "send an image" in descricao.lower():
        return "Erro visual: O modelo LLaVA não recebeu a imagem corretamente."
      
      return f"RELATÓRIO VISUAL DA TELA: {descricao}"
    else:
      return f"Erro na API visual: {response.text}"
    
  except Exception as e:
    return f"Erro ao processar visão: {str(e)}"