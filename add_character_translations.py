#!/usr/bin/env python3
"""Add character translations to all language files"""

import json
from pathlib import Path

LANGUAGES_DIR = Path(__file__).parent / "languages"

character_translations = {
    "select_title": "🎭 Choose Your AI Character",
    "select_subtitle": "Select a character that matches your style:",
    "selected": "✅ You selected: **{name}**\n\n{description}\n\nYou can change your character anytime from the menu!",
    "change_character": "🎭 Change Character",
    "no_character_selected": "⚠️ **Please select a character first!**\n\nUse /start to choose your AI character.",
    "current_character": "🎭 **Current Character:**\n**{name}**\n{description}"
}

language_files = ['es.json', 'fa.json', 'ar.json', 'ru.json', 'tr.json', 'zh.json']

for lang_file in language_files:
    file_path = LANGUAGES_DIR / lang_file
    
    if file_path.exists():
        print(f"Updating {lang_file}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add character section
        data['character'] = character_translations
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Updated {lang_file}")
    else:
        print(f"❌ File not found: {lang_file}")

print("\n✅ All language files updated with character translations!")
