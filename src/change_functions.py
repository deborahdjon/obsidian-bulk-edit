from datetime import datetime, timedelta
from tkinter import Tk, messagebox
import os
import re
import shutil
from logger_config import logger





def get_base_filename(file_path):
    # Get the base filename from the file path
    base_filename = os.path.basename(file_path)
    return base_filename

def get_file_creation_datetime(file_path):
    # Get the file creation timestamp
    creation_time = os.path.getctime(file_path)
    
    # Convert the timestamp to a formatted string in the desired format
    creation_datetime_str = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M")
    logger.debug("Type of create date function output: ", type(creation_datetime_str))
    return creation_datetime_str

def replace_time_in_datetime(datetime_string, time_input):
    try:
        datetime_string = datetime.strftime(datetime_string, "%Y-%m-%d %H:%M" ) 
       # hours, minutes = datetime_string.hour, datetime_string.minute
    except Exception as e:
        logger.info(f": {e}")
        
    
    # Parse the existing datetime string
    dt = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")
    
    try:
        int(time_input)
    except Exception as e:
        logger.info(f": {e}")
        

    # Handle time input based on its type or format
    if isinstance(time_input, str):
        time_input = time_input.strip()
        
        # Check if time input is in the format 'time: YYYY-MM-DD HH:MM:SS'
        match = re.match(r'time:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', time_input)
        if match:
            # Extract the time portion
            time_part = match.group(1)
            # Parse the extracted time
            parsed_time = datetime.strptime(time_part, "%Y-%m-%d %H:%M:%S")
            hours, minutes = parsed_time.hour, parsed_time.minute
        
        
        # Check if the input is in 'HH:MM' or ' HH:MM' format
        elif ":" in time_input:
            hours, minutes = map(int, time_input.split(":"))
        
        else:
            raise ValueError("Invalid time input format.")
    
    elif isinstance(time_input, int):
        # Convert minutes since midnight to hours and minutes
        hours, minutes = divmod(time_input, 60)
    
    else:
        raise ValueError("Invalid time input format.")
    
    # Replace the time in the datetime object
    new_dt = dt.replace(hour=hours, minute=minutes)
    
    # Return the formatted datetime string
    return new_dt.strftime("%Y-%m-%d %H:%M")


def remove_unwanted_frontmatter(frontmatter, content, file_path):
    unwanted_frontmatter = ["delete"]
    for attribute in unwanted_frontmatter: 
        if attribute in frontmatter: 
            frontmatter.pop(attribute)
    return (frontmatter, content, file_path)

def change_daily_note_frontmatter(frontmatter, content, file_path):
    filename = get_base_filename(file_path)

    if not frontmatter:
        frontmatter = {
            "type":"review/day",
            "date":filename[:10]
        }

    elif "type" not in frontmatter:
        frontmatter["type"] = "review/day"

    elif not frontmatter["type"] ==  "review/day":
        frontmatter["type"] = "review/day"
    
    elif "date" not in frontmatter:
        frontmatter["date"] = filename[:10]

    return (frontmatter, content, file_path)

def change_weekly_note_frontmatter(frontmatter, content, file_path):
    if not frontmatter:
        filename = get_base_filename(file_path)
        frontmatter = {
            "type": "review/week",
            "date":filename[:10],
            "week":int(filename[-5:-3])
        }
    elif "type" not in frontmatter:
        frontmatter["type"] = "review/week"

    elif  frontmatter["type"] ==  "review/week":
        frontmatter["type"] = "review/week"
    return (frontmatter, content, file_path)



def confirm_action(message):
    """Displays a confirmation dialog with the specified message."""
    return messagebox.askyesno("Confirmation", message)


