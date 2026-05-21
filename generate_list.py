import os
import configparser
import json
import re
import hashlib
import config
from mido import MidiFile
from tqdm import tqdm

SONGS_PATH = config.SONGS_PATH
CACHE_FILE = "scan_cache.json"  # lightweight index: { abs_path → hash }

DIFF_KEYS = [
    'diff_guitar', 'diff_rhythm', 'diff_bass',
    'diff_guitar_coop', 'diff_drums', 'diff_drums_real', 'diff_keys',
    'diff_guitarghl','diff_bassghl','diff_rhythm_ghl','diff_guitar_coop_ghl'
]

# Maps each diff_* key to the instrument name used in playable_levels.
# Convention: -1 = instrument not charted; >= 0 = instrument present.
DIFF_KEY_TO_INSTRUMENT = {
    'diff_guitar':      'Guitar',
    'diff_rhythm':      'Rhythm',
    'diff_bass':        'Bass',
    'diff_guitar_coop': 'Guitar Co-op',
    'diff_drums':       'Drums',
    'diff_drums_real':  'Pro Drums',
    'diff_keys':        'Keys',

    # Guitar Hero Live
    'diff_guitarghl':       'Guitar-Live',
    'diff_bassghl':         'Bass-Live',
    'diff_rhythm_ghl':      'Rhythm-Live',
    'diff_guitar_coop_ghl': 'Guitar Co-op-Live'

}

ENCODINGS = ['utf-8-sig', 'utf-16', 'utf-16-le', 'utf-16-be', 'utf-8', 'latin-1', 'cp1252']

# Keys used by .chart section names (e.g. [ExpertSingle], [HardBass])
CHART_TRACK_MAP = {
    'single':       'Guitar',
    'doubleguitar': 'Guitar Co-op',
    'rhythm':       'Rhythm',
    'bass':         'Bass',
    'drums':        'Drums',
    'keys':         'Keys',
    'doublebassdrum':   'Drums',   # legacy
    'doublerhythm':     'Rhythm',  
    # Guitar hero live
    'ghlguitar':    'Guitar-Live',
    'ghlbass':      'Bass-Live',
    'ghlcoop':      'Guitar Co-op-Live',
    'ghlrhythm':    'Rhythm-Live',
}

# Keys used by MIDI track names (e.g. "PART GUITAR", "PART BASS")
# Ordered so longer/more-specific names are checked first.
MIDI_TRACK_MAP = {
    'part guitar coop': 'Guitar Co-op',
    'part guitar':      'Guitar',
    'part rhythm':      'Rhythm',
    'part bass':        'Bass',
    'part drums':       'Drums',
    'part keys':        'Keys',
    # Legacy / fallback names (no "PART " prefix)
    'single':           'Guitar',
    'doubleguitar':     'Guitar Co-op',
    'rhythm':           'Rhythm',
    'bass':             'Bass',
    'drums':            'Drums',
    'keys':             'Keys',

    # Guitar Hero Live (I Have no idea if they use MIDI files as well, but Im putting this just in case)
    'part guitar ghl':      'Guitar-Live',
    'part bass ghl':        'Bass-Live',
    'part rhythm ghl':      'Rhythm-Live',
    'part guitar coop ghl': 'Guitar Co-op-Live',
               
}

# Pro Drums: presence of tom-marker notes in PART DRUMS signals Pro Drums support
PRO_DRUMS_MARKERS = {110, 111, 112}

DIFF_MAP = {
    'easy': 'Easy',
    'medium': 'Medium',
    'hard': 'Hard',
    'expert': 'Expert'
}


