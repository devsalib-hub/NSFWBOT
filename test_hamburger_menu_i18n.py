#!/usr/bin/env python3
"""
Test script for the hamburger menu internationalization (i18n) system.
This script tests the menu descriptions in all supported languages.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from translations import translation_manager, get_text
from database import Database

def test_menu_descriptions():
    """Test menu descriptions in all languages"""
    print("🧪 Testing Hamburger Menu Descriptions...")
    print("=" * 60)
    
    # Commands to test
    menu_commands = [
        'start', 'help', 'dashboard', 'reset', 'packages', 
        'balance', 'referral', 'language'
    ]
    
    languages = translation_manager.get_available_languages()
    
    for lang_code, lang_name in languages.items():
        print(f"\n🌐 {lang_name} ({lang_code}):")
        print("-" * 40)
        
        for command in menu_commands:
            description = get_text(f'menu_descriptions.{command}', lang_code)
            print(f"  /{command} - {description}")

def test_bot_menu_generation():
    """Test bot menu generation for different languages"""
    print("\n\n🧪 Testing Bot Menu Generation...")
    print("=" * 60)
    
    languages = translation_manager.get_available_languages()
    
    for lang_code, lang_name in languages.items():
        print(f"\n🌐 Bot Menu for {lang_name} ({lang_code}):")
        print("-" * 40)
        
        # Simulate bot menu commands
        menu_items = [
            ("start", get_text('menu_descriptions.start', lang_code)),
            ("help", get_text('menu_descriptions.help', lang_code)),
            ("language", get_text('menu_descriptions.language', lang_code)),
            ("dashboard", get_text('menu_descriptions.dashboard', lang_code)),
            ("reset", get_text('menu_descriptions.reset', lang_code)),
            ("packages", get_text('menu_descriptions.packages', lang_code)),
            ("balance", get_text('menu_descriptions.balance', lang_code)),
            ("referral", get_text('menu_descriptions.referral', lang_code))
        ]
        
        for command, description in menu_items:
            # Limit description length for display (Telegram has limits)
            truncated_desc = description[:60] + "..." if len(description) > 60 else description
            print(f"  BotCommand('{command}', '{truncated_desc}')")

def test_language_statistics():
    """Test language usage statistics"""
    print("\n\n🧪 Testing Language Usage Statistics...")
    print("=" * 60)
    
    try:
        db = Database()
        
        # Create some test users with different languages
        test_users = [
            (111111111, 'en'),
            (222222222, 'es'), 
            (333333333, 'es'),
            (444444444, 'ar'),
            (555555555, 'fa'),
            (666666666, 'es')  # Spanish is most common
        ]
        
        for user_id, lang in test_users:
            db.create_user(user_id, f"test_user_{user_id}", "Test", "User")
            db.set_user_language(user_id, lang)
        
        # Test most common language detection
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT language, COUNT(*) as count 
            FROM users 
            WHERE language IS NOT NULL 
            GROUP BY language 
            ORDER BY count DESC
        """)
        
        results = cursor.fetchall()
        
        print("\nLanguage usage statistics:")
        for lang, count in results:
            lang_name = translation_manager.get_language_name(lang)
            print(f"  {lang_name} ({lang}): {count} users")
        
        if results:
            most_common = results[0][0]
            most_common_name = translation_manager.get_language_name(most_common)
            print(f"\n✅ Most common language: {most_common_name} ({most_common})")
        
        # Clean up test users
        for user_id, _ in test_users:
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Language statistics test failed: {e}")

def test_menu_completeness():
    """Test if all menu descriptions are available in all languages"""
    print("\n\n🧪 Testing Menu Description Completeness...")
    print("=" * 60)
    
    languages = translation_manager.get_available_languages()
    menu_commands = [
        'start', 'help', 'dashboard', 'reset', 'packages', 
        'balance', 'referral', 'language', 'testapi', 'venicestatus'
    ]
    
    missing_translations = {}
    
    for lang_code in languages.keys():
        if lang_code == 'en':
            continue  # Skip English as it's the base
            
        missing_in_lang = []
        for command in menu_commands:
            description = translation_manager._get_nested_translation(
                translation_manager.translations.get(lang_code, {}), 
                f'menu_descriptions.{command}'
            )
            if description is None:
                missing_in_lang.append(command)
        
        if missing_in_lang:
            missing_translations[lang_code] = missing_in_lang
    
    if missing_translations:
        print("\n⚠️  Missing menu descriptions:")
        for lang_code, missing in missing_translations.items():
            lang_name = translation_manager.get_language_name(lang_code)
            print(f"  {lang_name} ({lang_code}): {', '.join(missing)}")
    else:
        print("\n✅ All menu descriptions are complete in all languages!")

def main():
    """Run all hamburger menu i18n tests"""
    print("🍔 Testing Hamburger Menu Internationalization (i18n)\n")
    
    test_menu_descriptions()
    test_bot_menu_generation() 
    test_language_statistics()
    test_menu_completeness()
    
    print("\n" + "=" * 60)
    print("🎉 Hamburger Menu i18n Test Complete!")
    print("\n📝 Notes:")
    print("- Telegram bot menus are global (affect all users)")
    print("- Menu updates when users change language")
    print("- Default menu uses most common user language")
    print("- Menu descriptions are limited to ~60 characters by Telegram")

if __name__ == "__main__":
    main()