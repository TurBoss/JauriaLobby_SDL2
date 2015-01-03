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

class CheckBox:
	"""Text Input"""
	def __init__(self, renderer, resources, checkboxid, label, posx, posy, state):#, handler):
		
		self.renderer = renderer
		self.resources = resources
		
		self.checkboxid = checkboxid
		
		self.label = label
		self.posx = posx
		self.posy = posy
		
		#self.handler = handler
		
		self.state = state
		
		self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
		self.ManagerFont = sdl2.ext.FontManager(self.resources.get_path("tuffy.ttf"), size = 20)
		self.uifactory = sdl2.ext.UIFactory(self.factory)
		
		self.checkbox_on = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("check_on.png"))
		
		self.checkbox_off = self.uifactory.from_image(sdl2.ext.BUTTON,
									self.resources.get_path("check_off.png"))
		
		self.checkboxlabel = self.factory.from_text(self.label,
									fontmanager=self.ManagerFont)
		
		self.checkboxlabel.position	= self.posx + 30, self.posy - 2
		self.checkbox_on.position		= self.posx, self.posy
		self.checkbox_off.position		= self.posx, self.posy
		
		self.checkbox_on.click += self.toggle
		self.checkbox_off.click += self.toggle
		
	def getevents(self, event):
		if self.state == 0:
			return self.checkbox_off
		else:
			return self.checkbox_on
		
	def drawlabel(self):
		return self.checkboxlabel
		
	def drawbox(self):
		if self.state == 0:
			return self.checkbox_off
		else:
			return self.checkbox_on
			
	def toggle(self, button, event):
		if self.state == 0:
			self.state = 1
		else:
			self.state = 0
			
