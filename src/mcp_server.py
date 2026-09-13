"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE

Mô phỏng MCP Server cho hệ thống thư viện.

Test Cases:

TC01: Direct query
    -> Không gọi Tool.

TC02: Single tool query
    -> check_book_status

TC03: Borrowed book renewal
    -> renew_borrowed_book

TC04: Multi-step reasoning
    -> search_books
    -> check_book_status

TC05: Edge case handling
    -> check_book_status
    -> NOT_FOUND
"""

import json
import sys
from typing import Dict, Any, List

from tools import TOOLS_SCHEMA, dispatch_tool_call


# ==============================================================================
# UTF-8 OUTPUT
# ==============================================================================

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# MCP SERVER
# ==============================================================================

class MCPLibraryServer:
    """
    Giả lập MCP Server cho hệ thống thư viện.
    """

    def __init__(
        self,
        server_name: str = "vinuni-library-mcp-server"
    ):
        self.server_name = server_name
        self.version = "2026.1.0"

    # --------------------------------------------------------------------------
    # LIST TOOLS
    # --------------------------------------------------------------------------

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Trả về danh sách Tool Schema được MCP Server công bố.
        """

        return TOOLS_SCHEMA

    # --------------------------------------------------------------------------
    # CALL TOOL
    # --------------------------------------------------------------------------

    def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Thực thi Tool thông qua Tool Router và trả về response
        theo cấu trúc JSON-RPC 2.0 mô phỏng.

        Args:
            tool_name:
                Tên Tool cần gọi.

            arguments:
                Arguments truyền vào Tool.

        Returns:
            Dictionary chứa response của MCP Server.
        """

        # ----------------------------------------------------------------------
        # 1. Gọi Tool Router
        # ----------------------------------------------------------------------

        result_json = dispatch_tool_call(
            tool_name,
            arguments
        )

        # ----------------------------------------------------------------------
        # 2. Parse JSON string -> Python Dictionary
        # ----------------------------------------------------------------------

        try:
            content = json.loads(result_json)

        except json.JSONDecodeError as e:
            content = {
                "status": "INVALID_TOOL_RESPONSE",
                "error": str(e)
            }

        # ----------------------------------------------------------------------
        # 3. Đóng gói response
        # ----------------------------------------------------------------------

        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": content
        }


# ==============================================================================
# LOCAL TEST HELPERS
# ==============================================================================

def print_separator():
    print("=" * 70)


def print_tool_call(
    server: MCPLibraryServer,
    test_case: str,
    description: str,
    tool_name: str,
    arguments: Dict[str, Any]
):
    """
    Chạy một Tool thông qua MCP Server và in kết quả.
    """

    print()
    print_separator()
    print(f"🧪 {test_case} - {description}")
    print_separator()

    print(f"🔧 Tool      : {tool_name}")
    print(
        f"📥 Arguments : "
        f"{json.dumps(arguments, ensure_ascii=False)}"
    )

    response = server.call_tool(
        tool_name,
        arguments
    )

    print()
    print("📤 MCP Response:")

    print(
        json.dumps(
            response,
            ensure_ascii=False,
            indent=2
        )
    )


# ==============================================================================
# MAIN - MCP SERVER TEST
# ==============================================================================

if __name__ == "__main__":

    print_separator()
    print("🔌 VINUNI LIBRARY MCP SERVER")
    print_separator()

    # --------------------------------------------------------------------------
    # Khởi tạo Server
    # --------------------------------------------------------------------------

    server = MCPLibraryServer()

    print(
        f"✅ Server       : {server.server_name}"
    )

    print(
        f"✅ Version      : {server.version}"
    )

    # --------------------------------------------------------------------------
    # Kiểm tra Tool Schema
    # --------------------------------------------------------------------------

    tools = server.list_tools()

    print(
        f"📦 Number Tools : {len(tools)}"
    )

    print()
    print("🛠️ Available Tools:")

    for index, tool in enumerate(tools, start=1):

        print(
            f"   {index}. {tool.get('name')}"
        )

    # --------------------------------------------------------------------------
    # TC01
    # --------------------------------------------------------------------------

    print()
    print_separator()
    print("🧪 TC01 - Direct Query")
    print_separator()

    print(
        "ℹ️ TC01 không gọi Tool."
    )

    print(
        "   User: Xin chào, tôi muốn biết quy trình đăng ký mượn sách?"
    )

    print(
        "   → Agent trả lời trực tiếp từ System Prompt."
    )

    # --------------------------------------------------------------------------
    # TC02
    # --------------------------------------------------------------------------

    print_tool_call(
        server=server,
        test_case="TC02",
        description="Check book status",
        tool_name="check_book_status",
        arguments={
            "book_name": "Python Programming"
        }
    )

    # --------------------------------------------------------------------------
    # TC03
    # --------------------------------------------------------------------------

    print_tool_call(
        server=server,
        test_case="TC03",
        description="Renew borrowed book",
        tool_name="renew_borrowed_book",
        arguments={
            "book_name": "Python Programming",
            "additional_weeks": 2
        }
    )

    # --------------------------------------------------------------------------
    # TC04 - STEP 1
    # --------------------------------------------------------------------------

    print_tool_call(
        server=server,
        test_case="TC04 - STEP 1",
        description="Search books",
        tool_name="search_books",
        arguments={
            "query": "ôn thi THPT quốc gia"
        }
    )

    # --------------------------------------------------------------------------
    # TC04 - STEP 2
    #
    # Đây là bước Agent sẽ thực hiện sau khi nhận kết quả search_books.
    # --------------------------------------------------------------------------

    print_tool_call(
        server=server,
        test_case="TC04 - STEP 2",
        description="Check book availability",
        tool_name="check_book_status",
        arguments={
            "book_name": "Toán học 12"
        }
    )

    # --------------------------------------------------------------------------
    # TC05
    # --------------------------------------------------------------------------

    print_tool_call(
        server=server,
        test_case="TC05",
        description="Book not found",
        tool_name="check_book_status",
        arguments={
            "book_name": "Advanced Quantum Mechanics"
        }
    )

    # --------------------------------------------------------------------------
    # DONE
    # --------------------------------------------------------------------------

    print()
    print_separator()
    print("✅ MCP SERVER TEST COMPLETED")
    print_separator()
