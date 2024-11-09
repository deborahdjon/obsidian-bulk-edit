from os import path

"/Users/Debby/Desktop/Edit_Obsidian_Vault/Personal_Copy_To_Edit copy 5/.obsidian/scripts/python"
"/Users/Debby/Desktop/Edit_Obsidian_Vault/Personal_Copy_To_Edit copy 5/../../.."
VAULT_PATH = "../../.././"

MOOC_FOLDER_PATH = path.join(VAULT_PATH + "01_MOOC/")
SOURCE_FOLDER_PATH = path.join(VAULT_PATH + "02_Source/")
ATOMIC_FOLDER_PATH = path.join(VAULT_PATH + "03_Atomic/")
PROJECTS_FOLDER_PATH = path.join(VAULT_PATH + "04_Project/")
PERMANENT_FOLDER_PATH = path.join(VAULT_PATH + "05_Permanent/")
ASSET_FOLDER_PATH = path.join(VAULT_PATH + "08_Asset/")

REVIEW_FOLDER_PATH = path.join(VAULT_PATH + "06_Review/")
DAY_FOLDER_PATH = path.join(REVIEW_FOLDER_PATH, "04_Day/" )
WEEK_FOLDER_PATH = path.join(REVIEW_FOLDER_PATH, "03_Week")

MAIN_EDIT_FOLDERS = [MOOC_FOLDER_PATH,SOURCE_FOLDER_PATH,PERMANENT_FOLDER_PATH]
ALL_EDIT_FOLDERS = MAIN_EDIT_FOLDERS + [REVIEW_FOLDER_PATH, PROJECTS_FOLDER_PATH]