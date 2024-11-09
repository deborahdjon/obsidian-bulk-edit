import VaultFolder
from VaultFolder import VaultFolder
import const
import change_functions
import os
from logger_config import logger
from utils import confirm_action, get_base_filename


if __name__ == "__main__":
    messege = """
    You are about to clean up your vault, performing these changes:
    🧹 Change the date property of weekly notes based on the file title
    🧹 Change the date property of daily notes based on the file title
    🧹 Edit all references to attachments, renaming broken references and deleting obsolete refererences.
    Before making any changes, make sure to make a copy of this vault.
    Do you wish to continue? 
    """
    if confirm_action(messege):
        # Change Daily Note Header Format
        message = """
        Do you want to change the properties of your daily notes?
        """
        if confirm_action(message):
            vault_folder = VaultFolder(const.DAY_FOLDER_PATH)
            vault_folder.make_change(change_functions.change_daily_note_frontmatter)
            logger.info("changed daily notes frontmatter")
            print("changed daily notes frontmatter")

        # Change Weekly Note Header Format
        message = """
        Do you want to change the properties of weekly daily notes?
        """
        if confirm_action(message):
            vault_folder = VaultFolder(const.WEEK_FOLDER_PATH)
            vault_folder.make_change(change_functions.change_weekly_note_frontmatter)
            logger.info("changed weekly notes frontmatter")
            print("changed weekly notes frontmatter")

        # Fix faulty Asset renaming, from prior asset moves
        message = """
        Do you fix currently broken asset references? Deleting all references that do not point to an asset and renaming broken references to existing assets?
        If you do not do this, you cannot move assets to the right location in the next step if.
        Do you want to continue? 
        """
        if confirm_action(message):
            for folder_path in const.ALL_EDIT_FOLDERS:
                vault_folder = VaultFolder(folder_path)
                vault_folder.make_change(change_functions.fix_asset_references)
                logger.info(f"Fixed refs in {get_base_filename(folder_path)}")
                print("fixed broken references")
       
        # Move all assets to the asset folder
        message = """
        Do you want to move all assets in your vault into your central assets folder?
        """
        if confirm_action(message):
            change_functions.clean_up_asset_folder(const.VAULT_PATH, const.ASSET_FOLDER_PATH)

            # Again fix assets, if this move caused fauts in asset namings
            for folder_path in const.ALL_EDIT_FOLDERS:
                vault_folder = VaultFolder(folder_path)
                vault_folder.make_change(change_functions.fix_asset_references)

            logger.info("cleaned out assets folder")
            print("cleaned out assets folder")
