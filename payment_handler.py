import asyncio
import logging
from typing import Optional, Dict, Any
import json
import aiohttp
import time
from config import Config
from database import Database

class PaymentHandler:
    def __init__(self, db: Database):
        self.db = db
        self.ton_network_mode = self.db.get_setting('ton_network_mode', 'sandbox')
        self.ton_testnet = self.ton_network_mode == 'sandbox'
        
        # TON API endpoints
        self.ton_api_endpoint = "https://testnet.toncenter.com/api/v2/" if self.ton_testnet else "https://toncenter.com/api/v2/"
        self.ton_api_key = self.db.get_setting('ton_api_key', '')  # Optional API key for higher limits
        
    def get_ton_wallet_address(self) -> str:
        """Get appropriate TON wallet address based on network mode"""
        if self.ton_network_mode == 'sandbox':
            return self.db.get_setting('ton_testnet_wallet_address', '')
        else:
            return self.db.get_setting('ton_mainnet_wallet_address', '')
        
    async def create_stars_payment(self, user_id: int, package_id: int, amount: int) -> Dict[str, Any]:
        """Create Telegram Stars payment"""
        try:
            package = self.db.get_package(package_id)
            if not package:
                return {"success": False, "error": "Package not found"}
            
            # Real Telegram Stars payment
            transaction_id = self.db.create_transaction(
                user_id, package_id, "stars", amount
            )
            
            # Create payment invoice (this would integrate with Telegram's payment API)
            payment_data = {
                "provider_token": "",  # Empty for Telegram Stars
                "currency": "XTR",  # Telegram Stars currency code
                "prices": [{"label": package['name'], "amount": amount}],
                "title": f"Package: {package['name']}",
                "description": f"{package['description']}\n" +
                              f"📝 {package['text_count']} text messages\n" +
                              f"🖼️ {package['image_count']} image messages\n" +
                              f"🎥 {package['video_count']} video messages",
                "payload": json.dumps({
                    "transaction_id": transaction_id,
                    "package_id": package_id,
                    "user_id": user_id
                }),
                "need_email": False,
                "need_phone_number": False,
                "is_flexible": False
            }
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "payment_data": payment_data,
                "message": f"💫 Payment created for {amount} Telegram Stars"
            }
            
        except Exception as e:
            logging.error(f"Error creating Stars payment: {str(e)}")
            return {"success": False, "error": "Failed to create payment"}
    
    async def create_ton_payment(self, user_id: int, package_id: int, amount: float) -> Dict[str, Any]:
        """Create TON payment"""
        try:
            package = self.db.get_package(package_id)
            if not package:
                return {"success": False, "error": "Package not found"}
            
            # Create TON payment transaction
            transaction_id = self.db.create_transaction(
                user_id, package_id, "ton", amount
            )
            
            # Generate TON payment URL
            payment_comment = f"Payment_{transaction_id}_{user_id}"
            ton_wallet_address = self.get_ton_wallet_address()
            
            # Convert TON to nanoTON for the payment URL (1 TON = 1,000,000,000 nanoTON)
            ton_amount_nanotone = int(amount * 1000000000)
            
            # Create payment URL (TON network is detected automatically by address)
            payment_url = (
                f"https://app.tonkeeper.com/transfer/"
                f"{ton_wallet_address}?"
                f"amount={ton_amount_nanotone}&"
                f"text={payment_comment}"
            )
            
            # Network info for display
            network_info = "🧪 TESTNET" if self.ton_testnet else "🌐 MAINNET"
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "payment_url": payment_url,
                "ton_address": ton_wallet_address,
                "amount": amount,
                "comment": payment_comment,
                "network": network_info,
                "message": f"💎 TON payment created for {amount} TON ({network_info})"
            }
            
        except Exception as e:
            logging.error(f"Error creating TON payment: {str(e)}")
            return {"success": False, "error": "Failed to create payment"}
    
    async def verify_stars_payment(self, transaction_id: int, telegram_payment_id: str) -> bool:
        """Verify Telegram Stars payment"""
        try:
            # In a real implementation, you would verify with Telegram's API
            # For now, we'll mark as completed when called
            self.db.complete_transaction(transaction_id, telegram_payment_id)
            
            # Add credits to user
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, package_id FROM transactions WHERE id = ?
            ''', (transaction_id,))
            
            result = cursor.fetchone()
            if result:
                user_id, package_id = result
                package = self.db.get_package(package_id)
                if package:
                    self.db.add_message_credits(
                        user_id,
                        package['text_count'],
                        package['image_count'],
                        package['video_count']
                    )
            
            conn.close()
            return True
            
        except Exception as e:
            logging.error(f"Error verifying Stars payment: {str(e)}")
            return False
    
    async def verify_ton_payment(self, transaction_id: int) -> bool:
        """Verify TON payment by checking blockchain"""
        try:
            # Get transaction details
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, package_id, amount, created_date FROM transactions 
                WHERE id = ? AND status = 'pending'
            ''', (transaction_id,))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False
            
            user_id, package_id, expected_amount, created_date = result
            conn.close()
            
            # Verify payment using TON API
            payment_comment = f"Payment_{transaction_id}_{user_id}"
            ton_wallet_address = self.get_ton_wallet_address()
            
            if await self._check_ton_transaction(ton_wallet_address, expected_amount, payment_comment, created_date):
                # Payment verified, complete transaction
                self.db.complete_transaction(transaction_id, f"ton_verified_{int(time.time())}")
                
                # Add credits to user
                package = self.db.get_package(package_id)
                if package:
                    self.db.add_message_credits(
                        user_id,
                        package['text_count'],
                        package['image_count'],
                        package['video_count']
                    )
                
                logging.info(f"TON payment verified and completed for transaction {transaction_id}")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error verifying TON payment: {str(e)}")
            return False
    
    async def _check_ton_transaction(self, wallet_address: str, expected_amount: float, expected_comment: str, since_timestamp: str) -> bool:
        """Check TON blockchain for specific transaction"""
        try:
            # Convert timestamp to Unix time for API
            import datetime
            since_dt = datetime.datetime.fromisoformat(since_timestamp.replace('Z', '+00:00'))
            since_unix = int(since_dt.timestamp())
            
            # Build API request URL
            url = f"{self.ton_api_endpoint}getTransactions"
            params = {
                'address': wallet_address,
                'limit': 100,  # Check last 100 transactions
                'to_lt': 0,
                'archival': True
            }
            
            if self.ton_api_key:
                params['api_key'] = self.ton_api_key
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        logging.error(f"TON API error: {response.status}")
                        return False
                    
                    data = await response.json()
                    
                    if not data.get('ok'):
                        logging.error(f"TON API response not ok: {data}")
                        return False
                    
                    transactions = data.get('result', [])
                    
                    # Check each transaction
                    for tx in transactions:
                        # Skip if transaction is older than our payment
                        if tx.get('utime', 0) < since_unix:
                            continue
                        
                        # Check incoming messages
                        in_msg = tx.get('in_msg', {})
                        if not in_msg:
                            continue
                        
                        # Check amount (convert from nanoTON)
                        value = int(in_msg.get('value', 0))
                        amount_ton = value / 1000000000
                        
                        # Check if amount matches (with small tolerance for fees)
                        if abs(amount_ton - expected_amount) < 0.001:
                            # Check comment/message
                            message = in_msg.get('message', '')
                            if expected_comment in message:
                                logging.info(f"Found matching TON transaction: {amount_ton} TON with comment '{message}'")
                                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error checking TON transaction: {str(e)}")
            return False
            
        except Exception as e:
            logging.error(f"Error verifying TON payment: {str(e)}")
            return False
    
    async def check_pending_payments(self):
        """Background task to check pending payments"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Get pending TON transactions older than 5 minutes
            cursor.execute('''
                SELECT id, user_id, package_id, amount FROM transactions 
                WHERE status = 'pending' 
                AND payment_method = 'ton' 
                AND created_date < datetime('now', '-5 minutes')
            ''')
            
            pending_transactions = cursor.fetchall()
            conn.close()
            
            for transaction in pending_transactions:
                transaction_id, user_id, package_id, amount = transaction
                
                if await self.verify_ton_payment(transaction_id):
                    logging.info(f"TON payment verified for transaction {transaction_id}")
                else:
                    logging.info(f"TON payment still pending for transaction {transaction_id}")
            
        except Exception as e:
            logging.error(f"Error checking pending payments: {str(e)}")
    
    def get_payment_status(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """Get payment status"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT status, payment_method, amount, created_date, completed_date 
                FROM transactions WHERE id = ?
            ''', (transaction_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                status, payment_method, amount, created_date, completed_date = result
                return {
                    "status": status,
                    "payment_method": payment_method,
                    "amount": amount,
                    "created_date": created_date,
                    "completed_date": completed_date
                }
            
            return None
            
        except Exception as e:
            logging.error(f"Error getting payment status: {str(e)}")
            return None