#Erwan's Password Gen 1.4.2


import string, os, sys, random, time, io
from secrets import choice, token_hex
from base64 import b64encode
from decimal import Decimal
from colorama import init
from termcolor import cprint, colored
from passgenlib import get_folder_size
init()

programVersion = "1.4.2"

print("MettaliKk's Automated Password Algorithm - MAPA")
print("Version " + programVersion)

cprint("===Warning===", "yellow")
print("Using this program can", colored("severely", "cyan"), "fragment your disk")
print("Please use it on an alternative drive")
print("As it can write thousands of time per second.")
print("\nPlease type 'YES' without quotes to start generating")
userContinue = input("Continue?> ")

if userContinue.lower() == "yes":
    print("")
    pass
else:
    print("Aborting...")
    sys.exit(0)
    #Exits the program with error code 0 (success)
    #Although it should be 1 (error), it's better to let it to 0
    #Because in some systems, it could be reported as a programming error
    #But as this is a user action, it should be 0

print("========")
print("Would you like to generate in Hexadeimals?")
print("If YES, it will generate unsecure passwords")
print("It should only be used when you are-")
print("securely erasing a disk")
print("It overrides:")
print("-Number of bits (from)")
print("-Additionnal infos")
print("-Charlist")
print("type 'YES' without quotes to enable it")
fast_gen = input(">") #Will use it in algorithm
if fast_gen.lower() == "yes":
    fast_gen = True
else:
    fast_gen = False

print("")

#Requesting informations --
#must be int
num_files = int(input("[INT] Number of files: "))
num_passwords = int(input("[INT] Number of codes: "))
num_bits_from = int(input("[INT] Number of bits (from): "))
num_bits_to = int(input("[INT] Number of bits (to): "))

#must be str
add_infos = str(input("[INT] Add additional infos in file? [1/0]: "))
folder_name = str(input("[STR] Folder name (create new): "))
file_prefix = str(input("[STR] File prefix: "))
file_extension = str(input("[STR] File extension: "))

#creating folder, works on Windows / Linux
print("Creating folder '" + colored(folder_name, "cyan") + "'...")
os.mkdir(folder_name)

#User selects charlist or create a new one
#Default: chars = string.ascii_uppercase + string.ascii_lowercase + string.digits

while True: #Loops menu, if invalid choice is selectd
    print("Please select a charlist:")
    print("1/ ASCII w/o specials")
    print("2/ ASCII w/ specials")
    print("3/ New charlist")
    charlistChoice = str(input("\n[INT] (1/2/3): "))
    if charlistChoice == "1": #Ascii w/o specials
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        break
    elif charlistChoice == "2": #Ascii w/ specials
        chars = string.punctuation + string.ascii_uppercase + string.ascii_lowercase + string.digits
        break
    elif charlistChoice == "3": #CUSTOM charlist (str)
        print("========")
        print("Please enter charlist on one line")
        print("Example: abcABC123?;!")
        chars = str(input("[CHARLIST]> "))
        break
    else:
        print("Invalid choice!")
        continue #Goes to the top of the while loop

#Users review choices
print("========")
print("Generation params:")
print("Files: "+str(num_files))
print("Bits: "+str(num_bits_from)+", "+str(num_bits_to))
print("Passwords: "+str(num_passwords))
#print("\nCharlist: "+str(chars))
print("========")

input("press [ENTER] to generate")

#Charlist has been set, starting generation
print("Please wait, this can take a while")
print("========")
startTime = time.time() #Picking current time, to substract later

for mult in range(num_files): #For given number of files
    file_name = file_prefix + str(mult) + file_extension
    fileBuffer = [] #Inits the file buffer
    print("Generating", str(num_passwords), "passwords in", file_name, "...")
    
    if fast_gen == True: #Faster possible
        currentFile = open(file_name, "w")
        for x in range(num_passwords):
            currentFile.write(token_hex(nbytes=num_bits_to)) #Max number of bits
        currentFile.close()
    else: #Normal Gen mode
        if add_infos == "1": #if user requested to write add. infos in file
            fileBuffer.append("====Generation====\n")
            fileBuffer.append("bits per line (from): "+str(num_bits_from)+"\n")
            fileBuffer.append("bits per line (to): "+str(num_bits_to)+"\n")
            fileBuffer.append("total codes: "+str(num_passwords)+"\n")
            fileBuffer.append("====Start====\n")
        
            for x in range(num_passwords):
                fileBuffer.append(str(x)+": "+''.join([choice(chars) for _ in range(random.randint(num_bits_from, num_bits_to))])+"\n")
        else: #Do not write additionnal infos in file

            for x in range(num_passwords): #Generate passwords with bits from int and to int
                fileBuffer.append(''.join([choice(chars) for _ in range(random.randint(num_bits_from, num_bits_to))])+"\n")
            
        currentFile = open(file_name, "w", 8196) #Writes to disk (buffers to 1 Megabyte - ssd friendly)
        currentFile.write(''.join(fileBuffer)) #Writes the buffer to the disk
        currentFile.close() #Flush IO
        del fileBuffer #Calls the GC (hopefully) - Deletes list fileBuffer
    os.system("move "+file_name+" "+folder_name) #Closes and move file to folder, iterating again


finalTime_seconds = int(time.time() - startTime)
finalTime_minutes = finalTime_seconds // 60
finalTime_hours = finalTime_minutes // 60

#It rounds these two vars by 3 additionnal decimals, 
sampleFileSize = round((Decimal(os.path.getsize(folder_name + "/" + file_name) / 1024 / 1024)), 3) #gets the size of the LAST file generated in Bytes, then round it in Megabytes
folderSize = round((Decimal(get_folder_size(folder_name + "/") / 1024 / 1024)), 3) #gets the folder size in Bytes, round it in Megabytes

#Generation completed, shows time taken to complete and size of files
print("\n\n========\nGeneration completed!")
print("Number of files: "+str(num_files))
print("Sample file size:", str(sampleFileSize) + "Mb")
print("Folder size:", str(folderSize) + "Mb")
print("Generation time:", str(finalTime_seconds), "seconds (" + str(finalTime_minutes), "minutes (" + str(finalTime_hours), "hours))")
print("========")
os.system("pause")
sys.exit(0) #Exits the program with error code 0 (success)