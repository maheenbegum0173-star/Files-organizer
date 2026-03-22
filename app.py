from flask import Flask, render_template, request
import os
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ORGANIZED_FOLDER = "organized"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ORGANIZED_FOLDER, exist_ok=True)

def get_folder(filename):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        return "Images"
    elif filename.endswith(".pdf"):
        return "Documents"
    elif filename.endswith((".mp4", ".mkv")):
        return "Videos"
    else:
        return "Others"

# 🔥 Smart rename (removes spaces)
def clean_name(filename):
    return filename.replace(" ", "_")

# 📊 Get file stats
def get_stats():
    stats = {}
    for folder in os.listdir(ORGANIZED_FOLDER):
        path = os.path.join(ORGANIZED_FOLDER, folder)
        if os.path.isdir(path):
            stats[folder] = len(os.listdir(path))
    return stats

# 📂 Get file list
def get_files():
    files = {}
    for folder in os.listdir(ORGANIZED_FOLDER):
        path = os.path.join(ORGANIZED_FOLDER, folder)
        if os.path.isdir(path):
            files[folder] = os.listdir(path)
    return files

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        file = request.files["file"]

        if file:
            filename = clean_name(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            folder = get_folder(filename)
            target_folder = os.path.join(ORGANIZED_FOLDER, folder)
            os.makedirs(target_folder, exist_ok=True)

            shutil.move(filepath, os.path.join(target_folder, filename))
            message = f"✅ File organized into {folder}"

    stats = get_stats()
    files = get_files()

    return render_template("index.html", message=message, stats=stats, files=files)

if __name__ == "__main__":
    app.run(debug=True)