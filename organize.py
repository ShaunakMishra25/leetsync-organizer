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

def update_existing_folder(source_path, destination_path):
    """Only overwrite code files in existing folder, don't move the folder itself"""
    code_extensions = ('.py', '.java', '.cpp', '.c', '.js', '.ts', '.rb', '.go', '.rs')
    
    for item in os.listdir(source_path):
        source_item = os.path.join(source_path, item)
        dest_item = os.path.join(destination_path, item)
        
        if os.path.isfile(source_item):
            if item.endswith(code_extensions) or item == 'README.md':
                shutil.copy2(source_item, dest_item)
                print(f"Updated file: {dest_item}")
        elif os.path.isdir(source_item):
            if os.path.exists(dest_item):
                shutil.rmtree(dest_item)
            shutil.copytree(source_item, dest_item)
            print(f"Updated folder: {dest_item}/")
    
    shutil.rmtree(source_path)

# --- MAIN SCRIPT ---
for diff in DIFFICULTIES:
    os.makedirs(os.path.join(BASE_DIR, diff), exist_ok=True)
os.makedirs("Unknown", exist_ok=True)

moved_count = 0
updated_count = 0

for item in os.listdir(BASE_DIR):
    if not should_organize_folder(item):
        continue
    
    item_path = os.path.join(BASE_DIR, item)
    difficulty = get_difficulty_from_readme(item_path)
    
    if difficulty and difficulty in DIFFICULTIES:
        target_dir = os.path.join(BASE_DIR, difficulty)
        target_path = os.path.join(target_dir, item)
        
        if os.path.exists(target_path):
            print(f"Updating existing: {difficulty}/{item}")
            update_existing_folder(item_path, target_path)
            updated_count += 1
        else:
            shutil.move(item_path, target_path)
            print(f"Moved: {item} → {difficulty}/")
            moved_count += 1
    else:
        target_path = os.path.join(BASE_DIR, "Unknown", item)
        if os.path.exists(target_path):
            print(f"Updating existing: Unknown/{item}")
            update_existing_folder(item_path, target_path)
            updated_count += 1
        else:
            shutil.move(item_path, target_path)
            print(f"Moved: {item} → Unknown/")
            moved_count += 1

print(f"\nOrganization complete! New: {moved_count}, Updated: {updated_count}")
