# Cosmic-Reach-Unofficial-Mac-Launcher
A launcher for the game "Cosmic Reach" intended to make it easier to update &amp; launch on macOS.

DISCLAIMER: Someone has reported that this app may not be working. I am not sure why, as it works fine on my mac. Please let me know if it also doesn't work for you!

<img width="482" alt="SCR-20240501-rnum" src="https://github.com/hw2007/Cosmic-Reach-Unofficial-Mac-Launcher/assets/60082961/422b90ec-9fda-4f01-9de9-dc9bf1c7a1e9">

# Installing
0. Install java 17 if you do not have it already.
1. Install the latest build, and unzip the zip file.
2. Open a new terminal inside that folder, and run <code>./Install.sh</code>
3. Open the app. If it opened properly, now you can move it into your applications folder or wherever you like.

When you open it for the first time, a log window will appear to display status updates while it downloads Cosmic Reach for you. Eventually, the log window will disappear and the launcher will open.

# Use case
This launcher was made to fix a problem: Cosmic Reach on mac has to be opened via a jar file, which can't be easily opened in spotlight search, and the itch.io app can't install it automatically. This launcher fixes both of these things!

# Features
- Simple UI which looks native to macOS
- Launch the game easily from the launcher
- Update the game automatically, with one click!
- Multi-version support is currently not implimented, but maybe in the future I'll add it if there is enough people wanting it.

# Credits
This project is made possible by a small project called **itch-dl** (https://github.com/DragoonAethis/itch-dl), which allows for easy downloading of itch.io games.

# Compiling from source
You could just run the python file without compiling, but if for whatever reason you want to compile from source, you can do so by installing pyinstaller by running <code>pip3 install pyinstaller</code>

After that, navigate to the same directory as "Cosmic Reach Mac Launcher.py" and run <code>./PACKAGE.sh</code>


NOTE: This will not work on windows even if you use the source code, since the version of itch-dl included is for unix.
