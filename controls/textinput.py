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

class TextInput:
	"""Text Input"""
	def __init__(self, renderer, resources, textinputid, label, posx, posy, textmsg=""):
		
		self.renderer = renderer
		self.resources = resources
		
		self.textinputid = textinputid
		
		self.label = label
		self.textmsg = textmsg
		self.posx = posx
		self.posy = posy
				
		self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
		self.ManagerFont = sdl2.ext.FontManager(self.resources.get_path("tuffy.ttf"), size = 14)
		self.uifactory = sdl2.ext.UIFactory(self.factory)
		
		
		
		if self.textmsg == "":
			self.text = self.factory.from_text(" ",
										fontmanager=self.ManagerFont)
		else:
			self.text = self.factory.from_text(self.textmsg,
										fontmanager=self.ManagerFont)
										
		self.textlabel = self.factory.from_text(self.label,
									fontmanager=self.ManagerFont)
									
		self.textinput = self.uifactory.from_image(sdl2.ext.TEXTENTRY,
									self.resources.get_path("textinput.png"))
		
		self.textinput.input 			+= self.inputtext
		self.textinput.pressed			+= self.inputtext
		
		self.textlabel.position			= self.posx+5, self.posy-20
		self.text.position 				= self.posx+5, self.posy+15
		self.textinput.position			= self.posx, self.posy
		
		
	def inputtext(self, entry, event):
		
		if event.type == 771:
			char = event.text.text
			self.textmsg += char.decode("utf-8")
			
	def getevents(self, event):

		if event.type == sdl2.SDL_KEYDOWN:
			key = sdl2.SDL_GetKeyName(event.key.keysym.sym).lower()
			if key == b'backspace':
				self. delval()
		return self.textinput
		
	def updatetext(self):
	
		if self.textmsg == "":
			self.text = self.factory.from_text(" ",
							fontmanager=self.ManagerFont)
		else:
			self.text = self.factory.from_text(self.textmsg,
							fontmanager=self.ManagerFont)
		self.text.position = self.posx+5, self.posy+15
	
	def drawlabel(self):
		return self.textlabel
		
	def drawbox(self):
		return self.textinput
		
	def drawtext(self):
		self.updatetext()
		return self.text
	
	def delval(self):
		self.textmsg = self.textmsg[:-1]
		
	def gettext(self):
		return self.textmsg
