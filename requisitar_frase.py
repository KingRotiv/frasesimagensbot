import random
import requests
from bs4 import BeautifulSoup




def obter(termo):
	try:
		url = f"https://www.frasestop.com/{termo}/{random.randint(1, 99)}"
		resposta = requests.get(url)
		lista_frases = []
		if resposta.status_code == 200:
			conteudo = BeautifulSoup(resposta.text, "html.parser")
			for div in conteudo.find_all("div"):
				if __class := div.attrs.get("class"):
					if "card-phrase" in __class:
						lista_frases.append(div)
			
		frases = []		
		for frase in lista_frases:
			frases.append(
				{
					"texto": frase.select(".phrase-title")[0].text,
					"img": frase.select(".phrase-image-img")[0].attrs.get("data-src")
				}
			)
		return random.choice(frases)
	except: return None