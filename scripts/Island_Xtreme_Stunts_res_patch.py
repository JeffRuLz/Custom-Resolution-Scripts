print("========================================================")
print("Custom resolution script for Island Xtreme Stunts for PC")
print("Hack method and Python script by JeffRuLz")
print("March 5th, 2022")
print("* NOTE: This patch only changes the aspect ratio. *")
print("* You need to use a program like dgVoodoo2 to run at *")
print("* higher resolutions. *")
print("========================================================")

# Patch only works with the "new" version of the game. See the PCGamingWiki page on how to upgrade.
# https://www.pcgamingwiki.com/wiki/Island_Xtreme_Stunts
#
# Changing the resolution forces the HUD into 640x480 in the center of the screen.
# Use dgVoodoo2 to force resolutions instead of patching.
#
# Game.exe ("new" version) addresses:
# 0x9F09 - Aspect ratio - 1.33333 [AB AA AA 3F]
# 0x9F17 - FOV - 512 [00 02 00 00]
# 0x1A79F8 - Screen Width - 1280 [00 05 00 00]
# 0x1A79FC - Screen Height - 1024 [00 04 00 00]

import os, shutil, struct, sys, time

exe_names = ["Game.exe"]
paths = [".\\", "C:\\Program Files (x86)\\LEGO Interactive\\Island Xtreme Stunts\\"]
path = ""

width = 0
height = 0
version = -1

no_input_mode = False
change_resolution = False

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
    
def hex_write_float(mem, addr, val):
    byte = bytearray(struct.pack("f", float(val)))
    mem[addr+0] = byte[0]
    mem[addr+1] = byte[1]
    mem[addr+2] = byte[2]
    mem[addr+3] = byte[3]
    
def version_check(mem):
    #"old" version
    if mem[0x5B32] == 0x01:
        if mem[0xDDCA4] == 0x1A:
            if mem[0x1C6B63] == 0x09:
                if mem[0x2BE90E] == 0x3A:
                    return 0
    #"new" version
    if mem[0x5B32] == 0xF6:
        if mem[0xDDCA4] == 0xE4:
            if mem[0x1C6B63] == 0xEF:
                if mem[0x2BE90E] == 0x09:
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
            elif sys.argv[i] == "-h":
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
    print("* ERROR: Random byte check failed. *")
    print("* Your version of the game is not compatible with this script. *\n")
    end_program()
if version == 0:
    print("* ERROR: Old version detected. *")
    print("* See the pcgamingwiki page on how to upgrade. *")
    print("* www.pcgamingwiki.com/wiki/Island_Xtreme_Stunts *\n")
    end_program()
elif version == 1:
    print("  New version detected.\n")
    
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

if change_resolution == True:
    #screen width
    address = [0x00, 0x1A79F8]
    hex_write_uint(mem, address[version], width)
    print("  Screen width: " + str(hex(width)) + " @ " + str(hex(address[version])))

    #screen height
    address = [0x00, 0x1A79FC]
    hex_write_uint(mem, address[version], height)
    print("  Screen height: " + str(hex(height)) + " @ " + str(hex(address[version])))

aspect = float(width / height)
address = [0x00, 0x9F09]
hex_write_float(mem, address[version], aspect)
print("  Aspect ratio: " + str(aspect) + " @ " + str(hex(address[version])))

default_fov = 512
temp_width = 600 * (width / height)
fov = int(float(default_fov * float(temp_width/800)))
address = [0x00, 0x9F17]
hex_write_uint(mem, address[version], fov)
print("  FOV: " + str(hex(fov)) + " @ " + str(hex(address[version])))

# === update file ===
if write_file(path, mem) == False:
    end_program()
print("")
end_program()