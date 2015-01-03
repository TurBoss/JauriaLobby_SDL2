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

class PopUp:
	"""Text Input"""
	def __init__(self, renderer, resources, popupid, label, msg, posx, posy):
		
		self.renderer = renderer
		self.resources = resources
		
		self.popupid = popupid
		
		self.label = label
		self.msg = msg
		self.posx = posx
		self.posy = posy
		
		self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
		self.ManagerFont = sdl2.ext.FontManager(self.resources.get_path("tuffy.ttf"), size = 14)
		self.uifactory = sdl2.ext.UIFactory(self.factory)
		
		self.textlabel = self.factory.from_text(self.label,
									fontmanager=self.ManagerFont)
		
		self.textmsg = self.factory.from_text(self.msg,
									fontmanager=self.ManagerFont)
		
		self.background = self.factory.from_image(self.resources.get_path("popup.png"))

		
		self.textlabel.position			= self.posx+5, self.posy-20
		self.textmsg.position 			= self.posx+5, self.posy+15
		self.background.position		= self.posx ,self.posy
		
	def drawbox(self):
		return self.background
		
	def drawlabel(self):
		return self.textlabel
		
	def drawmsg(self):
		return self.textmsg
