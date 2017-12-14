 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from multiprocessing import Process
from time import sleep
import paho.mqtt.client as mqtt
import argparse
from flask import Flask, render_template, request, redirect
import sqlite3
from model import *
from extras import *

global client

db = sqlite3.connect('devices.db')

app = Flask(__name__)


@app.route('/index',methods=["POST", "GET"])
def index():
	return render_template('index.html',name=None)

@app.route('/ar',methods=["POST", "GET"])
def ar_crud():
	global client

	db = sqlite3.connect('devices.db')
	c = db.cursor() 
	items = c.execute('''SELECT device_id, temperatura FROM ArCondicionado''').fetchall()

	if request.method == "POST":
		
		if request.form['comando_ar'] == 'EnviarComando':
			
			device_id = request.form['id']
			string = "commands/air_conditioner/" + str(device_id)
			print ("DEBUGGG " + string)
			client.publish("commands/air_conditioner/" + str(device_id), str(request.form['comando']))
			return redirect('ar')

	db.close()
	return render_template('ar.html',name=None, items=items)


@app.route('/termometro',methods=["POST", "GET"])
def termometro_crud():
	global client

	db = sqlite3.connect('devices.db')
	c = db.cursor() 
	items = c.execute('''SELECT device_id, temperatura FROM Termometro''').fetchall()

	if request.method == "POST":
		
		if request.form['comando_termometro'] == 'EnviarComando':
			
			device_id = request.form['id']
			string = "commands/air_conditioner/" + str(device_id)
			print ("DEBUGGG " + string)
			client.publish("devices/termometer/" + str(device_id), str(request.form['comando']))
			return redirect('termometro')

	db.close()
	return render_template('termometro.html',name=None, items=items)

	

@app.route('/lampada',methods=["POST", "GET"])
def lampada_crud():
	global client

	db = sqlite3.connect('devices.db')
	c = db.cursor() 
	items = c.execute('''SELECT device_id, status FROM Lampada''').fetchall()

	if request.method == "POST":
		
		if request.form['comando_lampada'] == 'EnviarComando':
			
			device_id = request.form['id']
			string = "commands/air_conditioner/" + str(device_id)
			print ("DEBUGGG " + string)
			client.publish("devices/smart_lamp/" + str(device_id), str(request.form['comando']))
			return redirect('lampada')

	db.close()
	return render_template('lampada.html',name=None, items=items)

@app.route('/fechadura',methods=["POST", "GET"])
def fechadura_crud():
	global client

	db = sqlite3.connect('devices.db')
	c = db.cursor() 
	items = c.execute('''SELECT device_id, status FROM Fechadura''').fetchall()

	if request.method == "POST":
		
		if request.form['comando_fechadura'] == 'EnviarComando':
			
			device_id = request.form['id']
			string = "commands/air_conditioner/" + str(device_id)
			print ("DEBUGGG " + string)
			client.publish("commands/smart_lock/" + str(device_id), str(request.form['comando']))
			return redirect('fechadura')

	db.close()
	return render_template('fechadura.html',name=None, items=items)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("#")

def on_disconnect(client, userdata, rc):
	print("disconnected")

def atualizar_banco(msg):
	db = sqlite3.connect('devices.db')
	cursor = db.cursor()
	device = ''
	#ar condicionado
	if '::' in msg:
		decode = msg.split('::')
		device_id = int(decode[0])
		temperatura = str(decode[1])
		try:
			cursor.execute('''INSERT INTO ArCondicionado(device_id, temperatura) VALUES (?,?)''',(device_id,temperatura))

		except Exception as e:
			cursor.execute('''UPDATE ArCondicionado SET temperatura = ? WHERE device_id = ?''',(temperatura, device_id) )
	#lampada
	if '=' in msg:
		decode = msg.split('=')
		device_id = int(decode[0])
		device_status = str(decode[1])
		try:
			cursor.execute('''INSERT INTO Lampada(device_id, status) VALUES (?,?)''',(device_id,device_status))
		except Exception as e:
			cursor.execute('''UPDATE Lampada SET status = ? WHERE device_id = ?''',(device_status, device_id) )

	#fechadura
	if ';' in msg:
		decode = msg.split(';')
		device_id = int(decode[0])
		device_status = str(decode[1])
		try:
			cursor.execute('INSERT INTO Fechadura(device_id, status) VALUES(?,?)',(device_id,device_status))
		except Exception as e:
			cursor.execute('''UPDATE Fechadura SET status = ? WHERE device_id = ?''',(device_status, device_id) )

	#termometro
	if '>' in msg:
		print ("DEBUG")
		decode = msg.split('>')
		device_id = int(decode[0])
		temperatura = str(decode[1])
		try:
			cursor.execute('''INSERT INTO Termometro(device_id, temperatura) VALUES (?,?)''',(device_id,temperatura))
		except:
			cursor.execute('''UPDATE Termometro SET temperatura = ? WHERE device_id = ?''',(temperatura, device_id) )
	db.commit()

def on_message(client, userdata, msg):
	mensagem = msg.payload.decode()
	#print(mensagem)
	atualizar_banco(mensagem)

if __name__ == '__main__':

	global client

	client = mqtt.Client()
	try:
		db = sqlite3.connect('devices.db')

		cursor = db.cursor()
		cursor.execute('''CREATE TABLE IF NOT EXISTS ArCondicionado(device_id INTEGER PRIMARY KEY, temperatura TEXT)''')
		cursor.execute('''CREATE TABLE IF NOT EXISTS Termometro(device_id INTEGER PRIMARY KEY, temperatura TEXT)''')
		cursor.execute('''CREATE TABLE IF NOT EXISTS Fechadura(device_id INTEGER PRIMARY KEY, status TEXT)''')
		cursor.execute('''CREATE TABLE IF NOT EXISTS Lampada(device_id INTEGER PRIMARY KEY, status TEXT)''')
		db.commit()
		
	except Exception as e:
	 	print("Problema na criação das tabelas.")
	 	exit(1)

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.on_disconnect = on_disconnect
	client.connect("10.10.0.1", 1883, 60)
	client.loop_start()

	app.run(debug=True, host='172.20.4.82',port=1883)










