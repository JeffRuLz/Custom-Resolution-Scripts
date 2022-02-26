### Custom Resolution Scripts
A collection of python scripts used to apply resolution/widescreen patches to PC games.

Whenever I look for a widescreen hack for an old computer game I will often find pre-patched exes for specific resolutions or a guide on how to edit the game with a hex editor. My goal is to automate the process with an easy to use script.

These hack methods are often created by other people. Open the script in a text editor to find a link to the source and a written explanation of the hack.

### Download Scripts
Right-click and select 'Save Link As...'

[Nickelodeon Barnyard](https://raw.githubusercontent.com/JeffRuLz/Custom-Resolution-Scripts/main/scripts/Barnyard_res_patch.py) (Widescreen works, ultrawide does not)

### Usage
1. Install [Python 3](https://www.python.org/downloads/) if you have not already.
2. Place the script in the same location as the game's exe file.
3. Double-click the script and follow the directions. Optionally, run the script with the arguments `script.py -w [width] -h [height]`

### Help
#### I got an error message saying my version of the game is unsupported.
I mainly play US or English versions of games. Create a new issue and include the exe file from your copy of the game.

#### When I double-click on the script it opens and closes right away.
Run the script in a command prompt, copy the error message, create a new issue and post it there.

#### Something went wrong and I want to undo the changes.
The script will try to create a backup ([game.exe].bak) before changing a file. Delete the modified file and remove the .bak extension from the backup file.

#### The script finished without error but the resolution did not change.
Read the note at the start of the script and make sure you change the in-game resolution to the one that is being replaced.

Make sure you're using a resolution that is supported by your graphics card. You may need to create a custom resolution profile for unusual resolutions.

Some games just react poorly to certain resolutions. I often test 1280x720, 1440x1080, 1920x1080, and 1920x800 and leave a note if one doesn't work.
