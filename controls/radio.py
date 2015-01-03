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

class Radio:
	"""Text Input"""
	def __init__(self, renderer, resources, radioid, label, posx, posy, state):#, handler):
		
		self.renderer = renderer
		self.resources = resources
		
		self.radioid = radioid
		
		self.label = label
		self.posx = posx
		self.posy = posy
		
		#self.handler = handler
		
		self.state = state
		
		self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
		self.ManagerFont = sdl2.ext.FontManager(self.resources.get_path("tuffy.ttf"), size = 20)
		self.uifactory = sdl2.ext.UIFactory(self.factory)
		
		self.radio_on = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("radio_on.png"))
		
		self.radio_off = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("radio_off.png"))
		
		self.radiolabel = self.factory.from_text(self.label,
									fontmanager=self.ManagerFont)
		
		self.radiolabel.position	= self.posx + 30, self.posy - 2
		self.radio_on.position		= self.posx, self.posy
		self.radio_off.position		= self.posx, self.posy
		
		self.radio_on.click += self.toggle
		self.radio_off.click += self.toggle
		
	def getevents(self, event):
		if self.state == 0:
			return self.radio_off
		else:
			return self.radio_on
		
	def drawlabel(self):
		return self.radiolabel
		
	def drawbox(self):
		if self.state == 0:
			return self.radio_off
		else:
			return self.radio_on
			
	def toggle(self, button, event):
		if self.state == 0:
			self.state = 1
		else:
			self.state = 0
			
