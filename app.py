# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'oi' in incoming_msg or 'eai' in incoming_msg:
        msg.body('''Oii! Eu sou a Lélia, pode me chamar de Lê. Posso te ajudar a encontrar as rodas para você se sentir mais segura. 
                    Além disso, pode contar comigo caso estiver em situação de risco.\n\nVocê está segura?\n\n1 - Perigo\n2 - Segura''')
        responded = False

    if 'perigo' in incoming_msg:
        msg.media('1 - EMERGENCIA \n2 - Compartilhe sua localizacao com a gente que ficaremos de olho.')
        responded = False

    if 'segura' in incoming_msg:
        msg.media('Que maravilha, fico muito feliz! Digite "Menu" pra eu poder te ajudar, amiga!')
        responded = False

    if 'menu' in incoming_msg:
        msg.media('Opções:\n1. Quero registrar um novo local de vulnerabilidade\n2. Quero saber se minha rota está tranquila\n3. Quero saber qual o melhor horário para passar pela minha rota')
        responded = False

    if not responded:
        msg.body('Desculpe, não entendi!')

    return str(resp)

if __name__ == '__main__':
   app.run()