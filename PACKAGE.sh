rm -r dist
pyinstaller "Cosmic Reach Mac Launcher.py" --add-data icon.png:. --windowed -i icon.icns --target-arch universal2 --add-data itch-dl:. --add-data itch_dl:./itch_dl
