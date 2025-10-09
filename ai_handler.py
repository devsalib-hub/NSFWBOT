import requests
import asyncio
import aiohttp
import http.client
import json
import ssl
from typing import Optional, Dict, Any

class OpenRouterAPI:
    def __init__(self, database=None):
        self.db = database
        # Get settings from database if available, otherwise use empty defaults
        if self.db:
            self.api_key = self.db.get_setting('ai_api_key', '')
            self.model = self.db.get_setting('ai_model', 'openai/gpt-3.5-turbo')
            self.base_url = self.db.get_setting('ai_base_url', 'https://openrouter.ai/api/v1')
        else:
            # No database available, use empty defaults
            self.api_key = ''
            self.model = 'openai/gpt-3.5-turbo'
            self.base_url = 'https://openrouter.ai/api/v1'
        
        # Set basic headers - additional headers added dynamically based on provider
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "TelegramBot/1.0"
        }
        
        # Add provider-specific headers
        self._add_provider_headers()
    
    def _add_provider_headers(self):
        """Add provider-specific headers based on base URL"""
        if 'openrouter.ai' in self.base_url:
            # OpenRouter-specific headers
            self.headers["HTTP-Referer"] = "https://telegram.org"
            self.headers["X-Title"] = "Telegram NSFW Bot"
        elif 'venice.ai' in self.base_url:
            # Venice AI - uses standard OpenAI format, no extra headers needed
            pass
        # Add other providers as needed
    
    def refresh_settings(self):
        """Refresh API settings from database"""
        if self.db:
            self.api_key = self.db.get_setting('ai_api_key', '')
            self.model = self.db.get_setting('ai_model', 'openai/gpt-3.5-turbo')
            self.base_url = self.db.get_setting('ai_base_url', 'https://openrouter.ai/api/v1')
            
            # Update headers with new API key and provider-specific headers
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "TelegramBot/1.0"
            }
            self._add_provider_headers()
    
    async def generate_text_response(self, user_message: str, user_context: str = None, conversation_history: list = None) -> str:
        """Generate AI text response using direct HTTP connection"""
        try:
            # Refresh settings from database
            self.refresh_settings()
            
            # Check if API key is available
            if not self.api_key:
                print("❌ AI API key not configured in database")
                return "Sorry, the AI service is not properly configured. Please contact the administrator."
            
            # Debug logging
            print(f"🔍 AI API Configuration:")
            print(f"   Base URL: {self.base_url}")
            print(f"   Model: {self.model}")
            print(f"   API Key: {'*' * (len(self.api_key) - 4) + self.api_key[-4:] if len(self.api_key) > 4 else '***'}")
            
            # Use direct HTTP connection approach like Venice AI example
            if 'venice.ai' in self.base_url:
                return await self._venice_direct_request(user_message, user_context, conversation_history)
            else:
                return await self._standard_openai_request(user_message, user_context, conversation_history)
        
        except Exception as e:
            print(f"Error in generate_text_response: {str(e)}")
            return "Sorry, I encountered an error while generating a response. Please try again."
    
    async def _venice_direct_request(self, user_message: str, user_context: str = None, conversation_history: list = None) -> str:
        """Direct HTTP request to Venice AI using requests library (works, unlike http.client)"""
        try:
            # HARDCODED Venice AI credentials - USE REQUESTS LIBRARY
            test_api_key = "af9uD9UxvcrqR3kACGqyILz4gHQ7oN839m10wKy5pm"
            test_model = "llama-3.2-3b"
            
            # Build system prompt
            system_prompt = """You are a helpful AI assistant in a Telegram bot. 
            Respond naturally and helpfully to user messages. Keep responses concise but informative.
            You can handle various topics but maintain appropriate boundaries.
            Use the conversation history to provide contextual and coherent responses."""
            
            if user_context:
                system_prompt += f"\n\nUser context: {user_context}"
            
            # Build messages array with conversation history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for entry in conversation_history:
                    user_msg = entry['user_message'] if entry['user_message'] else None
                    bot_resp = entry['bot_response'] if entry['bot_response'] else None
                    
                    if user_msg:
                        messages.append({"role": "user", "content": user_msg})
                    if bot_resp:
                        messages.append({"role": "assistant", "content": bot_resp})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Prepare request data using working format
            data = {
                "frequency_penalty": 0,
                "max_tokens": 4096,
                "messages": messages,
                "model": test_model,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.95
            }
            
            headers = {
                'Authorization': f'Bearer {test_api_key}',
                'Content-Type': 'application/json'
            }
            
            print(f"🔍 Venice Direct Request (USING REQUESTS):")
            print(f"   Model: {test_model}")
            print(f"   API Key: {test_api_key[:8]}...{test_api_key[-4:]}")
            
            # Use requests library (works unlike http.client)
            response = requests.post(
                "https://api.venice.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            print(f"📡 Venice Response Status: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                print(f"❌ Venice API error: {response.status_code} - {response.text}")
                return "Sorry, I'm having trouble connecting to the AI service right now. Please try again later."
                
        except Exception as e:
            print(f"Error in Venice direct request: {str(e)}")
            return "Sorry, I encountered an error while generating a response. Please try again."
    
    async def _standard_openai_request(self, user_message: str, user_context: str = None, conversation_history: list = None) -> str:
        """Standard OpenAI-compatible request for other providers"""
        try:
            system_prompt = """You are a helpful AI assistant in a Telegram bot. 
            Respond naturally and helpfully to user messages. Keep responses concise but informative.
            You can handle various topics but maintain appropriate boundaries.
            Use the conversation history to provide contextual and coherent responses."""
            
            if user_context:
                system_prompt += f"\n\nUser context: {user_context}"
            
            # Build messages array with conversation history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for entry in conversation_history:
                    user_msg = entry['user_message'] if entry['user_message'] else None
                    bot_resp = entry['bot_response'] if entry['bot_response'] else None
                    
                    if user_msg:
                        messages.append({"role": "user", "content": user_msg})
                    if bot_resp:
                        messages.append({"role": "assistant", "content": bot_resp})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            print(f"🔍 Standard API Request:")
            print(f"   URL: {self.base_url}/chat/completions")
            print(f"   Headers: {list(self.headers.keys())}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=data,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"].strip()
                    else:
                        error_text = await response.text()
                        print(f"❌ API error: {response.status} - {error_text}")
                        return "Sorry, I'm having trouble generating a response right now. Please try again later."
        
        except Exception as e:
            print(f"Error in standard request: {str(e)}")
            return "Sorry, I encountered an error while generating a response. Please try again."
    
    async def generate_image_response(self, user_message: str, image_data: bytes = None, conversation_history: list = None) -> str:
        """Generate AI response to an image using OpenRouter API with vision model"""
        try:
            # Refresh settings from database
            self.refresh_settings()
            
            # Check if API key is available
            if not self.api_key:
                print("❌ OpenRouter API key not configured in database")
                return "Sorry, the AI service is not properly configured. Please contact the administrator."
            # For image analysis, we'll use a vision-capable model
            vision_model = "openai/gpt-4-vision-preview"
            
            messages = [
                {
                    "role": "system", 
                    "content": "You are an AI assistant that can analyze images. Describe what you see in the image and respond helpfully to any questions about it. Use conversation history to provide contextual responses."
                }
            ]
            
            # Add conversation history (text only, as vision models typically don't support image history)
            if conversation_history:
                context_summary = "Recent conversation context: "
                for entry in conversation_history[-3:]:  # Last 3 exchanges for context
                    user_msg = entry['user_message'] if entry['user_message'] else ""
                    bot_resp = entry['bot_response'] if entry['bot_response'] else ""
                    if user_msg and bot_resp:
                        context_summary += f"User: {user_msg[:100]}... Bot: {bot_resp[:100]}... "
                messages[0]["content"] += f"\n\n{context_summary}"
            
            if image_data:
                # Convert image to base64 for API
                import base64
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_message if user_message else "What do you see in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": f"User sent an image with message: {user_message}. Please respond appropriately."
                })
            
            data = {
                "model": vision_model,
                "messages": messages,
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=data,
                    timeout=45
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"].strip()
                    else:
                        error_text = await response.text()
                        print(f"OpenRouter Vision API error: {response.status} - {error_text}")
                        return "I can see you sent an image! However, I'm having trouble analyzing it right now. Please try again later."
        
        except Exception as e:
            print(f"Error in generate_image_response: {str(e)}")
            return "Thanks for sharing the image! I'm having some technical difficulties analyzing it at the moment."
    
    async def generate_video_response(self, user_message: str, conversation_history: list = None) -> str:
        """Generate AI response for video content with conversation context"""
        try:
            # Refresh settings from database
            self.refresh_settings()
            
            # Check if API key is available
            if not self.api_key:
                print("❌ OpenRouter API key not configured in database")
                return "Sorry, the AI service is not properly configured. Please contact the administrator."
            
            system_prompt = """You are responding to a user who sent a video. 
            Since you cannot directly analyze video content, acknowledge the video 
            and respond based on any accompanying text message and conversation history."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history for context
            if conversation_history:
                for entry in conversation_history[-5:]:  # Last 5 exchanges for context
                    user_msg = entry['user_message'] if entry['user_message'] else None
                    bot_resp = entry['bot_response'] if entry['bot_response'] else None
                    
                    if user_msg:
                        messages.append({"role": "user", "content": user_msg})
                    if bot_resp:
                        messages.append({"role": "assistant", "content": bot_resp})
            
            # Add current video message
            messages.append({"role": "user", "content": f"User sent a video with message: '{user_message}'. Please respond appropriately."})
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=data,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"].strip()
                    else:
                        return "Thanks for sharing the video! I received it but I'm having some technical difficulties right now."
        
        except Exception as e:
            print(f"Error in generate_video_response: {str(e)}")
            return "Thanks for the video! I'm having some technical issues at the moment, but I appreciate you sharing it."
    
    async def test_api_connection(self) -> bool:
        """Test if the AI API is working"""
        try:
            # Refresh settings
            self.refresh_settings()
            
            if not self.api_key:
                print("❌ No API key configured")
                return False
            
            # Test Venice AI specifically
            if 'venice.ai' in self.base_url:
                print("🔍 Testing Venice AI with requests library (the one that works)...")  
                result = self._test_venice_api_requests()
                print(f"📊 Venice AI Test Result: {result}")
                return result
            else:
                return await self._test_standard_api()
                
        except Exception as e:
            print(f"API test failed: {str(e)}")
            return False
    
    async def _test_venice_api(self) -> bool:
        """Test Venice AI using exact format that works in curl"""
        try:
            # HARDCODED Venice AI credentials - MATCH WORKING CURL
            test_api_key = "af9uD9UxvcrqR3kACGqyILz4gHQ7oN839m10wKy5pm"
            test_model = "llama-3.2-3b"  # Same model as working curl
            
            headers = {
                'Authorization': f'Bearer {test_api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'python-httpx/0.24.1',  # Add User-Agent like curl
                'Accept': '*/*'  # Add Accept header
            }
            
            # Test data matching your EXACT working curl
            test_data = {
                "frequency_penalty": 0,
                "max_tokens": 4096,
                "messages": [
                    {
                        "content": "Say 'Venice AI test successful!' to confirm the connection works",
                        "role": "user"
                    }
                ],
                "model": test_model,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.95
            }
            
            print(f"🧪 Testing Venice AI API (DEBUGGING 403):")
            print(f"   URL: https://api.venice.ai/api/v1/chat/completions")
            print(f"   Model: {test_model}")
            print(f"   API Key: {test_api_key[:8]}...{test_api_key[-4:]}")
            print(f"   Headers: {headers}")
            
            # Use direct HTTP connection like Venice example
            conn = http.client.HTTPSConnection("api.venice.ai")
            
            # Convert data to JSON string
            json_data = json.dumps(test_data)
            print(f"   JSON Data: {json_data}")
            
            conn.request("POST", "/api/v1/chat/completions", json_data, headers)
            res = conn.getresponse()
            data = res.read()
            
            print(f"📡 Venice API Response Status: {res.status}")
            print(f"📡 Venice API Response Headers: {dict(res.getheaders())}")
            print(f"📡 Venice API Response Body: {data.decode('utf-8')}")
            
            if res.status == 200:
                response_data = json.loads(data.decode('utf-8'))
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    message = response_data['choices'][0].get('message', {}).get('content', '')
                    print(f"✅ Venice AI Test Success! Response: {message[:100]}...")
                    return True
                else:
                    print(f"❌ Venice API Test Failed: Invalid response format")
                    return False
            else:
                print(f"❌ Venice API Test Failed: {res.status}")
                return False
                
        except Exception as e:
            print(f"Venice API test error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _test_venice_api_requests(self) -> bool:
        """Test Venice AI using requests library (sync version)"""
        try:
            # HARDCODED Venice AI credentials - EXACT MATCH TO WORKING CURL
            test_api_key = "af9uD9UxvcrqR3kACGqyILz4gHQ7oN839m10wKy5pm"
            test_model = "llama-3.2-3b"
            
            headers = {
                'Authorization': f'Bearer {test_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Test data matching your EXACT working curl
            test_data = {
                "frequency_penalty": 0,
                "max_tokens": 4096,
                "messages": [
                    {
                        "content": "Say 'Venice AI test successful!' to confirm the connection works",
                        "role": "user"
                    }
                ],
                "model": test_model,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.95
            }
            
            print(f"🧪 Testing Venice AI API (USING REQUESTS LIBRARY):")
            print(f"   URL: https://api.venice.ai/api/v1/chat/completions")
            print(f"   Model: {test_model}")
            print(f"   API Key: {test_api_key[:8]}...{test_api_key[-4:]}")
            
            # Use requests library like your PowerShell curl
            response = requests.post(
                "https://api.venice.ai/api/v1/chat/completions",
                headers=headers,
                json=test_data,
                timeout=30
            )
            
            print(f"📡 Venice API Response Status: {response.status_code}")
            print(f"📡 Venice API Response Headers: {dict(response.headers)}")
            print(f"📡 Venice API Response Body: {response.text}")
            
            if response.status_code == 200:
                response_data = response.json()
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    message = response_data['choices'][0].get('message', {}).get('content', '')
                    print(f"✅ Venice AI Test Success! Response: {message[:100]}...")
                    return True
                else:
                    print(f"❌ Venice API Test Failed: Invalid response format")
                    return False
            else:
                print(f"❌ Venice API Test Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Venice API test error (requests): {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _test_standard_api(self) -> bool:
        """Test standard OpenAI-compatible API"""
        try:
            test_data = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 50
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=test_data,
                    timeout=10
                ) as response:
                    print(f"📡 Standard API Test Status: {response.status}")
                    if response.status == 200:
                        print("✅ Standard API Test Success!")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ Standard API Test Failed: {response.status} - {error_text}")
                        return False
        
        except Exception as e:
            print(f"Standard API test error: {str(e)}")
            return False