def load_cache() -> dict:
    """Load the hash index from disk. Structure: { abs_path: hash_str }"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_cache(cache: dict):
    """Persist the hash index to disk."""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4, ensure_ascii=False)


def hash_song_files(root: str, ini_filename: str) -> str:
    """Hash the content of song.ini + the chart file (if present).

    Using file content rather than mtime means the cache only invalidates
    when something genuinely changed, regardless of filesystem quirks or
    file copies that preserve timestamps.
    """
    h = hashlib.md5()
    for filename in [ini_filename, 'notes.chart', 'notes.mid', 'song.mid']:
        path = os.path.join(root, filename)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                h.update(f.read())
    return h.hexdigest()


def find_song_ini(files):
    """Search song.ini ignoring caps."""
    for f in files:
        if f.lower() == 'song.ini':
            return f
    return None


def read_config(filepath):
    """Try to read the file through several encodings."""
    for enc in ENCODINGS:
        try:
            cfg = configparser.ConfigParser(strict=False)
            cfg.read(filepath, encoding=enc)
            return cfg
        except Exception:
            continue
    return None


def find_song_section(cfg):
    """Search for the section [song] ignoring caps."""
    for section in cfg.sections():
        if section.lower() == 'song':
            return section
    return None


def ms_to_min_string(length_in_ms):
    """Convert ms value to a m:ss string for display."""
    try:
        length_in_sec = length_in_ms / 1000
        mins = int(length_in_sec / 60)
        secs = int(length_in_sec % 60)
        return f"{mins}:{secs:02d}"
    except (ValueError, TypeError):
        return "0:00"


def find_videos(root, OS):
    """Find video files for the video badge; checks for webm on Linux."""
    for file in os.listdir(root):
        if OS != "LINUX":
            if file.lower().endswith(('.mp4', '.webm')):
                return True
        else:
            if file.lower().endswith('.webm'):
                return True
    return False



def parse_chart_difficulties(filepath):
    """Parse a .chart file to find available instruments and difficulties."""
    avail_levels = {}
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        sections = re.findall(r'\[([^\]]+)\]', content)
        for sec in sections:
            sec_lower = sec.lower()
            for diff_raw, diff_clean in DIFF_MAP.items():
                if sec_lower.startswith(diff_raw):
                    track_raw = sec_lower.replace(diff_raw, '')
                    if track_raw in CHART_TRACK_MAP:
                        inst = CHART_TRACK_MAP[track_raw]
                        avail_levels.setdefault(inst, [])
                        if diff_clean not in avail_levels[inst]:
                            avail_levels[inst].append(diff_clean)
    except Exception:
        pass
    return avail_levels


def parse_midi_difficulties(filepath):
    """Parse a .mid file to find available instruments and difficulties.

    Clone Hero MIDIs follow the RB/GH convention: all difficulties for a
    given instrument live in a single unified track (e.g. "PART GUITAR"),
    with difficulty encoded in the note number:

        Easy   → 60–66
        Medium → 72–78
        Hard   → 84–90
        Expert → 96–102

    every note_on event (velocity > 0) in each track to see which
    ranges are actually used, so a song charted only on Expert won't
    incorrectly show Easy/Medium/Hard.
    """
    # Note number ranges for each difficulty
    DIFF_NOTE_RANGES = {
        'Easy':   range(60, 67),
        'Medium': range(72, 79),
        'Hard':   range(84, 91),
        'Expert': range(96, 103),
    }

    avail_levels = {}
    try:
        mid = MidiFile(filepath)
        for track in mid.tracks:
            track_name = track.name.lower().strip()

            # Match track name using MIDI_TRACK_MAP.
            # Longer keys are listed first so "part guitar coop" won't be
            # shadowed by "part guitar".
            matched_inst = None
            for track_raw, inst_clean in MIDI_TRACK_MAP.items():
                if track_name == track_raw or track_name.startswith(track_raw):
                    matched_inst = inst_clean
                    break

            if matched_inst is None:
                continue

            # Collect all note numbers that are actually played in this track
            played_notes = {
                msg.note
                for msg in track
                if msg.type == 'note_on' and msg.velocity > 0
            }

            # Check which difficulty ranges have at least one note
            found_diffs = [
                diff_name
                for diff_name, note_range in DIFF_NOTE_RANGES.items()
                if any(n in note_range for n in played_notes)
            ]

            if found_diffs:
                avail_levels[matched_inst] = found_diffs

            # Pro Drums: tom-marker notes (110-112) inside PART DRUMS signal
            # that this chart supports Pro Drums mode.
            if matched_inst == 'Drums' and played_notes & PRO_DRUMS_MARKERS:
                avail_levels['Pro Drums'] = found_diffs

    except Exception:
        pass
    return avail_levels


def get_chart_levels(root):
    """Find notes.chart or notes.mid and return playable difficulties."""
    for file in os.listdir(root):
        file_lower = file.lower()
        if file_lower == 'notes.chart':
            return parse_chart_difficulties(os.path.join(root, file))
        elif file_lower in ['notes.mid', 'song.mid']:
            return parse_midi_difficulties(os.path.join(root, file))
    return {}



def scan_songs(OS=config.OS):
    errors = []

    # Load hash index (path → hash) and existing catalog (for cache hits)
    hash_index = load_cache()
    existing_catalog = {}
    if os.path.exists("data.json"):
        try:
            with open("data.json", 'r', encoding='utf-8') as f:
                for entry in json.load(f):
                    # Key by (artist, name) so it can retrieve cached entries
                    key = (entry.get('artist', ''), entry.get('name', ''))
                    existing_catalog[key] = entry
        except Exception:
            pass

    print("Finding all song files...")
    song_ini_paths = []
    for root, dirs, files in os.walk(SONGS_PATH):
        ini_filename = find_song_ini(files)
        if ini_filename:
            song_ini_paths.append((root, ini_filename))

    catalog = []
    cache_hits = 0

    for root, ini_filename in tqdm(song_ini_paths, desc="Parsing Charts & Metadata", unit="song"):
        abs_root = os.path.abspath(root)
        current_hash = hash_song_files(root, ini_filename)

        # cache hit: files haven't changed
        if hash_index.get(abs_root) == current_hash:
            filepath = os.path.join(root, ini_filename)
            config_data = read_config(filepath)
            if config_data:
                section = find_song_section(config_data)
                if section:
                    lookup_key = (
                        config_data.get(section, 'artist', fallback='Unknown').strip(),
                        config_data.get(section, 'name',   fallback='Unknown').strip(),
                    )
                    if lookup_key in existing_catalog:
                        catalog.append(existing_catalog[lookup_key])
                        cache_hits += 1
                        continue

        # cache miss: parse from scratch 
        filepath = os.path.join(root, ini_filename)
        config_data = read_config(filepath)

        if config_data is None:
            errors.append(f"[ENCODING ERROR] {filepath}")
            continue

        section = find_song_section(config_data)
        if section is None:
            errors.append(f"[NO SECTION 'song'] {filepath}")
            continue

        try:
            chart_levels = get_chart_levels(root)

            entry = {
                'artist':  config_data.get(section, 'artist',  fallback='Unknown').strip(),
                'name':    config_data.get(section, 'name',    fallback='Unknown').strip(),
                'year':    config_data.get(section, 'year',    fallback='Unknown').strip(),
                'album':   config_data.get(section, 'album',   fallback='').strip(),
                'charter': (config_data.get(section, 'charter', fallback='').strip()
                            or config_data.get(section, 'frets', fallback='').strip()),
                'lenght':  ms_to_min_string(int(config_data.get(section, 'song_length', fallback='0').strip())),
                'video_avail': str(find_videos(root, OS)),
                'genre':   config_data.get(section, 'genre',   fallback='Unknown').strip().title(),
                'playable_levels': chart_levels,
            }

            for key in DIFF_KEYS:
                raw = config_data.get(section, key, fallback='').strip()
                if raw:
                    try:
                        val = int(raw)
                        entry[key] = val

                        inst = DIFF_KEY_TO_INSTRUMENT.get(key)
                        if inst and val >= 0 and inst not in chart_levels:
                            chart_levels[inst] = ['Expert']
                    except ValueError:
                        pass

            catalog.append(entry)
            hash_index[abs_root] = current_hash  # update index with new hash

        except Exception as e:
            errors.append(f"[ERROR PARSEO] {filepath} → {e}")

    # Prune stale index entries (folders that no longer exist)
    existing_roots = {os.path.abspath(r) for r, _ in song_ini_paths}
    stale_keys = [k for k in hash_index if k not in existing_roots]
    for k in stale_keys:
        del hash_index[k]

    save_cache(hash_index)

    with open("data.json", 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=4, ensure_ascii=False)

    with open("logs/scan_errors.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(errors))

    print(f"{len(catalog)} songs saved to data.json  "
          f"({cache_hits} from cache, {len(catalog) - cache_hits} freshly parsed)")
    print(f"{len(errors)} errors saved to logs/scan_errors.txt")
    if stale_keys:
        print(f"{len(stale_keys)} stale cache entries removed.")


def save_genres():
    """Save unique genres to genres.json"""
    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    genres = sorted({item['genre'] for item in data})
    with open("genres.json", 'w', encoding='utf-8') as f:
        json.dump(genres, f, indent=4, ensure_ascii=False)


def get_levels():
    """Aggregate all unique instruments and difficulties across the catalog."""
    levels_summary = {}
    try:
        with open("data.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        for song in data:
            for inst, diffs in song.get('playable_levels', {}).items():
                levels_summary.setdefault(inst, set()).update(diffs)
        return {k: sorted(list(v)) for k, v in levels_summary.items()}
    except Exception:
        return {}


if __name__ == "__main__":
    scan_songs()
    save_genres()

    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "**Mevami** is an automated system" in content:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write("# My Clone Hero Setlist\n\nPowered by [Mevami](https://github.com/s3vro-h1/mevami)\n")
            print("README.md updated for your personal repo.")