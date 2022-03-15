print("=======================================================")
print("Custom resolution script for Over the Hedge for Windows")
print("Hack method by Czarman on Widescreen Gaming Forum")
print("Python script by JeffRuLz")
print("March 13th, 2022")
print("* NOTE: This patch replaces the 800x600 mode. *")
print("=======================================================")

# Hack method by Czarman
# https://www.wsgf.org/phpBB3/viewtopic.php?p=172308#p172308
#
# hedge.exe (4409KB version) addresses:
# Resolution addresses unknown. Encrypted exe?
#
# hedge.exe (3052KB version) addresses:
# 0x187C13 - Screen Width - 800 [20 03 00 00]
# 0x187C1A - Screen Height - 600 [58 02 00 00]

import os, shutil, stat, struct, sys, time

exe_names = ["hedge.exe"]
paths = [".\\", "C:\\Program Files (x86)\\Activision\\Over the Hedge\\"]
path = ""

width = 0
height = 0
version = -1

no_input_mode = False

def end_program():
    if no_input_mode == True:
        print("Closing in 3 seconds...")
        time.sleep(3)
    else:
        input("Press Enter to exit...")
    quit()
        
def backup_file(fpath):
    if os.path.exists(fpath + ".bak") == False:
        try:
            shutil.copyfile(fpath, fpath + ".bak")
            print("  Created backup file: " + fpath + ".bak")
            return True
        except:
            print("* ERROR: Could not create backup for *")
            print("* " + fpath + " *\n")
            return False
    else:
        return False
    
def load_file(fpath):
    try:
        f = open(fpath, "rb")
        mem = bytearray(f.read())
        f.close()
        return mem
    except:
        print("* ERROR: Could not read file *")
        print("* " + fpath + " *\n")
        return None
        
def write_file(fpath, mem):
    try:
        f = open(fpath, "wb")
        f.write(mem)
        f.close()
        print("  Wrote file: " + fpath)
        return True
    except:
        print("* ERROR: Could not write to file *")
        print("* " + fpath + " *\n")
        return False

def find_file(paths, files):
    for a in range(0, len(paths)):
        for b in range(0, len(files)):
            if os.path.exists(paths[a] + files[b]) == True:
                return paths[a] + files[b]
    return None
    
def hex_write_uint(mem, addr, val):
    byte = bytearray(struct.pack("I", val & 0xFFFFFFFF))
    mem[addr+0] = byte[0]
    mem[addr+1] = byte[1]
    mem[addr+2] = byte[2]
    mem[addr+3] = byte[3]
    
def version_check(mem):
    # 4409KB version
    if mem[0x57570] == 0x62:
        if mem[0xF3DF4] == 0x8F:
            if mem[0x20DA48] == 0x47:
                if mem[0x2A442D] == 0x79:
                    return 0
    # 3052KB version
    if mem[0x57570] == 0x06:
        if mem[0xF3DF4] == 0x0F:
            if mem[0x20DA48] == 0x20:
                if mem[0x2A442D] == 0x79:
                    return 1
    return -1
    

# command line arguments
n = len(sys.argv)
if n > 1:
    no_input_mode = True
    error = False
    
    try:
        for i in range(1, n):        
            if sys.argv[i] == "-w":
                width = int(sys.argv[i+1])
            if sys.argv[i] == "-h":
                height = int(sys.argv[i+1])
        
        if width == 0 or height == 0:
            error = True
    except:
        error = True
        
    if error == True:
        print("* ERROR: Invalid arguments. *")
        print("* Usage: script.py -w [width] -h [height] *")
        print("* Or don't use any arguments for manual mode. *\n")
        end_program()
        
# check if exe exists
path = find_file(paths, exe_names)
if path == None:
    print("* ERROR: " + exe_names[0] + " was not found. *")
    print("* Run this script from the same location as the game's exe file. *\n")
    end_program()
    
print("Found: " + path)

# load file into memory
mem = load_file(path)
if mem == None:
    end_program()
    
# check compatibility
version = version_check(mem)
if version == -1:
    print("* ERROR: Byte check failed. *")
    print("* Your version of the game is not compatible with this script. *\n")
    end_program()
elif version == 0:
    print("* ERROR: 4409KB version detected. *")
    print("* Your version of the game is not compatible with this script. *")
    print("* See the PCGamingWiki page for an alternative method. *\n")
    end_program()
elif version == 1:
    print("  3052KB version detected\n")
    
# resolution prompt
if no_input_mode == True:
    print("Width: " + str(width))
    print("Height: " + str(height) + "\n")
else:
    try:
        print("Enter screen width:")
        width = int(input())
        print("Enter screen height:")
        height = int(input())
        print("")
    except:
        print("* ERROR: Invalid input. *")
        print("* Only whole numbers may be accepted. *\n")
        end_program()
        
# resolution hack start
print("Modifying " + path)

backup_file(path)
    
# screen width
address = [0x0, 0x187C13]
hex_write_uint(mem, address[version], width)
print("  Screen width: " + str(hex(width)) + " @ " + str(hex(address[version])))

# screen height
address = [0x0, 0x187C1A]
hex_write_uint(mem, address[version], height)
print("  Screen height: " + str(hex(height)) + " @ " + str(hex(address[version])))

# update file  
if write_file(path, mem) == False:
    end_program()  
print("")
end_program()