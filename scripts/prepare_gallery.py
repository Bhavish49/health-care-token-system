import shutil
import os

images = [
    r"C:\Users\Vikram\.gemini\antigravity\brain\4e389d21-ae68-4d0b-a56e-cc6f154e2db0\media__1777479969141.png",
    r"C:\Users\Vikram\.gemini\antigravity\brain\4e389d21-ae68-4d0b-a56e-cc6f154e2db0\media__1777480713887.png",
    r"C:\Users\Vikram\.gemini\antigravity\brain\4e389d21-ae68-4d0b-a56e-cc6f154e2db0\media__1777481878939.jpg"
]

dest_dir = r"c:\healthCareTokenSystem"

for img in images:
    if os.path.exists(img):
        shutil.copy(img, dest_dir)
        print(f"Copied {img} to {dest_dir}")
    else:
        print(f"File not found: {img}")

html_content = """
<!DOCTYPE html>
<html>
<head><title>Gallery</title></head>
<body>
    <h1>Image 1</h1>
    <img src="media__1777479969141.png" style="max-width: 100%;">
    <h1>Image 2</h1>
    <img src="media__1777480713887.png" style="max-width: 100%;">
    <h1>Image 3</h1>
    <img src="media__1777481878939.jpg" style="max-width: 100%;">
</body>
</html>
"""

with open(os.path.join(dest_dir, "gallery.html"), "w") as f:
    f.write(html_content)

print("Gallery generated.")
