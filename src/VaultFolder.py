import oyaml as yaml
import os
from os import path
from utils import get_terminal_title
from re import findall
from logger_config import logger

# TODO: is there some way to make sure that the change method has the right shape
# and arguments? Maybe by using classes?

class VaultFolder():
    def __init__(self, root_path):
        self.ROOT_PATH = root_path

    # TODO: add support for changing file name and location:
    # Add a paramater `filename` to the change method (and the value it returns).
    def make_change(self, change):
        self.apply_change(change, save=True)

    def preview_change(self, change, limiting_amount=None):
        self.apply_change(change, save=False)

    def apply_change(self, change, save):
        for dirpath, _, filenames in os.walk(self.ROOT_PATH):
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.readlines()

                    frontmatter, content = VaultFolder._extract_frontmatter(content, filename)
                    new_frontmatter, new_content, new_file_path = change(frontmatter, content, file_path)

                    if save:
                        VaultFolder._save_file(new_frontmatter, new_content, new_file_path)
                    else:
                        info = get_terminal_title(filename)
                        logger.info(info)
                        VaultFolder._print_preview(new_frontmatter, new_content, new_file_path)

    def _extract_frontmatter(content, filename):
        if not content:
            return ({}, [])

        frontmatter_lines = []
        content_lines = []
        
        # does the file have a frontmatter?
        if content[0].strip() == '---':
            valid_frontmatter = False
            for line in content[1:]:
                references = findall(r'\[\[([^\[\]]+?)\]\]', line)
                for ref in references:
                    actual_ref = ref.split('|')[0]
                    line = line.replace(ref, actual_ref)
                if line.strip() == '---':
                    valid_frontmatter = True
                    break

                frontmatter_lines.append(line)
            
            if not valid_frontmatter:
                raise ValueError("Invalid frontmatter definition!")
            
            try:
                frontmatter = yaml.load("\n".join(frontmatter_lines), Loader=yaml.Loader) if frontmatter_lines else {}
            except yaml.scanner.ScannerError:
                frontmatter = {}
                logger.debug(f"ERROR: could not extract frontmatter for {filename}!")
            except yaml.constructor.ConstructorError:
                frontmatter = {}
                logger.debug("Could not extract Frontmatter due to maldefined YAML.")
                logger.debug(content[1:])
                logger.debug(filename)
            except yaml.parser.ParserError:
                frontmatter = {}
                logger.debug("Could not extract Frontmatter due to maldefined YAML.")
                logger.debug(content[1:])
                logger.debug(filename)

        
            content_lines = content[len(frontmatter_lines) + 2:]
        # no frontmatter, so we just return the content
        else:
            content_lines = content
            frontmatter = {}
        return (frontmatter, content_lines)

    def _save_file(frontmatter, content, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            if frontmatter:
                file.write('---\n')
                file.write(yaml.dump(frontmatter, default_flow_style=False))
                file.write('---\n')
            file.writelines(content)

    def _print_preview(frontmatter, content, file_path):
        title = "Preview for: " + file_path
        info = get_terminal_title(title, filler="=")
        info += "\n"
        info += '---\n'
        info += yaml.dump(frontmatter, default_flow_style=False).strip()
        info += "\n"
        info += '---\n'
        info += ''.join(content)
        info += "\n"
        logger.info(info)
