"""
🛠️ LIBRARY TOOL DEFINITIONS & EXECUTION BACKEND

Các Tool phục vụ Test Case:

TC01: Direct query
    -> Không sử dụng Tool.

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
from typing import Dict, Any


# ==============================================================================
# 1. TOOL SCHEMAS
# ==============================================================================

TOOLS_SCHEMA = [

    # --------------------------------------------------------------------------
    # Tool 1: Tìm kiếm sách
    # Dùng cho TC04
    # --------------------------------------------------------------------------
    {
        "name": "search_books",
        "description": (
            "Tìm kiếm các cuốn sách trong thư viện theo tên, chủ đề "
            "hoặc nhu cầu học tập."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Từ khóa hoặc chủ đề cần tìm kiếm. "
                        "Ví dụ: 'ôn thi THPT quốc gia'."
                    )
                }
            },
            "required": ["query"]
        }
    },

    # --------------------------------------------------------------------------
    # Tool 2: Kiểm tra tình trạng sách
    # Dùng cho TC02, TC04, TC05
    # --------------------------------------------------------------------------
    {
        "name": "check_book_status",
        "description": (
            "Tra cứu tình trạng mượn trả và khả năng sẵn có "
            "của một cuốn sách trong thư viện."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "book_name": {
                    "type": "string",
                    "description": (
                        "Tên cuốn sách cần tra cứu. "
                        "Ví dụ: 'Python Programming'."
                    )
                }
            },
            "required": ["book_name"]
        }
    },

    # --------------------------------------------------------------------------
    # Tool 3: Gia hạn sách đang mượn
    # Dùng cho TC03
    # --------------------------------------------------------------------------
    {
        "name": "renew_borrowed_book",
        "description": (
            "Gia hạn thời gian mượn một cuốn sách đang được sinh viên mượn."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "book_name": {
                    "type": "string",
                    "description": (
                        "Tên cuốn sách cần gia hạn. "
                        "Ví dụ: 'Python Programming'."
                    )
                },
                "student_id": {
                    "type": "string",
                    "description": (
                        "Mã sinh viên đang mượn sách. "
                        "Ví dụ: 'SV2026001'."
                    )
                },
                "additional_weeks": {
                    "type": "integer",
                    "description": (
                        "Số tuần muốn gia hạn thêm. "
                        "Ví dụ: 2."
                    ),
                    "minimum": 1
                }
            },
            "required": [
                "book_name",
                "student_id",
                "additional_weeks"
            ]
        }
    }

]


# ==============================================================================
# 2. MOCK LIBRARY DATABASE
# ==============================================================================

BOOK_DATABASE = {

    # --------------------------------------------------------------------------
    # TC02 + TC03
    # --------------------------------------------------------------------------
    "python programming": {
        "book_id": "BOOK-PYTHON-001",
        "title": "Python Programming",
        "author": "John Smith",
        "category": "Programming",
        "status": "BORROWED",
        "borrower": "SV2026001",
        "due_date": "30/09/2026",
        "renewable": True
    },

    # --------------------------------------------------------------------------
    # TC04 - Các sách liên quan đến THPT Quốc gia
    # --------------------------------------------------------------------------
    "toan hoc 12": {
        "book_id": "BOOK-MATH12-001",
        "title": "Toán học 12",
        "author": "Nguyễn Văn C",
        "category": "THPT Quốc gia",
        "status": "AVAILABLE",
        "borrower": None,
        "due_date": None,
        "renewable": False
    },

    "ngu van 12": {
        "book_id": "BOOK-LIT12-001",
        "title": "Ngữ văn 12",
        "author": "Trần Thị D",
        "category": "THPT Quốc gia",
        "status": "AVAILABLE",
        "borrower": None,
        "due_date": None,
        "renewable": False
    },

    "luyen thi thpt quoc gia mon toan": {
        "book_id": "BOOK-MATH-THPT-001",
        "title": "Luyện thi THPT Quốc gia môn Toán",
        "author": "Phạm Văn E",
        "category": "THPT Quốc gia",
        "status": "AVAILABLE",
        "borrower": None,
        "due_date": None,
        "renewable": False
    },

    "luyen thi thpt quoc gia mon ngu van": {
        "book_id": "BOOK-LIT-THPT-001",
        "title": "Luyện thi THPT Quốc gia môn Ngữ văn",
        "author": "Lê Thị F",
        "category": "THPT Quốc gia",
        "status": "BORROWED",
        "borrower": "SV2026002",
        "due_date": "25/09/2026",
        "renewable": True
    },

    "vat ly 12": {
        "book_id": "BOOK-PHYS12-001",
        "title": "Vật lý 12",
        "author": "Đỗ Văn G",
        "category": "THPT Quốc gia",
        "status": "AVAILABLE",
        "borrower": None,
        "due_date": None,
        "renewable": False
    }
}


# ==============================================================================
# 3. HELPER
# ==============================================================================

def normalize_text(text: str) -> str:
    """Chuẩn hóa chuỗi để tìm kiếm."""
    return " ".join(text.strip().lower().split())


# ==============================================================================
# 4. TOOL IMPLEMENTATIONS
# ==============================================================================

def execute_search_books(query: str) -> str:
    """
    Tìm sách theo chủ đề/từ khóa.

    TC04:
        search_books("ôn thi THPT quốc gia")
    """

    query_normalized = normalize_text(query)

    # Trường hợp TC04
    if (
        "thpt" in query_normalized
        or "quoc gia" in query_normalized
        or "ôn thi" in query_normalized
        or "on thi" in query_normalized
    ):
        books = [
            {
                "book_id": book["book_id"],
                "title": book["title"],
                "author": book["author"],
                "category": book["category"]
            }
            for book in BOOK_DATABASE.values()
            if book["category"] == "THPT Quốc gia"
        ]

        return json.dumps({
            "status": "SUCCESS",
            "query": query,
            "count": len(books),
            "books": books
        }, ensure_ascii=False)

    # Tìm kiếm thông thường
    results = []

    for book in BOOK_DATABASE.values():
        searchable = normalize_text(
            f"{book['title']} "
            f"{book['author']} "
            f"{book['category']}"
        )

        if query_normalized in searchable:
            results.append({
                "book_id": book["book_id"],
                "title": book["title"],
                "author": book["author"],
                "category": book["category"]
            })

    if not results:
        return json.dumps({
            "status": "NOT_FOUND",
            "query": query,
            "books": [],
            "message": (
                f"Không tìm thấy sách phù hợp với '{query}'."
            )
        }, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "query": query,
        "count": len(results),
        "books": results
    }, ensure_ascii=False)


def execute_check_book_status(book_name: str) -> str:
    """
    Kiểm tra tình trạng sách.

    TC02:
        Python Programming -> BORROWED

    TC05:
        Advanced Quantum Mechanics -> NOT_FOUND
    """

    normalized_name = normalize_text(book_name)

    book = BOOK_DATABASE.get(normalized_name)

    if not book:
        return json.dumps({
            "status": "NOT_FOUND",
            "book_name": book_name,
            "message": (
                f"Không tìm thấy cuốn sách '{book_name}' "
                "trong thư viện."
            )
        }, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "book": {
            "book_id": book["book_id"],
            "title": book["title"],
            "author": book["author"],
            "category": book["category"],
            "status": book["status"],
            "borrower": book["borrower"],
            "due_date": book["due_date"],
            "renewable": book["renewable"]
        }
    }, ensure_ascii=False)


def execute_renew_borrowed_book(
    book_name: str,
    student_id: str,
    additional_weeks: int
) -> str:
    """
    Gia hạn sách đang mượn.

    TC03:
        book_name = Python Programming
        additional_weeks = 2
    """

    normalized_name = normalize_text(book_name)
    normalized_student_id = student_id.strip().upper()

    # Kiểm tra số tuần
    if additional_weeks <= 0:
        return json.dumps({
            "status": "INVALID_ARGUMENT",
            "message": "Số tuần gia hạn phải lớn hơn 0."
        }, ensure_ascii=False)

    # Kiểm tra sách
    book = BOOK_DATABASE.get(normalized_name)

    if not book:
        return json.dumps({
            "status": "NOT_FOUND",
            "book_name": book_name,
            "message": (
                f"Không tìm thấy cuốn sách '{book_name}' "
                "trong thư viện."
            )
        }, ensure_ascii=False)

    # Kiểm tra sách có đang được mượn
    if book["status"] != "BORROWED":
        return json.dumps({
            "status": "NOT_BORROWED",
            "book_name": book["title"],
            "message": (
                f"Cuốn sách '{book['title']}' "
                "hiện không được mượn."
            )
        }, ensure_ascii=False)

    # Kiểm tra người mượn
    if book["borrower"] != normalized_student_id:
        return json.dumps({
            "status": "BORROWER_MISMATCH",
            "book_name": book["title"],
            "message": (
                f"Sinh viên {normalized_student_id} "
                f"không phải người đang mượn "
                f"'{book['title']}'."
            )
        }, ensure_ascii=False)

    # Kiểm tra có được gia hạn
    if not book["renewable"]:
        return json.dumps({
            "status": "RENEWAL_NOT_ALLOWED",
            "book_name": book["title"],
            "message": (
                f"Cuốn sách '{book['title']}' "
                "không được phép gia hạn."
            )
        }, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "book_id": book["book_id"],
        "book_name": book["title"],
        "student_id": normalized_student_id,
        "additional_weeks": additional_weeks,
        "current_due_date": book["due_date"],
        "message": (
            f"Gia hạn thành công cuốn sách "
            f"'{book['title']}' thêm "
            f"{additional_weeks} tuần."
        )
    }, ensure_ascii=False)


# ==============================================================================
# 5. TOOL ROUTER
# ==============================================================================

TOOL_ROUTER = {
    "search_books": execute_search_books,
    "check_book_status": execute_check_book_status,
    "renew_borrowed_book": execute_renew_borrowed_book
}


# ==============================================================================
# 6. DISPATCH TOOL CALL
# ==============================================================================

def dispatch_tool_call(
    tool_name: str,
    arguments: Dict[str, Any]
) -> str:
    """
    Trung chuyển request tới đúng Tool.
    """

    tool = TOOL_ROUTER.get(tool_name)

    if not tool:
        return json.dumps({
            "status": "UNKNOWN_TOOL",
            "error": f"Tool '{tool_name}' không tồn tại!"
        }, ensure_ascii=False)

    try:
        return tool(**arguments)

    except TypeError as e:
        return json.dumps({
            "status": "INVALID_ARGUMENT",
            "error": str(e)
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "status": "EXECUTION_ERROR",
            "error": str(e)
        }, ensure_ascii=False)
