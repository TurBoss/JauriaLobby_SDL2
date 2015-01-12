#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import time
import socket
import traceback

from threading import Timer
from threading import Thread
from utilities import *
from clientobjects import (User, Channel, ChannelList,
			Motd, ServerEvents, Flags)



class Client:
	"""main client object"""
	def __init__(self):
		self.events = ServerEvents()
		self.channels = ChannelList()
		self.flags = Flags()
		
		self.updateThread = Thread(target=self.monitor)
		self.updateThread.daemon = True	
		
		self.server =  "lobby.springrts.com"#"192.168.8.107" #"lobby.springrts.com"
		self.port = "8200"
		
		self.connected = False
		self.username = ""
		self.password = ""
		self.password2 = ""
		self.cpu = 1
		self.lanip = ""
		self.client = ""
		self.chatinput= ""
		self.users = dict()
		
	
	def login(self):
		connected = self.connect(self.server, self.port)
		if connected:
			print("login")
			
			phash = hash_password(self.password)
			msg = ("LOGIN %s %s %i %s %s\t0\t%s\n" %
								(self.username, phash.decode('utf-8'), self.cpu, self.lanip, self.client, "a sp"))
			
			try:
				self.socket.sendall(msg.encode('utf-8'))
				self.receive()
				if self.connected:
					
					self.updateThread.start()
					return "OK"
				else:
					return "INVALIDUSERNAME"
			
			except Exception as e:
				print("Cannot send login command")
				print(e)
				return "SERVERDOWN"
			#self.channels = ChannelList()
			#print(self.receive())
		else:
			return "SERVERDOWN"
	
	def register(self):
		connected = self.connect(self.server, self.port)
		if connected:
			print("register")
			phash = hash_password(self.password)
			try:
				print("Trying to register account")
				msg = ("REGISTER %s %s\n" % (self.username, phash.decode('utf-8')))
				print(msg)
				self.socket.sendall(msg.encode('utf-8'))
				resp = self.socket.recv(1024)
				print(resp)
				if b'REGISTRATIONDENIED' in resp:
					return "REGISTRATIONDENIED"
				elif b'REGISTRATIONACCEPTED' in resp:
					return "REGISTRATIONACCEPTED"
			except Exception as e:
				print("Cannot send register command")
				print(e)
				return "SERVERDOWN"
		else:
			return "SERVERDOWN"
	
	def disconnect(self):
		msg = ("EXIT %s\n" % ("leave"))
		print("disconnect")
	
	def join(self):
		print("join")
	
	def leave(self):
		print("leave")
	
	def connect(self, server, port):
		port = int(port)
		print("connecting")
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.settimeout(40)
			self.socket.connect((server, port))
			resp = self.socket.recv(1024)
			print(resp)
			self.connected = True
			return True
		except SystemExit:
			raise SystemExit(0)
		except Exception as e:
			self.connected = False
			print("Cannot connect, retrying in 40 secs...")
			print(e)
			return False
			time.sleep(40.0)
	
	def parsecommand(self, command, args):
		if command.strip() != "":
			self.events.oncommandfromserver(command, args, self.socket)
			if command == "JOIN" and len(args) >= 1:
				if not args[0] in self.channels:
					self.channels.add(args[0])
					Log.good("Joined #%s" % args[0])
			elif command == "FORCELEAVECHANNEL" and len(args) >= 2:
				if args[0] in self.channels:
					self.channels.remove(args[0])
					Log.bad("I've been kicked from #%s by <%s>" % (args[0], args[1]))
				else:
					Log.error("I've been kicked from a channel that i haven't joined")
			elif command == "TASSERVER":
				Log.good("Connected to server")
				if self.flags.register:
					self.register(self.uname, self.password)
					self.receive()
				else:
					self.events.onconnected()
			elif command == 'LEFT':
				chan = args[0]
				nick = args[1]
				self.channels[chan].del_user(self.users[nick])
			elif command == 'JOINED':
				chan = args[0]
				nick = args[1]
				self.channels[chan].add_user(self.users[nick])
			elif command == 'CLIENTS':
				chan = args[0]
				for nick in args[1:]:
					self.channels[chan].add_user(self.users[nick])
			elif command == "AGREEMENTEND":
				Log.notice("accepting agreement")
				self.socket.send("CONFIRMAGREEMENT\n")
				self.login(self.uname, self.password, "BOT", 2000)
				self.events.onloggedin(self.socket)
			elif command == "MOTD":
				self.events.onmotd(" ".join(args))
			elif command == "ACCEPTED":
				self.connected = True
			elif command == "DENIED" and ' '.join(args).lower().count("already") == 0:
				print("Login failed ( %s ), trying to register..." % ' '.join(args))
				print("Closing Connection")
				self.socket.close()
				self.flags.register = True
				self.connect(self.lastserver, self.lastport)
			elif command == "REGISTRATIONACCEPTED":
				print("Registered")
				print("Closing Connection")
				self.socket.close()
				self.flags.register = False
				self.connect(self.lastserver, self.lastport)
			elif command == "PONG":
				print("PONG")
				self.lpo = time.time()
				self.events.onpong()
			elif command == "JOINEDBATTLE" and len(args) >= 2:
				try:
					self.users[args[1]].battleid = int(args[0])
				except Exception:
					print("Invalid JOINEDBATTLE Command from server: %s %s" %
								(command, str(args)))
					print(traceback.format_exc())
			elif command == "BATTLEOPENED" and len(args) >= 4:
				self.users[args[3]].battleid = int(args[0])
				try:
					self.users[args[3]].battleid = int(args[0])
				except Exception:
					print("Invalid BATTLEOPENED Command from server: %s %s" %
								(command, str(args)))
					print(traceback.format_exc())
			elif command == "LEFTBATTLE" and len(args) >= 2:
				try:
					self.users[args[1]].battleid = -1
				except Exception:
					print("Invalid LEFTBATTLE Command from server: %s %s" %
								(command, str(args)))
					print(traceback.format_exc())
			elif command == "SAIDPRIVATE" and len(args) >= 2:
				self.events.onsaidprivate(args[0], ' '.join(args[1:]))
			elif command == "ADDUSER":
				try:
					if len(args) == 4:
						#Account id
						self.users[args[0]] = User(args[0], int(args[3]), args[1], int(args[2]))
					elif len(args) == 3:
						self.users[args[0]] = User(args[0], int(-1), args[1], int(args[2]))
					else:
						print("Invalid ADDUSER Command from server: %s %s" %
								(command, str(args)))
				except Exception as e:
					print("Invalid ADDUSER Command from server: %s %s" %
								(command, str(args)))
					print(e)
			elif command == "REMOVEUSER":
				if len(args) == 1:
					if args[0] in self.users:
						self.channels.clear_user(self.users[args[0]])
						del self.users[args[0]]
					else:
						print("Invalid REMOVEUSER Command: no such user %s" % args[0])
				else:
						Log.error("Invalid REMOVEUSER Command: not enough arguments")
			elif command == "CLIENTSTATUS":
				if len(args) == 2:
					if args[0] in self.users:
						try:
							self.users[args[0]].clientstatus(int(args[1]))
						except Exception:
							print("Malformed CLIENTSTATUS")
							print(traceback.format_exc())
					else:
						print("Invalid CLIENTSTATUS: No such user <%s>" % args[0])
	
	def start_timer(self):
		Timer(60, self.ping_server, ()).start()
		
	def monitor(self):
		self.start_timer()
		
		while(True):
			self.receive()
	
	def ping_server(self):
		print("PING")
		self.start_timer()
		msg = ("PING")
		self.socket.sendall(msg.encode('utf-8'))
		self.receive()
	
	def receive(self):
		"""return commandname & args"""
		if not self.socket:
			return 1
		buf = ""
		try:
			while not buf.strip("\r ").endswith("\n"):
				print ("Receiving incomplete command...")
				nbuf = self.socket.recv(512)
				print(nbuf)
				if nbuf == "":
					return 1
				buf += nbuf.decode("utf-8")
		except Exception as e:
			#Connection broken
			print(e)
			return 1
		commands = buf.strip("\r ").split("\n")
		for cmd in commands:
			c = cmd.split(" ")[0].upper()
			args = cmd.split(" ")[1:]
			print(c)
			print(args)
			#print(args)
			self.parsecommand(c, args)
		return 0
