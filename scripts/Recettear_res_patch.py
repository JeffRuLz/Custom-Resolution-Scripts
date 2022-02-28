print("==================================================================")
print("Custom resolution script for Recettear: An Item Shop's Tale for PC")
print("Hack method and script by JeffRuLz")
print("February 28th, 2022")
print("* NOTE: Only 4:3 ratios are supported for now. *")
print("* This hack replaces the 1280x960 resolution setting. *")
print("==================================================================")

# Replaces the 1280x960 resolution setting.
# Widescreen hack is incomplete. 2D elements are not positioned correctly.
# The 2D "screen" scales with the screen width, cutting off the bottom if wider than 4:3
#
# recettear.exe version 1.108 addresses:
# 0x79B91 - Screen Width - 1280 [00 05 00 00]
# 0x79B9B - Screen Height - 960 [C0 03 00 00]
# 0x117D38 - 3D Aspect Ratio - 1.33333 [AB AA AA 3F]
#
# Steam version encrypts the exe. Use the official patch to remove DRM.
# http://www.carpefulgur.com/recettear/downloads.htm

import configparser, os, shutil, stat, struct, sys, time

exe_names = ["recettear.exe"]
custom_names = ["custom.exe"]
config_names = ["recet.ini"]
paths = [".\\"]
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
    
def disable_read_only(fpath):
    try:
        os.chmod(fpath, stat.S_IWRITE)
        return True
    except:
        return False
        
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
    byte = bytearray(struct.pack('H', val & 0xFFFF))
    mem[addr+0] = byte[0]
    mem[addr+1] = byte[1]
    
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
    
def hex_write_string(mem, addr, text):
    for i in range(0, len(text)):
        mem[addr+i] = ord(text[i])
    
def registry_read(reg_path, name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return value
    except WindowsError:
        return None
    
def registry_write(reg_value, name, val):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, val)
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False
    
def version_check(mem):
    #GOG 1.108
    if mem[0xE02] == 0xD4:
        if mem[0x9DB76] == 0x74:
            if mem[0x2A2EB8] == 0xF2:
                if mem[0x36339A] == 0x57:
                    return 0                    
    #steam
    if mem[0xE02] == 0x77:
        if mem[0x9DB76] == 0xD3:
            if mem[0x2A2EB8] == 0xF2:
                if mem[0x36339A] == 0x57:
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
    print("  version 1.108\n")
elif version == 1:
    print("  Steam version 1.108")
    print("* ERROR: Steam version is unsupported. *")
    print("* Install the official patch to remove DRM. *")
    print("http://www.carpefulgur.com/recettear/downloads.htm\n")
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

if backup_file(path) == True:
    print("  Created backup file: " + path + ".bak")
    
# screen width
address = [0x79B91]
width = int(height * (4/3))
hex_write_uint(mem, address[version], width)
print("  Screen Width: " + hex(width) + " @ " + hex(address[version]))

# screen height
address = [0x79B9B]
hex_write_uint(mem, address[version], height)
print("  Screen Height: " + hex(height) + " @ " + hex(address[version]))

# aspect ratio
#address = [0x117D38]
#aspect = float(width / height)
#hex_write_float(mem, address[version], aspect)
#print("  Aspect Ratio: " + str(aspect) + " @ " + hex(address[version]))

# 2D x pointer
#address = [0x43AE]
#ptr = 0x099532C0
#hex_write_uint(mem, address[version], ptr)
#print("  2D X Offset Ptr: " + hex(ptr) + " @ " + hex(address[version]))

# 2D screen x offset
#address = [0x5062C0]
#temp_w = int(height * (640.0/480.0))
#xoffset = int((width - temp_w) / 2)
#hex_write_uint(mem, address[version], xoffset)
#print("  2D X Offset: " + hex(xoffset) + " @ " + hex(address[version]))

# 2D width pointer
#address = [0x4317]
#ptr = 0x909532C8
#hex_write_uint(mem, address[version], ptr)
#print("  2D Width Ptr: " + hex(ptr) + " @ " + hex(address[version]))

# 2D screen width
#address = [0x5062C8]
#hex_write_float(mem, address[version], float(temp_w))
#print("  2D Width: " + str(temp_w) + " @ " + hex(address[version]))

if write_file(path, mem) == False:
    print("* ERROR: Could not overwrite " + path + " *\n")
    end_program()
else:
    print("  Overwrote " + path + "\n")
    
# change screen size in config file
path = find_file(paths, config_names)
if path == None:
    print("* ERROR: Could not find " + config_names[0] + " *")
    print("* Use custom.exe to change the resolution to 1280x960. *")
else:
    config = configparser.ConfigParser()
    config.read(path)
    if config.getint('setup', 'screen') != 3:   
        print("Modifying " + path)
        if backup_file(path) == True:
            print("  Created backup file: " + path + ".bak")

        config = configparser.ConfigParser()
        config.read(path)
        config.set('setup', 'screen', '3')
        with open(path, 'w') as configfile:
            config.write(configfile)  

        print("  [setup]")
        print("  screen = 3\n")

end_program()