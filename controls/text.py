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

class Text:
	"""Text Input"""
	def __init__(self, renderer, resources, textid, label , posx, posy, size):
		
		self.renderer = renderer
		self.resources = resources
		
		self.textid = textid
		
		self.label = label
		self.posx = posx
		self.posy = posy
		self.size = size
		
		self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
		self.ManagerFont = sdl2.ext.FontManager(self.resources.get_path("tuffy.ttf"), size = self.size)
		self.uifactory = sdl2.ext.UIFactory(self.factory)
		
		self.textlabel = self.factory.from_text(self.label,
									fontmanager=self.ManagerFont)
				
		self.textlabel.position			= self.posx, self.posy
		
		
			
		
	def updatetext(self):
	
		if self.textmsg != "":
			self.text = self.factory.from_text(self.textmsg,
							fontmanager=self.ManagerFont)
		else:
			self.text = self.factory.from_text(" ",
							fontmanager=self.ManagerFont)
		self.text.position = self.posx+5, self.posy+15
	
	def drawlabel(self):
		return self.textlabel
		
		
	def gettext(self):
		return self.label
