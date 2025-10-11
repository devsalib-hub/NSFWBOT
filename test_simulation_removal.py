#!/usr/bin/env python3
"""
Test script to verify simulation mode has been removed and only network mode (sandbox vs mainnet) remains
"""
import sys
sys.path.append('.')

from database import Database
from payment_handler import PaymentHandler

def test_simulation_removal():
    """Test that simulation mode has been properly removed"""
    print("🧪 Testing Simulation Mode Removal")
    print("=" * 50)
    
    db = Database()
    
    # Test 1: Check that PaymentHandler no longer has simulation_mode
    print("\n1️⃣ Testing PaymentHandler initialization...")
    payment_handler = PaymentHandler(db)
    
    has_simulation_mode = hasattr(payment_handler, 'simulation_mode')
    print(f"   - PaymentHandler has simulation_mode attribute: {has_simulation_mode}")
    
    if not has_simulation_mode:
        print("   ✅ SUCCESS: simulation_mode attribute removed from PaymentHandler")
    else:
        print("   ❌ FAIL: simulation_mode attribute still exists")
    
    # Test 2: Check network mode functionality
    print("\n2️⃣ Testing Network Mode functionality...")
    print(f"   - Current network mode: {payment_handler.ton_network_mode}")
    print(f"   - Is testnet/sandbox: {payment_handler.ton_testnet}")
    print(f"   - API endpoint: {payment_handler.ton_api_endpoint}")
    print(f"   - Wallet address: {payment_handler.get_ton_wallet_address()}")
    
    # Test 3: Test both network modes
    print("\n3️⃣ Testing network mode switching...")
    
    for mode in ['sandbox', 'mainnet']:
        print(f"\n   Testing {mode.upper()} mode:")
        db.update_setting('ton_network_mode', mode)
        
        # Create new handler to test updated settings
        test_handler = PaymentHandler(db)
        expected_testnet = mode == 'sandbox'
        
        print(f"   - Network mode: {test_handler.ton_network_mode}")
        print(f"   - Is testnet: {test_handler.ton_testnet} (expected: {expected_testnet})")
        print(f"   - API endpoint: {test_handler.ton_api_endpoint}")
        
        if test_handler.ton_testnet == expected_testnet:
            print(f"   ✅ {mode.upper()} mode working correctly")
        else:
            print(f"   ❌ {mode.upper()} mode not working correctly")
    
    # Test 4: Check database doesn't have simulation_mode in defaults
    print("\n4️⃣ Testing database defaults...")
    simulation_setting = db.get_setting('simulation_mode', 'NOT_FOUND')
    print(f"   - simulation_mode setting: {simulation_setting}")
    
    if simulation_setting == 'NOT_FOUND':
        print("   ✅ SUCCESS: simulation_mode not in database defaults")
    else:
        print("   ⚠️  WARNING: simulation_mode still exists in database")
    
    # Test 5: Test that only network mode boolean exists
    print("\n5️⃣ Testing final configuration...")
    network_mode = db.get_setting('ton_network_mode', 'sandbox')
    is_sandbox = network_mode == 'sandbox'
    
    print(f"   - Network mode setting: {network_mode}")
    print(f"   - Is sandbox (boolean): {is_sandbox}")
    print(f"   - Wallet for current mode: {payment_handler.get_ton_wallet_address()}")
    
    print("\n" + "=" * 50)
    print("✅ Simulation mode removal test completed!")
    print("💡 The system now uses only network mode (sandbox=true/false)")

if __name__ == "__main__":
    test_simulation_removal()