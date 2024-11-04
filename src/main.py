import VaultFolder
from VaultFolder import VaultFolder
import const
import change_functions
import os
from logger_config import logger


if __name__ == "__main__":
    # print(os.listdir("../../../."))
    # # Change Daily Note Header Format
    # vault_folder = VaultFolder(const.DAY_FOLDER_PATH)
    # logger.debug(os.listdir(const.VAULT_PATH))
    # vault_folder.make_change(change_functions.change_daily_note_frontmatter)
    # logger.info("changed daily notes frontmatter")
    # print("changed daily notes frontmatter")


    # # Change Weekly Note Header Format
    # vault_folder = VaultFolder(const.WEEK_FOLDER_PATH)
    # logger.debug(os.listdir(const.VAULT_PATH))
    # vault_folder.make_change(change_functions.change_weekly_note_frontmatter)
    # logger.info("changed weekly notes frontmatter")
    # print("changed weekly notes frontmatter")

    # Clean out Assets
    change_functions.clean_up_asset_folder(const.VAULT_PATH, const.ASSET_FOLDER_PATH)
    logger.info("cleaned out assets folder")
    print("cleaned out assets folder")
