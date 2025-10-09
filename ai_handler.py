import requests
import asyncio
import aiohttp
import json
from typing import Optional, Dict, Any
from config import Config

class OpenRouterAPI:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.model = Config.OPENROUTER_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://telegram.org",
            "X-Title": "Telegram NSFW Bot"
        }
    
    async def generate_text_response(self, user_message: str, user_context: str = None) -> str:
        """Generate AI text response using OpenRouter API"""
        try:
            system_prompt = """You are a helpful AI assistant in a Telegram bot. 
            Respond naturally and helpfully to user messages. Keep responses concise but informative.
            You can handle various topics but maintain appropriate boundaries."""
            
            if user_context:
                system_prompt += f"\n\nUser context: {user_context}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 500,
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
                        error_text = await response.text()
                        print(f"OpenRouter API error: {response.status} - {error_text}")
                        return "Sorry, I'm having trouble generating a response right now. Please try again later."
        
        except asyncio.TimeoutError:
            return "Sorry, the response took too long to generate. Please try again."
        except Exception as e:
            print(f"Error in generate_text_response: {str(e)}")
            return "Sorry, I encountered an error while generating a response. Please try again."
    
    async def generate_image_response(self, user_message: str, image_data: bytes = None) -> str:
        """Generate AI response to an image using OpenRouter API with vision model"""
        try:
            # For image analysis, we'll use a vision-capable model
            vision_model = "openai/gpt-4-vision-preview"
            
            messages = [
                {
                    "role": "system", 
                    "content": "You are an AI assistant that can analyze images. Describe what you see in the image and respond helpfully to any questions about it."
                }
            ]
            
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
    
    async def generate_video_response(self, user_message: str) -> str:
        """Generate AI response for video content"""
        try:
            system_prompt = """You are responding to a user who sent a video. 
            Since you cannot directly analyze video content, acknowledge the video 
            and respond based on any accompanying text message."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User sent a video with message: '{user_message}'. Please respond appropriately."}
            ]
            
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
        """Test if the OpenRouter API is working"""
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
                    return response.status == 200
        
        except Exception as e:
            print(f"API test failed: {str(e)}")
            return False