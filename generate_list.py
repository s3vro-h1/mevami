import os
import configparser
import json
import config

SONGS_PATH = config.SONGS_PATH


DIFF_KEYS = [
    'diff_guitar', 'diff_rhythm', 'diff_bass',
    'diff_guitar_coop', 'diff_drums', 'diff_drums_real', 'diff_keys',
]

ENCODINGS = ['utf-8-sig', 'utf-16', 'utf-16-le', 'utf-16-be', 'utf-8', 'latin-1', 'cp1252']

def find_song_ini(files):
    """search song.ini ignoring caps."""
    for f in files:
        if f.lower() == 'song.ini':
            return f
    return None

def read_config(filepath):
    """tries to read the file trough several encodings."""
    for enc in ENCODINGS:
        try:
            config = configparser.ConfigParser(strict=False)  
            config.read(filepath, encoding=enc)
            return config
        except Exception:
            continue
    return None

def find_song_section(config):
    """Search for the section [song] ignoraning caps."""
    for section in config.sections():
        if section.lower() == 'song':
            return section
    return None

def ms_to_min_string(lenght_in_ms):
    """Convert ms value to seconds string for display purposes"""
    try:
        lenght_in_sec = lenght_in_ms/1000

        min = int(lenght_in_sec/60)
        sec = int(lenght_in_sec%60)

        return f"{min}:{sec:02d}"  
    except (ValueError, TypeError):
        return "0:00"

def find_videos(root,OS):
    """Find the video files for the video badge, checks for webm if OS is linux"""
    video_avail = False
    
    for file in os.listdir(root):
        if OS != "LINUX":
            if file.lower().endswith(('.mp4', '.webm')):
                video_avail = True
        else:
            if file.lower().endswith('.webm'):
                video_avail = True
    
    return video_avail


def scan_songs(OS = config.OS):
    catalog = []
    errors = []

    for root, dirs, files in os.walk(SONGS_PATH):
        ini_filename = find_song_ini(files)
        if not ini_filename:
            continue

        filepath = os.path.join(root, ini_filename)
        config = read_config(filepath)

        if config is None:
            errors.append(f"[ENCODING ERROR] {filepath}")
            continue

        section = find_song_section(config)
        if section is None:
            errors.append(f"[NO SECTION 'song'] {filepath}")
            continue

        try:
            entry = {
                'artist':  config.get(section, 'artist',  fallback='Unknown').strip(),
                'name':    config.get(section, 'name',    fallback='Unknown').strip(),
                'year': config.get(section, 'year',  fallback='Unknown').strip(),
                'album':   config.get(section, 'album',   fallback='').strip(),
                'charter': (config.get(section, 'charter', fallback='').strip()
                            or config.get(section, 'frets', fallback='').strip()),
                'lenght': ms_to_min_string(int(config.get(section, 'song_length',  fallback='Unknown').strip())),
                'video_avail': str(find_videos(root,OS)),
                'genre': config.get(section, 'genre',  fallback='Unknown').strip().title()
            }

            for key in DIFF_KEYS:
                raw = config.get(section, key, fallback='').strip()
                if raw:
                    try:
                        entry[key] = int(raw)
                    except ValueError:
                        pass

            catalog.append(entry)

        except Exception as e:
            errors.append(f"[ERROR PARSEO] {filepath} → {e}")

    with open("data.json", 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=4, ensure_ascii=False)

    with open("logs/scan_errors.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(errors))

    print(f"{len(catalog)} songs saved on data.json")
    print(f"{len(errors)} errors saved on logs/scan_errors.txt")

def save_genres():
    """Saves on a json the genres"""
    genres = []
    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        genres = list({item['genre'] for item in data})
        genres.sort()
    
    with open("genres.json", 'w', encoding='utf-8') as f:
        json.dump(genres, f, indent=4, ensure_ascii=False)

    

if __name__ == "__main__":
    scan_songs()
    save_genres()

    # Replace README on first publish
    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "**Mevami** is an automated system" in content:
            with open(readme_path, "w", encoding="utf-8") as f:
                # You can put whatever you want here
                # I just put it so when you upload your repo
                # It doesnt have the same readme as the original
                f.write("# My Clone Hero Setlist\n\nPowered by [Mevami](https://github.com/s3vro-h1/mevami)\n")
            print("README.md updated for your personal repo.")
