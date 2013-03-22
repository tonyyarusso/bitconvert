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
# Usage: bitconvert.py -p|-s <value> [-b|-B]
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

bitpattern = re.compile(r'^(\d*\.?\d+)(K|k|M|m|G|g|T|t|P|p|E|e)?(b|B)?(.*)$')

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
	print "Usage: bitconvert.py -p|-s <value> [-b|-B]"
	print "e.g. bitconvert.py -p 235235235"
	print ""
	print "Options:"
	print " -h, --help"
	print "       Print help screen"
	print " -p, --prefixed"
	print "       Convert from simple input to prefixed human-readable output"
	print " -s, --simple"
	print "       Convert from prefixed human-readable input to simple output"
	print " -b, --bits"
	print "       Convert from bytes to bits"
	print " -B, --bytes"
	print "       Convert from bits to bytes"
	sys.exit(0)

def convert_to_prefixed(count):
	if count < 1024:
		num_part = count
		prefix = ""
	elif count < 1048576:
		num_part = float(count)/float(1024)
		prefix = "K"
	elif count < 1073741824:
		num_part = float(count)/float(1048576)
		prefix = "M"
	elif count < 1099511627776:
		num_part = float(count)/float(1073741824)
		prefix = "G"
	elif count < 1125899906842624:
		num_part = float(count)/float(1099511627776)
		prefix = "T"
	elif count < 11592921504606846976:
		num_part = float(count)/float(1125899906842624)
		prefix = "P"
	else:
		num_part = float(count)/float(11592921504606846976)
		prefix = "E"
	return [num_part, prefix]

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

def bits_to_bytes(count, suffix):
	if suffix == "B":
		# Input value already in bytes; not converting
		return count
	else:
		return float(count)/float(8)

def bytes_to_bits(count, suffix):
	if suffix == "b":
		# Input value already in bits; not converting
		return count
	else:
		return count * 8

def main(argv):
	user_input = None
	scale = None
	try:
		opts, args = getopt.getopt(argv, "hbBp:s:", ["help", "bits", "bytes", "prefixed=", "simple="])
	except getopt.GetoptError:
		usage()
		sys.exit(127)
	if len(opts) == 0:
		usage()
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
		elif opt in ("-b", "--bits"):
			scale = "to_bits"
		elif opt in ("-B", "--bytes"):
			scale = "to_bytes"
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
	
	if scale == "to_bits":
		adj_input = (bytes_to_bits(float(input[0]), input[2]), input[1], "b")
	elif scale == "to_bytes":
		adj_input = (bits_to_bytes(float(input[0]), input[2]), input[1], "B")
	else:
		adj_input = (float(input[0]), input[1], input[2])
	
	if direction == "simple_to_prefixed":
		try:
			float(adj_input[0])
		except getopt.GetoptError:
			usage()
			sys.exit(127)
		converted = convert_to_prefixed(convert_to_simple(float(adj_input[0]), adj_input[1]))
		converted.extend([adj_input[2]])
	elif direction == "prefixed_to_simple":
		try:
			float(adj_input[0])
			str(adj_input[1])
		except getopt.GetoptError:
			usage()
			sys.exit(127)
		converted = [convert_to_simple(float(adj_input[0]), adj_input[1]), "", adj_input[2]]
	else:
		print "Must specify either direction of conversion as either --prefixed or --simple"
		usage()
	
	if input[3]:
		converted.extend([input[3]])
	else:
		converted.extend([""])
	
	if converted[2] is not None:
		result = str(round(converted[0], 1)) + str(converted[1]) + str(converted[2]) + str(converted[3])
	else:
		result = str(round(converted[0], 1)) + str(converted[1]) + str(converted[3])

	return result
	
if __name__ == "__main__":
	result = sys.exit(main(sys.argv[1:]))
	print result
