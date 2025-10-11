#!/usr/bin/env python3
"""
Simple test for payment settings migration
"""
import sys
sys.path.append('.')

from database import Database

def test_migration():
    """Test the payment settings migration"""
    print("🔄 Testing payment settings migration...")
    
    db = Database()
    
    # Check current settings
    print("\n📋 Current settings:")
    print(f"   - Old TON wallet: {db.get_setting('ton_wallet_address', 'NOT_SET')}")
    print(f"   - Old testnet mode: {db.get_setting('ton_testnet_mode', 'NOT_SET')}")
    print(f"   - New mainnet wallet: {db.get_setting('ton_mainnet_wallet_address', 'NOT_SET')}")
    print(f"   - New testnet wallet: {db.get_setting('ton_testnet_wallet_address', 'NOT_SET')}")
    print(f"   - New network mode: {db.get_setting('ton_network_mode', 'NOT_SET')}")
    
    # If we have old settings but no new ones, simulate migration
    old_wallet = db.get_setting('ton_wallet_address', '')
    old_testnet = db.get_setting('ton_testnet_mode', 'true').lower() == 'true'
    
    if old_wallet:
        print(f"\n🔧 Setting up new payment settings based on old ones...")
        db.update_setting('ton_mainnet_wallet_address', old_wallet)
        db.update_setting('ton_testnet_wallet_address', old_wallet)
        db.update_setting('ton_network_mode', 'sandbox' if old_testnet else 'mainnet')
        print("✅ Migration completed!")
    else:
        print("\n💡 Setting up sample settings for testing...")
        db.update_setting('ton_mainnet_wallet_address', 'UQMainnetSampleWalletAddress123')
        db.update_setting('ton_testnet_wallet_address', 'UQTestnetSampleWalletAddress456')
        db.update_setting('ton_network_mode', 'sandbox')
        print("✅ Sample settings created!")
    
    print("\n📋 Final settings:")
    print(f"   - Mainnet wallet: {db.get_setting('ton_mainnet_wallet_address', 'NOT_SET')}")
    print(f"   - Testnet wallet: {db.get_setting('ton_testnet_wallet_address', 'NOT_SET')}")
    print(f"   - Network mode: {db.get_setting('ton_network_mode', 'NOT_SET')}")

if __name__ == "__main__":
    test_migration()