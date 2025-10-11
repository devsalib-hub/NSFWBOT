#!/usr/bin/env python3
"""
Clean up script to remove simulation_mode setting from database
"""
import sys
import sqlite3
sys.path.append('.')

from database import Database

def cleanup_simulation_mode():
    """Remove simulation_mode setting from database"""
    print("🧹 Cleaning up simulation_mode from database...")
    
    db = Database()
    
    # Check if simulation_mode exists
    simulation_setting = db.get_setting('simulation_mode', 'NOT_FOUND')
    print(f"Current simulation_mode value: {simulation_setting}")
    
    if simulation_setting != 'NOT_FOUND':
        # Remove the setting from database
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM admin_settings WHERE key = ?', ('simulation_mode',))
        conn.commit()
        conn.close()
        
        print("✅ simulation_mode setting removed from database")
        
        # Verify removal
        verification = db.get_setting('simulation_mode', 'NOT_FOUND')
        if verification == 'NOT_FOUND':
            print("✅ Verification: simulation_mode successfully removed")
        else:
            print("❌ Verification failed: simulation_mode still exists")
    else:
        print("ℹ️  simulation_mode setting not found in database")
    
    print("\n📋 Current payment-related settings:")
    settings = ['ton_network_mode', 'ton_mainnet_wallet_address', 'ton_testnet_wallet_address']
    for setting in settings:
        value = db.get_setting(setting, 'NOT_SET')
        print(f"   - {setting}: {value}")

if __name__ == "__main__":
    cleanup_simulation_mode()