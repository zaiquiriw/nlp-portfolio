from langdetect import detect_langs
import os

# Remove all files that are not in English
for filename in os.listdir(os.getcwd()):
    if filename.endswith("clean.txt"):
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "r", encoding="utf8") as f:
            text = f.read()
            print(f"Detecting language in file {filepath}...")
            try:
                # get the language code with the highest probability
                lang = detect_langs(text)[0].lang
                print(f"Language detected: {lang}")
                if lang != "en":  # delete the file if it's not in English
                    try:
                        f.close()
                        os.remove(filepath)
                    except Exception as e:
                        print(f"Error deleting file {filepath}: {e}")

            except:
                print(f"Error detecting language in file {filepath}")

for filename in os.listdir(os.getcwd()):
    if filename.endswith("file.txt"):
        os.remove(filename)
