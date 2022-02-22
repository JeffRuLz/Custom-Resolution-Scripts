print("===============================================================")
print("Custom resolution script for Nickelodeon's Barnyard for Windows")
print("Hack method by AuToMaNiAk005")
print("Python script by JeffRuLz")
print("February 22nd, 2022")
print("* NOTE: The game will reject some resolutions and *")
print("* default to 800x600. (Such as ultra wide aspect ratios.) *")
print("===============================================================")

# Widescreen hack by AuToMaNiAk005 on youtube
# https://www.youtube.com/watch?v=HB0yvDiOiXE
#
# Right click on Barnyard.exe, click properties, and uncheck read-only.
# Open Barnyard.exe in a hex editor.
# At address 0x23563A replace '00 00 48 44' with:
#    00 40 85 44 for 16:9
#    00 00 70 44 for 16:10
#    00 80 3B 44 for 5:4
#    00 80 6A 44 for 25:16
#    00 00 7A 44 for 15:9
# At address 0x262DFD replace '20 03' with your width:
#    00 05 for 1280
#    56 05 for 1366
#    80 07 for 1920
#    00 0A for 2560
#    00 0F for 3840
# At address 0x262E05 replace '58 02' with your height:
#    D0 02 for 720
#    00 03 for 768
#    38 04 for 1080
#    A0 05 for 1440
#    70 08 for 2160
# At address 0x3081D6 replace '92 0A 86 3F' with:
#    62 10 A8 3F for 16:9
#    1D B9 9C 3F for 16:10
#    D6 83 7E 3F for 5:4
#    91 95 97 3F for 25:16
#    EE 8E 9F 3F for 15:9
#
# Right click on Setup.exe, click properties, and uncheck read-only.
# Open Setup.exe in a hex editor.
# At address 0xB06C replace '20 03' with your width. See above.
# At address 0xB070 replace '58 02' with your height. See above.
#
# Run Setup.exe and choose your new resolution.
# Or change the resolution registry values manually.
# HKEY_CURRENT_USER\Software\THQ\Barnyard\Width
# HKEY_CURRENT_USER\Software\THQ\Barnyard\Height

import os, shutil, stat, struct, sys, time, winreg

exe_names = ["Barnyard.exe"]
setup_names = ["Setup\\Setup.exe"]
paths = [".\\", "C:\\Program Files (x86)\\THQ\\Blue Tongue Entertainment\\Barnyard\\"]
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
        f = open(path, "wb")
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
    
def hex_write_uint(mem, addr, val):
    byte = bytearray(struct.pack("I", int(val)))
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
    if mem[0x12E6] == 0xEC:
        if mem[0xC08EC] == 0x40:
            if mem[0x19FCC0] == 0xC7:
                if mem[0x340A34] == 0x53:
                    return 0
    return -1
    
def version_check_setup(mem):
    if mem[0xB2] == 0x54:
        if mem[0x4755] == 0xC7:
            if mem[0x7458] == 0xF2:
                if mem[0xC02C] == 0x88:
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
    print("* Run this script from the same location as the game's .exe. *\n")
    end_program()
        
print("Found: " + path + "\n")
    
# load file into memory
mem = load_file(path)
if mem == None:
    print("\n* ERROR: Error reading " + path + " *\n")
    end_program()    

# version check
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
    
# game modifications
print("Modifying " + path)

if backup_file(path) == True:
    print("  Created backup file: " + path + ".bak")

# HUD width
fov = float(600 * width / height)

address = [0x23563A]
hex_write_float(mem, address[version], fov)
print("  HUD width: " + str(fov) + " @ " + str(hex(address[version])))

# screen width
address = [0x262DFD]
hex_write_ushort(mem, address[version], width)
print("  Screen width: " + str(hex(width)) + " @ " + str(hex(address[version])))

# screen height
address = [0x262E05]
hex_write_ushort(mem, address[version], height)
print("  Screen height: " + str(hex(height)) + " @ " + str(hex(address[version])))

# screen FOV
default_fov = 1.04719758
temp_width = 600 * (width / height)
fov = float(default_fov + (1.0 - (800/temp_width)))

address = [0x3081D6]
hex_write_float(mem, address[version], fov)
print("  FOV: " + str(fov) + " @ " + str(hex(address[version])))

# update file
if disable_read_only(path) == False:
    print("* WARNING: Could not disable read-only mode. *")
    
if write_file(path, mem) == True:
    print("  Overwrote " + path + "\n")
else:
    print("* ERROR: Could not overwrite " + path + " *\n")
    end_program()    

# modify Setup.exe
path = find_file(paths, setup_names)
if path == None:
    print("* WARNING: Could not find " + setup_names[0] + " *\n")
else:
    print("Modifying " + path)
    backup_file(path)
        
    mem = load_file(path)
    if mem == None:
        print("* WARNING: Could not read " + path + " *")
        print("* " + path + " will not be changed. *\n")
    else:
        version = version_check_setup(mem)
        if version == -1:
            print("* WARNING: Byte check failed. *")
            print("* " + path + " will not be changed. *\n")
        else:    
            # screen width
            address = [0xB06A]
            hex_write_uint(mem, address[version], width)
            print("  Screen width: " + str(hex(width)) + " @ " + str(hex(address[version])))

            # screen height
            address = [0xB06E]
            hex_write_uint(mem, address[version], height)
            print("  Screen height: " + str(hex(height)) + " @ " + str(hex(address[version])))

            # update file
            if disable_read_only(path) == False:
                print("* WARNING: Could not disable read-only mode. *")
                
            if write_file(path, mem) == True:
                print("  Overwrote " + path + "\n")
            else:
                print("* WARNING: Could not overwrite " + path + " *\n")                

# update registry values
reg_path = r"Software\THQ\Barnyard"
if registry_read(reg_path, "Width") != None and registry_read(reg_path, "Height") != None:
    print("Updating registry values.")
    registry_write(reg_path, "Width", width)
    print("  HKEY_CURRENT_USER\\" + reg_path + "\\Width = " + str(width))
    registry_write(reg_path, "Height", height)
    print("  HKEY_CURRENT_USER\\" + reg_path + "\\Height = " + str(height) + "\n")
else:
    print("* WARNING: Could not update registry values. *")
    print("* Set your resolution with Setup.exe. *\n")

end_program()