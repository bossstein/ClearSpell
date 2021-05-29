#! /usr/bin/python3

from enum import Enum, auto, unique
import re
import sys

@unique
class State(Enum):
	ITITIAL = auto()
	PREV_IS_TITLE = auto()
	PREV_IS_ENGLISH = auto()
	PREV_IS_IPA = auto()
	SKIP_UNTIL_TITLE = auto()

IS_TITLE_RE = re.compile("^<")
IS_ENGLISH_RE = re.compile("^=")
IS_IPA_RE = re.compile("^\*")

STDIN = sys.stdin
STDOUT = sys.stdout

class UnnecessaryLineRemover:
	def __init__(self, list_of_lines):
		self.list_of_lines = list_of_lines
		self.state = State.ITITIAL
		self.i = 0
	def process_line(self):
		if self.state == State.SKIP_UNTIL_TITLE:
			return
		elif self.state == State.PREV_IS_TITLE: 
			if IS_IPA_RE.match(self.list_of_lines[self.i]):
				STDOUT.write(self.list_of_lines[self.i - 1])
				STDOUT.write(self.list_of_lines[self.i])
		elif self.state == State.PREV_IS_ENGLISH: 
			if IS_IPA_RE.match(self.list_of_lines[self.i]):
				STDOUT.write(self.list_of_lines[self.i - 2])
				STDOUT.write(self.list_of_lines[self.i])
		elif self.state == State.PREV_IS_IPA: 
			if IS_IPA_RE.match(self.list_of_lines[self.i]):
				STDOUT.write(self.list_of_lines[self.i])
	def update_state(self):
		line = self.list_of_lines[self.i]
		if self.state == State.SKIP_UNTIL_TITLE and (not IS_TITLE_RE.match(line)):
			return
		elif IS_ENGLISH_RE.match(line) and ( self.state == State.PREV_IS_IPA or self.state == State.PREV_IS_ENGLISH ):
			self.state = State.SKIP_UNTIL_TITLE
		elif IS_ENGLISH_RE.match(line):
			self.state = State.PREV_IS_ENGLISH
		elif IS_TITLE_RE.match(line):
			self.state = State.PREV_IS_TITLE
		elif IS_IPA_RE.match(line):
			self.state = State.PREV_IS_IPA
	def loop_over_file(self):
		while self.i < len(self.list_of_lines):
			self.process_line()
			self.update_state()
			self.i += 1
	def remove(self):
		self.update_state()
		self.i += 1
		self.loop_over_file()

UnnecessaryLineRemover(STDIN.readlines()).remove()
