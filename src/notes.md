make new venv  
    `python3.12 -m venv venv`  
activate it  
    `. venv/bin/activate`  
install requirements  
    `pip install -r requirements.txt`  
run thonny  
    `thonny`  
    (it's possible you will also need to install tk from apt `sudo apt install python3.12-tk`)

plug in pi pico w while holding the button. click the bottom right edge of the thonny window, and choose install micropython. family: RP2, variant: pico w, version: 1.24.1. Version may be newer by the time you are doing this, use that version and fix any bugs that crop up. if you insist on using not the latset version of micropython, make sure you pip install the matching version of mpremote as well. click install, wait, click close. click the stopsign button to connect to the board, and go to view>files to make sure there are no other files on the board. click the bottom right and choose local python (or just close thonny). this frees the board so mpremote can do its thing later.  

edit `networks.py.example` to add the wifi networks you want to connect to and save as `networks.py`  

make a note of the wifi password in `host.py` should it be needed. change the settings in there too if you want.  

in `menorah.py` near the top is a tuple called `pins`. if yours ends up wired different (almost certainly) you will need to come back here and change the order of this tuple to match what you actually built. there are also some buttons that need to be on the correct pins (or left off completely).

run setup.py  
    `python setup.py`  
this will install all the libraries and copy all the files needed into the pi pico w. it will then try to run `main.py` on the board. this is just for convenience, the board will always run `main.py` when it first powers on. you can run `setup.py` again whenever you want. pass `-u` to force it to redownload libraies (for updates) or pass `-i` to skip checking for libraries at all (faster, but the libraries still better be there). Note that the board itself will also check for the libraries and even try its best to obtain them itself when it runs. `-i` will not disable that check.
