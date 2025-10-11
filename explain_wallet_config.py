#!/usr/bin/env python3
"""
Check and explain current wallet configuration
"""

from database import Database

def explain_wallet_config():
    """Explain the current wallet configuration"""
    print("🔍 TON Wallet Configuration Explanation")
    print("=" * 50)
    
    db = Database()
    
    # Get current settings
    wallet_address = db.get_setting('ton_wallet_address', '')
    testnet_mode = db.get_setting('ton_testnet_mode', 'true') == 'true'
    simulation_mode = db.get_setting('simulation_mode', 'false') == 'true'
    
    print(f"\n📍 Current Configuration:")
    print(f"   Wallet Address: {wallet_address}")
    print(f"   Testnet Mode: {testnet_mode}")
    print(f"   Simulation Mode: {simulation_mode}")
    
    if not wallet_address:
        print(f"\n❌ No wallet address configured!")
        print(f"   You need to set your wallet address in admin dashboard")
        return
    
    print(f"\n🔍 What This Means:")
    
    if simulation_mode:
        print(f"   🎮 SIMULATION MODE - No real transactions")
        print(f"   - Payments auto-complete instantly")
        print(f"   - No blockchain interaction")
        print(f"   - Perfect for testing bot functionality")
    elif testnet_mode:
        print(f"   🧪 TESTNET MODE - Real blockchain, test tokens")
        print(f"   - Transactions go to: {wallet_address} on TESTNET")
        print(f"   - You receive: TEST TON (no real value)")
        print(f"   - Blockchain: TON Testnet")
        print(f"   - API: https://testnet.toncenter.com/api/v2/")
    else:
        print(f"   🌐 MAINNET MODE - Real blockchain, real money!")
        print(f"   - Transactions go to: {wallet_address} on MAINNET")
        print(f"   - You receive: REAL TON (real value)")
        print(f"   - Blockchain: TON Mainnet")
        print(f"   - API: https://toncenter.com/api/v2/")
    
    print(f"\n💡 Key Points:")
    print(f"   ✅ Same wallet address works for both testnet and mainnet")
    print(f"   ✅ Network is determined by 'TON Testnet Mode' setting")
    print(f"   ✅ Your private key/seed phrase stays the same")
    print(f"   ✅ Only the blockchain network changes")
    
    print(f"\n🎯 For Testing:")
    print(f"   1. Use your REAL wallet address in bot settings")
    print(f"   2. Enable 'TON Testnet Mode' for safe testing")
    print(f"   3. Get test TON from faucet for that same address")
    print(f"   4. Test payments will go to testnet version of your address")
    
    print(f"\n🚀 For Production:")
    print(f"   1. Keep the SAME wallet address")
    print(f"   2. Disable 'TON Testnet Mode'")
    print(f"   3. Real payments will go to mainnet version of your address")

if __name__ == "__main__":
    explain_wallet_config()