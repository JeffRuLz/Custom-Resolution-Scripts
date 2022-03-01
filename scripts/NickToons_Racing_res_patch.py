print("=========================================================")
print("Custom resolution script for NickToons Racing for Windows")
print("Hack method and script by JeffRuLz")
print("February 28th, 2022")
print("=========================================================")

# NickToonsRacing.cfg addresses:
# 0x0 - Screen Width - 640 [80 02 00 00]
# 0x4 - Screen Height - 480 [e0 01 00 00]

import os, shutil, stat, struct, sys, time

config_names = ["NickToonsRacing.cfg"]
paths = [".\\", "C:\\Program Files (x86)\\Hasbro Interactive\\NickToons Racing\\"]
path = ""

width = 0
height = 0
version = 0

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
path = find_file(paths, config_names)
if path == None:
    print("* ERROR: " + config_names[0] + " was not found. *")
    print("* Run this script from the same location as the game's exe file. *")
    print("* Run the game at least once. *")
    end_program()
    
print("Found: " + path + "\n")

# load file into memory
mem = load_file(path)
if mem == None:
    end_program()
    
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
address = [0x0]
hex_write_uint(mem, address[version], width)
print("  Screen Width: " + str(hex(width)) + " @ " + str(hex(address[version])))

# screen height
address = [0x4]
hex_write_uint(mem, address[version], height)
print("  Screen Height: " + str(hex(height)) + " @ " + str(hex(address[version])))

# update file  
if write_file(path, mem) == False:
    end_program()  
print("")
end_program()