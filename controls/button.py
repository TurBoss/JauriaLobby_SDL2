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

class Button:
	"""Text Input"""
	def __init__(self, renderer, resources, buttonid, label , posx, posy, handler):
		
		self.renderer = renderer
		self.resources = resources
		
		self.buttonid = buttonid
		
		self.label = label
		self.posx = posx
		self.posy = posy
		
		self.handler = handler
		
		self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
		self.ManagerFont = sdl2.ext.FontManager(self.resources.get_path("tuffy.ttf"), size = 20)
		self.uifactory = sdl2.ext.UIFactory(self.factory)
		
		self.button = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("button.png"))
		self.buttonlabel = self.factory.from_text(self.label,
									fontmanager=self.ManagerFont)
		
		self.buttonlabel.position	= self.posx+20, self.posy+10
		self.button.position		= self.posx, self.posy
		
		self.button.click += self.handler
		
	def getevents(self, event):
		return self.button
		
	def drawlabel(self):
		return self.buttonlabel
		
	def drawbox(self):
		return self.button
