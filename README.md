# DISCLAIMER
**Due to problems with the Aubio Python library, this program is not working anymore. I started this project to learn more about audio programming with Python. It's been a long time since I made this, and I think the project has already fulfilled its original purpose, which was for people, including myself, to learn something from it. I at least know I did back when I made this. As such, I will not be attempting to fix this program, as I also believe it not to be worth the effort. The program still serves its original educative purpose. I hope this project is of use to anyone, and if anyone wants to fix the program, feel free to fork the repository. I wish anyone reading this a nice day! Thanks for checking out one of my old projects.**
# Proteus Voice Changer
A program that gives the user the ability to change the pitch of an audio file to that of another. It also allows you to adjust the pitch manually.

## Download and Installation instructions

**Linux**
- Clone the repository: ```$ git clone https://github.com/0x736e6f776f776c/Proteus-Voice-Changer/```
- ```cd``` into the repository: ```cd Proteus-Voice-Changer```
- Install the requirements.txt:
- Run main.py: ```python3 main.py```

### Usage
- Run the script.
- Once the window shows up, you can use the buttons to navigate through the GUI.
- You can use the button below the Proteus image to switch between mimic and manual mode.
- You can press the question mark **'?'** button to read instructions on how to use the mode you are currently in.
#### Mimic mode
- Use the button under the Proteus image to go into mimic mode.
- Left side (Input file): click the 'Browse files' button, select the file of which you want to change the pitch. After selecting the file, you should be able to see the path to the directory on the left side of the Proteus image.
- Right side (Modifier file): click the 'Browse files' buttom, select the file you want to extract the pitch from. After selecting the file, you should be able to see the path to the directory on the right side of the Proteus image.
- You can now click on the Proteus image. You will be asked to choose where you want to save the output file. Once you've chosen a driectory, the Proteus algorithm wil apply the pitch of the modifier file to the contents of the input file and produce an ouput file in your destination folder. If all went well, you should receive a message confirming this. 



**Project transferred to a new repository for privacy-related reasons, I originally made this project in 2018**

The mimic modification process is now done.
#### Manual mode
- Use the button under the Proteus image to go into manual mode.
- Left side (Input file): click the 'Browse files' button, select the file of which you want to change the pitch. After selecting the file, you should be able to see the path to the directory on the left side of the Proteus image.
- Right side (Set pitch): type the desired pitch in Hertz (Hz) in the textfield under 'Set pitch'. Press the 'Set pitch' button to set the pitch you have entered as the modification pitch. You'll see what it's currently set to on the right side of the Proteus image.
- You can now click on the Proteus image. You will be asked to choose where you want to save the output file. Once you've chosen a driectory, the Proteus algorithm wil apply the pitch you've set to the contents of the input file and produce an ouput file in your destination folder. If all went well, you should receive a message confirming this. 
The manual modification process is now done.
