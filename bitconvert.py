#!/usr/bin/env python
# ======================================================================================================================
# Basic bit/byte converter
#
# Copyright:   2013, Tony Yarusso
# Author:      Tony Yarusso <tonyyarusso@gmail.com>
# License:     BSD 3-clause <http://opensource.org/licenses/BSD-3-Clause>
# Description: A simple script to convert bit or byte values between simple unprefixed numbers and
#              human-readable prefixed forms (eg. 235235235B vs 224.3MB)
#
# Usage: bitconvert.py -p|-s <value>
# e.g. bitconvert.py -p 235235235
#
# ----------------------------------------------------------------------------------------------------------------------
#
# Full license text:
#
# Copyright (c) 2013, Tony Yarusso
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#   disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the name of Tony Yarusso nor the names of other contributors may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ======================================================================================================================

import getopt, re, sys

bitpattern = re.compile(r'^(\d*\.?\d+)(K|k|M|m|G|g|T|t|P|p|E|e)?$')

def usage():
	print "Name:         Basic bit/byte converter"
	print "Description:  A simple script to convert bit or byte values"
	print "              between simple unprefixed numbers and"
	print "              human-readable prefixed forms"
	print "              (eg. 235235235 vs 224.3M)"
	print "Author:       Tony Yarusso <tonyyarusso@gmail.com>"
	print "Copyright:    2013, Tony Yarusso"
	print "License:      BSD 3-clause"
	print "              <http://opensource.org/licenses/BSD-3-Clause>"
	print ""
	print "Usage: bitconvert.py -p|-s <value>"
	print "e.g. bitconvert.py -p 235235235"
	print ""
	print "Options:"
	print " -h, --help"
	print "       Print help screen"
	print " -p, --prefixed"
	print "       Convert from simple input to prefixed human-readable output"
	print " -s, --simple"
	print "       Convert from prefixed human-readable input to simple output"
	sys.exit(0)

def convert_to_prefixed(count):
	if count < 1024:
		num_part = count
		prefix = ""
	elif count < 1048576:
		num_part = round(float(count)/float(1024), 1)
		prefix = "K"
	elif count < 1073741824:
		num_part = round(float(count)/float(1048576), 1)
		prefix = "M"
	elif count < 1099511627776:
		num_part = round(float(count)/float(1073741824), 1)
		prefix = "G"
	elif count < 1125899906842624:
		num_part = round(float(count)/float(1099511627776), 1)
		prefix = "T"
	elif count < 11592921504606846976:
		num_part = round(float(count)/float(1125899906842624), 1)
		prefix = "P"
	else:
		num_part = round(float(count)/float(11592921504606846976), 1)
		prefix = "E"
	return (num_part, prefix)

def convert_to_simple(count, prefix):
	if prefix == 'K' or prefix == 'k':
		bits = count * 1024
	elif prefix == 'M' or prefix == 'm':
		bits = count * 1048576
	elif prefix == 'G' or prefix == 'g':
		bits = count * 1073741824
	elif prefix == 'T' or prefix == 't':
		bits = count * 1099511627776
	elif prefix == 'P' or prefix == 'p':
		bits = count * 1125899906842624
	elif prefix is None:
		bits = count
	else:
		print "Unsupported prefix"
		sys.exit(1)
	return int(bits)

def main(argv):
	user_input = None
	try:
		opts, args = getopt.getopt(argv, "hp:s:", ["help", "prefixed=", "simple="])
	except getopt.GetoptError:
		usage()
		sys.exit(127)
	if len(opts) == 0:
		usage()
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
		elif opt in ("-p", "--prefixed"):
			direction = "simple_to_prefixed"
			user_input = arg
		elif opt in ("-s", "--simple"):
			direction = "prefixed_to_simple"
			user_input = arg
		else:
			usage()
	
	if user_input:
		input = bitpattern.search(user_input).groups()
	else:
		print "An input value is required"
		usage()
	
	if direction == "simple_to_prefixed":
		try:
			int(input[0])
		except getopt.GetoptError:
			usage()
			sys.exit(127)
		result = convert_to_prefixed(int(input[0]))
		print str(result[0]) + str(result[1])
	elif direction == "prefixed_to_simple":
		try:
			int(input[0])
			str(input[1])
		except getopt.GetoptError:
			usage()
			sys.exit(127)
		result = convert_to_simple(int(input[0]), input[1])
		print str(result)
	else:
		print "Must specify either direction of conversion as either --prefixed or --simple"
		usage()
	
if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))