def clean_up_asset_folder(vault_folder: str, asset_folder: str):
    root = Tk()
    root.withdraw()  # Hide the main window as we only want dialogs

    # Set to store asset references found in markdown files
    assets_in_vault = set()
    assets_to_move = []  # List to store paths of all non-.md files that need to be moved to the asset folder

    # Function to recursively gather asset references in markdown files, excluding the .obsidian folder
    def gather_assets_and_find_files_to_move(path):
        logger.debug("Vault Files")
        for root, dirs, files in os.walk(path):           
            for file in files:
                file_path = os.path.join(root, file)
                # Skip hidden items like .obsidian and .DSfolders
                hidden_item = re.search(r'/\.[^/\.]+', file_path)
                zotero_connector_file = "ZoteroLibrary.json" in file_path
                if not hidden_item or not zotero_connector_file:  
                    # Gather non-.md files for moving
                    if not file_path.endswith('.md') and not "/08_Asset"  in file_path and not "04_Project"  in file_path:
                        logger.debug(file_path)
                        assets_to_move.append(file_path)
                    
                    # Only process .md files for asset reference extraction
                    elif file.endswith('.md'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Find all references to assets in [[]] brackets
                            references = re.findall(r'\[\[([^\[\]]+?)\]\]', content)
                            # Process each reference to remove alias and check for non-markdown files
                            for ref in references:
                                # Remove alias if present (everything after |)
                                actual_ref = ref.split('|')[0]
                                # Check if the reference has an extension and is not .md
                                if '.' in actual_ref and not actual_ref.endswith('.md'):
                                    assets_in_vault.add(actual_ref)

    # Gather assets in markdown references and list of all non-md files to move
    gather_assets_and_find_files_to_move(vault_folder)
    
    # Refresh the list of asset files in the asset folder after moving assets
    asset_files = os.listdir(asset_folder)
    logger.debug("Assets in vault")
    logger.debug(assets_in_vault)

    # List to store assets identified as obsolete
    assets_to_delete = []
    
    # Go through the asset folder and identify obsolete assets based on references found in markdown files
    missing = [os.path.basename(a) for a in assets_in_vault if os.path.basename(a) not in asset_files]
    for asset in asset_files:
        if asset not in assets_in_vault:
            assets_to_delete.append(asset)
    
    # Print stats on obsolete assets
    total_assets = len(asset_files)
    obsolete_count = len(assets_to_delete)
    percentage = (obsolete_count / total_assets) * 100 if total_assets else 0

    logger.info(f"Number of assets in vault: {len(assets_in_vault)}")
    logger.info(f"Number of missing assets in vault: {len(missing)}")
    logger.info(f"Obsolete assets in asset folder: {obsolete_count} / {total_assets} ({percentage:.2f}%)")
    
    if confirm_action(f"You are about to delete {obsolete_count} obsolete assets out of a total of {total_assets} ({percentage:.2f}%) assets in your vault. Do you want to proceed?"):
        # Move assets not in asset folder to the asset folder
        for asset_path in assets_to_move:
            asset_name = os.path.basename(asset_path)
            destination_path = os.path.join(asset_folder, asset_name)
            try:
                shutil.move(asset_path, destination_path)
                logger.debug(f"Moved {asset_name} to asset folder")
            except Exception as e:
                logger.debug(f"Could not move {asset_name}: {e}") 

        # Delete obsolete assets
        for asset in assets_to_delete:
            try:
                asset_path = os.path.join(asset_folder, asset)
                os.remove(asset_path)
                if not os.path.exists(asset_path):
                    logger.debug(f"Deleted {asset}")
            except Exception as e:
                logger.debug(f"Could not delete {asset}: {e}")


    lines = []
    lines.append(" Logging Obsidian cleaning \n\n\n")
    lines.append(" ================ All Assets in Vault ================ \n")
    lines += asset_files
    lines.append(" ================ Assets With Reference But Missing in Vault ================ \n")
    lines += missing
    lines.append("\n\n\n")
    lines.append(" ================ Assets Without Reference And Therfore Deleted ================ \n")
    lines += assets_to_delete
    logger.info("\n".join(lines))
    
    # # Delete logs older than 1 month
    # log_files = os.listdir(log_folder).remove(log_filename)

    # for log in log_files:
    #     log_time = datetime.fromtimestamp(float(log.replace("-clean_vault.log", "")))
    #     logfile_path = log_folder+log
    #     if datetime.timestamp(datetime.now()) > (log_time + timedelta(weeks=4)) and  os.path.exists(logfile_path):
    #         os.remove(logfile_path)
            
    logger.info("Completed asset clean-up.")    



