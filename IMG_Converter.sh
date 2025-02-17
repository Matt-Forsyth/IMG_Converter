#!/bin/bash

# Ensure dependencies are installed
for cmd in zenity convert ffmpeg; do
    if ! command -v "$cmd" &>/dev/null; then
        sudo apt install -y "$cmd"
    fi
done

# Prompt the user to select the folder containing images/videos
SOURCE_DIR=$(zenity --file-selection --directory --title="Select Folder with Images and Videos")
if [ -z "$SOURCE_DIR" ]; then
    exit 1
fi

# Prompt the user to select the destination folder
DEST_DIR=$(zenity --file-selection --directory --title="Select Destination Folder for Converted Files")
if [ -z "$DEST_DIR" ]; then
    exit 1
fi

# Persistent counter file to keep track of numbering
COUNTER_FILE="$DEST_DIR/.conversion_counter"

# Load the last used counter or start from 1
if [ -f "$COUNTER_FILE" ]; then
    count=$(cat "$COUNTER_FILE")
else
    count=1
fi

# Convert images to PNG
for file in "$SOURCE_DIR"/*.{jpg,jpeg,bmp,tiff,webp,gif,png}; do
    [ -e "$file" ] || continue  # Skip if no matching files

    new_filename=$(printf "%s/%d.png" "$DEST_DIR" "$count")

    convert "$file" "$new_filename"

    if [ $? -eq 0 ]; then
        rm "$file"  # Delete original file
        echo "Converted and removed: $file -> $new_filename"
        count=$((count + 1))
    else
        echo "Failed to convert: $file"
    fi
done

# Convert videos to MP4
for file in "$SOURCE_DIR"/*.{avi,mkv,mov,flv,wmv,webm}; do
    [ -e "$file" ] || continue  # Skip if no matching files

    new_filename=$(printf "%s/%d.mp4" "$DEST_DIR" "$count")

    ffmpeg -i "$file" -c:v libx264 -preset fast -crf 22 -c:a aac -b:a 192k "$new_filename"

    if [ $? -eq 0 ]; then
        rm "$file"  # Delete original file
        echo "Converted and removed: $file -> $new_filename"
        count=$((count + 1))
    else
        echo "Failed to convert: $file"
    fi
done

# Save the updated counter value
echo "$count" > "$COUNTER_FILE"

# Notify user of completion
zenity --info --text="All images and videos have been converted and saved to:\n$DEST_DIR" --title="Conversion Complete"
