#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import time
from ctypes import py_object, pointer, cast, c_void_p, POINTER

if os.name == "nt":
	if getattr(sys, 'frozen', False):
		# frozen
		sdlpath = 'libs'
	else:
		# unfrozen
		sdlpath = os.path.join(os.path.dirname(__file__), 'libs')
		
	os.environ['PYSDL2_DLL_PATH'] = sdlpath


import sdl2.ext as sdl2ext

from sdl2 import	 (	pixels,
				render,
				events as sdlevents,
				surface,
				error,
				timer,
				SDL_Delay,
				SDL_WINDOW_BORDERLESS
			)

from sdl2.sdlttf import	(	TTF_OpenFont, 
				TTF_RenderText_Shaded,
				TTF_GetError,
				TTF_Init,
				TTF_Quit
			)


class TextSprite(sdl2ext.TextureSprite):
	def __init__	(self,	renderer,
				font = None,
				text = "",
				fontSize = 16, 
				textColor = pixels.SDL_Color(255, 255, 255), 
				backgroundColor = pixels.SDL_Color(0, 0, 0)
			):
		if isinstance(renderer, sdl2ext.Renderer):
			self.renderer = renderer.renderer
		elif isinstance(renderer, render.SDL_Renderer):
			self.renderer = renderer
		else:
			raise TypeError("unsupported renderer type")

		if getattr(sys, 'frozen', False):
			# frozen
			self.resources = sdl2.ext.Resources(sys.executable, "../resources")
		else:
			# unfrozen
			self.resources = sdl2ext.Resources(__file__, "../resources")
		
		if font is None:
			font = self.resources.get_path("tuffy.ttf")
		elif not os.path.isfile(font):
			font = self.resources.get_path(font + ".otf")
			
		self.font = TTF_OpenFont(font, fontSize)
		if self.font is None:
			raise TTF_GetError()
		self._text = text
		self.fontSize = fontSize
		self.textColor = textColor
		self.backgroundColor = backgroundColor
		texture = self._createTexture()
		
		super(TextSprite, self).__init__(texture)
	
	def _createTexture(self):
		textSurface = TTF_RenderText_Shaded(self.font, self._text, self.textColor, self.backgroundColor)
		if textSurface is None:
			raise TTF_GetError()
		texture = render.SDL_CreateTextureFromSurface(self.renderer, textSurface)
		if texture is None:
			raise sdl2ext.SDLError()
		surface.SDL_FreeSurface(textSurface)
		return texture
	
	def _updateTexture(self):
		textureToDelete = self.texture
		
		texture = self._createTexture()
		super(TextSprite, self).__init__(texture)

		render.SDL_DestroyTexture(textureToDelete)
	
	@property
	def text(self):
		return self._text
	
	@text.setter
	def text(self, value):
		if self._text == value:
			return
		self._text = value
		self._updateTexture()

class Label(object):
	def __init__(self, sprite):
		super(Label, self).__init__()
		self.label = "label"
		self.text = sprite

class LabelText(sdl2ext.Entity):
	def __init__(self, world, *args, **kwargs):
		if "renderer" not in kwargs:
			raise ValueError("you have to provide a renderer= argument")
		renderer = kwargs['renderer']
		super().__init__()
		textSprite = TextSprite(renderer, "FreeMonoBold", "FPS: -")
		self.fps = FPS(textSprite)
		self.textSprite = textSprite

def main():
	sdl2ext.init()
	TTF_Init()
	
	window = sdl2ext.Window("Jauria Lobby", size=(800, 600),flags = SDL_WINDOW_BORDERLESS)
	window.show()
	
	renderer = sdl2ext.Renderer(window)
	factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
	world = sdl2ext.World()
	
	
	label = LabelText(world, renderer=renderer)
	
	spriteRenderer = factory.create_sprite_renderer()
	
	running = True
	
	while running:
		for event in sdl2ext.get_events():
			if event.type == sdlevents.SDL_QUIT:
				running = False
				break
		renderer.clear()
		world.process()
		SDL_Delay(1)
		
	TTF_Quit()
	sdl2ext.quit()
	return 0

if __name__ == '__main__':
	
	main()

