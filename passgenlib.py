import os

def get_folder_size(start_path): #Gets size of folder in Bytes (recursive)
    total_size = 0
    for dirpath, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size