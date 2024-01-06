'''
set_offset_time.py

Created with ChatGPT to set the time zone Exif tags for all jpg images in a directory.
Requires:
1. Set the path to ExifTool.
2. Install the rich python library: "pip install rich"
'''

import sys
import os
import subprocess
import re
import logging
from rich.progress import Progress

# Configuration Options
exiftool_path = r'<PATH TO EXIFTOOL>'

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def validate_timezone_format(offset_value):
    """Validate the format of the provided time zone."""
    pattern = re.compile(r'^[+-]\d{2}:\d{2}$')
    return bool(pattern.match(offset_value))

def process_file(file, offset_value, overall_task, progress):
    """Process an individual file, updating the progress bar."""
    try:
        file_path = os.path.join(os.getcwd(), file)
        
        # The actual cmd for ExifTool: 
        command = [exiftool_path, '-overwrite_original_in_place', '-preserve', '-offsettime*=' + offset_value, file_path]
        
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        progress.advance(overall_task)
        progress.description = f"[cyan]Processing...[/]"
        progress.console.print(f'[magenta]Processed file:[/] {file}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error processing {file}: {e}')
        logging.error(f'ExifTool output: {e.output.decode("utf-8")}')
        progress.console.print(f'[red]Error processing file:[/] {file}')

def main(offset_value):
    """Main function to set the OffsetTime for all JPG files in the current directory."""
    try:
        # Validate time zone format
        if not validate_timezone_format(offset_value):
            raise ValueError("Invalid time zone format. Use format like '+07:00'.")

        current_directory = os.getcwd()
        jpg_files = [file for file in os.listdir(current_directory) if file.lower().endswith('.jpg')]

        total_files = len(jpg_files)

        with Progress() as progress:
            overall_task = progress.add_task("[cyan]Processing...", total=total_files)
            progress.update(overall_task, description="[bold]Overall Progress")

            for file in jpg_files:
                process_file(file, offset_value, overall_task, progress)

        logging.info(f'OffsetTime set successfully for all JPG files in the current directory with an offset of {offset_value}.')

    except ValueError as ve:
        logging.error(str(ve))
        logging.error("Ensure the correct time zone format is provided.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.error("Usage: set_offset_time.py +07:00 (Time zone info must be formatted as shown)")
        sys.exit(1)

    offset_value = sys.argv[1]
    main(offset_value)
