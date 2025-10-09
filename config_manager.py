#!/usr/bin/env python3
"""
Configuration Management Utility
Helps manage bot configuration through command line or interactive mode
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self, env_file='.env'):
        self.env_file = Path(env_file)
        self.config = {}
        
        if self.env_file.exists():
            self.load_config()
    
    def load_config(self):
        """Load configuration from .env file"""
        with open(self.env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    self.config[key.strip()] = value.strip()
    
    def save_config(self):
        """Save configuration to .env file"""
        with open(self.env_file, 'w') as f:
            f.write("# Telegram Bot Configuration\n")
            f.write("# Generated automatically - modify with caution\n\n")
            
            for key, value in self.config.items():
                f.write(f"{key}={value}\n")
        
        print(f"✅ Configuration saved to {self.env_file}")
    
    def set_config(self, key: str, value: str):
        """Set a configuration value"""
        self.config[key] = value
        print(f"✅ Set {key} = {value}")
    
    def get_config(self, key: str) -> str:
        """Get a configuration value"""
        return self.config.get(key, "")
    
    def interactive_setup(self):
        """Interactive configuration setup"""
        print("🤖 Telegram Bot Configuration Setup")
        print("=" * 50)
        
        # Bot Token
        bot_token = input("Enter your Telegram Bot Token (from @BotFather): ").strip()
        if bot_token:
            self.set_config('BOT_TOKEN', bot_token)
        
        # Admin Chat ID
        admin_id = input("Enter your Telegram User ID (admin): ").strip()
        if admin_id:
            self.set_config('ADMIN_CHAT_ID', admin_id)
        
        # OpenRouter API Key
        print("\n🧠 AI Configuration")
        openrouter_key = input("Enter your OpenRouter API Key (from openrouter.ai): ").strip()
        if openrouter_key:
            self.set_config('OPENROUTER_API_KEY', openrouter_key)
        
        # AI Model
        print("\nAvailable AI Models:")
        models = [
            "openai/gpt-3.5-turbo (Fast, cheap)",
            "openai/gpt-4 (Better quality, more expensive)",
            "anthropic/claude-3-haiku (Fast Claude)",
            "anthropic/claude-3-sonnet (Balanced Claude)",
            "google/gemini-pro (Google's model)",
            "mistralai/mistral-7b-instruct (Open source)"
        ]
        
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
        
        model_choice = input("Choose AI model (1-6, default: 1): ").strip()
        model_map = {
            '1': 'openai/gpt-3.5-turbo',
            '2': 'openai/gpt-4',
            '3': 'anthropic/claude-3-haiku',
            '4': 'anthropic/claude-3-sonnet',
            '5': 'google/gemini-pro',
            '6': 'mistralai/mistral-7b-instruct'
        }
        
        selected_model = model_map.get(model_choice, 'openai/gpt-3.5-turbo')
        self.set_config('OPENROUTER_MODEL', selected_model)
        
        # Payment Configuration
        print("\n💰 Payment Configuration")
        ton_wallet = input("Enter your TON Wallet Address (optional): ").strip()
        if ton_wallet:
            self.set_config('TON_WALLET_ADDRESS', ton_wallet)
        
        # Admin Dashboard
        print("\n🔧 Admin Dashboard")
        admin_user = input("Admin username (default: admin): ").strip() or "admin"
        admin_pass = input("Admin password (default: admin123): ").strip() or "admin123"
        
        self.set_config('ADMIN_USERNAME', admin_user)
        self.set_config('ADMIN_PASSWORD', admin_pass)
        
        # Basic Settings
        print("\n⚙️ Basic Settings")
        sim_mode = input("Enable simulation mode for testing? (y/N): ").strip().lower()
        self.set_config('SIMULATION_MODE', 'true' if sim_mode == 'y' else 'false')
        
        free_msgs = input("Number of free messages per user (default: 1): ").strip() or "1"
        self.set_config('FREE_MESSAGES', free_msgs)
        
        # Set defaults for other settings
        self.set_config('DATABASE_PATH', 'bot_database.db')
        self.set_config('DASHBOARD_HOST', '127.0.0.1')
        self.set_config('DASHBOARD_PORT', '5000')
        self.set_config('SECRET_KEY', 'change-this-secret-key-in-production')
        self.set_config('BOT_RUNNING', 'true')
        self.set_config('TELEGRAM_STARS_ENABLED', 'true')
        self.set_config('TON_ENABLED', 'true')
        self.set_config('DEFAULT_TEXT_PRICE', '1')
        self.set_config('DEFAULT_IMAGE_PRICE', '2')
        self.set_config('DEFAULT_VIDEO_PRICE', '3')
        self.set_config('MAX_IMAGE_SIZE', '10')
        self.set_config('MAX_VIDEO_SIZE', '50')
        self.set_config('AI_RESPONSE_TIMEOUT', '30')
        self.set_config('MAX_REQUESTS_PER_MINUTE', '20')
        self.set_config('MAX_REQUESTS_PER_HOUR', '100')
        self.set_config('LOG_LEVEL', 'INFO')
        
        print("\n✅ Configuration complete!")
        
        save = input("Save configuration to .env file? (Y/n): ").strip().lower()
        if save != 'n':
            self.save_config()
    
    def validate_config(self):
        """Validate current configuration"""
        errors = []
        warnings = []
        
        # Required settings
        required = ['BOT_TOKEN', 'OPENROUTER_API_KEY']
        for key in required:
            if not self.config.get(key):
                errors.append(f"Missing required setting: {key}")
        
        # Recommended settings
        recommended = ['ADMIN_CHAT_ID', 'TON_WALLET_ADDRESS']
        for key in recommended:
            if not self.config.get(key):
                warnings.append(f"Recommended setting not configured: {key}")
        
        # Validate values
        try:
            int(self.config.get('ADMIN_CHAT_ID', '0'))
        except ValueError:
            errors.append("ADMIN_CHAT_ID must be a number")
        
        try:
            int(self.config.get('FREE_MESSAGES', '1'))
        except ValueError:
            errors.append("FREE_MESSAGES must be a number")
        
        # Print results
        if errors:
            print("❌ Configuration Errors:")
            for error in errors:
                print(f"  - {error}")
        
        if warnings:
            print("⚠️ Configuration Warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        
        if not errors and not warnings:
            print("✅ Configuration is valid!")
        
        return len(errors) == 0
    
    def show_config(self):
        """Display current configuration (masking sensitive values)"""
        print("📋 Current Configuration:")
        print("=" * 50)
        
        sensitive_keys = ['BOT_TOKEN', 'OPENROUTER_API_KEY', 'ADMIN_PASSWORD', 'SECRET_KEY']
        
        for key, value in sorted(self.config.items()):
            if key in sensitive_keys and value:
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                display_value = value
            
            print(f"{key:<25} = {display_value}")

def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Telegram Bot Configuration Manager")
    parser.add_argument('--setup', action='store_true', help='Interactive setup')
    parser.add_argument('--validate', action='store_true', help='Validate configuration')
    parser.add_argument('--show', action='store_true', help='Show current configuration')
    parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='Set configuration value')
    parser.add_argument('--get', metavar='KEY', help='Get configuration value')
    parser.add_argument('--env-file', default='.env', help='Environment file path')
    
    args = parser.parse_args()
    
    config_manager = ConfigManager(args.env_file)
    
    if args.setup:
        config_manager.interactive_setup()
    elif args.validate:
        config_manager.validate_config()
    elif args.show:
        config_manager.show_config()
    elif args.set:
        key, value = args.set
        config_manager.set_config(key, value)
        config_manager.save_config()
    elif args.get:
        value = config_manager.get_config(args.get)
        print(f"{args.get} = {value}")
    else:
        print("🤖 Telegram Bot Configuration Manager")
        print("Use --help for available options")
        print("\nQuick start: python config_manager.py --setup")

if __name__ == "__main__":
    main()