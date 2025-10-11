#!/usr/bin/env python3
"""
Test the new payment handler with network mode selection
"""
import sys
import asyncio
sys.path.append('.')

from database import Database
from payment_handler import PaymentHandler

async def test_payment_handler():
    """Test the new payment handler"""
    print("🧪 Testing Payment Handler with Network Mode Selection")
    print("=" * 60)
    
    db = Database()
    payment_handler = PaymentHandler(db)
    
    # Show current configuration
    print(f"🔧 Current Configuration:")
    print(f"   - Network Mode: {payment_handler.ton_network_mode}")
    print(f"   - Using Testnet: {payment_handler.ton_testnet}")
    print(f"   - API Endpoint: {payment_handler.ton_api_endpoint}")
    print(f"   - Wallet Address: {payment_handler.get_ton_wallet_address()}")
    print()
    
    # Test both network modes
    for network_mode in ['sandbox', 'mainnet']:
        print(f"🔄 Testing {network_mode.upper()} mode...")
        
        # Update network mode
        db.update_setting('ton_network_mode', network_mode)
        
        # Create new payment handler instance with updated settings
        test_handler = PaymentHandler(db)
        
        print(f"   - Network Mode: {test_handler.ton_network_mode}")
        print(f"   - Using Testnet: {test_handler.ton_testnet}")
        print(f"   - API Endpoint: {test_handler.ton_api_endpoint}")
        print(f"   - Wallet Address: {test_handler.get_ton_wallet_address()}")
        
        # Test creating a payment (simulation mode for safety)
        try:
            result = await test_handler.create_ton_payment(user_id=12345, package_id=1, amount=1.0)
            print(f"   - Payment creation: {'✅ Success' if result['success'] else '❌ Failed'}")
            if result['success']:
                print(f"   - Payment URL: {result.get('payment_url', 'N/A')[:50]}...")
        except Exception as e:
            print(f"   - Payment creation: ❌ Error - {str(e)}")
        
        print()
    
    # Restore original setting
    db.update_setting('ton_network_mode', 'sandbox')
    print("✅ Test completed!")

if __name__ == "__main__":
    asyncio.run(test_payment_handler())