"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """
    Offline Mock Provider cho Library Agent.

    Compatible with MCPLibraryServer + tools.py.

    Test Cases:

    TC01:
        Direct query
        -> Không gọi Tool

    TC02:
        Check Python Programming
        -> check_book_status

    TC03:
        Renew Python Programming
        -> renew_borrowed_book

    TC04:
        Tìm sách ôn thi THPT Quốc gia
        -> search_books
        -> check_book_status

    TC05:
        Advanced Quantum Mechanics
        -> check_book_status
        -> NOT_FOUND
    """

    def __init__(self):
        self.model_name = "Offline-Library-Mock-Model-2026"

    # ======================================================================
    # DIRECT RESPONSE
    # ======================================================================

    def generate(
        self,
        prompt: str,
        system_prompt: str = ""
    ) -> str:

        prompt_lower = prompt.lower()

        # TC01
        if "đăng ký mượn sách" in prompt_lower:
            return (
                "[Mock Chatbot Response]: "
                "Để đăng ký mượn sách, bạn cần tìm kiếm cuốn sách "
                "trong thư viện, kiểm tra tình trạng sách và thực hiện "
                "yêu cầu mượn nếu sách đang ở trạng thái AVAILABLE."
            )

        return (
            "[Mock Chatbot Response]: "
            f"Tôi đã nhận được câu hỏi '{prompt}'."
        )

    # ======================================================================
    # TOOL-AWARE RESPONSE
    # ======================================================================

    def generate_with_tools(
        self,
        prompt: str,
        tools_schema: List[Dict[str, Any]],
        system_prompt: str = ""
    ) -> Dict[str, Any]:

        prompt_lower = prompt.lower()

        # ==================================================================
        # TC03
        # Gia hạn Python Programming thêm 2 tuần
        #
        # IMPORTANT:
        # renew_borrowed_book trong tools.py hiện tại chỉ yêu cầu:
        #   book_name
        #   additional_weeks
        #
        # Không truyền student_id.
        # ==================================================================

        if (
            "gia hạn" in prompt_lower
            and "python programming" in prompt_lower
        ):
            return {
                "type": "tool_call",

                "tool_name": "renew_borrowed_book",

                "arguments": {
                    "book_name": "Python Programming",
                    "additional_weeks": 2
                },

                "thought": (
                    "Người dùng muốn gia hạn cuốn sách "
                    "'Python Programming' thêm 2 tuần. "
                    "Tôi sẽ gọi tool renew_borrowed_book."
                )
            }

        # ==================================================================
        # TC04 - STEP 2
        #
        # Nếu Agent đã nhận kết quả search_books và prompt/context
        # chứa "Toán học 12", kiểm tra tình trạng sách.
        # ==================================================================

        if (
            "toán học 12" in prompt_lower
            and (
                "kết quả" in prompt_lower
                or "search_books" in prompt_lower
                or "available" in prompt_lower
                or "tool" in prompt_lower
            )
        ):
            return {
                "type": "tool_call",

                "tool_name": "check_book_status",

                "arguments": {
                    "book_name": "Toán học 12"
                },

                "thought": (
                    "Tôi đã tìm được cuốn 'Toán học 12'. "
                    "Tôi sẽ kiểm tra tình trạng mượn trả của "
                    "cuốn sách để xác định sách có thể cho mượn hay không."
                )
            }

        # ==================================================================
        # TC04 - STEP 1
        #
        # Tìm sách liên quan đến ôn thi THPT Quốc gia.
        # ==================================================================

        if (
            "ôn thi thpt quốc gia" in prompt_lower
            or "on thi thpt quoc gia" in prompt_lower
            or (
                "mượn sách" in prompt_lower
                and "thpt" in prompt_lower
            )
        ):
            return {
                "type": "tool_call",

                "tool_name": "search_books",

                "arguments": {
                    "query": "ôn thi THPT quốc gia"
                },

                "thought": (
                    "Người dùng muốn tìm sách để ôn thi "
                    "THPT Quốc gia. Tôi sẽ gọi search_books "
                    "để tìm các sách phù hợp."
                )
            }

        # ==================================================================
        # TC05
        #
        # Sách không tồn tại.
        # Tool sẽ trả về NOT_FOUND.
        # ==================================================================

        if "advanced quantum mechanics" in prompt_lower:
            return {
                "type": "tool_call",

                "tool_name": "check_book_status",

                "arguments": {
                    "book_name": "Advanced Quantum Mechanics"
                },

                "thought": (
                    "Người dùng muốn mượn cuốn sách "
                    "'Advanced Quantum Mechanics'. "
                    "Tôi cần kiểm tra xem sách có tồn tại "
                    "trong thư viện hay không."
                )
            }

        # ==================================================================
        # TC02
        #
        # Kiểm tra Python Programming.
        # ==================================================================

        if (
            "python programming" in prompt_lower
            and (
                "tình trạng" in prompt_lower
                or "mượn trả" in prompt_lower
                or "tra cứu" in prompt_lower
                or "kiểm tra" in prompt_lower
            )
        ):
            return {
                "type": "tool_call",

                "tool_name": "check_book_status",

                "arguments": {
                    "book_name": "Python Programming"
                },

                "thought": (
                    "Người dùng muốn tra cứu tình trạng "
                    "mượn trả của 'Python Programming'. "
                    "Tôi sẽ gọi check_book_status."
                )
            }

        # ==================================================================
        # FALLBACK
        # ==================================================================

        return {
            "type": "text",

            "content": (
                "[Mock Agent Response]: "
                "Bạn cần có mã sinh viên hợp lệ để mượn sách, "
                "đồng thời cần cung cấp tên sách chính xác để mình kiểm tra trong hệ thống thư viện."
            ),

            "thought": (
                "Câu hỏi không yêu cầu sử dụng Tool "
                "trong các Test Case hiện tại."
            )
        }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không
            if response.function_calls:
                call = response.function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": response.text or "",
                    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()
