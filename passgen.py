import string, os, sys, random, time, gc
from secrets import choice, token_hex
from decimal import Decimal
from colorama import init
from termcolor import cprint, colored
init() #Makes colors work on windows terminals

def get_folder_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

programVersion = "1.2"

print("MTLK's Password Generator")
print("Version", colored(programVersion, "cyan"))

print("====Selectionnez un mode====")
print("1/ Génération rapide ("+colored("hexadécimal", "yellow")+")")
print("2/ Génération lente ("+colored("ascii", "green")+")")

fast_gen = input(">")
if fast_gen == "1":
    fast_gen = True


#Requesting informations -
#must be int
num_files = int(input("[INT] Nombre de fichiers: "))
num_passwords = int(input("[INT] Nombre de codes: "))
num_bits_from = int(input("[INT] Nombre de caractères (début): "))
num_bits_to = int(input("[INT] Nombre de caractères (fin): "))
_BUFFERSIZE = int(input("[INT] Taille du buffer (16000000 recommandé): "))

#must be str
add_infos = str(input("[INT] Augmenter la verbosité? [1/0]: "))
folder_name = str(input("[STR] Nom du dossier (créer un nouveau si possible): "))
file_prefix = str(input("[STR] Préfixe du fichier: "))
file_extension = str(input("[STR] Extension du fichier (ex: .txt): "))

#creating folder, works on Windows / Linux
print("Création du dossier '" + colored(folder_name, "cyan") + "'...")

try:
    os.mkdir(folder_name)
except: #Assuming that the folder already exists
    print("->Le dossier existe peut-être déjà (returned OSError)")


#User selects charlist or create a new one

while True: #Loops menu if invalid choice is selected
    print("========")
    print("Veuillez séléctionnez une table de caractères:")
    print("1/ ASCII sans ponctuation")
    print("2/ ASCII avec ponctuation")
    print("3/ Créer une table")
    print("4/ Charger dans un fichier")
    charlistChoice = str(input("\n[INT] (1/2/3/4): "))

    if charlistChoice == "1": #Ascii w/o specials
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        break

    elif charlistChoice == "2": #Ascii w/ specials
        chars = string.punctuation + string.ascii_uppercase + string.ascii_lowercase + string.digits
        break

    elif charlistChoice == "3": #CUSTOM charlist (str)
        print("========")
        print("Veuillez entrer une table de caractères sur une ligne")
        print("Exemple: abcABC123?;!")
        chars = str(input("> "))
        break
    
    elif charlistChoice == "4":
        print("Veuillez spécfier le fichier (relatif - Exemple: Table.txt)")
        userFile = input("Fichier> ")
        
        try:
            fileChars = open(userFile, "r")
            chars = fileChars.read() #Tries to read and affect to the chars var
            fileChars.close()
            break

        except:
            cprint("Une erreur est survenue lors de l'ouverture du fichier", "red")
            cprint("Veuillez vérifier que celui-ci existe", "yellow")
            continue

    else:
        print("Invalid choice!")
        continue #Goes to the top of the while loop

print("========")
input("Appuyez sur [ENTRÉE] pour commencer") #like pause but with enter only
print("Veuillez patienter, cela peut prendre un moment")
print("========")
startTime = time.time() #Picking current time, to substract later

for mult in range(num_files): #For given number of files
    gc.collect() # Just in case
    file_name = file_prefix + str(mult) + file_extension
    print("Génération de", str(num_passwords), "codes dans", file_name, "...")
    currentFile = open(file_name, "w", _BUFFERSIZE) # Buffers to 16 Mbytes in RAM
    if fast_gen == True: #Fast generation; not secure
        currentFile = open(file_name, "w")
        for x in range(num_passwords):
            currentFile.write(token_hex(nbytes=num_bits_to)+"\n")
        currentFile.close()

    else: #Normal Gen mode
        if add_infos == "1": #if user requested to write add. infos in file
            currentFile.write("====Infos====\n")
            currentFile.write("bits per line (min): "+str(num_bits_from)+"\n")
            currentFile.write("bits per line (max): "+str(num_bits_to)+"\n")
            currentFile.write("char table: "+str(chars))
            currentFile.write("file name : "+str(file_name))
            currentFile.write("Buffer size : "+str(_BUFFERSIZE))
            currentFile.write("generator version: "+str(programVersion))
            currentFile.write("total codes: "+str(num_passwords)+"\n")
            currentFile.write("====Start====\n")
        
            for x in range(num_passwords):
                currentFile.write(str(x)+": "+''.join([choice(chars) for _ in range(random.randint(num_bits_from, num_bits_to))])+"\n")
        
        else: #Do not write additionnal infos in file
            for x in range(num_passwords): currentFile.write(''.join([choice(chars) for _ in range(random.randint(num_bits_from, num_bits_to))])+"\n")

    currentFile.close()
    print("-> Déplacement du fichier généré...")
    os.system("move "+file_name+" "+folder_name) #moves file to folder, iterating again if needed

finalTime_seconds = int(time.time() - startTime)
finalTime_minutes = finalTime_seconds // 60
finalTime_hours = finalTime_minutes // 60

#It rounds these two vars by 3 additionnal decimals, 
lastFileSize = round((Decimal(os.path.getsize(folder_name + "/" + file_name) / 1024 / 1024)), 3) #gets the size of the LAST file generated in Bytes, then round it in Megabytes
folderSize = round((Decimal(get_folder_size(folder_name + "/") / 1024 / 1024)), 3) #gets the folder size in Bytes, round it in Megabytes

#Generation completed, shows time taken to complete and size of files
print("\n\n========\n")
cprint("Terminé!", "green")
print("========")
print("Nombre de fichiers: "+str(num_files))
print("Taille du dernier fichier généré:", colored(str(lastFileSize) + " Mb", "cyan"))
print("Taille du dossier:", colored(str(folderSize) + " Mb", "magenta"))
print("Temps de génération:", str(finalTime_seconds), "secondes (" + str(finalTime_minutes), "minutes (" + str(finalTime_hours), "heures))")
print("========")
input("-> Press [ENTER] to continue...")
sys.exit()