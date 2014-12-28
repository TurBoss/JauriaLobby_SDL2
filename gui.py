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
		
		self.spriterenderer = self.factory.create_sprite_render_system(self.window)
		
		self.background = self.factory.from_image(self.resources.get_path("background.png"))
		
		
		self.auxwindow = self.factory.from_image(self.resources.get_path("auxwin.png"))
		self.chatoutput = self.factory.from_image(self.resources.get_path("chatoutput.png"))
		
		self.tagusername = self.factory.from_text("Username",
									fontmanager=self.ManagerFont)
		self.tagpassword = self.factory.from_text("Password",
									fontmanager=self.ManagerFont)
		self.textentryusername = self.factory.from_text(" ",
									fontmanager=self.ManagerFont)
		self.textentrypassword = self.factory.from_text(" ",
									fontmanager=self.ManagerFont)
		self.textentrypassword2 = self.factory.from_text(" ",
									fontmanager=self.ManagerFont)
		self.emptyuserpass = self.factory.from_text("Empty username or password",
									fontmanager=self.ManagerFont)
		self.registrationdenied = self.factory.from_text("Username already exists",
									fontmanager=self.ManagerFont)
		self.registrationaccepted = self.factory.from_text("Registration Succesful",
									fontmanager=self.ManagerFont)
		self.serverdown = self.factory.from_text("Server Down",
									fontmanager=self.ManagerFont)
		self.invalidpassword = self.factory.from_text("Invalid username or password",
									fontmanager=self.ManagerFont)
		self.textentrychat= self.factory.from_text(" ",
									fontmanager=self.ManagerFont)
		self.chatout = self.factory.from_text(" ",
									fontmanager=self.ManagerFont)

		self.buttonconnect = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("connect.png"))
		self.buttonexit = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("exit.png"))
		self.buttonback = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("back.png"))
		self.buttonlogin = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("button.png"))
		self.buttonreg = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("register.png"))
		
		self.textinputusername = self.uifactory.from_image(sdl2.ext.TEXTENTRY,
									self.resources.get_path("textinput.png"))
		self.textinputpassword = self.uifactory.from_image(sdl2.ext.TEXTENTRY,
									self.resources.get_path("textinput.png"))
		self.textinputpassword2 = self.uifactory.from_image(sdl2.ext.TEXTENTRY,
									self.resources.get_path("textinput.png"))
		self.textinputchat = self.uifactory.from_image(sdl2.ext.TEXTENTRY,
									self.resources.get_path("chatinput.png"))
		
		
		# Button Events
		self.buttonconnect.click += self.onclickconnect
		self.buttonexit.click += self.onclickexit
		self.buttonback.click += self.onclickback
		self.buttonlogin.click += self.onclicklogin
		self.buttonreg.click += self.onclickreg
		
		# Button positions
		self.buttonconnect.position = 450, 500
		self.buttonexit.position = 450, 560
		
		self.buttonlogin.position = 450, 440
		self.buttonreg.position = 450, 500
		self.buttonback.position = 450, 560
		
		# Textinput Events
		self.textinputusername.input += self.inputusername
		self.textinputpassword.input += self.inputpassword
		self.textinputpassword2.input += self.inputpassword2
		self.textinputchat.input += self.inputchat
		
		self.textinputusername.pressed += self.inputusername
		self.textinputpassword.pressed += self.inputpassword
		self.textinputpassword2.pressed += self.inputpassword2
		self.textinputchat.pressed += self.inputchat
		
		# Textinput position
		self.textinputusername.position = 450, 260
		self.textinputpassword.position = 450, 330
		self.textinputpassword2.position = 450, 400
		self.textinputchat.position = 400, 400
		
		# Text posiotion
		self.tagusername.position = 450, 240
		self.tagpassword.position = 450, 310
		self.emptyuserpass.position = 400, 300
		self.registrationdenied.position = 400,300
		self.serverdown.position = 400, 300
		self.invalidpassword.position = 400, 300
		
		# Window position
		self.auxwindow.position = 400, 300
		self.chatoutput.position = 200, 100
		
		
		self.spriterenderer.render((self.background))
		
		self.uiprocessor = sdl2.ext.UIProcessor()
		
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
					self.uiprocessor.dispatch([self.buttonconnect, self.buttonexit], event)
				self.spriterenderer.render((self.background, self.buttonconnect, self.buttonexit))

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
						if key == b'backspace':
							self.delval()
							break
					self.uiprocessor.dispatch([self.textinputusername,
							self.textinputpassword, self.buttonlogin,
							self.buttonreg, self.buttonback], event)
				
					if self.client.username != "":
						self.textentryusername = self.factory.from_text(self.client.username, fontmanager=self.ManagerFont)
						self.textentryusername.position = 460,275
					elif self.client.username == "":
						self.textentryusername = self.factory.from_text(" ", fontmanager=self.ManagerFont)
						self.textentryusername.position = 460,275
						
					if self.client.password != "":
						self.textentrypassword = self.factory.from_text(self.client.password, fontmanager=self.ManagerFont)
						self.textentrypassword.position = 460,345
					elif self.client.password == "":
						self.textentrypassword = self.factory.from_text(" ", fontmanager=self.ManagerFont)
						self.textentrypassword.position = 460,345
						
						
						
				self.spriterenderer.render((self.background, self.tagusername,
						self.tagpassword, self.textinputusername,
						self.textinputpassword, self.textentryusername,
						self.textentrypassword, self.buttonlogin,
						self.buttonreg, self.buttonback))
			
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
						if key == b'backspace':
							self.delval()
							break
					self.uiprocessor.dispatch([self.textinputusername,
							self.textinputpassword, self.textinputpassword2,
							self.buttonreg, self.buttonback], event)
				
					if self.client.username != "":
						self.textentryusername = self.factory.from_text(self.client.username, fontmanager=self.ManagerFont)
						self.textentryusername.position = 460,275
					elif self.client.username == "":
						self.textentryusername = self.factory.from_text(" ", fontmanager=self.ManagerFont)
						self.textentryusername.position = 460,275
						
					if self.client.password != "":
						self.textentrypassword = self.factory.from_text(self.client.password, fontmanager=self.ManagerFont)
						self.textentrypassword.position = 460,345
					elif self.client.password == "":
						self.textentrypassword = self.factory.from_text(" ", fontmanager=self.ManagerFont)
						self.textentrypassword.position = 460,345
						
					if self.client.password2 != "":
						self.textentrypassword2 = self.factory.from_text(self.client.password2, fontmanager=self.ManagerFont)
						self.textentrypassword2.position = 460,415
					elif self.client.password2 == "":
						self.textentrypassword2 = self.factory.from_text(" ", fontmanager=self.ManagerFont)
						self.textentrypassword2.position = 460,415
						
						
						
						
				self.spriterenderer.render((self.background,
						self.tagusername, self.tagpassword,
						self.textinputusername, self.textinputpassword,
						self.textinputpassword2, self.textentryusername,
						self.textentrypassword, self.textentrypassword2,
						self.buttonreg, self.buttonback))
						
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
						if key == b'backspace':
							self.delval()
							break
						if key == b'return':
							self.chatsend()
							break
							
					self.uiprocessor.dispatch([self.buttonback, self.textinputchat], event)
					
					
					if self.client.chatinput != "":
						self.textentrychat = self.factory.from_text(self.client.chatinput, fontmanager=self.ManagerFont)
						self.textentrychat.position = 410,410
					elif self.client.chatinput == "":
						self.textentrychat = self.factory.from_text(" ", fontmanager=self.ManagerFont)
						self.textentrychat.position = 410,410
						
				self.spriterenderer.render((self.background,self.chatoutput,
						self.buttonback, self.textinputchat, self.textentrychat))
			sdl2.SDL_Delay(1)

	def onclickconnect(self, button, event,):
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
				self.spriterenderer.render((self.auxwindow, self.serverdown))
				sdl2.SDL_Delay(2000)
			elif "INVALIDUSERNAME" in login:
				self.spriterenderer.render((self.auxwindow, self.invalidpassword))
				sdl2.SDL_Delay(2000)
			else:
				self.page=3
		else:
			print("empty username or password")
			self.spriterenderer.render((self.auxwindow, self.emptyuserpass))
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
	
	def inputusername(self, entry, event):
		if event.type == 771:
			char = event.text.text
			self.client.username += char.decode("utf-8")
		self.textinputindex = 1
		
	def inputpassword(self, entry, event):
		if event.type == 771:
			char = event.text.text
			self.client.password += char.decode("utf-8")
		self.textinputindex = 2
		
	def inputpassword2(self, entry, event):
		if event.type == 771:
			char = event.text.text
			self.client.password2 += char.decode("utf-8")
		self.textinputindex = 3
		
	def inputchat(self, entry, event):
		if event.type == 771:
			char = event.text.text
			self.client.chatinput += char.decode("utf-8")
		self.textinputindex = 4
		
	def chatsend(self):
		if self.textinputindex == 4:
			print("RETURN")
			self.client.chatinput = ""
			self.textentrychat = self.factory.from_text(" ", fontmanager=self.ManagerFont)
			self.textentrychat.position = 410,410
