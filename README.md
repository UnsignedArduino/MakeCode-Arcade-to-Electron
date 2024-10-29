# MakeCode-Arcade-to-Electron

This is a simple script that allows you to convert your MakeCode Arcade games
to a standalone offline-capable Electron app!

## Install

1. Have Python and Node.js installed and available at the command line. (on
   PATH basically)
2. Clone this repo.
3. Install [`requirements.txt`](./requirements.txt). (to a virtual
   environment is recommended)

## Usage

1. Have a MakeCode Arcade game on GitHub.
2. Deploy to GitHub Pages by creating a release and noting the version number.
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
```
