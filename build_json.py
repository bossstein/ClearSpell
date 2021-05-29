#! /usr/bin/python3

import re
import sys
import json

IS_TITLE_RE = re.compile("^<")
IS_IPA_RE = re.compile("^\*")

TITLE_NAME_RE = re.compile("^<title>(\w+)</title>$")

DIELECT_RE = re.compile("\* {{a\|([^|}]+)")
IPA_RE = re.compile("{{IPA\|en\|/([^/]+)")

STDIN = sys.stdin
STDOUT = sys.stdout

current_list = list()
eng_to_ipa_dict = dict()

PREF_DIELECTS = ["UK", "RP", "US", "GA", "Canada", ""]

def determine_en_word(title_line):
	return TITLE_NAME_RE.match(title_line).group(1)

def extract_ipa(en_word, line):
	match = IPA_RE.search(line)
	if not match:
		return "!!" + en_word + "!!"
	return match.group(1)

def determine_ipa_word(en_word, lines):
	dialect_to_ipa = dict()
	if len(lines) == 1:
		return extract_ipa(en_word, lines[0])
	for line in lines:
		dielect_match = DIELECT_RE.match(line)
		if dielect_match:	
			dielect = dielect_match.group(1)
		else:
			dielect = ""
		dialect_to_ipa[dielect] = extract_ipa(en_word, line)
	for d in PREF_DIELECTS:
		if d in dialect_to_ipa:
			return dialect_to_ipa[d]
	return extract_ipa(en_word, lines[0])

def add_prev_list(one_word_list):
	if len(one_word_list) <= 1:
		return
	en_word = determine_en_word(one_word_list[0])
	ipa_word = determine_ipa_word(en_word, one_word_list[1:])
	eng_to_ipa_dict[en_word] = ipa_word

for line in STDIN.readlines():
	if IS_TITLE_RE.match(line):
		add_prev_list(current_list)
		current_list = []
	current_list.append(line)

json.dump(eng_to_ipa_dict, STDOUT)
