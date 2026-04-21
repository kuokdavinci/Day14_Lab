# 🧠 Failure Analysis Report (5 Whys)

Trong phiên chạy Benchmark ngày 21/04/2026, hệ thống ghi nhận **5 thất bại** (điểm < 5). Dưới đây là phân tích chi tiết.

## 1. Phân tích nguyên nhân gốc rễ (Root Cause Analysis)

Đa số các lỗi (4/5) đều đến từ cùng một nguyên nhân kỹ thuật.

### Lỗi: Rate Limit Exceeded (TPM Limit)
*   **Hiện tượng:** 4 câu hỏi nhận về câu trả lời: "Đã có lỗi xảy ra: litellm.RateLimitError".
*   **5 Whys:**
    1.  **Tại sao Agent không trả lời được?** -> Vì API Groq bị lỗi Rate Limit (429).
    2.  **Tại sao bị Rate Limit?** -> Vì tổng số Token yêu cầu vượt quá hạn mức 6000 TPM của tài khoản.
    3.  **Tại sao vượt quá 6000 TPM dù đã chạy tuần tự?** -> Do Context truyền vào Agent (3 chunks) cộng với Prompt của Judge quá lớn, gây ra các đỉnh (spikes) về token dù có khoảng nghỉ 10s.
    4.  **Tại sao không có cơ chế bù đắp?** -> Do Semaphore chưa đủ giãn hoặc chưa có hàng đợi (queue) thông minh để tính toán Token trước khi gửi.
    5.  **Giải pháp gốc rễ là gì?** -> Cần nâng cấp Tier API hoặc sử dụng logic tính toán Token động để kiểm soát tốc độ gửi requests dựa trên TPM thực tế.

---

## 2. Phân tích lỗi Logic (RAG Failure)

### Trường hợp Case #1 (Ambiguity Category) - Score 3.5
*   **Câu hỏi:** "Mức trợ cấp là bao nhiêu?"
*   **Lỗi:** Agent trả lời về trợ cấp thâm niên, nhưng Expected Answer yêu cầu Agent phải hỏi lại thông tin (vì câu hỏi quá chung chung).
*   **5 Whys:**
    1.  **Tại sao điểm thấp?** -> Vì Agent không yêu cầu làm rõ câu hỏi (Clarification).
    2.  **Tại sao Agent không hỏi lại?** -> Vì System Prompt chưa nhấn mạnh đủ việc phải "Socratic questioning" khi thông tin mơ hồ.
    3.  **Tại sao Retrieval lại tìm thấy trợ cấp thâm niên?** -> Do Hybrid Search tìm thấy từ "Trợ cấp" và chunk có điểm cao nhất là trợ cấp thâm niên.
    4.  **Tại sao không có bước Re-rank để lọc bỏ?** -> Do chúng ta đã tắt Jina Reranker để ổn định mạng, làm giảm khả năng lọc các context không sát.
    5.  **Giải pháp gốc rễ là gì?** -> Cần thêm module **Intent Classification** để nhận diện câu hỏi mơ hồ trước khi thực hiện Retrieval.

---

## 3. Đề xuất cải tiến (Action Plan)

1.  **Hạ tầng:** Chuyển sang sử dụng **OpenAI GPT-4o-mini** cho tất cả các Judge để tận dụng hạn mức Token lớn hơn, chỉ dùng Groq cho Agent.
2.  **Chỉnh sửa Prompt:** Cập nhật System Prompt của Agent: "Nếu câu hỏi có ít hơn 5 từ hoặc quá chung chung, hãy yêu cầu người dùng làm rõ trước khi trả lời."
3.  **Bật lại Rerank:** Khi mạng ổn định, cần bật lại **Jina Reranker** để Hit Rate tăng lên (mục tiêu > 85%).
4.  **Hiệu năng:** Tăng thời gian `asyncio.sleep` lên 15-20 giây cho các tài khoản Tier 1.
