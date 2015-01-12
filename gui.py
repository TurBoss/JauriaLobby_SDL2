#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import time

if os.name == "nt":
	if getattr(sys, 'frozen', False):
		# frozen
		sdlpath = 'libs'
	else:
		# unfrozen
		sdlpath = os.path.join(os.path.dirname(__file__), 'libs')
		
	os.environ['PYSDL2_DLL_PATH'] = sdlpath

import sdl2
import sdl2.ext
from sdl2.sdlttf import TTF_OpenFont, TTF_RenderText_Solid

from client import Client

from controls.text		import Text
from controls.textinput	import TextInput
from controls.button 	import Button
from controls.checkbox 	import CheckBox
from controls.radio 	import Radio
from controls.popup 	import PopUp

class Gui:
	"""lobby gui"""
	def __init__(self):
		
		self.client = Client()
		
		self.page = 0
		self.lastpage = 0
		self.textinputindex = 0
		self.running = 1
		
		
		if getattr(sys, 'frozen', False):
			# frozen
			self.resources = sdl2.ext.Resources(sys.executable, "resources")
		else:
			# unfrozen
			self.resources = sdl2.ext.Resources(__file__, "resources")
		
		sdl2.ext.init()
		self.screenX = 1024
		self.screenZ = 768
		
		self.window = sdl2.ext.Window("Jauria Lobby", size=(self.screenX, self.screenZ),flags = sdl2.SDL_WINDOW_BORDERLESS)
		self.window.show()
		
		self.renderer = sdl2.ext.Renderer(self.window)
		
		self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
		self.ManagerFont = sdl2.ext.FontManager(self.resources.get_path("tuffy.ttf"), size = 14)
		self.uifactory = sdl2.ext.UIFactory(self.factory)
		self.uiprocessor = sdl2.ext.UIProcessor()
		
		self.spriterenderer = self.factory.create_sprite_render_system(self.window)
		
		self.background = self.factory.from_image(self.resources.get_path("background.png"))
		
		# =============================================================================
		
		self.textwelcome 		= Text(			self.renderer, self.resources, "welcome0", "JauriaRts", 450, 80, 30)
		
		self.checkbox1 			= CheckBox(		self.renderer, self.resources, "checkbox0", "checkbox0", 450, 120, 0)
		self.checkbox2 			= CheckBox(		self.renderer, self.resources, "checkbox1", "checkbox1", 450, 150, 1)
		
		self.radio1 			= Radio(		self.renderer, self.resources, "radio0", "checkbox0", 450, 180, 1)
		self.radio2 			= Radio(		self.renderer, self.resources, "radio1", "checkbox1", 450, 210, 0)
		
		self.textinputserver 	= TextInput(	self.renderer, self.resources, "server0", "Server", 450, 190, self.client.server)
		self.textinputusername 	= TextInput(	self.renderer, self.resources, "username0", "Usename", 450, 260)
		self.textinputpassword	= TextInput(	self.renderer, self.resources, "password0", "Password", 450, 330)
		self.textinputpassword2	= TextInput(	self.renderer, self.resources, "password1", "Password", 450, 400)
		self.textinputchat		= TextInput(	self.renderer, self.resources, "chat0", "Chat", 450, 450)
		
		self.buttonconnect		= Button(		self.renderer, self.resources, "connect0", "Conect", 450, 500, self.onclickconnect)
		self.buttonexit			= Button(		self.renderer, self.resources, "exit0", "Exit", 450, 560, self.onclickexit)
		
		self.buttonlogin		= Button(		self.renderer, self.resources, "login0", "Login", 450, 440, self.onclicklogin)
		self.buttonregister		= Button(		self.renderer, self.resources, "register0", "Register", 450, 500, self.onclickreg)
		self.buttonback			= Button(		self.renderer, self.resources, "back0", "Back", 450, 560, self.onclickback)
		
		self.serverdown_popup	= PopUp(		self.renderer, self.resources, "popup0", "Server Down", "Connection to server Timeout", 300,110)
		self.denied_popup		= PopUp(		self.renderer, self.resources, "popup1", "Denied", "Invalid Username or password", 300,110)
		self.empty_popup		= PopUp(		self.renderer, self.resources, "popup2", "Empty", "Missing Username or password", 300,110)

		# =============================================================================
		
		
		self.registrationdenied = self.factory.from_text("Username already exists",
									fontmanager=self.ManagerFont)
		self.registrationaccepted = self.factory.from_text("Registration Succesful",
									fontmanager=self.ManagerFont)
		self.serverdown = self.factory.from_text("Server Down",
									fontmanager=self.ManagerFont)
		self.invalidpassword = self.factory.from_text("Invalid username or password",
									fontmanager=self.ManagerFont)
		
		
		
		self.spriterenderer.render((self.background))
		
		
		self.start = sdl2.SDL_GetTicks()
	
	def run(self):
		while self.running:
			#print(self.page)
			if self.page == 0:
				""" Main Page """
				
				events = sdl2.ext.get_events()
				for event in events:
					if event.type == sdl2.SDL_QUIT:
						self.running = 0
						break
					elif event.type == sdl2.SDL_KEYDOWN:
						key = sdl2.SDL_GetKeyName(event.key.keysym.sym).lower()
						if key == b'escape':
							self.running = 0
							break
					
					self.uiprocessor.dispatch([
									self.checkbox1.getevents(event),
									self.checkbox2.getevents(event),
									
									self.radio1.getevents(event),
									self.radio2.getevents(event),
									
									self.buttonconnect.getevents(event),
									self.buttonexit.getevents(event)
									], event)
				
				self.spriterenderer.render((
								self.background,
								
								self.textwelcome.drawlabel(),
								
								self.checkbox1.drawlabel(),
								self.checkbox1.drawbox(),
								
								self.checkbox2.drawlabel(),
								self.checkbox2.drawbox(),
								
								self.radio1.drawlabel(),
								self.radio1.drawbox(),
								
								self.radio2.drawlabel(),
								self.radio2.drawbox(),
								
								self.buttonconnect.drawbox(),
								self.buttonconnect.drawlabel(),
								
								self.buttonexit.drawbox(),
								self.buttonexit.drawlabel()
								))
				
				
			if self.page == 1:
				""" Login Page """
				
				events = sdl2.ext.get_events()
				for event in events:
					if event.type == sdl2.SDL_QUIT:
						self.running = 0
						break
					elif event.type == sdl2.SDL_KEYDOWN:
						key = sdl2.SDL_GetKeyName(event.key.keysym.sym).lower()
						if key == b'escape':
							self.page= 0
							break
					self.uiprocessor.dispatch([
									self.textinputserver.getevents(event),
									self.textinputusername.getevents(event),
									self.textinputpassword.getevents(event),
									
									self.buttonlogin.getevents(event),
									self.buttonregister.getevents(event),
									self.buttonback.getevents(event)
									], event)
				
				self.spriterenderer.render((
								self.background,
								
								self.textinputserver.drawlabel(),
								self.textinputserver.drawbox(),
								self.textinputserver.drawtext(),
								
								self.textinputusername.drawlabel(),
								self.textinputusername.drawbox(),
								self.textinputusername.drawtext(),
								
								self.textinputpassword.drawlabel(),
								self.textinputpassword.drawbox(),
								self.textinputpassword.drawtext(),
								
								self.buttonlogin.drawbox(),
								self.buttonlogin.drawlabel(),
								
								self.buttonregister.drawbox(),
								self.buttonregister.drawlabel(),
								
								self.buttonback.drawbox(),
								self.buttonback.drawlabel(),
								))
				
				self.client.server = self.textinputserver.gettext()
				self.client.username = self.textinputusername.gettext()
				self.client.password = self.textinputpassword.gettext()
				self.client.server = self.textinputserver.gettext()
				
			if self.page == 2:
				""" Register Page """
				
				events = sdl2.ext.get_events()
				for event in events:
					if event.type == sdl2.SDL_QUIT:
						self.running = 0
						break
					elif event.type == sdl2.SDL_KEYDOWN:
						key = sdl2.SDL_GetKeyName(event.key.keysym.sym).lower()
						if key == b'escape':
							self.page= 1
							break
					self.uiprocessor.dispatch([
									self.textinputusername.getevents(event),
									self.textinputpassword.getevents(event),
									self.textinputpassword2.getevents(event),
									
									self.buttonregister.getevents(event),
									self.buttonback.getevents(event)
								], event)
				
				self.spriterenderer.render((
								self.background,
								
								self.textinputusername.drawlabel(),
								self.textinputusername.drawbox(),
								self.textinputusername.drawtext(),
								
								self.textinputpassword.drawlabel(),
								self.textinputpassword.drawbox(),
								self.textinputpassword.drawtext(),
								
								self.textinputpassword2.drawlabel(),
								self.textinputpassword2.drawbox(),
								self.textinputpassword2.drawtext(),
								
								self.buttonregister.drawbox(),
								self.buttonregister.drawlabel(),
								
								self.buttonback.drawbox(),
								self.buttonback.drawlabel(),
							))
				
				self.client.username = self.textinputusername.gettext()
				self.client.password = self.textinputpassword.gettext()
						
			if self.page == 3:
				""" Lobby Page """
				
				events = sdl2.ext.get_events()
				for event in events:
					if event.type == sdl2.SDL_QUIT:
						self.running = 0
						break
					elif event.type == sdl2.SDL_KEYDOWN:
						key = sdl2.SDL_GetKeyName(event.key.keysym.sym).lower()
						if key == b'escape':
							self.page = 1
							break
					
					self.uiprocessor.dispatch([
									self.buttonback.getevents(event),
									self.textinputchat.getevents(event)
									], event)
				
				self.spriterenderer.render((
								self.background,
								
								self.textinputchat.drawlabel(),
								self.textinputchat.drawbox(),
								self.textinputchat.drawtext(),
								
								self.buttonback.drawbox(),
								self.buttonback.drawlabel(),
								))
			
			sdl2.SDL_Delay(60)

	def onclickconnect(self, button, event):
		
		self.page = 1
	
	def onclickexit(self, button, event):
		
		self.running = 0
	
	def onclickback(self, button, event):
		
		if self.page == 1:
			self.page = 0
		if self.page == 2:
			self.page = 1
		if self.page == 3:
			self.client.disconnect()
			self.page = 1
	
	def onclicklogin(self, button, event):
		
		if (self.client.username != "" )| (self.client.username != ""):
			login = self.client.login()
			if "SERVERDOWN" in login:
				self.spriterenderer.render((	self.serverdown_popup.drawbox(),
												self.serverdown_popup.drawlabel(),
												self.serverdown_popup.drawmsg()
												))
				sdl2.SDL_Delay(2000)
			elif "INVALIDUSERNAME" in login:
				self.spriterenderer.render((	self.denied_popup.drawbox(),
												self.denied_popup.drawlabel(),
												self.denied_popup.drawmsg()
												))
				sdl2.SDL_Delay(2000)
			else:
				self.page=3
		else:
			print("empty username or password")
			self.spriterenderer.render((		self.empty_popup.drawbox(),
												self.empty_popup.drawlabel(),
												self.empty_popup.drawmsg()
												))
			sdl2.SDL_Delay(2000)
			
	def onclickreg(self, button, event):
		
		if self.page == 1 :
			self.page = 2
		else:
			if (self.client.username != "" ) | (self.client.username != "") | (self.client.password2 != ""):
				resp = self.client.register()
				if 'REGISTRATIONDENIED' in resp:
					print("username already exist")
					self.spriterenderer.render((self.auxwindow, self.registrationdenied))
					sdl2.SDL_Delay(2000)
				elif 'REGISTRATIONACCEPTED' in resp:
					print("Registration Succesfull")
					self.spriterenderer.render((self.auxwindow, self.registrationaccepted))
					sdl2.SDL_Delay(2000)
					self.page = 1
				elif 'SERVERDOWN' in resp:
					print("ServerDown")
					self.spriterenderer.render((self.auxwindow, self.serverdown))
					sdl2.SDL_Delay(2000)
			else:
				print("empty username or password")
				self.spriterenderer.render((self.auxwindow, self.emptyuserpass))
				sdl2.SDL_Delay(2000)
	
	def delval(self):
		
		if self.textinputindex == 1:
			self.client.username = self.client.username[:-1]
		elif self.textinputindex == 2:
			self.client.password = self.client.password[:-1]
		elif self.textinputindex == 3:
			self.client.password2 = self.client.password2[:-1]
		elif self.textinputindex == 4:
			self.client.chatinput = self.client.chatinput[:-1]
