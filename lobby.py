import os
import sys
import socket
import time

from gui import Gui
from client import Client


class Lobby:
	"""main springlobby object"""
	def __init__(self):
		self.connected = False
		self.running = 1
		self.gui = Gui()

	def run(self):
		"""the main loop for Lobby"""
		self.gui.run()
