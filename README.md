# MakeCode-Arcade-to-Electron

This is a simple script that allows you to convert your MakeCode Arcade games
to a standalone offline-capable Electron app!

## Install

1. Have Python and Node.js installed and available at the command line. (on
   PATH)
2. Clone this repo.
3. Install [`requirements.txt`](./requirements.txt). (to a virtual
   environment is recommended)

## Usage

1. Have a MakeCode Arcade game on GitHub.
2. Deploy to GitHub Pages by creating a release and noting the version number.
   (This script relies on the game being compiled on GitHub Pages)
3. Run [`src/main.py`](./src/main.py). Use `-h` to view all arguments.
   For example, if I want to convert
   [Racers!](https://github.com/UnsignedArduino/Racers) v1.3.1 to an Electron
   app, I would run:
   ```sh
   python src/main.py -r "UnsignedArduino/Racers" ^
   -v "1.3.1" -n "Racers" -a "Cyrus Yiu" ^
   -d "Enjoy the high-speed thrills of car racing in MakeCode Arcade! For the MakeCode Arcade Mini Game Jam #3." ^
   -i "C:\Users\ckyiu\Downloads\icon.png"
   ```

   (yes I use Windows command prompt)

   Check the help text for what each argument does. On successful completion,
   it will list the directory where the Electron app is located.

### Icons for your Electron app

If you want to have an icon for your Electron app, you can pass in a path to an
image file that is able to be read by Python's Pillow library. It is
recommended that the size be 512x512px. If you want to convert your MakeCode
Arcade images to an actual image, follow the instructions in
[this](https://forum.makecode.com/t/turning-arcade-images-into-actual-images/25831/3?u=unsignedarduino)
forum post.

### Help

Current help text: (It is recommended that you check in the terminal for the
most up-to-date help text.)

```
E:\MakeCode-Arcade-to-Electron\.venv\Scripts\python.exe E:\MakeCode-Arcade-to-Electron\src\main.py -h 
2024-10-30 21:28:03,058 - utils.download - DEBUG - Created logger named 'utils.download' with level 10
2024-10-30 21:28:03,058 - utils.download - DEBUG - Handlers for 'utils.download': [<StreamHandler <stdout> (DEBUG)>, <StreamHandler <stderr> (WARNING)>]
2024-10-30 21:28:03,064 - utils.extract - DEBUG - Created logger named 'utils.extract' with level 10
2024-10-30 21:28:03,064 - utils.extract - DEBUG - Handlers for 'utils.extract': [<StreamHandler <stdout> (DEBUG)>, <StreamHandler <stderr> (WARNING)>]
2024-10-30 21:28:03,064 - app.app_builder - DEBUG - Created logger named 'app.app_builder' with level 10
2024-10-30 21:28:03,064 - app.app_builder - DEBUG - Handlers for 'app.app_builder': [<StreamHandler <stdout> (DEBUG)>, <StreamHandler <stderr> (WARNING)>]
2024-10-30 21:28:03,065 - app.app_args - DEBUG - Created logger named 'app.app_args' with level 10
2024-10-30 21:28:03,065 - app.app_args - DEBUG - Handlers for 'app.app_args': [<StreamHandler <stdout> (DEBUG)>, <StreamHandler <stderr> (WARNING)>]
usage: MakeCode-Arcade-to-Electron [-h] --repo REPO --version VERSION --name
                                   NAME --author AUTHOR --description
                                   DESCRIPTION [--icon ICON] [--prep-only]
                                   [--debug]

A program to convert MakeCode Arcade games to Electron apps.

options:
  -h, --help            show this help message and exit
  --repo REPO, -r REPO  The path to the MakeCode Arcade game repository on
                        GitHub. For example, "UnsignedArduino/Racers" points
                        to https://github.com/UnsignedArduino/Racers.
  --version VERSION, -v VERSION
                        The version of the MakeCode Arcade game to convert.
                        Must be an already existing and working built version
                        on GitHub Pages. For example, "1.0.0". (do not include
                        the "v" prefix)
  --name NAME, -n NAME  The name of the game. This will be the name of the
                        Electron app. For example, "Racers".
  --author AUTHOR, -a AUTHOR
                        The author of the game. For example, "Cyrus Yiu".
  --description DESCRIPTION, -d DESCRIPTION
                        The description of the game. For example, "Enjoy the
                        high-speed thrills of car racing in MakeCode Arcade!
                        For the MakeCode Arcade Mini Game Jam #3.".
  --icon ICON, -i ICON  The path to the icon file to use for the Electron app.
                        This needs to be an image that is supported by the
                        Python Pillow library. For example, "icon.png". If you
                        want to convert your MakeCode Arcade images to an
                        actual image, follow the instructions in the README.
  --prep-only           Only prepare the app, do not build it.
  --debug               Include debug messages. Defaults to info and greater
                        severity messages only.

Process finished with exit code 0
```
