from os import get_terminal_size, path
from logger_config import logger
from datetime import datetime
import re
from tkinter import Tk, messagebox, PhotoImage




def get_terminal_title(title_content, filler="*"):
    try:
        width, _ = get_terminal_size()
    except:
        width = 80
        if len(title_content)/2 < width:
            width = int(len(title_content)/2) + 1


    title = filler
    title += " " * int(((width / 2) - (len(title_content) / 2)))
    title += title_content
    title += " " * int((width - len(filler) - 1))
    title += filler


    return  "\n"+filler * width + "\n"+ title_content + "\n" + filler * width


def get_base_filename(file_path):
    # Get the base filename from the file path
    base_filename = path.basename(file_path)
    return base_filename

def get_file_creation_datetime(file_path):
    # Get the file creation timestamp
    creation_time = path.getctime(file_path)
    
    # Convert the timestamp to a formatted string in the desired format
    creation_datetime_str = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M")
    logger.debug("Type of create date function output: ", type(creation_datetime_str))
    return creation_datetime_str





# def replace_time_in_datetime(datetime_string, time_input):
#     try:
#         datetime_string = datetime.strftime(datetime_string, "%Y-%m-%d %H:%M" ) 
#        # hours, minutes = datetime_string.hour, datetime_string.minute
#     except Exception as e:
#         logger.info(f": {e}")
        
    
#     # Parse the existing datetime string
#     dt = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")
    
#     try:
#         int(time_input)
#     except Exception as e:
#         logger.info(f": {e}")
        

#     # Handle time input based on its type or format
#     if isinstance(time_input, str):
#         time_input = time_input.strip()
        
#         # Check if time input is in the format 'time: YYYY-MM-DD HH:MM:SS'
#         match = re.match(r'time:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', time_input)
#         if match:
#             # Extract the time portion
#             time_part = match.group(1)
#             # Parse the extracted time
#             parsed_time = datetime.strptime(time_part, "%Y-%m-%d %H:%M:%S")
#             hours, minutes = parsed_time.hour, parsed_time.minute
        
        
#         # Check if the input is in 'HH:MM' or ' HH:MM' format
#         elif ":" in time_input:
#             hours, minutes = map(int, time_input.split(":"))
        
#         else:
#             raise ValueError("Invalid time input format.")
    
#     elif isinstance(time_input, int):
#         # Convert minutes since midnight to hours and minutes
#         hours, minutes = divmod(time_input, 60)
    
#     else:
#         raise ValueError("Invalid time input format.")
    
#     # Replace the time in the datetime object
#     new_dt = dt.replace(hour=hours, minute=minutes)
    
#     # Return the formatted datetime string
#     return new_dt.strftime("%Y-%m-%d %H:%M")



def confirm_action(message):
    """Displays a confirmation dialog with the specified message."""
    return messagebox.askyesno("Confirmation", message)



def find_asset_references(content):
    """Find all asset references in a text and return them"""
    references = re.findall(r'\[\[([^\[\]]+?)\]\]', content)
    referenced_assets = set()
    # Process each reference to remove alias and check for non-markdown files
    for ref in references:
        # Remove alias if present (everything after |)
        actual_ref = ref.split('|')[0]
        # Check if the reference has an extension and is not .md
        if '.' in actual_ref and not actual_ref.endswith('.md'):
            referenced_assets.add(actual_ref)
    return referenced_assets 
