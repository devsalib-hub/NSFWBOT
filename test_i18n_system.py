#!/usr/bin/env python3
"""
Test script for the i18n (internationalization) system.
This script tests all major components of the translation system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from translations import translation_manager, get_text, get_user_language, set_user_language
from database import Database

def test_translation_manager():
    """Test the translation manager functionality"""
    print("🧪 Testing Translation Manager...")
    
    # Test supported languages
    languages = translation_manager.get_available_languages()
    print(f"✅ Supported languages: {list(languages.keys())}")
    
    # Test translation loading
    for lang_code in languages.keys():
        welcome_msg = get_text('welcome.title', lang_code, first_name='Test')
        print(f"   {lang_code}: {welcome_msg}")
    
    print()

def test_database_integration():
    """Test database language preference functionality"""
    print("🧪 Testing Database Integration...")
    
    try:
        db = Database()
        test_user_id = 999999999  # Test user ID
        
        # Create test user first
        db.create_user(test_user_id, "test_user", "Test", "User")
        
        # Test setting language preference
        db.set_user_language(test_user_id, 'es')
        user_lang = db.get_user_language(test_user_id)
        print(f"✅ Set user language to 'es', retrieved: '{user_lang}'")
        
        # Test default language for non-existent user
        default_lang = db.get_user_language(888888888)
        print(f"✅ Default language for new user: '{default_lang}'")
        
        # Clean up test user
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (test_user_id,))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
    
    print()

def test_fallback_system():
    """Test translation fallback system"""
    print("🧪 Testing Fallback System...")
    
    # Test key that doesn't exist - should return the key itself
    missing_key = get_text('nonexistent.key', 'en')
    print(f"✅ Missing key fallback: '{missing_key}'")
    
    # Test language that doesn't exist - should fallback to English
    fallback_text = get_text('welcome.title', 'invalid_lang', first_name='Test')
    english_text = get_text('welcome.title', 'en', first_name='Test')
    if fallback_text == english_text:
        print(f"✅ Language fallback to English works")
    else:
        print(f"❌ Language fallback failed")
    
    print()

def test_variable_formatting():
    """Test variable formatting in translations"""
    print("🧪 Testing Variable Formatting...")
    
    # Test with variables
    text_with_vars = get_text('welcome.free_messages', 'en', 
                            free_text=10, free_image=5, free_video=3)
    print(f"✅ Variable formatting: {text_with_vars[:50]}...")
    
    # Test with missing variables - should not crash
    try:
        text_missing_vars = get_text('welcome.free_messages', 'en')
        print(f"✅ Missing variables handled gracefully")
    except Exception as e:
        print(f"❌ Missing variables caused error: {e}")
    
    print()

def test_all_languages_completeness():
    """Test if all languages have the same keys available"""
    print("🧪 Testing Language Completeness...")
    
    languages = translation_manager.get_available_languages()
    
    # Get all keys from English (base language)
    english_keys = set()
    def collect_keys(obj, prefix=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, str):
                    english_keys.add(full_key)
                else:
                    collect_keys(value, full_key)
    
    en_translations = translation_manager.translations.get('en', {})
    collect_keys(en_translations)
    
    print(f"✅ Found {len(english_keys)} translation keys in English")
    
    # Check each language for missing keys
    for lang_code in languages.keys():
        if lang_code == 'en':
            continue
            
        missing_keys = []
        for key in english_keys:
            text = translation_manager._get_nested_translation(
                translation_manager.translations.get(lang_code, {}), key)
            if text is None:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"⚠️  {lang_code}: Missing {len(missing_keys)} keys")
        else:
            print(f"✅ {lang_code}: All keys present")
    
    print()

def main():
    """Run all tests"""
    print("🌐 Testing Internationalization (i18n) System\n")
    print("=" * 50)
    
    test_translation_manager()
    test_database_integration()
    test_fallback_system()
    test_variable_formatting()
    test_all_languages_completeness()
    
    print("=" * 50)
    print("🎉 i18n System Test Complete!")

if __name__ == "__main__":
    main()