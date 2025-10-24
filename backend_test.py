#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Tribe AI Platform
Tests all API endpoints for production deployment readiness
"""

import requests
import json
import base64
import time
from typing import Dict, Any, Optional
import uuid

# Configuration
BASE_URL = "https://tribe-multiverse.preview.emergentagent.com/api"
TEST_USER_EMAIL = "test.user@tribeai.com"
TEST_USER_PASSWORD = "SecurePassword123!"
TEST_USER_NAME = "Test User"

class TribeAITester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None
        self.session_id = str(uuid.uuid4())
        self.test_results = {}
        
    def log_result(self, test_name: str, success: bool, message: str, response_data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results[test_name] = {
            "success": success,
            "message": message,
            "response_data": response_data
        }
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, files: Dict = None, headers: Dict = None) -> requests.Response:
        """Make HTTP request with proper headers"""
        url = f"{BASE_URL}{endpoint}"
        request_headers = {"Content-Type": "application/json"}
        
        if headers:
            request_headers.update(headers)
            
        if self.auth_token:
            request_headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=request_headers)
            elif method.upper() == "POST":
                if files:
                    # Remove Content-Type for file uploads
                    request_headers.pop("Content-Type", None)
                    response = self.session.post(url, data=data, files=files, headers=request_headers)
                else:
                    response = self.session.post(url, json=data, headers=request_headers)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=request_headers)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=request_headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
        except Exception as e:
            print(f"Request failed: {e}")
            raise

    # ============= Authentication Tests =============
    
    def test_auth_register(self):
        """Test user registration"""
        try:
            data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD,
                "name": TEST_USER_NAME
            }
            
            response = self.make_request("POST", "/auth/register", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("user"):
                    self.user_id = result["user"]["id"]
                    # Extract token from cookies if available
                    if "session_token" in response.cookies:
                        self.auth_token = response.cookies["session_token"]
                    self.log_result("Auth Register", True, f"User registered successfully: {result['user']['email']}")
                    return True
                else:
                    self.log_result("Auth Register", False, f"Registration failed: {result}")
                    return False
            elif response.status_code == 400:
                # User might already exist, try login instead
                self.log_result("Auth Register", True, "User already exists (expected for repeated tests)")
                return self.test_auth_login()
            else:
                self.log_result("Auth Register", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Auth Register", False, f"Exception: {str(e)}")
            return False
    
    def test_auth_login(self):
        """Test user login"""
        try:
            data = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            }
            
            response = self.make_request("POST", "/auth/login", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("user"):
                    self.user_id = result["user"]["id"]
                    # Extract token from cookies if available
                    if "session_token" in response.cookies:
                        self.auth_token = response.cookies["session_token"]
                    self.log_result("Auth Login", True, f"Login successful: {result['user']['email']}")
                    return True
                else:
                    self.log_result("Auth Login", False, f"Login failed: {result}")
                    return False
            else:
                self.log_result("Auth Login", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Auth Login", False, f"Exception: {str(e)}")
            return False
    
    def test_auth_session(self):
        """Test getting current session"""
        try:
            response = self.make_request("GET", "/auth/session")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("authenticated"):
                    self.log_result("Auth Session", True, f"Session valid for user: {result['user']['email']}")
                    return True
                else:
                    self.log_result("Auth Session", False, "Not authenticated")
                    return False
            else:
                self.log_result("Auth Session", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Auth Session", False, f"Exception: {str(e)}")
            return False

    # ============= Alpha Chat Tests =============
    
    def test_chat_gpt5(self):
        """Test chat with GPT-5"""
        try:
            data = {
                "message": "Hello! Can you tell me about artificial intelligence?",
                "model": "gpt-5",
                "session_id": self.session_id
            }
            
            response = self.make_request("POST", "/chat", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("response"):
                    self.log_result("Chat GPT-5", True, f"Chat response received (length: {len(result['response'])})")
                    return True
                else:
                    self.log_result("Chat GPT-5", False, f"No response: {result}")
                    return False
            else:
                self.log_result("Chat GPT-5", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Chat GPT-5", False, f"Exception: {str(e)}")
            return False
    
    def test_chat_claude(self):
        """Test chat with Claude"""
        try:
            data = {
                "message": "What are the benefits of renewable energy?",
                "model": "claude-4-sonnet-20250514",
                "session_id": self.session_id
            }
            
            response = self.make_request("POST", "/chat", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("response"):
                    self.log_result("Chat Claude", True, f"Claude response received (length: {len(result['response'])})")
                    return True
                else:
                    self.log_result("Chat Claude", False, f"No response: {result}")
                    return False
            else:
                self.log_result("Chat Claude", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Chat Claude", False, f"Exception: {str(e)}")
            return False
    
    def test_chat_gemini(self):
        """Test chat with Gemini"""
        try:
            data = {
                "message": "Explain quantum computing in simple terms.",
                "model": "gemini-2.5-pro",
                "session_id": self.session_id
            }
            
            response = self.make_request("POST", "/chat", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("response"):
                    self.log_result("Chat Gemini", True, f"Gemini response received (length: {len(result['response'])})")
                    return True
                else:
                    self.log_result("Chat Gemini", False, f"No response: {result}")
                    return False
            else:
                self.log_result("Chat Gemini", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Chat Gemini", False, f"Exception: {str(e)}")
            return False

    # ============= Image Generation Tests =============
    
    def test_image_generation(self):
        """Test image generation"""
        try:
            data = {
                "prompt": "A beautiful sunset over mountains with vibrant colors",
                "number_of_images": 1
            }
            
            response = self.make_request("POST", "/image/generate", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("images"):
                    # Verify base64 image
                    image_data = result["images"][0]
                    if image_data and len(image_data) > 100:  # Basic validation
                        self.log_result("Image Generation", True, f"Image generated successfully (size: {len(image_data)} chars)")
                        return True
                    else:
                        self.log_result("Image Generation", False, "Invalid image data received")
                        return False
                else:
                    self.log_result("Image Generation", False, f"No image generated: {result}")
                    return False
            else:
                self.log_result("Image Generation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Image Generation", False, f"Exception: {str(e)}")
            return False

    # ============= Code Assistant Tests =============
    
    def test_code_assistant_python(self):
        """Test code assistant with Python"""
        try:
            data = {
                "prompt": "Write a Python function to calculate fibonacci numbers",
                "language": "python"
            }
            
            response = self.make_request("POST", "/code/assist", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("response"):
                    self.log_result("Code Assistant Python", True, f"Code assistance provided (length: {len(result['response'])})")
                    return True
                else:
                    self.log_result("Code Assistant Python", False, f"No response: {result}")
                    return False
            else:
                self.log_result("Code Assistant Python", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Code Assistant Python", False, f"Exception: {str(e)}")
            return False
    
    def test_code_assistant_javascript(self):
        """Test code assistant with JavaScript"""
        try:
            data = {
                "prompt": "Create a JavaScript function to validate email addresses",
                "language": "javascript"
            }
            
            response = self.make_request("POST", "/code/assist", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("response"):
                    self.log_result("Code Assistant JavaScript", True, f"JavaScript code assistance provided")
                    return True
                else:
                    self.log_result("Code Assistant JavaScript", False, f"No response: {result}")
                    return False
            else:
                self.log_result("Code Assistant JavaScript", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Code Assistant JavaScript", False, f"Exception: {str(e)}")
            return False

    # ============= Law Library Tests =============
    
    def test_law_search(self):
        """Test legal information search"""
        try:
            data = {
                "query": "tenant rights and landlord responsibilities",
                "category": "Landlord-Tenant"
            }
            
            response = self.make_request("POST", "/law/search", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("information") and result.get("resources"):
                    self.log_result("Law Search", True, f"Legal information provided with {len(result['resources'])} resources")
                    return True
                else:
                    self.log_result("Law Search", False, f"Incomplete response: {result}")
                    return False
            else:
                self.log_result("Law Search", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Law Search", False, f"Exception: {str(e)}")
            return False
    
    def test_law_assist(self):
        """Test AI-guided form filling"""
        try:
            data = {
                "form_type": "rental_agreement",
                "conversation": [
                    {"role": "user", "content": "I need help filling out a rental agreement"}
                ],
                "current_data": {}
            }
            
            response = self.make_request("POST", "/law/assist", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("message"):
                    self.log_result("Law Assist", True, f"AI assistance provided: {result['message'][:100]}...")
                    return True
                else:
                    self.log_result("Law Assist", False, f"No assistance message: {result}")
                    return False
            else:
                self.log_result("Law Assist", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Law Assist", False, f"Exception: {str(e)}")
            return False
    
    def test_law_download(self):
        """Test PDF form download"""
        try:
            data = {
                "form_type": "rental_agreement",
                "form_data": {
                    "tenant_name": "John Doe",
                    "landlord_name": "Jane Smith",
                    "property_address": "123 Main St, City, State",
                    "rent_amount": "$1200",
                    "lease_term": "12 months"
                },
                "jurisdiction": "California"
            }
            
            response = self.make_request("POST", "/law/download", data)
            
            if response.status_code == 200:
                # Check if it's a PDF response
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    self.log_result("Law Download", True, f"PDF generated successfully (size: {len(response.content)} bytes)")
                    return True
                else:
                    self.log_result("Law Download", False, f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_result("Law Download", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Law Download", False, f"Exception: {str(e)}")
            return False

    # ============= Tribe Office Tests =============
    
    def test_office_word_create(self):
        """Test Word document creation"""
        try:
            data = {
                "title": "Test Document",
                "heading": "Introduction",
                "paragraphs": [
                    "This is the first paragraph of our test document.",
                    "This is the second paragraph with more content.",
                    "Finally, this is the third paragraph to complete our test."
                ]
            }
            
            response = self.make_request("POST", "/office/word/create", data)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'officedocument.wordprocessingml.document' in content_type:
                    self.log_result("Office Word Create", True, f"Word document created (size: {len(response.content)} bytes)")
                    return True
                else:
                    self.log_result("Office Word Create", False, f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_result("Office Word Create", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Office Word Create", False, f"Exception: {str(e)}")
            return False
    
    def test_office_excel_create(self):
        """Test Excel spreadsheet creation"""
        try:
            data = {
                "filename": "test_spreadsheet",
                "sheet_name": "Sales Data",
                "headers": ["Product", "Quantity", "Price", "Total"],
                "data": [
                    ["Widget A", 10, 25.50, 255.00],
                    ["Widget B", 5, 45.00, 225.00],
                    ["Widget C", 8, 30.75, 246.00]
                ]
            }
            
            response = self.make_request("POST", "/office/excel/create", data)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'spreadsheetml.sheet' in content_type:
                    self.log_result("Office Excel Create", True, f"Excel spreadsheet created (size: {len(response.content)} bytes)")
                    return True
                else:
                    self.log_result("Office Excel Create", False, f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_result("Office Excel Create", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Office Excel Create", False, f"Exception: {str(e)}")
            return False
    
    def test_office_powerpoint_create(self):
        """Test PowerPoint presentation creation"""
        try:
            data = {
                "title": "Test Presentation",
                "slides": [
                    {
                        "type": "title",
                        "title": "Welcome to Our Presentation",
                        "content": ["Subtitle: Testing PowerPoint Generation"]
                    },
                    {
                        "type": "bullet",
                        "title": "Key Points",
                        "content": [
                            "First important point",
                            "Second key insight",
                            "Third valuable information"
                        ]
                    },
                    {
                        "type": "bullet",
                        "title": "Conclusion",
                        "content": [
                            "Summary of findings",
                            "Next steps",
                            "Thank you for your attention"
                        ]
                    }
                ]
            }
            
            response = self.make_request("POST", "/office/powerpoint/create", data)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'presentationml.presentation' in content_type:
                    self.log_result("Office PowerPoint Create", True, f"PowerPoint created (size: {len(response.content)} bytes)")
                    return True
                else:
                    self.log_result("Office PowerPoint Create", False, f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_result("Office PowerPoint Create", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Office PowerPoint Create", False, f"Exception: {str(e)}")
            return False
    
    def test_office_integrations_status(self):
        """Test office integrations status"""
        try:
            response = self.make_request("GET", "/office/integrations/status")
            
            if response.status_code == 200:
                result = response.json()
                if "microsoft" in result and "google" in result:
                    self.log_result("Office Integrations Status", True, "Integration status retrieved successfully")
                    return True
                else:
                    self.log_result("Office Integrations Status", False, f"Incomplete status: {result}")
                    return False
            else:
                self.log_result("Office Integrations Status", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Office Integrations Status", False, f"Exception: {str(e)}")
            return False

    # ============= Tribe Studio Tests =============
    
    def test_studio_generate_video(self):
        """Test AI video generation"""
        try:
            # Using form data as the endpoint expects
            data = {
                "prompt": "A cat playing with a ball of yarn in a sunny room",
                "style": "realistic",
                "service": "modelscope"
            }
            
            # Send as form data, not JSON
            url = f"{BASE_URL}/studio/generate-video"
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            
            response = self.session.post(url, data=data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") and result.get("service"):
                    self.log_result("Studio Video Generation", True, f"Video generation info received: {result['message']}")
                    return True
                else:
                    self.log_result("Studio Video Generation", False, f"Incomplete response: {result}")
                    return False
            else:
                self.log_result("Studio Video Generation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Studio Video Generation", False, f"Exception: {str(e)}")
            return False

    # ============= Translation Tests =============
    
    def test_translation_spanish(self):
        """Test translation feature - English to Spanish"""
        try:
            data = {
                "message": "Hello, how are you today? I hope you are having a wonderful day.",
                "model": "gpt-5",
                "session_id": self.session_id,
                "language": "es"  # Spanish
            }
            
            response = self.make_request("POST", "/chat", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("response"):
                    # Check if response is in Spanish (basic validation)
                    spanish_response = result["response"]
                    if result.get("language") == "es" and len(spanish_response) > 0:
                        self.log_result("Translation Spanish", True, f"Spanish translation received: {spanish_response[:100]}...")
                        return True
                    else:
                        self.log_result("Translation Spanish", False, f"Translation failed or incorrect language: {result}")
                        return False
                else:
                    self.log_result("Translation Spanish", False, f"No response: {result}")
                    return False
            else:
                self.log_result("Translation Spanish", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Translation Spanish", False, f"Exception: {str(e)}")
            return False
    
    def test_translation_french(self):
        """Test translation feature - English to French"""
        try:
            data = {
                "message": "Good morning! Can you help me with my project?",
                "model": "gpt-5",
                "session_id": self.session_id,
                "language": "fr"  # French
            }
            
            response = self.make_request("POST", "/chat", data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("response"):
                    # Check if response is in French (basic validation)
                    french_response = result["response"]
                    if result.get("language") == "fr" and len(french_response) > 0:
                        self.log_result("Translation French", True, f"French translation received: {french_response[:100]}...")
                        return True
                    else:
                        self.log_result("Translation French", False, f"Translation failed or incorrect language: {result}")
                        return False
                else:
                    self.log_result("Translation French", False, f"No response: {result}")
                    return False
            else:
                self.log_result("Translation French", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Translation French", False, f"Exception: {str(e)}")
            return False

    # ============= Export Chat History Tests =============
    
    def test_export_chat_history_pdf(self):
        """Test export chat history as PDF"""
        try:
            # First, ensure we have a conversation in the session
            chat_data = {
                "message": "This is a test message for export functionality.",
                "model": "gpt-5",
                "session_id": self.session_id
            }
            
            # Send a message to create conversation history
            chat_response = self.make_request("POST", "/chat", chat_data)
            if chat_response.status_code != 200:
                self.log_result("Export Chat History PDF", False, "Failed to create conversation for export test")
                return False
            
            # Now test the export
            export_data = {
                "format": "pdf",
                "session_id": self.session_id
            }
            
            response = self.make_request("POST", "/chat/export", export_data)
            
            if response.status_code == 200:
                # Check if it's a PDF response
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    content_disposition = response.headers.get('content-disposition', '')
                    if 'attachment' in content_disposition and '.pdf' in content_disposition:
                        self.log_result("Export Chat History PDF", True, f"PDF export successful (size: {len(response.content)} bytes)")
                        return True
                    else:
                        self.log_result("Export Chat History PDF", False, f"Invalid content disposition: {content_disposition}")
                        return False
                else:
                    self.log_result("Export Chat History PDF", False, f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_result("Export Chat History PDF", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Export Chat History PDF", False, f"Exception: {str(e)}")
            return False
    
    def test_export_chat_history_txt(self):
        """Test export chat history as TXT"""
        try:
            export_data = {
                "format": "txt",
                "session_id": self.session_id
            }
            
            response = self.make_request("POST", "/chat/export", export_data)
            
            if response.status_code == 200:
                # Check if it's a TXT response
                content_type = response.headers.get('content-type', '')
                if 'text/plain' in content_type:
                    content_disposition = response.headers.get('content-disposition', '')
                    if 'attachment' in content_disposition and '.txt' in content_disposition:
                        self.log_result("Export Chat History TXT", True, f"TXT export successful (size: {len(response.content)} bytes)")
                        return True
                    else:
                        self.log_result("Export Chat History TXT", False, f"Invalid content disposition: {content_disposition}")
                        return False
                else:
                    self.log_result("Export Chat History TXT", False, f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_result("Export Chat History TXT", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Export Chat History TXT", False, f"Exception: {str(e)}")
            return False

    # ============= User Statistics Tests =============
    
    def test_user_statistics(self):
        """Test user statistics endpoint"""
        try:
            response = self.make_request("GET", "/user/stats")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("stats"):
                    stats = result["stats"]
                    
                    # Verify expected fields are present
                    expected_fields = [
                        "total_messages", "total_images", "total_code_requests", 
                        "total_sessions", "last_activity"
                    ]
                    
                    missing_fields = []
                    for field in expected_fields:
                        if field not in stats:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        self.log_result("User Statistics", False, f"Missing fields: {missing_fields}")
                        return False
                    
                    # Verify data types
                    if (isinstance(stats["total_messages"], int) and 
                        isinstance(stats["total_images"], int) and
                        isinstance(stats["total_code_requests"], int) and
                        isinstance(stats["total_sessions"], int)):
                        
                        self.log_result("User Statistics", True, 
                                      f"Stats retrieved: {stats['total_messages']} chats, "
                                      f"{stats['total_images']} images, "
                                      f"{stats['total_code_requests']} code assists, "
                                      f"{stats['total_sessions']} sessions")
                        return True
                    else:
                        self.log_result("User Statistics", False, "Invalid data types in statistics")
                        return False
                else:
                    self.log_result("User Statistics", False, f"Invalid response format: {result}")
                    return False
            else:
                self.log_result("User Statistics", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("User Statistics", False, f"Exception: {str(e)}")
            return False

    # ============= Health Check =============
    
    def test_health_check(self):
        """Test health endpoint"""
        try:
            response = self.make_request("GET", "/health")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "healthy":
                    self.log_result("Health Check", True, "API is healthy")
                    return True
                else:
                    self.log_result("Health Check", False, f"Unhealthy status: {result}")
                    return False
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Health Check", False, f"Exception: {str(e)}")
            return False

    # ============= Main Test Runner =============
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting Comprehensive Backend API Testing for Tribe AI Platform")
        print("=" * 80)
        
        # Test order: Authentication first, then other features
        tests = [
            # Health check first
            ("Health Check", self.test_health_check),
            
            # Authentication tests
            ("Authentication - Register", self.test_auth_register),
            ("Authentication - Login", self.test_auth_login),
            ("Authentication - Session", self.test_auth_session),
            
            # Alpha Chat tests (Existing Features Regression Testing)
            ("Alpha Chat - GPT-5", self.test_chat_gpt5),
            ("Alpha Chat - Claude", self.test_chat_claude),
            ("Alpha Chat - Gemini", self.test_chat_gemini),
            
            # Translation Feature Tests
            ("Translation - English to Spanish", self.test_translation_spanish),
            ("Translation - English to French", self.test_translation_french),
            
            # Export Chat History Tests
            ("Export Chat History - PDF", self.test_export_chat_history_pdf),
            ("Export Chat History - TXT", self.test_export_chat_history_txt),
            
            # User Statistics Tests
            ("User Statistics Dashboard", self.test_user_statistics),
            
            # Image Generation (Existing Features Regression Testing)
            ("Image Generation", self.test_image_generation),
            
            # Code Assistant (Existing Features Regression Testing)
            ("Code Assistant - Python", self.test_code_assistant_python),
            ("Code Assistant - JavaScript", self.test_code_assistant_javascript),
            
            # Law Library
            ("Law Library - Search", self.test_law_search),
            ("Law Library - Assist", self.test_law_assist),
            ("Law Library - Download", self.test_law_download),
            
            # Tribe Office
            ("Tribe Office - Word Create", self.test_office_word_create),
            ("Tribe Office - Excel Create", self.test_office_excel_create),
            ("Tribe Office - PowerPoint Create", self.test_office_powerpoint_create),
            ("Tribe Office - Integrations Status", self.test_office_integrations_status),
            
            # Tribe Studio
            ("Tribe Studio - Video Generation", self.test_studio_generate_video),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running: {test_name}")
            try:
                success = test_func()
                if success:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ FAIL {test_name}: Unexpected error - {str(e)}")
                failed += 1
            
            # Small delay between tests
            time.sleep(0.5)
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed > 0:
            print("\n🔍 FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if not result["success"]:
                    print(f"   ❌ {test_name}: {result['message']}")
        
        return passed, failed

def main():
    """Main function to run all tests"""
    tester = TribeAITester()
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()