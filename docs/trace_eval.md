# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Tuấn Khanh
> **Mã Sinh Viên / Mã Học viên:** 2A202602819  
> **Chủ đề Lựa chọn:** Tra cứu vị trí sách, tình trạng mượn/trả và gia hạn tài liệu.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 3/5 | Người dùng có thể yêu cầu nhiều thao tác liên tiếp: xác định tài liệu dựa trên mô tả → kiểm tra vị trí/kệ → kiểm tra tình trạng còn sẵn hay đang được mượn → kiểm tra thông tin người mượn/hạn trả → xác định tài liệu có đủ điều kiện gia hạn hay không → thực hiện gia hạn. Các bước có quan hệ với nhau, không đơn thuần là các câu hỏi độc lập với nhau.
| **2. Tool Interaction** | 5/ 5 | Agent cần tương tác với MCP Server/CSDL thư viện để tìm kiếm catalogue, vị trí tài liệu, trạng thái mượn/trả và có thể thực hiện thao tác gia hạn.
| **3. Dynamic Decision** | 5/ 5 | Có những yêu cầu từ người dùng chỉ cần 1 thao tác ngắn nhưng cũng có những yêu cầu cần được thực hiện qua nhiều bước liên tiếp, trong đó kết quả của bước trước sẽ được dùng để quyết định bước tiếp theo. Ví dụ, tra cứu vị trí sách có workflow như sau:
||  1: Sách có trong hệ thống hay không -> 2.1 hoặc 2.2 |
||  2.1: Tra cứu tình trạng mượn trả (nếu sách có trong hệ thống) -> 3.1 hoặc 3.2 |
||  2.2: Thông báo không tìm thấy sách trong hệ thống -> End flow |
||  3.1: Tìm vị trí của sách nếu sách vẫn còn -> 4.1 |
||  3.2: Thông báo sách đã được mượn và ngày sách được trả lại -> 4.2 |
||  4.1: Thông báo vị trí của sách -> End flow |
||  4.2: Hỏi người mượn có muốn gợi ý những sách với nội dung tương tự không -> 5 |
||  5: Gợi ý các sách với nội dung tương tự (Một work flow khác) |
| **4. Long Horizon Goal** | 3/ 5 | Các yêu cầu thường có thể được giải quyết chỉ trong 1 lượt tương tác nếu yêu cầu được đưa ra rõ ràng (tìm sách với tên cụ thể, tra cứu tình trạng mượn trả, thực hiện mượn/ trả/ gia hạn mượn). Đối với các yêu cầu mơ hồ (VD: Tôi muốn mượn 1 cuốn sách để ôn tập cho kỳ thi tuyển sinh lớp 10) thì hệ thống sẽ cần cung cấp thêm thông tin và hỏi ý kiến người đối thoại ở các lượt tương tác tiếp theo trước khi giải quyết được yêu cầu đặt ra ban đầu bởi người dùng. Nhưng xác suất của các yêu cầu này có thể không nhiều.
| **TỔNG ĐIỂM AGENTIC FIT** | **16/20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Tôi muốn mượn sách liên quan đến THPT Quốc gia",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "search_books",
    "arguments": {
      "query": "THPT quốc gia"
    },
    "observation": {
      "status": "SUCCESS",
      "query": "THPT quốc gia",
      "count": 5,
      "books": [
        {
          "book_id": "BOOK-MATH12-001",
          "title": "Toán học 12",
          "author": "Nguyễn Văn C",
          "category": "THPT Quốc gia"
        },
        {
          "book_id": "BOOK-LIT12-001",
          "title": "Ngữ văn 12",
          "author": "Trần Thị D",
          "category": "THPT Quốc gia"
        },
        {
          "book_id": "BOOK-MATH-THPT-001",
          "title": "Luyện thi THPT Quốc gia môn Toán",
          "author": "Phạm Văn E",
          "category": "THPT Quốc gia"
        },
        {
          "book_id": "BOOK-LIT-THPT-001",
          "title": "Luyện thi THPT Quốc gia môn Ngữ văn",
          "author": "Lê Thị F",
          "category": "THPT Quốc gia"
        },
        {
          "book_id": "BOOK-PHYS12-001",
          "title": "Vật lý 12",
          "author": "Đỗ Văn G",
          "category": "THPT Quốc gia"
        }
      ]
    },
    "latency_ms": 2942.15
  },
  {
    "step": 2,
    "query": "Tôi muốn mượn sách liên quan đến THPT Quốc gia",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Đã hoàn tất xử lý qua MCP Server: {\"status\": \"SUCCESS\", \"query\": \"THPT quốc gia\", \"count\": 5, \"books\": [{\"book_id\": \"BOOK-MATH12-001\", \"title\": \"Toán học 12\", \"author\": \"Nguyễn Văn C\", \"category\": \"THPT Quốc gia\"}, {\"book_id\": \"BOOK-LIT12-001\", \"title\": \"Ngữ văn 12\", \"author\": \"Trần Thị D\", \"category\": \"THPT Quốc gia\"}, {\"book_id\": \"BOOK-MATH-THPT-001\", \"title\": \"Luyện thi THPT Quốc gia môn Toán\", \"author\": \"Phạm Văn E\", \"category\": \"THPT Quốc gia\"}, {\"book_id\": \"BOOK-LIT-THPT-001\", \"title\": \"Luyện thi THPT Quốc gia môn Ngữ văn\", \"author\": \"Lê Thị F\", \"category\": \"THPT Quốc gia\"}, {\"book_id\": \"BOOK-PHYS12-001\", \"title\": \"Vật lý 12\", \"author\": \"Đỗ Văn G\", \"category\": \"THPT Quốc gia\"}]}",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [X] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 7 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
