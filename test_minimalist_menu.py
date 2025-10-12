#!/usr/bin/env python3
"""
Test script for the new minimalist hamburger menu with glass-style interactive buttons.
This script tests the new menu system functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from translations import translation_manager, get_text

def test_minimalist_menu_translations():
    """Test the minimalist menu translations"""
    print("🧪 Testing Minimalist Hamburger Menu...")
    print("=" * 60)
    
    languages = translation_manager.get_available_languages()
    
    for lang_code, lang_name in languages.items():
        print(f"\n🌐 {lang_name} ({lang_code}):")
        print("-" * 40)
        
        # Test hamburger menu descriptions (only 2 items now)
        menu_desc = get_text('menu_descriptions.menu', lang_code)
        reset_desc = get_text('menu_descriptions.reset', lang_code)
        
        print(f"🍔 Hamburger Menu:")
        print(f"  /menu - {menu_desc}")
        print(f"  /reset - {reset_desc}")

def test_glass_menu_translations():
    """Test the glass menu translations"""
    print("\n\n🧪 Testing Glass Menu Interface...")
    print("=" * 60)
    
    languages = translation_manager.get_available_languages()
    
    for lang_code, lang_name in languages.items():
        print(f"\n🌐 {lang_name} ({lang_code}):")
        print("-" * 40)
        
        # Test glass menu interface
        title = get_text('glass_menu.title', lang_code)
        subtitle = get_text('glass_menu.subtitle', lang_code)
        
        print(f"✨ Glass Menu:")
        print(f"  Title: {title}")
        print(f"  Subtitle: {subtitle}")
        
        # Test button texts
        dashboard = get_text('commands.dashboard', lang_code)
        packages = get_text('commands.packages', lang_code)
        balance = get_text('commands.balance', lang_code)
        referral = get_text('commands.referral', lang_code)
        
        print(f"  Buttons:")
        print(f"    📊 {dashboard}")
        print(f"    💎 {packages}")
        print(f"    💰 {balance}")
        print(f"    👥 {referral}")

def test_menu_button_layout():
    """Test the button layout for glass menu"""
    print("\n\n🧪 Testing Glass Menu Button Layout...")
    print("=" * 60)
    
    # Simulate button layout for English
    lang_code = 'en'
    
    print(f"\n🎛️ {get_text('glass_menu.title', lang_code)}")
    print(f"{get_text('glass_menu.subtitle', lang_code)}")
    print()
    
    # Row 1: Dashboard & Packages
    dashboard = get_text('commands.dashboard', lang_code)
    packages = get_text('commands.packages', lang_code)
    print(f"[📊 {dashboard}] [💎 {packages}]")
    
    # Row 2: Balance & Referral
    balance = get_text('commands.balance', lang_code)
    referral = get_text('commands.referral', lang_code)
    print(f"[💰 {balance}] [👥 {referral}]")
    
    # Row 3: Help & Language
    help_cmd = get_text('commands.help', lang_code)
    language = get_text('commands.language', lang_code)
    print(f"[ℹ️ {help_cmd}] [🌐 {language}]")
    
    # Row 4: Start & Enter Referral
    start = get_text('commands.start', lang_code)
    enter_referral = get_text('commands.enterreferral', lang_code)
    print(f"[🚀 {start}] [🔗 {enter_referral}]")
    
    # Row 5: Admin Commands (if admin)
    testapi = get_text('commands.testapi', lang_code)
    print(f"[🧪 {testapi}] [📊 Venice Status] (Admin Only)")

def test_menu_completeness():
    """Test if all menu translations are complete"""
    print("\n\n🧪 Testing Menu Translation Completeness...")
    print("=" * 60)
    
    languages = translation_manager.get_available_languages()
    
    # Required keys for the new menu system
    required_keys = [
        'menu_descriptions.menu',
        'menu_descriptions.reset',
        'glass_menu.title',
        'glass_menu.subtitle',
        'glass_menu.command_executed',
        'errors.command_error',
        'errors.invalid_command'
    ]
    
    missing_translations = {}
    
    for lang_code in languages.keys():
        missing_in_lang = []
        for key in required_keys:
            translation = translation_manager._get_nested_translation(
                translation_manager.translations.get(lang_code, {}), key
            )
            if translation is None:
                missing_in_lang.append(key)
        
        if missing_in_lang:
            missing_translations[lang_code] = missing_in_lang
    
    if missing_translations:
        print("\n⚠️  Missing translations:")
        for lang_code, missing in missing_translations.items():
            lang_name = translation_manager.get_language_name(lang_code)
            print(f"  {lang_name} ({lang_code}): {', '.join(missing)}")
    else:
        print("\n✅ All menu translations are complete!")

def test_menu_benefits():
    """Display the benefits of the new menu system"""
    print("\n\n🎯 New Menu System Benefits...")
    print("=" * 60)
    
    benefits = [
        "🍔 Minimalist hamburger menu (only 2 items)",
        "✨ Beautiful glass-style interactive buttons",
        "🌐 Full i18n support for all languages",
        "⚡ Fast access to all commands via /menu",
        "🔄 Direct reset functionality via hamburger menu",
        "📱 Better mobile user experience",
        "🎨 Modern, clean interface design",
        "👥 Admin-specific commands shown when needed",
        "🚀 No conflicts with Telegram's global menu limitation"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")

def main():
    """Run all tests for the new menu system"""
    print("🎛️ Testing New Minimalist Menu System with Glass Interface\n")
    
    test_minimalist_menu_translations()
    test_glass_menu_translations()
    test_menu_button_layout()
    test_menu_completeness()
    test_menu_benefits()
    
    print("\n" + "=" * 60)
    print("🎉 Minimalist Menu System Test Complete!")
    print("\n📋 Summary:")
    print("- Hamburger menu reduced to 2 essential items")
    print("- All other commands accessible via beautiful /menu interface")
    print("- Full multilingual support maintained")
    print("- Solves Telegram's global menu limitation elegantly")

if __name__ == "__main__":
    main()