# Passgen -- A password generator written in Python 3
# File: Main script (is the freezed script)
# ---------------------------------------------------

programVersion = "1.2.5"

import string
import os
import sys
import random
import time
import gc
import shutil
from secrets import choice, token_hex
from decimal import Decimal
from colorama import init
from termcolor import cprint, colored

init() # From colorama, makes colors work on non-compatible terminals

def get_folder_size(start_path): # Returns the directory size in bytes
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	return total_size

def main():
	print(colored("Sandai", "magenta") + "'s Password Generator")
	print("Version", colored(programVersion, "cyan"))

	print("====Select a generation mode====")
	print("1/ secrets.token_hex()")
	print("2/ secrets.choice() [" + colored("recommended", "green") + "]")

	if input("> ") == "1":
		str_generation_mode = "HEX"
	else:
		str_generation_mode = "ASCII"

	int_files_to_generate = int(input("[INT] Number of files to create? : "))
	int_passwords_to_generate = int(input("[INT] Number of passwords to generate in each file? : "))
	int_bits_to_generate_min = int(input("[INT] Minimum number of bits? : "))
	int_bits_to_generate_max = int(input("[INT] Maximum number of bits? : "))
	int_buffer_size = int(input("[INT] Disk buffer size in bytes? : "))
	int_binchoice_add_verbosity = int(input("[INT] Augmenter la verbosité? [1/0]: "))

	str_folder_name = str(input("[STR] Folder name? : "))
	str_file_prefix = str(input("[STR] File prefix? : "))
	str_file_extension = str(input("[STR] File extension? : "))

	#creating folder, works on Windows / Linux
	cprint("[INFO]: Creating folder '" + str_folder_name + "'...", "green")

	try:
		os.mkdir(str_folder_name)
	except:
	 	cprint("[WARN]: The folder may already exist", "yellow")


	# Here the user selects a set of characters to generate

	if str_file_extension == "HEX":
		pass

	else:
		while True:
			print("========")
			print("Please select a list of characters to generate:")
			print("1/ ASCII + digits")
			print("2/ ASCII + digits + punctuaction")
			print("3/ Create a new set")
			print("4/ Load a new set from a file")
			int_charlist_choice = str(input("\n[INT] (1/2/3/4): "))

			if int_charlist_choice == "1": # Ascii w/o specials
				str_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
				break

			elif int_charlist_choice == "2": # Ascii w/ specials
				str_charset = string.punctuation + string.ascii_uppercase + string.ascii_lowercase + string.digits
				break

			elif int_charlist_choice == "3": # CUSTOM charlist (str)
				print("========")
				print("Please enter a new set on this line")
				print("Exemple: abcABC123?;!")
				str_charset = str(input("> "))
				break
			
			elif int_charlist_choice == "4":
				cprint("Please specify the file to load (Exemple: charset.txt)", "cyan")
				userFile = input("File> ")
				
				try:
					with open(userFile, "r") as filestr_charset:
						str_charset = filestr_charset.read() # Tries to read and set the new charset
						break

				except Exception as e:
					cprint("An error happended while reading the file", "red")
					cprint("Reason: " + str(e), "yellow")
					continue

			else:
				cprint("Invalid choice!", "yellow")
				continue

	print("========")
	input("Press [ENTER] to continue...")
	cprint("Please wait, this can take a while...", "cyan")
	print("========")

	startTime = time.time()

	for int_file_index in range(int_files_to_generate):

		str_current_file_name = str_file_prefix + str(int_file_index) + str_file_extension
		cprint("Generating " + str(int_passwords_to_generate) + " passwords in " + str_current_file_name + "...", "cyan")

		currentFile = open(str_current_file_name, "w", int_buffer_size)
		
		if str_generation_mode == "HEX": # Generate using secrets.token_hex()
			
            for x in range(int_passwords_to_generate):
				currentFile.write(token_hex(nbytes=random.randint(int_bits_to_generate_min, int_bits_to_generate_max))+"\n")

			currentFile.close()

		elif str_generation_mode == "ASCII": # Generate using secrets.choice()
			if int_binchoice_add_verbosity == 1: # if user requested to write add. infos in file
				currentFile.write("====Infos====\n")
				currentFile.write("bits per line (min): " + str(int_bits_to_generate_min) + "\n")
				currentFile.write("bits per line (max): " + str(int_bits_to_generate_max) + "\n")
				currentFile.write("char table: " + str(str_charset) + "\n")
				currentFile.write("file name : " + str(str_current_file_name) + "\n")
				currentFile.write("Buffer size : " + str(int_buffer_size) + "\n")
				currentFile.write("generator version: " + str(programVersion) + "\n")
				currentFile.write("total passwords: " + str(int_passwords_to_generate) + "\n")
				currentFile.write("====Start====\n")
			
				for x in range(int_passwords_to_generate):
					currentFile.write(''.join([choice(str_charset) for character in range(random.randint(int_bits_to_generate_min, int_bits_to_generate_max))])+"\n")
			
			else: # Do not write additionnal infos in file
				for x in range(int_passwords_to_generate):
					currentFile.write(''.join([choice(str_charset) for character in range(random.randint(int_bits_to_generate_min, int_bits_to_generate_max))])+"\n")

		currentFile.close()
		cprint("[INFO]: -> Moving file...", "cyan")

		shutil.move(str_current_file_name, str_folder_name) # that should fix the crash when moving a file (hopefully)
		
        # Old method used to move files, replaced by shutil.move()
		#if os.name == 'nt':
		#	os.system("move '" + str_current_file_name + "' '" + str_folder_name + "'")
		#else:
		#	os.system("mv '" + str_current_file_name + "' '" + str_folder_name + "'")

	int_finalTime_seconds = int(time.time() - startTime)
	int_finalTime_minutes = int_finalTime_seconds // 60
	int_finalTime_hours = int_finalTime_minutes // 60

	# It rounds these by 3 additionnal decimals, 
	int_lastFileSize = round((Decimal(os.path.getsize(str_folder_name + "/" + str_current_file_name) / 1024 / 1024)), 3) # Gets the size of the last file generated in Bytes, then round it in Megabytes
	int_folderSize = round((Decimal(get_folder_size(str_folder_name + "/") / 1024 / 1024)), 3) # Gets the folder size in Bytes, round it in Megabytes

	print("========")
	cprint("Done!", "green")
	print("========")
	print("Number of files : " + str(int_files_to_generate))
	print("Size of the last file generated : ", colored(str(int_lastFileSize) + " Mb", "cyan"))
	print("Folder size (total) : ", colored(str(int_folderSize) + " Mb", "magenta"))
	print("Generation time : ", str(int_finalTime_seconds), "seconds (" + str(int_finalTime_minutes), "minutes (" + str(int_finalTime_hours), "hours))")
	print("========")

	input("-> Press [ENTER] to quit...")
	sys.exit()
main()