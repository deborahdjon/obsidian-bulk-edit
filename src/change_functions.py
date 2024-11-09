from datetime import datetime

from tkinter import Tk, messagebox, PhotoImage
import os
import re
import shutil
from logger_config import logger
from const import ASSET_FOLDER_PATH

from utils import *



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


def fix_asset_references(frontmatter, content, filepath):
    """
    When moving assets into the asset folder, the reference can be broken.
    This function renames asset references in files to fix this issue.
    """
    content = "".join(content)
    references = find_asset_references(content)
    if len(references) > 0:
        briefed = False
        assets_in_vault = os.listdir(ASSET_FOLDER_PATH)
        for ref in references:
            asset_name = get_base_filename(ref)
            # Fix the asset reference if the asset is in the vault
            if (asset_name in assets_in_vault and not (ref == asset_name)):
                if not briefed:         
                    logger.info(f'Fixed references to the following assets in "{filepath}" :')
                    briefed = True
                content = content.replace(ref, asset_name)
                logger.info(asset_name)
            ## Remove the empty referecne 
            else: 
                content.replace(ref, "")

    content = content.replace("![[]]", "")
    content = content.replace("[[]]", "")
    content = content.strip()
    content = content.splitlines(keepends=True)
    return (frontmatter, content, filepath)


def clean_up_asset_folder(vault_folder: str, asset_folder: str):
    root = Tk()
    root.withdraw()  # Hide the main window as we only want dialogs
    # Keep the popup window on top of all windows
    root.attributes("-topmost", True)

    icon_path = "clean_up_vault/src/icons/alarm.png"
    root.iconphoto(False, PhotoImage(file=icon_path))



    assets_to_move = []  # List to store paths of all non-.md files that need to be moved to the asset folder

    # Function to recursively gather asset references in markdown files, excluding the .obsidian folder
    def gather_assets_and_find_files_to_move(path):
        # Set to store asset references found in markdown files
        referenced_assets = set()
        logger.debug("Vault Files")
        for root, dirs, files in os.walk(path):   
            logger.info(files)        
            for file in files:
                file_path = os.path.join(root, file)
                # Skip hidden items like .obsidian and .DSfolders
                hidden_item = re.search(r'/\.[^/\.]+', file_path) 
                hidden_item = re.search(r'/\.[^/\.]+', file_path) 
                zotero_connector_file = "ZoteroLibrary.json" in file_path
                is_md_file = file_path.endswith('.md') 
                is_project_file = "04_Project" in file_path
                is_already_in_asset_folder = "08_Asset" in file_path
                # Find stray assets
                if not (hidden_item 
                        or zotero_connector_file 
                        or is_md_file 
                        or is_project_file 
                        or is_already_in_asset_folder):
                        # Gather non-.md files for moving
                        # logger.debug(file_path)
                        assets_to_move.append(file_path)
                    
                # Only process .md files for asset reference extraction
                elif file.endswith('.md'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        references = find_asset_references(content)
                        referenced_assets = referenced_assets.union(references)
        return referenced_assets

    # Gather assets in markdown references and list of all non-md files to move
    referenced_assets = gather_assets_and_find_files_to_move(vault_folder)
    logger.debug("Referenced assets: ", referenced_assets)

    # Refresh the list of asset files in the asset folder after moving assets
    asset_folder_files = os.listdir(asset_folder)

    # Go through the asset folder and identify obsolete assets based on references found in markdown files
    assets_to_delete = [os.path.basename(a) for a in asset_folder_files if os.path.basename(a) not in referenced_assets]

    # Print stats on (obsolete) assets
    assets_outside_asset_folder_count = len(assets_to_move)
    referenced_assets_count = len(referenced_assets)
    assets_without_reference_count = len(assets_to_delete)
    total_asset_count = len(asset_folder_files) + assets_outside_asset_folder_count
    percentage_obsolete = (assets_without_reference_count / total_asset_count) * 100 if total_asset_count else 0
    
    logger.info(" ================ Obsidian cleaning file information +++++++++++++++++++ \n\n\n")
    logger.info(f"Number of assets outsied asset_folder to be moved: {assets_outside_asset_folder_count}")
    logger.info(f"Number of referenced assets in vault: {referenced_assets_count}")
    logger.info(f"Number of assets without reference: {assets_without_reference_count}")
    logger.info(f"Obsolete assets in asset folder: {assets_without_reference_count} / {total_asset_count} ({percentage_obsolete:.0f}%)")
    
    lines = []
    lines.append(" ================ All Assets in Vault ================ \n")
    lines += asset_folder_files
    lines.append("\n\n\n")
    lines.append(" ================ Asset References ================ \n")
    lines += referenced_assets
    lines.append("\n\n\n")
    lines.append(" ================ Assets Without Reference And Therfore Deleted ================ \n")
    lines += assets_to_delete
    logger.info("\n".join(lines))
    

    if confirm_action(f"You have {total_asset_count} assets in your vault. {assets_outside_asset_folder_count} loose items were moved to the assets folder. \nYou are about to delete {assets_without_reference_count} assets that are in the assets folder but have no reference ({percentage_obsolete:.0f}%). \nDo you want to proceed?"):
        # Move assets not in asset folder to the asset folder
        for asset_path in assets_to_move:
            asset_name = os.path.basename(asset_path)
            destination_path = os.path.join(asset_folder, asset_name)
            try:
                shutil.move(asset_path, destination_path)
                logger.info(f"Moved asset {asset_path} to {destination_path}")
            except Exception as e:
                logger.info(f"Could not move {asset_name}: {e}") 

        # Delete obsolete assets
        for asset in assets_to_delete:
            try:
                asset_path = os.path.join(asset_folder, asset)
                os.remove(asset_path)
                if not os.path.exists(asset_path):
                    logger.info(f"Deleted {asset}")
            except Exception as e:
                logger.info(f"Could not delete {asset}: {e}")


 
    # # Delete logs older than 1 month
    # log_files = os.listdir(log_folder).remove(log_filename)

    # for log in log_files:
    #     log_time = datetime.fromtimestamp(float(log.replace("-clean_vault.log", "")))
    #     logfile_path = log_folder+log
    #     if datetime.timestamp(datetime.now()) > (log_time + timedelta(weeks=4)) and  os.path.exists(logfile_path):
    #         os.remove(logfile_path)
            
    logger.info("Completed asset clean-up.")    



