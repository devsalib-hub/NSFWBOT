#!/usr/bin/env python3
"""
Quick setup script for TON Testnet testing
"""

from database import Database
import sys

def setup_testnet_mode():
    """Configure bot for testnet testing"""
    print("🧪 Setting up TON Testnet Mode...")
    
    db = Database()
    
    # Get current settings
    current_sim = db.get_setting('simulation_mode', 'true')
    current_testnet = db.get_setting('ton_testnet_mode', 'true')
    current_wallet = db.get_setting('ton_wallet_address', '')
    
    print(f"\n📋 Current Configuration:")
    print(f"   Simulation Mode: {current_sim}")
    print(f"   TON Testnet Mode: {current_testnet}")
    print(f"   Wallet Address: {current_wallet[:20]}..." if current_wallet else "   Wallet Address: Not set")
    
    print(f"\n🔧 Configuring for Testnet Testing...")
    
    # Configure for testnet
    settings = {
        'simulation_mode': 'false',          # Disable simulation
        'ton_testnet_mode': 'true',          # Enable testnet
        'ton_enabled': 'true',               # Enable TON payments
        'telegram_stars_enabled': 'true',    # Keep stars enabled too
    }
    
    for key, value in settings.items():
        db.update_setting(key, value)
        print(f"   ✅ {key}: {value}")
    
    print(f"\n⚠️  IMPORTANT: You still need to:")
    print(f"   1. Set your testnet wallet address in admin dashboard")
    print(f"   2. Get test TON from faucet")
    print(f"   3. Test payment flow")
    
    print(f"\n🌐 Admin Dashboard: http://localhost:5000/settings")
    print(f"🔗 Testnet Faucet: https://testnet.tonscan.org/faucet")
    
    return True

def setup_simulation_mode():
    """Configure bot for simulation testing"""
    print("🎮 Setting up Simulation Mode...")
    
    db = Database()
    
    # Configure for simulation
    settings = {
        'simulation_mode': 'true',           # Enable simulation
        'ton_testnet_mode': 'true',          # Keep testnet mode for consistency
        'ton_enabled': 'true',               # Enable TON payments
        'telegram_stars_enabled': 'true',    # Keep stars enabled too
    }
    
    for key, value in settings.items():
        db.update_setting(key, value)
        print(f"   ✅ {key}: {value}")
    
    print(f"\n✅ Simulation mode enabled - all payments will auto-complete!")
    return True

def setup_production_mode():
    """Configure bot for production (mainnet)"""
    print("🌐 Setting up Production Mode...")
    
    db = Database()
    current_wallet = db.get_setting('ton_wallet_address', '')
    
    if not current_wallet:
        print("❌ ERROR: No wallet address set!")
        print("   Please set your MAINNET wallet address first!")
        return False
    
    print("⚠️  WARNING: This will enable REAL payments with REAL money!")
    confirm = input("Type 'CONFIRM' to enable production mode: ")
    
    if confirm != 'CONFIRM':
        print("❌ Production mode setup cancelled.")
        return False
    
    # Configure for production
    settings = {
        'simulation_mode': 'false',          # Disable simulation
        'ton_testnet_mode': 'false',         # Disable testnet (use mainnet)
        'ton_enabled': 'true',               # Enable TON payments
        'telegram_stars_enabled': 'true',    # Keep stars enabled
    }
    
    for key, value in settings.items():
        db.update_setting(key, value)
        print(f"   ✅ {key}: {value}")
    
    print(f"\n🚨 PRODUCTION MODE ENABLED!")
    print(f"   Real payments will be processed!")
    print(f"   Monitor closely for initial transactions!")
    
    return True

def show_current_status():
    """Show current bot payment configuration"""
    print("📊 Current Bot Payment Configuration:")
    
    db = Database()
    
    settings = {
        'simulation_mode': db.get_setting('simulation_mode', 'true'),
        'ton_testnet_mode': db.get_setting('ton_testnet_mode', 'true'),
        'ton_enabled': db.get_setting('ton_enabled', 'true'),
        'telegram_stars_enabled': db.get_setting('telegram_stars_enabled', 'true'),
        'ton_wallet_address': db.get_setting('ton_wallet_address', ''),
        'ton_api_key': db.get_setting('ton_api_key', '')
    }
    
    print(f"\n🔧 Payment Settings:")
    for key, value in settings.items():
        if key == 'ton_wallet_address' and value:
            print(f"   {key}: {value[:20]}...")
        elif key == 'ton_api_key' and value:
            print(f"   {key}: ***set***")
        else:
            print(f"   {key}: {value}")
    
    # Determine mode
    sim_mode = settings['simulation_mode'] == 'true'
    testnet_mode = settings['ton_testnet_mode'] == 'true'
    
    if sim_mode:
        mode = "🎮 SIMULATION MODE"
        description = "All payments auto-complete, no real transactions"
    elif testnet_mode:
        mode = "🧪 TESTNET MODE"
        description = "Real blockchain with test tokens"
    else:
        mode = "🌐 PRODUCTION MODE"
        description = "Real payments with real money!"
    
    print(f"\n📍 Current Mode: {mode}")
    print(f"   {description}")
    
    # Show what user will see
    if sim_mode:
        print(f"\n👤 User Experience:")
        print(f"   - Payments complete instantly")
        print(f"   - No wallet interaction needed")
        print(f"   - Perfect for testing bot functionality")
    elif testnet_mode:
        print(f"\n👤 User Experience:")
        print(f"   - Real payment flow with Tonkeeper")
        print(f"   - Uses free test TON tokens")
        print(f"   - Payment URLs include 'testnet=true'")
        print(f"   - Blockchain verification (5-10 min)")
    else:
        print(f"\n👤 User Experience:")
        print(f"   - Real payment flow with Tonkeeper")
        print(f"   - Uses real TON tokens (costs real money)")
        print(f"   - Production blockchain verification")
        print(f"   - Real financial transactions!")

def main():
    """Main menu for payment testing setup"""
    print("=" * 60)
    print("🚀 TON Payment Testing Setup Utility")
    print("=" * 60)
    
    while True:
        print(f"\n📋 Choose an option:")
        print(f"   1. 📊 Show current configuration")
        print(f"   2. 🎮 Setup Simulation Mode (safe testing)")
        print(f"   3. 🧪 Setup Testnet Mode (blockchain testing)")
        print(f"   4. 🌐 Setup Production Mode (real payments)")
        print(f"   5. ❌ Exit")
        
        choice = input(f"\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            show_current_status()
        elif choice == '2':
            setup_simulation_mode()
        elif choice == '3':
            setup_testnet_mode()
        elif choice == '4':
            setup_production_mode()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()