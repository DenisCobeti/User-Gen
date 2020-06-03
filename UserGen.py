
__author__ = 'Denis C.'
__date__ = '2020.05.20'
__version__ = '0.1'

"""

Generator of password, user name and email for a specific user

The generator starts by n encrypting the user name 
with 5 diferent algorithms, taking the first NUM_HASH 
characters from each one and joining them.

"""

import hashlib
import random
import json
import argparse
from os import path

"""  Class that generates most things needed for a user: email, username and password """
class UserGenerator:

	def __init__(self, names, prefix, sufix, joiner):
		self.names = names
		self.prefix = prefix
		self.sufix = sufix
		self.joiner = joiner

	def chanceJoiner(self, chance, str1, str2):
		if random.random() <= chance:
			return (str1 + random.choice(self.joiner) + str2)
		else:
			return (str1 + str2)
			
	""" Function that generates a password that will alwas¡ys have the same results depending on the user name"""
	def genPassword(self, user):

		# All the encription functions and how many letter will be taken from each hash result
		# It is recommecomended to modify this when using this script for personal reasons
		ENCRYPT_FUNCS = [(hashlib.sha1, 3), (hashlib.md5, 4), (hashlib.sha224, 3), 
						(hashlib.sha512, 5), (hashlib.sha384, 6)]
		MAX_END_lEN = 7

		passwd = ""
		user = user.encode('utf-8')

		for i in range(len(ENCRYPT_FUNCS)):
			passwd += ENCRYPT_FUNCS[i][0](user).hexdigest()[:ENCRYPT_FUNCS[i][1]]
			
		# 
		ending = len(user) % MAX_END_lEN
		passwd += passwd[:ending] + '?'

		# Aapitalize the first found letter
		for i, char in enumerate(passwd):
			if(char.isalpha()):
				passwd = passwd [:i] + passwd[i:].capitalize()
				break

		return passwd

	def genUserName(self):
		
		# hance of the username having a sufix / prefix
		SUFIX_CHANCE = 0.80
		PREFIX_CHANCE = 0.80
		# Chance of using a joiner when concatenating strings
		JOINER_CHANCE = 0.40
		# If the username lengh is less that this threshold, a sufix is guaranteed
		NAME_PREFIX_THRESHOLD = 10
		# Chance of the first name to just be an initial
		INITIAL_CHANCE = 0.30

		# Chance of the second name being an initial of the first name is not
		SECOND_INITIAL_FULL = 0.50
		# Chance of the second name being an intial if the first one is as well
		SECOND_INITIAL_PARCIAL = 0.30

		# Chance of a third initial
		THIRD_INITIAL = 0.40
		# Chance of a third name
		THIRD_NAME = 0.20
		
		user_prefix = ''
		user_sufix = ''

		user_name = random.choice(self.names)
		second_name = random.choice(self.names)
		third_name = random.choice(self.names)

		# The username has a n chance of having a prefix
		if random.random() <= PREFIX_CHANCE:
			user_prefix = random.choice(self.prefix)
		
		# N chance of the first name to just be the initial
		if random.random() <= INITIAL_CHANCE:
			user_name = user_name[0]

			# Chance of the second name also being an initial, the third name gets appended
			if random.random() <= SECOND_INITIAL_PARCIAL:
				user_name = self.chanceJoiner(JOINER_CHANCE, user_name, second_name)
				user_name = self.chanceJoiner(JOINER_CHANCE, user_name, third_name)
			else:
				user_name += second_name
				# Chance of it having a third initial if the second name is appended fully
				if random.random() <= THIRD_INITIAL:
					user_name = self.chanceJoiner(JOINER_CHANCE, user_name, third_name[0])

		else:
			# Chance of the second name being an intial if the first one isnt 
			if random.random() <= SECOND_INITIAL_FULL:
				user_name = self.chanceJoiner(JOINER_CHANCE, user_name, second_name[0])
			else:
				user_name = self.chanceJoiner(JOINER_CHANCE, user_name, second_name)
			
			# Chance of a third name
			if random.random() <= THIRD_NAME:
				user_name = self.chanceJoiner(JOINER_CHANCE, user_name, third_name)
			else: 
				user_name = self.chanceJoiner(JOINER_CHANCE, user_name, third_name[0])

		# If the lenght is less than the threashold, a sufix is guaranteed, if not its chance
		if len(user_name) < NAME_PREFIX_THRESHOLD:
			user_sufix = random.choice(self.sufix)
		else:
			# Chance of a sufix
			if random.random() < SUFIX_CHANCE:
				user_sufix = random.choice(self.sufix)
		
		user_name = user_prefix + user_name + user_sufix
		return user_name
	

	def genEmail(self, user_name):
		# All possible email endings
		EMAIL_END = ["@gmail.com", "@hotmail.com", "@yahoo.com"]

		return user_name + random.choice(EMAIL_END)

	def genUsers(self, num):
		NAME = 'name'
		PASS = 'password'

		users = {}

		for i in range(num):
			user_name = self.genUserName()

			users[self.genEmail(user_name)] = {
				NAME: user_name,
				PASS: self.genPassword(user_name)
			}
		return users
		
	def exportUsersJson(self, num, file):
		users = self.genUsers(num)

		with open(file, 'w') as json_file:
			json.dump(users, json_file)
		
		return users

# class User:

# 	JSON_NAME = 'name'
# 	JSON_PASS = 'password'

# 	def __init__(self, name, email, password):
# 		self.name = name
# 		self.email = email
# 		self.password = password
		
# 	def dataFormat(self):
# 		data = {}
		
# 		data[self.email].append({
# 			self.JSON_PASS: self.password,
# 			self.JSON_NAME: self.name,
# 		})

# 		return data

if __name__ == "__main__":

	file_names = open('names.json').read()
	file_joiner = open('joiner.json').read()
	file_suffix = open('suffixes.json').read()
	file_prefix = open('prefixes.json').read()

	names = json.loads(file_names)
	joiner = json.loads(file_joiner)
	suffixes = json.loads(file_suffix)
	prefixes = json.loads(file_prefix)

	my_parser = argparse.ArgumentParser(description='Generates user names, emails and passwords in JSON format')
	# Add the arguments
	my_parser.add_argument('Count', metavar='Count', type=int, 
							help='the number of generated users')
	my_parser.add_argument('-p', '--passwd', action='store', metavar='USERNAME',
							help='check the password of the inputed user name')
	my_parser.add_argument('-o', '--output', action='store', metavar='PATH',
							help='file to output the users', default='export.json')
	args = my_parser.parse_args()

	count = args.Count
	check_password = args.passwd
	output = args.output
	
	generator = UserGenerator(names, prefixes, suffixes, joiner)

	if check_password is not None:
		print (generator.genPassword(check_password))
	if count != 0:
		print(generator.exportUsersJson(count, output))

