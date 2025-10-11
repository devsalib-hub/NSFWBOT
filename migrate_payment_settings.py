#!/usr/bin/env python3
"""
Migration script to update payment settings from old format to new format.

This script migrates:
- ton_wallet_address -> ton_mainnet_wallet_address and ton_testnet_wallet_address
- ton_testnet_mode -> ton_network_mode (boolean to dropdown)

Run this once after updating to the new payment system.
"""

import sqlite3
import sys
import os
from database import Database

def migrate_payment_settings():
    """Migrate old payment settings to new format"""
    print("🔄 Migrating payment settings...")
    
    try:
        db = Database()
        
        # Get existing settings
        old_wallet_address = db.get_setting('ton_wallet_address', '')
        old_testnet_mode = db.get_setting('ton_testnet_mode', 'true').lower() == 'true'
        
        # Check if migration is needed
        if not old_wallet_address:
            print("ℹ️  No existing TON wallet address found, skipping migration.")
            return True
            
        # Check if new settings already exist
        mainnet_wallet = db.get_setting('ton_mainnet_wallet_address', '')
        testnet_wallet = db.get_setting('ton_testnet_wallet_address', '')
        network_mode = db.get_setting('ton_network_mode', '')
        
        if mainnet_wallet or testnet_wallet or network_mode:
            print("ℹ️  New payment settings already exist, skipping migration.")
            return True
        
        print(f"📋 Found existing settings:")
        print(f"   - TON Wallet Address: {old_wallet_address}")
        print(f"   - Testnet Mode: {old_testnet_mode}")
        
        # Migrate wallet addresses
        # Set the old address to both mainnet and testnet (user can update later)
        db.update_setting('ton_mainnet_wallet_address', old_wallet_address)
        db.update_setting('ton_testnet_wallet_address', old_wallet_address)
        
        # Migrate network mode
        if old_testnet_mode:
            db.update_setting('ton_network_mode', 'sandbox')
        else:
            db.update_setting('ton_network_mode', 'mainnet')
        
        print("✅ Migration completed successfully!")
        print(f"   - Mainnet wallet address: {old_wallet_address}")
        print(f"   - Testnet wallet address: {old_wallet_address}")
        print(f"   - Network mode: {'sandbox' if old_testnet_mode else 'mainnet'}")
        print("")
        print("💡 You can now update the wallet addresses separately in the admin dashboard.")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False

def main():
    """Main migration function"""
    print("🚀 Payment Settings Migration Tool")
    print("=" * 50)
    
    if migrate_payment_settings():
        print("\n🎉 Migration completed successfully!")
        print("You can now use the new payment configuration UI in the admin dashboard.")
    else:
        print("\n💥 Migration failed! Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()