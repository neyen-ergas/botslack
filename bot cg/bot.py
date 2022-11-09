from cmath import log
from concurrent.futures import thread
from json import load
from lib2to3.pgen2 import token
from operator import contains
from ssl import CHANNEL_BINDING_TYPES
from turtle import dot
import slack
import os
from pathlib import  Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from collections import Counter
import json
import datetime
from datetime import datetime
from threading import Timer


env_path = Path('.')/ '.env'
load_dotenv(dotenv_path=env_path)
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

client= slack.WebClient(token=os.environ['SLACK_TOKEN'])

pedidos=[]
pedidosformato=[]
pedidosUser=[]
pdia=[]

carta=["*------------------------------------------------------------------------------Carta:male-cook:------------------------------------------------------------------------------*",":fork_and_knife: _*Ingredientes especiales: pollo, aceitunas, tomates secos, champiñones, jamón cocido, huevo duro, queso*_",":fork_and_knife: _*Las ensaladas de guarnición pueden ser de hasta tres ingredientes: lechuga, tomate, semillas, zanahoria, cebolla, rúcula, choclo, repollo, pepino,huevo duro*_",":hamburger:_Hamburguesa casera completa (jamón, queso, tomate y cebolla morada) con papas_",":sandwich:_Sandwich de pollo completo (queso, tomate y rúcula)_",":sandwich:_Sandwich de milanesa (de carne ó de pollo) completo (jamón, queso, tomate y lechuga_",":sandwich:_Sandwich de bondiola completo (jamón, queso, tomate y lechuga)_",":sandwich:_Sandwich vegetariano (provoleta, rúcula, tomate, cebolla morada y hongos)_",":sandwich:_Sandwich de jamón crudo (queso, tomate y verdes)_",":cut_of_meat:_Milanesa (de carne ó de pollo) con papas fritas, arroz ó ensalada_",":cut_of_meat:_Milanesa (de carne ó de pollo) a la napolitana con papas fritas, arroz ó ensalada_ ",":cut_of_meat: _Bife de chorizo con arroz, papas fritas o ensalada_ ",":poultry_leg: _Pollo grille con ensalada, arroz o papas fritas_", 
":shallow_pan_of_food: _Salteado de vegetales (podes agregarle arroz o fideos)_",":shallow_pan_of_food: _Salteado de vegetales con pollo, carne o cerdo (podes agregarle arroz o fideos)_",":green_salad: _Ensalada hasta 5 ingredientes (lechuga, tomate, semillas, zanahoria, cebolla, rúcula, croutons, repollo, arroz, pepino, brotes de soja)_",":green_salad: _Ensalada hasta 7 ingredientes (los mencionados anteriormente, mas 2 ingredientes especiales)_",":green_salad: _Ensalada Caesar_ ","*------------------------------------------------------------------------------Platos del dia:knife_fork_plate:------------------------------------------------------------------------------*"]
comandos=["_*! carta* para ver la carta_","_*! platodia* para agrega platos del dia_","_*! quiero* para hacer un pedido_","_*! pedido* para ver lo pedido hasta el momento_","_*! borrarPedidos* para borrar los pedidos_","_*! borrarPdia* para borrar los platos del dia_"]      

@ slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    name_user = event.get('users_profile_get')
    text = event.get('text')
    ts= event.get('ts')

    
    
    #Borrar lista de pedidos        
    if text.lower() == "!borrarPedidos" :
        pedidos.clear()

    #Borrar platos del dia
    if text.lower() == "!borrarPdia" :
        pdia.clear()       
    

    
    

    #Cargar platos del dia
    if "!platodia" in text.lower():
        pdia.append(":knife_fork_plate:"+""+text[9:])
    
    #Realizar pedido
    if "!quiero" in text.lower()[:7]:
        pedidos.append(text[7:])
        pedidosUser.append(text[7:]+str(name_user))
        print(name_user)
        client.chat_postMessage(channel=channel_id,thread_ts=ts,text="Anotado :white_check_mark:")
    
    #Mostrar carta 
    if text.lower() == "!carta":
        cartamsg = '\n'.join(carta)
        pdiamsg= '\n'.join(pdia) 
        client.chat_postMessage(channel=channel_id,text=cartamsg)
        client.chat_postMessage(channel=channel_id,text=pdiamsg)  
    
    #Mostrar pedido
    if text.lower() == "!pedido":
        for comida, numero in Counter(pedidos).most_common():
            pedidosformato.append(str(numero)+""+comida)
        msgpedidos = '\n'.join(pedidosformato)
        client.chat_postMessage(channel=channel_id,text=msgpedidos)
                        
    #Mostrar carta 
    if text.lower() == "!comandos":
        msgcomandos = '\n'.join(comandos)
        client.chat_postMessage(channel=channel_id,text=msgcomandos)

    #Creador
    if text.lower() == "!creador":
        client.chat_postMessage(channel=channel_id,text="Mi creador es Neyen Ergas :)")  

     
    #Borrarpedido                   
    if text.lower() == "!borrarmipedido":
        for pu in pedidosUser:
            if user_id == pu[:user_id.len()]:
                pedidos.drop(pu[pu])

    #Mostrar pedido con usuarios
    if text.lower() == "!pedidouser":
        pedidomsg= '\n'.join(pedidosUser)   
        client.chat_postMessage(channel=channel_id,text=pedidomsg)   
    
    

    

            
 

if __name__ == "__main__":
    app.run(debug=True)

