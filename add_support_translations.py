#!/usr/bin/env python3
"""Add support button translation to all language files"""

import json
from pathlib import Path

LANGUAGES_DIR = Path(__file__).parent / "languages"

language_files = ['es.json', 'fa.json', 'ar.json', 'ru.json', 'tr.json', 'zh.json']

for lang_file in language_files:
    file_path = LANGUAGES_DIR / lang_file
    
    if file_path.exists():
        print(f"Updating {lang_file}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add support button translation
        if 'buttons' in data:
            data['buttons']['contact_support'] = "💬 Contact Support"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Updated {lang_file}")
    else:
        print(f"❌ File not found: {lang_file}")

print("\n✅ All language files updated with support button translation!")
