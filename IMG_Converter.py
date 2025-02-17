import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import ffmpeg

source_dir = None
dest_dir = None

# Function to select a directory
def select_directory(title):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder = filedialog.askdirectory(title=title)
    return folder if folder else None

def convert_files(src_dir=None, dst_dir=None, show_gui=False):
    """
    Convert images and videos to standardized formats
    Args:
        src_dir (str): Source directory path
        dst_dir (str): Destination directory path
        show_gui (bool): Whether to show GUI notifications
    """
    if not src_dir or not dst_dir:
        return False
        
    # Create destination directory if it doesn't exist
    os.makedirs(dst_dir, exist_ok=True)

    # Persistent counter file
    counter_file = os.path.join(dst_dir, ".conversion_counter")

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
    for file in os.listdir(src_dir):
        file_path = os.path.join(src_dir, file)
        if file.lower().endswith(image_formats):
            try:
                img = Image.open(file_path)
                new_filename = os.path.join(dst_dir, f"{count}.png")
                img.save(new_filename, "PNG")
                os.remove(file_path)  # Delete original
                print(f"Converted and removed: {file_path} -> {new_filename}")
                count += 1
            except Exception as e:
                print(f"Failed to convert: {file_path}, Error: {e}")

    # Convert videos to MP4
    for file in os.listdir(src_dir):
        file_path = os.path.join(src_dir, file)
        if file.lower().endswith(video_formats):
            try:
                new_filename = os.path.join(dst_dir, f"{count}.mp4")
                ffmpeg.input(file_path).output(new_filename, vcodec="libx264", preset="fast", crf=22, acodec="aac", audio_bitrate="192k").run()
                os.remove(file_path)  # Delete original
                print(f"Converted and removed: {file_path} -> {new_filename}")
                count += 1
            except Exception as e:
                print(f"Failed to convert: {file_path}, Error: {e}")

    # Save the updated counter value
    with open(counter_file, "w") as f:
        f.write(str(count))

    # Only show GUI notification if requested
    if show_gui:
        messagebox.showinfo("Conversion Complete", 
                          f"All files converted to:\n{dst_dir}")
    
    return True

if __name__ == "__main__":
    # GUI imports only needed for direct execution
    import tkinter as tk
    from tkinter import filedialog
    
    def select_directory(title):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askdirectory(title=title)
    
    # When run directly, use GUI mode
    source_dir = select_directory("Select Folder with Images and Videos")
    if not source_dir:
        exit()
        
    dest_dir = select_directory("Select Destination Folder for Converted Files")
    if not dest_dir:
        exit()
        
    convert_files(source_dir, dest_dir, show_gui=True)
