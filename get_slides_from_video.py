import os
import subprocess

# Prompt the user for input video file and output directory
input_file = input("Enter the path to the input video file: ").strip()
output_dir = input("Enter the name of the output directory (default: extracted_imgs): ").strip() or "extracted_imgs"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Construct the FFmpeg command
command = [
    "ffmpeg",
    "-i", input_file,
    "-filter_complex", "select=gt(scene\\,0.01)",
    os.path.join(output_dir, "%04d.jpg"),
    "-vsync", "drop"
]

# Execute the command
try:
    print(command)
    print("Extracting frames... This may take a while.")
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    print("Frames extracted successfully!")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("An error occurred while extracting frames:")
    print(e.stderr)
