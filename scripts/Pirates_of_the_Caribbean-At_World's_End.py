print("============================================================================")
print("Custom resolution script for Pirates of the Caribbean: At World's End for PC")
print("Hack method by Squ1zZy at Widescreen Gaming Forum")
print("Python script by JeffRuLz")
print("February 22nd, 2022")
print("* NOTE: This will replace the in-game 640x480 resolution option. *")
print("* Large resolutions will cause the HUD to become very small. *")
print("============================================================================")

# Widescreen hack by Squ1zZy at Widescreen Gaming Forum
# https://www.wsgf.org/dr/pirates-caribbean-worlds-end/en
#
# Open 'At Worlds End.exe' in a hex editor.
# At address 0x35E4E replace '80 02' with your screen width.
# At address 0x35E54 replace 'E0 01' with your screen height.
# Address 0x1E7DA4 holds the text string '640 x 480'
# Change the in-game resolution.

import os, shutil, struct, sys, time

exe_names = ["At Worlds End.exe"]
paths = [".\\", "C:\\Program Files (x86)\\Disney Interactive Studios\\Pirates of the Caribbean - At Worlds End\\"]
path = ""

width = 0;
height = 0;
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
        shutil.copyfile(fpath, fpath + ".bak")
        return True
    else:
        return False
    
def load_file(fpath):
    try:
        f = open(fpath, "rb")
        mem = bytearray(f.read())
        f.close()
        return mem
    except:
        return None
        
def write_file(fpath, mem):
    try:
        f = open(fpath, "wb")
        f.write(mem)
        f.close()
        return True
    except:
        return False

def find_file(paths, files):
    for a in range(0, len(paths)):
        for b in range(0, len(files)):
            if os.path.exists(paths[a] + files[b]) == True:
                return paths[a] + files[b]
    return None
    
def hex_write_ushort(mem, addr, val):
    byte = bytearray(struct.pack('H', int(val) & 0xFFFF))
    mem[addr+0] = byte[0]
    mem[addr+1] = byte[1]
    
def hex_write_string(mem, addr, text):
    for i in range(0, len(text)):
        mem[addr+i] = ord(text[i])
    
def version_check(mem):
    # retail version
    if mem[0x96681] == 0x24:
        if mem[0x15A254] == 0xE9:
            if mem[0x25D237] == 0x3B:
                if mem[0x383F2C] == 0xB1:
                    return 0
                    
    # Alt version (Steam? Exe version provided by Squ1zZy)
    if mem[0x96681] == 0x46:
        if mem[0x15A254] == 0x5D:
            if mem[0x25D237] == 0x72:
                if mem[0x383F2C] == 0x9B:
                    return 1
        
    return -1

# === command line arguments ===
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
    print("* Run this script from the same location as the game's .exe. *\n")
    end_program()
    
print("Found: " + path)
        
# load file into memory
mem = load_file(path)
if mem == None:
    print("\n* ERROR: Error reading " + path + " *\n")
    end_program()

# check compatibility
version = version_check(mem)
if version == -1:
    print("* ERROR: Byte check failed. *")
    print("* Your version of the game is not compatible with this script. *\n")
    end_program()
elif version == 0:
    print("  Retail version detected.\n")
elif version == 1:
    print("  Alt version detected.\n")

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

if backup_file(path) == True:
    print("  Created backup file: " + path + ".bak")
    
# screen width
address = [0x35E6E, 0x35E4E]
hex_write_ushort(mem, address[version], width)
print("  Screen width: " + str(hex(width)) + " @ " + str(hex(address[version])))

# screen height
address = [0x35E74, 0x35E54]
hex_write_ushort(mem, address[version], height)
print("  Screen height: " + str(hex(height)) + " @ " + str(hex(address[version])))

# format resolution text string
max_len = 11
text = '{w} x {h}'.format(w=width, h=height)
if len(text) > max_len:
    text = '{w}x{h}'.format(w=width, h=height)
# add trailing 0 value characters
l = len(text)
for i in range(l, max_len):
    text = text + chr(0)
text = text[:max_len]

address = [0x1E7C44, 0x1E7DA4]
hex_write_string(mem, address[version], text)
print("  Text '" + text + "' @ " + str(hex(address[version])))

# update file
if write_file(path, mem) == True:
    print("  Overwrote " + path + "\n")
else:
    print("* ERROR: Could not overwrite " + path + " *\n")
    end_program()
    
# update config file

        
end_program()