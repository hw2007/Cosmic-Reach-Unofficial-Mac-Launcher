import os, zipfile, shutil, threading, subprocess, sys
import tkinter as tk
import itch_dl


script_path = os.path.dirname(os.path.abspath(__file__))
UI_OPEN = False


def unzip(zip_file, extract_to): # Unzips files
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def update_game(): # Create a thread to update the game, and update UI
	status_text.set(value="Update in progress...")
	thread = threading.Thread(target=run_update)
	thread.start()


def run_update(): # Runs a game update
	exit_status = ""

	# Create new window to display logs
	if UI_OPEN:
		log_window = tk.Toplevel(root)
	else:
		log_window = tk.Tk()
		log_window.geometry("+100+100")
		dock_image = tk.PhotoImage(file=dock_image_path)
		log_window.iconphoto(False, dock_image) # Set dock icon

	log_window.title("Downloading Cosmic Reach...")
	log_window.geometry("640x320")
	log_window.resizable(False, False)

	log_window.grab_set() # Prevents the root window from being interacted with while the log window is opened

	# Text box to display logs
	log_text = tk.Text(log_window, undo=False, state="disabled")
	log_text.pack(expand=True, fill="both")

	# Download Cosmic Reach
	try:
		downloader = subprocess.Popen([os.path.join(script_path, "itch-dl"), "https://finalforeach.itch.io/cosmic-reach", "--api-key", "c0G9LLdzsK6zu3IIeMDw3wct6HQHN0NZ1rAjFYPY"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

		while downloader.poll() is None:  # Check if the process is still running
			line = downloader.stderr.readline()  # Read a line from the process output

			if not line:
				break

			log_text.config(state="normal") # The text box needs to be enabled to add text
			log_text.insert(tk.END, line)  # Display the output in the Text widget
			log_text.see(tk.END)  # Scroll to the end to show the latest logs
			log_text.config(state="disabled") # Keep it disabled so that the user cannot edit the text
			log_window.update()
	except Exception as error:
		exit_status = "⚠️ An error occured while trying to download the update!"

		log_text.config(state="normal") # The text box needs to be enabled to add text
		log_text.insert(tk.END, str(error))  # Display the output in the Text widget
		log_text.see(tk.END)  # Scroll to the end to show the latest logs
		log_text.config(state="disabled") # Keep it disabled so that the user cannot edit the text
		log_window.update()

	try:
		# Unzip the linux version of Cosmic Reach. We use the linux version because it contains both an easy to access icon, and the cosmic reach jar.
		unzip("finalforeach/cosmic-reach/files/cosmic-reach-linux.zip", "cosmicreach")
		os.rename("cosmicreach/lib/Cosmic Reach.png", "icon.png") # Grab the icon file

		# Grabbing the jar file
		jar_directory = "cosmicreach/lib/app" # Directory containing the jar
		old_name = "Error" # If something goes wrong, the user will see "Error" as the version name

		# Iterate through the files in the directory
		for filename in os.listdir(jar_directory):
			if filename.endswith(".jar"): # Going through each file with the .jar extension
				new_filename = "cosmicreach.jar"  # Renaming the jar to something we can use later
				old_path = os.path.join(jar_directory, filename)
				old_name = os.path.splitext(filename)[0]
				os.rename(old_path, new_filename) # Moving the jar
				break # We can stop once we have found the jar

		# Remove leftover files, leaving just the jar & icon.
		shutil.rmtree("finalforeach")
		shutil.rmtree("cosmicreach")
	except Exception as error:
		if exit_status == "":
			exit_status = "⚠️ An error occured while trying to extract the update!"

			log_text.config(state="normal") # The text box needs to be enabled to add text
			log_text.insert(tk.END, str(error))  # Display the output in the Text widget
			log_text.see(tk.END)  # Scroll to the end to show the latest logs
			log_text.config(state="disabled") # Keep it disabled so that the user cannot edit the text
			log_window.update()

	if UI_OPEN:
		root.after(0, lambda: process_finish(log_window, exit_status))
	elif exit_status == "":
		log_window.destroy()
	else:
		log_window.title("[FAILED] Downloading Cosmic Reach...")


def launch_game(): # Create a thread to launch the game, and update UI
	subprocess.Popen(["java", "-jar", "cosmicreach.jar"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	root.destroy()
	sys.exit()


def process_finish(log_window, status): # Called when either an update or run ends. Will reset the GUI to normal.
	status_text.set(value=status)

	if status == "":
		log_window.destroy()
	else:
		log_window.title("[FAILED] Downloading Cosmic Reach...")


# Scale a tkinter image to some size
def scale_image(image, target_size):
    # Calculate the scaling factor for width and height
    width_factor = target_size[0] / image.width()
    height_factor = target_size[1] / image.height()
    # Scale the image using the larger factor to maintain aspect ratio
    scaling_factor = max(width_factor, height_factor)
    scaled_image = image.subsample(int(1 / scaling_factor), int(1 / scaling_factor))
    return scaled_image


# Setup working directory and install cosmic reach if needed
def initialize():
	global dock_image, banner_image

	# Set working directory
	home_dir = os.path.expanduser("~")
	working_dir = os.path.join(home_dir, "Library/cosmic_reach_mac_launcher")

	if not os.path.exists(working_dir):
		os.mkdir(working_dir)

	os.chdir(working_dir)

	if not os.path.exists(os.path.join(working_dir, "icon.png")) or not os.path.exists(os.path.join(working_dir, "cosmicreach.jar")):
		run_update()

# Get the app icon image path
dock_image_path = os.path.join(script_path, "icon.png")

# Initialize everything
initialize()


##### GUI STUFF #####

# Setup main tkinter window
UI_OPEN = True

root = tk.Tk()
root.title("Cosmic Reach Unofficial Mac Launcher")
root.geometry("480x360")
root.geometry("+100+100")
root.resizable(False, False)

dock_image = tk.PhotoImage(file=dock_image_path)
root.iconphoto(False, dock_image) # Set dock icon

status_text = tk.StringVar(value="")

# Disable the default macOS menu bar
root.option_add('*tearOff', False)

# Create a custom menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Displays the cosmic reach icon inside the window
banner_image = tk.PhotoImage(file="icon.png")
banner_image = scale_image(banner_image, [128, 128])
banner = tk.Label(root, image=banner_image)
banner.grid(row=0, pady=20, columnspan=3, sticky="n")

# Heading text
heading = tk.Label(root, text="What would you like to do?", font=("System", 24))
heading.grid(row=1, pady=(0, 40), columnspan=3)

# Work some magic to center the buttons. Creates a hidden column which acts as the center between the two of them.
root.grid_columnconfigure(1, weight=1)

# Launch button
launch = tk.Button(root, text="🚀 Launch Cosmic Reach", command=launch_game, width=20, height=2)
launch.grid(row=2, column=0, padx=(20, 0))

# Status subtext
status = tk.Label(root, textvariable=status_text, font=("System", 10))
status.grid(row=3, column=0, pady=(20, 0), columnspan=3)

# Update button
update = tk.Button(root, text="⬇️ Update Cosmic Reach", command=update_game, width=20, height=2)
update.grid(row=2, column=2, padx=(0, 20))

# Reload the UI
root.mainloop()
