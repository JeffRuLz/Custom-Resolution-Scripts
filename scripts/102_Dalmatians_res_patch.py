print("=========================================================================")
print("Custom resolution script for 102 Dalmatians: Puppies to the Rescue for PC")
print("Hack method by Nastys on PCGamingWiki")
print("Python script by JeffRuLz")
print("March 6th, 2022")
print("* NOTE: This patch will only change the aspect ratio. Use dgVoodoo2 to *")
print("* force higher resolutions. *")
print("=========================================================================")

# Widescreen hack by Nastys on PCGamingWiki
# www.pcgamingwiki.com/wiki/102_Dalmatians:_Puppies_to_the_Rescue#Widescreen_resolution
#
# Higher resolutions can only be forced with dgVoodoo2.
#
# Pcdogs.exe (English) addresses:
# 0x50F60 - Horizontal aspect ratio - 4096 [00 10 00 00]
#
# Pcdogs.exe (French/German/Italian/Spanish/Dutch) addresses:
# 0x52F58 - Horizontal aspect ratio - 4096 [00 10 00 00]

import os, shutil, stat, struct, sys, time

exe_names = ["Pcdogs.exe"]
paths = [".\\", "C:\\Program Files\\Disney Interactive\\102 Dalmatians\\"]
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
    #english version
    if mem[0x4B90] == 0x75:
        if mem[0x1C0A4] == 0x03:
            if mem[0x39D38] == 0x8B:
                if mem[0x561CC] == 0x38:
                    return 0
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
    print("  English version detected.\n")
    
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
    
aspect = int( 4096 * float(4/3) / float(width/height) )
address = [0x50F60, 0x52F58]
hex_write_uint(mem, address[version], aspect)
print("  Aspect ratio: " + str(hex(aspect)) + " @ " + str(hex(address[version])))

# update file  
if write_file(path, mem) == False:
    end_program()  
print("")
end_program()