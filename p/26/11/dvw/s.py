#!/usr/bin/env python3
import os
import sys
from pathlib import Path

"""
Script conceived, written and edited by sgn98 from and to 12·Nov·2026; with final refinements on 19·Nov·2026.

To execute it, from in a terminal, bash or cmd:
python s.py
"""

"""
Script ideato, scritto e curato da sgn98 dal e al 12·Nov·2026, ma rifinito meglio nel 19·Nov·2026.

Per eseguirlo, da terminale, bash o cmd:
python s.py
"""

RULES_CONFIG = {
    'ita': {
        'a': 'h', 'A': 'H',
        'e': 'l', 'E': 'L',
        'i': 'j', 'I': 'J',
        'o': 'v', 'O': 'V',
        'u': 'w', 'U': 'W',
        'y': 'z', 'Y': 'Z' },
    'eng': {
        'a': 'r', 'A': 'R',
        'e': 's', 'E': 'S',
        'i': 'y', 'I': 'Y',
        'o': 'w', 'O': 'W',
        'u': 'j', 'U': 'J',
        'y': 'h', 'Y': 'H' } }

EXTENSIONS = {'.txt', '.md', '.html'}

def get_files_in_directory(directory_path):
    files = []
    if not directory_path.exists(): sys.exit(1)
    if not directory_path.is_dir(): sys.exit(1)

    for f in directory_path.iterdir():
        if f.is_file() and f.suffix.lower() in EXTENSIONS: files.append(f)
            
    return sorted(files, key=lambda p: p.name)

def convert_file(src_path, dst_path, rules):
    try:
        try:
            content = src_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = src_path.read_text(encoding='latin-1')

        trans_table = str.maketrans(rules)
        converted_content = content.translate(trans_table)

        dst_path.write_text(converted_content, encoding='utf-8')
        return True
        
    except Exception as e:
        return False

def main():
    print("\n### CHOOSE LANG. / SCEGLI LINGUA ###")
    print("1) Italiano")
    print("2) English")
    
    lang_choice = input("-> ").strip()
    if lang_choice == '1':
        current_rules = RULES_CONFIG['ita']
        lang_name = "Italiano"
    elif lang_choice == '2':
        current_rules = RULES_CONFIG['eng']
        lang_name = "English"
    else:
        print("→ Default: Italiano")
        current_rules = RULES_CONFIG['ita']
        lang_name = "Default"

    target_dir = Path.cwd()
    
    available_files = get_files_in_directory(target_dir)
    
    if not available_files: return

    print("\n### WHICH ONE TO CONVERT? / QUALE CONVERTI? ###")
    for i, fpath in enumerate(available_files, 1):
        print(f"{i}) {fpath.name}")
    
    try:
        choice_idx = int(input("-> ")) - 1
        if 0 <= choice_idx < len(available_files):
            selected_file = available_files[choice_idx]
        else:
            return
    except ValueError:
        return

    src_path = selected_file
    name_part = src_path.stem
    ext_part = src_path.suffix
    dst_filename = f"{name_part}_converted{ext_part}"
    dst_path = target_dir / dst_filename
    
    if convert_file(src_path, dst_path, current_rules):
        print(f"Before / Prima: {src_path.name}")
        print(f"After / Dopo: {dst_filename}")
        
        try:
            preview = dst_path.read_text(encoding='utf-8')
            lines = preview.splitlines()[:5]
            if lines:
                print("\n### PREVIEW / ANTEPRIMA ###")
                for line in lines:
                    print(line)
            else:
                print("(Empty file / File vuoto)")
        except Exception as e:
            print(f"(Unreadable Preview / Anteprima illegibile: {e})")
    else:
        print("Ouch...")

if __name__ == "__main__":
    main()