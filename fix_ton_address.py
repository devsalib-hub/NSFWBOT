#!/usr/bin/env python3
"""
Convert TON address formats and update bot configuration
"""

from database import Database

def convert_ton_address():
    """Convert and set the correct TON address format"""
    print("🔄 TON Address Format Converter")
    print("=" * 40)
    
    # Your current address
    raw_address = "UQARoaV0BXX9sjot32RxbziHoFYN1kJptSznDsRDimYVqkQX"
    user_friendly_address = "EQARoaV0BXX9sjot32RxbziHoFYN1kJptSznDsRDimYVqkQX"
    
    print(f"\n📍 Address Conversion:")
    print(f"   Raw Format (UQ):        {raw_address}")
    print(f"   User-Friendly (EQ):     {user_friendly_address}")
    
    print(f"\n🔧 Setting correct address in bot...")
    
    # Update database with correct format
    db = Database()
    db.update_setting('ton_wallet_address', user_friendly_address)
    
    print(f"✅ Address updated successfully!")
    
    # Show current configuration
    print(f"\n📊 Current Bot Configuration:")
    settings = {
        'ton_wallet_address': db.get_setting('ton_wallet_address'),
        'ton_testnet_mode': db.get_setting('ton_testnet_mode', 'true'),
        'simulation_mode': db.get_setting('simulation_mode', 'false')
    }
    
    for key, value in settings.items():
        print(f"   {key}: {value}")
    
    # Determine mode
    testnet_mode = settings['ton_testnet_mode'] == 'true'
    simulation_mode = settings['simulation_mode'] == 'true'
    
    if simulation_mode:
        mode = "🎮 SIMULATION"
        network = "No blockchain"
    elif testnet_mode:
        mode = "🧪 TESTNET"
        network = "TON Testnet blockchain"
    else:
        mode = "🌐 MAINNET"
        network = "TON Mainnet blockchain"
    
    print(f"\n📍 Current Mode: {mode}")
    print(f"   Network: {network}")
    print(f"   Address: {user_friendly_address}")
    
    print(f"\n💡 What This Means:")
    if testnet_mode and not simulation_mode:
        print(f"   ✅ Ready for testnet testing!")
        print(f"   ✅ Payments will go to your address on TESTNET")
        print(f"   ✅ You'll receive test TON (no real value)")
        print(f"   ✅ Same address works for both testnet and mainnet")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Get test TON from faucet: https://testnet.tonscan.org/faucet")
    print(f"   2. Use address: {user_friendly_address}")
    print(f"   3. Test bot payment flow")
    print(f"   4. Check admin dashboard: http://localhost:5000/settings")

if __name__ == "__main__":
    convert_ton_address()