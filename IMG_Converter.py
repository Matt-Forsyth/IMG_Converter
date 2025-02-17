import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import ffmpeg

# Function to select a directory
def select_directory(title):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder = filedialog.askdirectory(title=title)
    return folder if folder else None

# Select source and destination directories
source_dir = select_directory("Select Folder with Images and Videos")
if not source_dir:
    exit()

dest_dir = select_directory("Select Destination Folder for Converted Files")
if not dest_dir:
    exit()

# Persistent counter file
counter_file = os.path.join(dest_dir, ".conversion_counter")

# Load or initialize counter
if os.path.exists(counter_file):
    with open(counter_file, "r") as f:
        count = int(f.read().strip())
else:
    count = 1

# Supported formats
image_formats = (".jpg", ".jpeg", ".bmp", ".tiff", ".webp", ".gif", ".png")
video_formats = (".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm")

# Convert images to PNG
for file in os.listdir(source_dir):
    file_path = os.path.join(source_dir, file)
    if file.lower().endswith(image_formats):
        try:
            img = Image.open(file_path)
            new_filename = os.path.join(dest_dir, f"{count}.png")
            img.save(new_filename, "PNG")
            os.remove(file_path)  # Delete original
            print(f"Converted and removed: {file_path} -> {new_filename}")
            count += 1
        except Exception as e:
            print(f"Failed to convert: {file_path}, Error: {e}")

# Convert videos to MP4
for file in os.listdir(source_dir):
    file_path = os.path.join(source_dir, file)
    if file.lower().endswith(video_formats):
        try:
            new_filename = os.path.join(dest_dir, f"{count}.mp4")
            ffmpeg.input(file_path).output(new_filename, vcodec="libx264", preset="fast", crf=22, acodec="aac", audio_bitrate="192k").run()
            os.remove(file_path)  # Delete original
            print(f"Converted and removed: {file_path} -> {new_filename}")
            count += 1
        except Exception as e:
            print(f"Failed to convert: {file_path}, Error: {e}")

# Save the updated counter value
with open(counter_file, "w") as f:
    f.write(str(count))

# Notify user of completion
messagebox.showinfo("Conversion Complete", f"All images and videos have been converted and saved to:\n{dest_dir}")
