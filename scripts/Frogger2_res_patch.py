print("==================================================")
print("Custom resolution script for Frogger 2 for Windows")
print("Hack method and python script by JeffRuLz")
print("February 26th, 2022")
print("==================================================")

# Frogger 2 stores its resolution setting in:
# HKEY_CLASSES_ROOT\VirtualStore\MACHINE\SOFTWARE\Wow6432Node\Hasbro Interactive\Frogger2\Resolution
# Width and height are 16 bits each, stored in a single 32 bit value.
#
# Game install directory can be found at:
# HKEY_CLASSES_ROOT\VirtualStore\MACHINE\SOFTWARE\Wow6432Node\Hasbro Interactive\Frogger2\InstallDir
# 
# Widescreen resolution works but cuts off the top and bottom of the screen.
# I could not find the FOV modifier value.

import os, shutil, stat, struct, sys, time, winreg

exe_names = ["Frogger2.exe"]
paths = [".\\", "C:\\Program Files (x86)\\Hasbro Interactive\\Frogger2\\"]
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
        print("  Allowed write permission for " + fpath)
        return True
    except:
        print("* WARNING: Could not disable read-only permission. *")
        print("* " + fpath + " *")
        return False
        
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
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, reg_path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return value
    except WindowsError:
        return None
        
def registry_read_string(reg_path, name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, reg_path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return value
    except WindowsError:
        return None
    
def registry_write(reg_value, name, val):
    try:
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path)
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, val)
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False
    
def version_check(mem):
    if mem[0x1000] == 0x56:
        if mem[0x19E64] == 0x7C:
            if mem[0x42C39] == 0x34:
                if mem[0x73F7E] == 0x76:
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
reg_path = r"VirtualStore\MACHINE\SOFTWARE\Wow6432Node\Hasbro Interactive\Frogger2"
#installDir = registry_read_string(reg_path, "InstallDir")
#if installDir != None:
#    paths.insert(0, installDir)

#path = find_file(paths, exe_names)
#if path == None:
#    print("* ERROR: " + exe_names[0] + " was not found. *")
#    print("* Run this script from the same location as the game's exe file. *\n")
#    end_program()
    
#print("Found: " + path + "\n")

# load file into memory
#mem = load_file(path)
#if mem == None:
#    end_program()
    
# check compatibility
#version = version_check(mem)
#if version == -1:
#    print("* ERROR: Byte check failed. *")
#    print("* Your version of the game is not compatible with this script. *\n")
#    end_program()
    
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
#print("Modifying " + path)

#backup_file(path)
    
val = (width << 16) | height

if registry_read(reg_path, "Resolution") == None:
    print("* ERROR: Could not find registry value: *")
    print("* HKEY_CLASSES_ROOT\\" + reg_path + "\\Resolution *\n")
    end_program()
else:
    print("Updating registry value.")
    registry_write(reg_path, "Resolution", val)
    print("  HKEY_CLASSES_ROOT\\" + reg_path + "\\Resolution = " + hex(val) + "\n")

# update file  
#if write_file(path, mem) == False:
#    end_program()  
    
end_program()