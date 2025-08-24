# LeetSync Difficulty Organizer 🚀

Automatically organizes your LeetCode solutions into `Easy`, `Medium`, `Hard`, and `Unknown` folders based on problem difficulty — all powered by LeetSync metadata.

---

## ✨ Features

- ✅ **Auto-detects difficulty** from `README.md` or LeetSync metadata  
- ✅ **Preserves Git history** with `git mv`  
- ✅ **Runs as a GitHub Action** (automatically)
- ✅ **Handles unknown difficulties** gracefully  

---

## 📦 Installation

> ⚠️ Requires **Python 3.9+**

```bash
# Check your Python version
python --version  # Should output 3.9.x or higher

# Clone your LeetCode repository
git clone <your-leetcode-repo>
cd <your-leetcode-repo>

# Add the organizer script files (organize.py, config.json, etc.)
# Or copy this tool's contents into your repo
```

---

## ⚙️ Usage

### 🔁 Basic Usage

```bash
python organize.py
```

---

## 🔄 GitHub Action Setup

Automatically run the organizer every Sunday (or trigger manually):

1. Copy the GitHub Action workflow file to your repo:

    ```bash
    .github/workflows/organize.yml
    ```

2. Ensure the `organize.py` and config files are committed to your repo.

3. The workflow will:
   - Submit in LeetCode it will categorize the problem accordingly

✅ Example `organize.yml` is included in this repo.

---

## 📁 Example

### Before

```
my-leetcode/
├── two-sum/
├── reverse-linked-list/
├── merge-intervals/
```

### After

```
my-leetcode/
├── Easy/
│   ├── two-sum/
│   └── reverse-linked-list/
├── Medium/
│   └── merge-intervals/
├── Hard/
├── Unknown/
```

---

## 🧠 Why I Built This

I had over **300+ LeetCode solutions** in a flat directory structure — difficult to navigate and impossible to track difficulty progression.

This tool helps:

- 📊 Track progress by difficulty  
- 🔍 Find problems quickly  
- 🎯 Prepare for interviews more efficiently  
- 💼 Showcase clean, organized work to recruiters and employers  

---

## 💡 Tip

Run in `--dry-run` mode first to preview changes **without moving any files**.

---

## 📜 License

MIT License

---

## 🙌 Contributing

Pull requests and improvements are welcome! Open an issue if you spot a bug or want a new feature.

---
