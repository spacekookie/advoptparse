# Copyright (C) 2014 Katharina Sabel
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#


	# Some variables to be used.
__VALUE__ = 'value'
__PREFIX__ = 'prefix'
__FIELD__ = 'field'


# Main class
#
class OptParseAdv:

	def __init__(self, parent, masters = None):
		self.parent = parent #Is this needed?
		self.set_masters(masters)
		self.iterating = False
		self.opt_hash = {}


	# Hash of master level commands. CAN contain a global function to determine actions of
	# subcommands.
	# (See docs).
	#
	def set_masters(self, masters):
		if masters == None:
			print "Warning! You shouldn't init a parser without your master commands set!"
		self.masters = masters



	# Takes the master level command and a hash of data
	# The hash of data needs to be formatted in the following sense:
	# {'X': funct} where X is any variable, option or command INCLUDING DASHES AND DOUBLE DASHES you want
	# to add to your parser.
	# Additionally you pass a function from your parent class that gets called when this option is detected in a
	# string that is being parsed. The function by detault takes three parameters: 
	# 
	# master command (i.e. copy), parent option (i.e. '-v'), data field (i.e. 'false'). So in an example for
	#
	# "clone -L 2"
	#
	# it would call the function: func('clone', '-L', '2') in the specified container class/ env.
	#
	# use parameters include:	'value'	: -v
	# 							'prefix': --logging true
	#							'field'	: --file=/some/data
	#
	# 
	def add_suboption(self, master, data, use = 'value'):
		self.opt_hash[master] = (use, data)


	# Create aliases for a master command that invoke the same
	# functions as the actual master command.
	# 
	# This can be used to shorten commands that user need to
	# input (such as 'rails server' vs 'rails s' does it)
	#
	def asign_aliases(self, master, aliases):
		pass


	def make_raw(self, string):
		return string.replace('-', '')


	def parse(self, c = None):
		content = (sys.args if (c == None) else c.replace("=", " ").split())

		option_input = []
		tmp = []
		focus = None
		cmd_range = []

		print self.opt_hash
		return


		# This piece of code breaks the input up into sub-master command strings to be handled
		# one at a time.
		#
		for mi, item in enumerate(content):
			if item in self.masters:
				tmp.append(mi)

		for first in tmp:
			if (first + 1) >= len(tmp):
				cmd_range.append((tmp[-1], len(content)))
				break
			cmd_range.append((tmp[first], tmp[first + 1]))
		
		for master in cmd_range:
			start = master[0]
			end = master[-1]

			tmp_cut = content[start:end]
			tmp_opt = { 'self' : content[start] }

			print tmp_cut


			for i in range(0, len(tmp_cut)):
				can = tmp_cut[i]
				par = self.opt_hash[tmp_opt['self']]

				if can in par[1]:
					if par[0] == __PREFIX__:
						# TODO: Check if the next field isn't missing. If it is, throw error.
						#  Also check that it is in fact a valid data field (not another command)
						tmp_opt[can] = tmp_cut[i + 1]
					elif par[0] == __FIELD__:
						# TODO: See above
						tmp_opt[self.make_raw(can)] = tmp_cut[i  + 1]
					elif par[0] == __VALUE__:
						tmp_opt[self.make_raw(can)] = True
						pass

			option_input.append(tmp_opt)
						
					

			# for i, cmd in enumerate(tmp_cut):
			# 	if tmp_cut[i] in (self.opt_hash[tmp_cut[0]]):
			# 		print tmp_cut[i]


			# print 
		print option_input
		return

		for idx, master in enumerate(content):
			tmp_opt = {'self':master} # Put all stuff in here
			s_idx = idx
			e_idx = -1

			for run, n in enumerate(content, start=idx):
				if n in self.masters or n == None:
					e_idx = run
					break

			print s_idx, e_idx

			# print idx, val
		return

		index = 0
		while content: # Stops if list is empty
			tmp_opt = {}
			tmp = content.pop(0)

			if tmp in self.masters:
				if focus == None:
					# Means it's the first master level command
					focus = tmp
					tmp_opt['self'] = 'focus'
				
					# Means it's the next master level command
					option_input.append(tmp_opt) # Add the option hash to the list
				index += 1
				continue

			if tmp in self.opt_hash[focus]:
				print "YAY! I found: '" + tmp + "' at index %i" % index
			index += 1

		print option_input



		# COMMAND copy /some/file -t /var/www connect nuclear -u root -t /var/www
		# 
		#
		#
			



class Test:

	def __init__(self):
		p = OptParseAdv(self, {'connect':self.connect,'copy':self.copy}) # Sets up the master level commands to connect and copy
		p.add_suboption('connect', {'--file': None}, use=__FIELD__)
		# p.add_suboption('connect', {'-t': None}, use='prefix')
		p.add_suboption('copy', {'--file': None}, use=__FIELD__)
		p.parse("copy --file=/path/to/file")

	def connect(self, master, sub, data):
		print sub + ": " + data
		pass

	def copy(self, master, sub, data):
		pass

if __name__ == "__main__":
	t = Test()