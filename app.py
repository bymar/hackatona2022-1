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
        msg.body('''Oii! Eu sou a Lélia, pode me chamar de Lê. Posso te ajudar a encontrar as rodas para você se sentir mais segura. Além disso, pode contar comigo caso estiver em situação de risco.\n\nVocê está segura?\n\n1 - Perigo\n2 - Segura''')
        responded = True

    if 'perigo' in incoming_msg or '1' in incoming_msg:
        msg.media('1 - EMERGENCIA \n2 - Compartilhe sua localizacao com a gente que ficaremos de olho.')
        responded = True

    if 'segura' in incoming_msg or '2' in incoming_msg:
        msg.media('Que maravilha, fico muito feliz! Digite "Menu" pra eu poder te ajudar, amiga!')
        responded = True

    if 'menu' in incoming_msg:
        msg.media('Opções:\nA - Quero registrar um novo local de vulnerabilidade\nB - Quero saber se minha rota está tranquila\nC - Quero saber qual o melhor horário para passar pela minha rota')
        responded = True

    if 'a' in incoming_msg or 'b' in incoming_msg or 'c' in incoming_msg:
        msg.media('')
        responded = True

    if not responded:
        msg.body('Desculpe, não entendi!')

    return str(resp)

if __name__ == '__main__':
   app.run()