#!/usr/bin/env python3
"""
Test TON payment URL generation
"""
import sys
sys.path.append('.')

from database import Database
from payment_handler import PaymentHandler

async def test_payment_url():
    """Test payment URL generation with different amounts"""
    print("🧪 Testing TON Payment URL Generation")
    print("=" * 50)
    
    db = Database()
    payment_handler = PaymentHandler(db)
    
    test_amounts = [0.5, 1.0, 5.0, 10.0]
    
    for amount in test_amounts:
        print(f"\n🔄 Testing amount: {amount} TON")
        
        try:
            result = await payment_handler.create_ton_payment(
                user_id=12345,
                package_id=1,
                amount=amount
            )
            
            if result['success']:
                print(f"✅ Payment URL generated successfully")
                print(f"   - Amount in URL: {amount} TON")
                print(f"   - URL: {result['payment_url']}")
                print(f"   - Comment: {result['comment']}")
            else:
                print(f"❌ Failed to generate URL: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ URL generation test completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_payment_url())