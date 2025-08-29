import os
import shutil
import re

BASE_DIR = "."
DIFFICULTIES = ["Easy", "Medium", "Hard"]

def get_difficulty_from_readme(folder_path):
    """Extracts difficulty from LeetSync's README badge format"""
    readme_path = os.path.join(folder_path, 'README.md')
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            badge_match = re.search(r'Difficulty-(\w+)-', content)
            if badge_match:
                difficulty = badge_match.group(1).capitalize()
                if difficulty in DIFFICULTIES:
                    return difficulty
        except:
            pass
    return None

def should_organize_folder(folder_name):
    """Check if this is a problem folder (contains hyphen and number)"""
    return (os.path.isdir(os.path.join(BASE_DIR, folder_name)) and
            '-' in folder_name and
            folder_name.split('-')[0].isdigit() and
            folder_name not in DIFFICULTIES and
            folder_name != "Unknown")

# Create difficulty folders
for diff in DIFFICULTIES:
    os.makedirs(os.path.join(BASE_DIR, diff), exist_ok=True)
os.makedirs("Unknown", exist_ok=True)

# Organize all problem folders
moved_count = 0
skipped_count = 0

for item in os.listdir(BASE_DIR):
    if not should_organize_folder(item):
        continue
    
    item_path = os.path.join(BASE_DIR, item)
    difficulty = get_difficulty_from_readme(item_path)
    
    if difficulty and difficulty in DIFFICULTIES:
        target_dir = os.path.join(BASE_DIR, difficulty)
        target_path = os.path.join(target_dir, item)
        
        if os.path.exists(target_path):
            # Folder already exists in destination - JUST UPDATE CODE FILES
            print(f"Updating code files in {difficulty}/{item}")
            update_existing_folder(item_path, target_path)
            skipped_count += 1
        else:
            # New folder - move entirely
            shutil.move(item_path, target_path)
            print(f"Moved {item} to {difficulty}/")
            moved_count += 1
    else:
        target_path = os.path.join(BASE_DIR, "Unknown", item)
        if os.path.exists(target_path):
            print(f"Updating code files in Unknown/{item}")
            update_existing_folder(item_path, target_path)
            skipped_count += 1
        else:
            shutil.move(item_path, target_path)
            print(f" Moved {item} to Unknown/")
            moved_count += 1

print(f"\nOrganization complete! New: {moved_count}, Updated: {skipped_count}")

def update_existing_folder(source_path, destination_path):
    """
    Only overwrite code files in existing folder, don't move the folder itself
    """
    # Define which files to update (code files and README)
    code_extensions = ('.py', '.java', '.cpp', '.c', '.js', '.ts', '.rb', '.go', '.rs')
    
    for item in os.listdir(source_path):
        source_item = os.path.join(source_path, item)
        dest_item = os.path.join(destination_path, item)
        
        if os.path.isfile(source_item):
            # Always overwrite code files and README
            if item.endswith(code_extensions) or item == 'README.md':
                shutil.copy2(source_item, dest_item)
                print(f" Updated {item}")
        elif os.path.isdir(source_item):
            # For subdirectories, copy recursively
            if os.path.exists(dest_item):
                shutil.rmtree(dest_item)
            shutil.copytree(source_item, dest_item)
            print(f" Updated {item}/")
    
    # Remove the source folder after copying
    shutil.rmtree(source_path)