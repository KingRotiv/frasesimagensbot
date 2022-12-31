import os
import logging

import telebot
from telebot.util import escape
from telebot.types import (
	ReplyKeyboardMarkup
)

import requisitar_frase




TOKEN = os.environ.get("BOT_TOKEN")
assert TOKEN, "Token do bot não informada!"

bot = telebot.TeleBot(TOKEN, parse_mode="html")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

termos = {
	"reflexão": "frases-de-reflexao",
	"atitude": "frases-de-atitude",
	"amor": "frases-de-amor",
	"amizade": "frases-de_amizade",
	"felicidade": "frases-de_felicidade",
	"bonitas": "frases-bonitas",
	"auto-confiança": "frases-de_auto-confianca",
	"deus": "frases-deus",
	"engraçadas": "frases-engracadas",
	"motivação": "frases-de-motivacao",
	"ano novo": "frases-ano-novo",
	"sonhos": "frases-sonhos"
}


# Menu
def menu_start():
	menu = ReplyKeyboardMarkup(
		input_field_placeholder="Temas",
		resize_keyboard=True,
	)
	menu.add(*list(map(lambda _: _.title(), termos.keys())))
	return menu
	

# Retornando frase	
@bot.message_handler(func=lambda _: _.text.lower() in termos.keys())
def responder_frase(mensagem):
	bot.send_chat_action(
		chat_id=mensagem.from_user.id,
		action="typing"
	)
	termo = mensagem.text.lower()
	frase = requisitar_frase.obter(f"{termos[termo]}")
	if frase:
		bot.send_photo(
			chat_id=mensagem.from_user.id,
			photo=frase["img"],
			caption=f'<code>{escape(frase["texto"])}</code>'
		)
	else:
		bot.send_message(
			chat_id=mensagem.from_user.id,
			text="Não foi possível encontrar uma frase. Tente mais tarde..."
		)
	

# Comando start	
@bot.message_handler(commands=["start"])
def comando_start(mensagem):
	nome = escape(mensagem.from_user.first_name)
	bot.send_message(
		chat_id=mensagem.from_user.id,
		text=f"😊 Olá, <u>{nome}</u>! Use os botões abaixo para escolher o tema da frase.",
		reply_markup=menu_start()
	)
	
	
# Iniciando o bot
if __name__ == "__main__":
	bot.infinity_polling()