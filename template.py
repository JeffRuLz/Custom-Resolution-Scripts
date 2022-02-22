print("==============================================================")
print("Custom resolution script for [Game Title] for Windows")
print("Hack method by [Widescreen hack creator]")
print("Python script by [Your name here]")
print("[today's date]")
print("* NOTE: [importaint information that no one will read] *")
print("* [no one will read this line either] *")
print("==============================================================")

# Include a written explaination of the widescreen hack in case the script
# doesn't work for certain versions of the game

import os, shutil, stat, struct, sys, time, winreg

exe_names = ["game.exe", "juego.exe"]
paths = [".\\", "C:\\Program Files (x86)\\Default Install Path\\"]
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
    #if mem[0x] == 0x:
    #    if mem[0x] == 0x:
    #        if mem[0x] == 0x:
    #            if mem[0x] == 0x:
    #                return 0
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
    
print("Found: " + path + "\n")

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
    
# ============= Actual work goes here ==================
#
#
#
#
#
#
#
#
#
#
# ======================================================
    
end_program()