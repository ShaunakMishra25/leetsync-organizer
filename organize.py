import os
import shutil
import re

BASE_DIR = "."
DIFFICULTIES = ["Easy", "Medium", "Hard"]

# Make sure difficulty folders exist
for diff in DIFFICULTIES:
    os.makedirs(os.path.join(BASE_DIR, diff), exist_ok=True)

def get_difficulty_from_readme(folder_path):
    """
    Read difficulty from README.md file that LeetSync creates
    """
    readme_path = os.path.join(folder_path, 'README.md')
    
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for the badge pattern: <img src='.../Difficulty-Easy-brightgreen' ... />
            badge_match = re.search(r'Difficulty-(\w+)-', content)
            if badge_match:
                difficulty = badge_match.group(1).capitalize()
                if difficulty in DIFFICULTIES:
                    return difficulty
            
            # Alternative: look for alt text: alt='Difficulty: Easy'
            alt_match = re.search(r"alt=['\"]Difficulty:? (\w+)['\"]", content, re.IGNORECASE)
            if alt_match:
                difficulty = alt_match.group(1).capitalize()
                if difficulty in DIFFICULTIES:
                    return difficulty
                    
        except UnicodeDecodeError:
            # Try with different encoding if needed
            try:
                with open(readme_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                badge_match = re.search(r'Difficulty-(\w+)-', content)
                if badge_match:
                    difficulty = badge_match.group(1).capitalize()
                    if difficulty in DIFFICULTIES:
                        return difficulty
            except:
                pass
    
    return None

# Go through all folders in repo root
moved_count = 0
unknown_count = 0

for item in os.listdir(BASE_DIR):
    item_path = os.path.join(BASE_DIR, item)
    
    # Skip non-relevant items
    if (item == "organize.py" or item in DIFFICULTIES or 
        item.startswith('.') or not os.path.isdir(item_path)):
        continue
    
    # Get difficulty from README.md
    difficulty = get_difficulty_from_readme(item_path)
    
    if difficulty and difficulty in DIFFICULTIES:
        target_path = os.path.join(BASE_DIR, difficulty, item)
        shutil.move(item_path, target_path)
        moved_count += 1
    else:
        os.makedirs("Unknown", exist_ok=True)
        shutil.move(item_path, os.path.join(BASE_DIR, "Unknown", item))
        unknown_count += 1