#!/usr/bin/python
#==============================================================================================================#
#                                                                                                              #
# uploadWspr - Python program for loading wspr spots to wsprnet.org                                            #
#                                                                                                              #
# Copyright (C) 2019 Graham Collins ve3gtc                                                                     #
#                                                                                                              #
# This program is free software; you can redistribute it and/or modify                                         #
# it under the terms of the GNU General Public License as published by                                         #
# the Free Software Foundation; either version 2 of the License, or                                            #
# (at your option) any later version.                                                                          #
#                                                                                                              #
#  http://www.gnu.org/licenses/gpl-3.0.html                                                                    #
#                                                                                                              #
# This program is distributed in the hope that it will be useful,                                              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                                               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                                #
# GNU General Public License for more details.                                                                 #
#                                                                                                              #
# You should have received a copy of the GNU General Public License along                                      #
# with this program; if not, write to the Free Software Foundation, Inc.,                                      #
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.                                                  #
#                                                                                                              #
#==============================================================================================================#
"""
upload wspr spots in all_wspr.txt to wsprnet.org
"""
import sys
import time
import requests

#
# mimics simple unix / linux tail command
#
# called with file name, number of lines to return, and block size
# 	line count and blocksize are optional as defaults are provided
#
"""
mimics simple unix / linux tail command
"""
def tail(sourceFile, lineCount=1, blockSize=1024):

	try:
		with open( sourceFile, 'r') as file:
			file.seek(0,2)
	
			numberOfLines = 1 - file.read(1).count('\n')
			B = file.tell()
	
			while lineCount >= numberOfLines and B > 0:
				block = min(blockSize, B)
				B -= block
				file.seek(B, 0)
				numberOfLines += file.read(block).count('\n')
			
			file.seek(B, 0)
			numberOfLines = min(numberOfLines, lineCount)
	
			lines = file.readlines()[-numberOfLines:]
	
			file.close()
	
			return lines
	
	except IOError:
		
		with open('log.txt', 'a') as log_file:
			log_file.write(time.ctime() + ' : tail cannot find ' + sourceFile + ' file\n')
			log_file.close()

			return False
			
			
#
# start here
#

with open('log.txt', 'a') as log_file:
	log_file.write(time.ctime() + ' : |---------- upload.py started  ----------------------------------------------------------|\n')
	log_file.close()

	
# 
# get the last count of lines in ALL_WSPR.TXT in lastLineCount.txt file
# 	if ALL_WSPR.TXT exists, get the count of lines in the current ALL_WSPR.TXT file 
#
# 	if ALL_WSPR.TXT does not exist, log an error
#
try:
	with open ('lastLineCount.txt', 'r') as lastCount:
		lastLineCount = int( lastCount.read() )
		lastCount.close()
		
		try:
			currentLineCount = len(open('ALL_WSPR.TXT').readlines( ))
			
			lines = tail('ALL_WSPR.TXT', currentLineCount - lastLineCount)
			
			if lines != False:
			
				with open('all_mept.txt', 'w') as allMeptFile:
					
					for line in lines:
						allMeptFile.write( line )

					allMeptFile.close()
					
				targetURL = 'http://wsprnet.org/post'
				wsprFile = 'all_mept.txt'
				myCall = 'myCall'
				myGrid = 'myGrid'

				files = { 'allmept': open(wsprFile, 'r') }
				params = { 'call': myCall, 'grid': myGrid }

				try:
					response = requests.post('http://wsprnet.org/post', files=files, params=params)

				except requests.ConnectionError as exception:

					with open('log.txt', 'a') as log_file:
						log_file.write(time.ctime() + ' : connection error connecting to wsprnet.org\n')
						log_file.write( str(exception) + '\n' )						
						log_file.close()

					sys.exit(1)
	
				except requests.exceptions.Timeout:

					with open('log.txt', 'a') as log_file:
						log_file.write(time.ctime() + ' : post request timed out\n')
						log_file.close()
						
					sys.exit(1)
	
				except requests.exceptions.RequestException as exception:
					with open('log.txt', 'a') as log_file:
						log_file.write(time.ctime() + ' : catastrophic error posting to wsprnet.org\n')
						log_file.write( str(exception) + '\n' )
						log_file.close()
				
					sys.exit(1)
	
				with open('log.txt', 'a') as log_file:
					log_file.write(time.ctime() + ' : ' + str(currentLineCount - lastLineCount) +' wspr records uploaded\n')
					
					for line in lines:
						log_file.write(time.ctime() + ' : ' + line)
					
					log_file.close()
			
				with open ('lastLineCount.txt', 'w') as lastCount:
					lastCount.write( str( currentLineCount ) )
					lastCount.close()
			
		except IOError:

			with open('log.txt', 'a') as log_file:
				log_file.write(time.ctime() + ' : lastLineCount.txt found but ALL_WSPR.TXT not found\n')
				log_file.close()

			
#
# when lastLineCount.txt file does not exist
# create it, count the number of lines in ALL_WSPR.TXT, and put that number in lastLastCount.txt
#
except IOError:
	
		try:
			currentLineCount = len(open('ALL_WSPR.TXT').readlines( ) )
				
			with open ('lastLineCount.txt', 'w') as lastCount:
				lastCount.write( str( currentLineCount ) )
				lastCount.close()
			
		except IOError:
		
			with open('log.txt', 'a') as log_file:
				log_file.write(time.ctime() + ' : lastLineCount.txt not found AND ALL_WSPR.TXT not found\n')
				log_file.close()

#
# that's all folks!
#
with open('log.txt', 'a') as log_file:
	log_file.write(time.ctime() + ' : |---------- upload.py finished ----------------------------------------------------------|\n')
	log_file.close()
	

sys.exit(0)

#------------------------------------------------------------------------------------------------------------------------------------------#
	
	


