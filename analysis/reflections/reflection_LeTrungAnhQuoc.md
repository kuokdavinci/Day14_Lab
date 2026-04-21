# 🧠 Cá nhân Phản ánh (Individual Reflection)

**Họ và tên:** Lê Trung Anh Quốc 
**MSSV:** 2A202600108
**Nhóm:** Cá nhân (bởi vì làm cá nhân mang lại nhiều giá trị về mặt kiến thức, dễ dàng theo dõi các bước thực hiện và cấu trúc của bài lab, đặc biệt trong dự án này)

---

## 1. Đóng góp cụ thể (Engineering Contribution)
- [x] Thiết kế Golden Dataset & Script SDG.
- [x] Triển khai Multi-Judge Engine.
- [x] Xây dựng Async Pipeline & Logic Batching.
- [x] Phân tích lỗi (Failure Analysis) & 5 Whys.
- [x] Tối ưu System Prompt cho Agent V2.

## 2. Bài học kỹ thuật (Technical Depth)
Qua bài Lab này, tôi đã hiểu sâu hơn về:
- **Metrics**: MRR giúp đánh giá chất lượng vị trí của tài liệu tìm kiếm được, khắt khe hơn Hit Rate thông thường.
- **Judge Reliability**: Tầm quan trọng của việc dùng Multi-Judge để khử nhiễu (Position Bias) và tăng tính khách quan cho Benchmarking.
- **Async/Batching**: Cách tối ưu hóa hiệu năng gọi LLM hàng loạt mà không vi phạm Rate Limit của nhà cung cấp.
- **Grounding & Model Intelligence**: Tôi nhận ra rằng với các model thông minh như Qwen, nếu System Prompt (V1) không có tính **Grounding** khắt khe, mô hình sẽ tự ý "sáng tạo" thêm thông tin ngoài ngữ cảnh. Thậm chí các model Judge như GPT-4o-mini cũng có thể bị đánh lừa bởi sự nhiệt tình (Helpfulness) này nếu chúng ta không thiết lập các tiêu chí chấm điểm (Rubric) cực kỳ chặt chẽ về tính An toàn và Fact-checking.

## 3. Khó khăn & Cách giải quyết (Problem Solving)
- **Thử thách 1 (Performance vs Rate Limit):** Khi cố gắng đẩy tốc độ benchmark lên tối đa bằng cách sử dụng `acompletion` (bất đồng bộ hoàn toàn) để gửi 150 yêu cầu AI cùng lúc cho 50 test cases, hệ thống đã ngay lập tức bị chặn bởi lỗi **`litellm.RateLimitError` (429)** từ phía DashScope (Qwen), khiến toàn bộ tiến trình bị sập giữa chừng.
- **Giải quyết:** Tôi đã thực hiện "lùi một bước để tiến hai bước" bằng cách:
    1. Quay lại sử dụng cơ chế **Thread-pooling (`asyncio.to_thread`)** kết hợp với **Batching (20-50 câu/lượt)**. Việc này tạo ra một "hệ thống phanh" tự nhiên cho RPM (Request Per Minute).
    2. Loại bỏ hoàn toàn Gemini và Groq do hạn mức RPM quá thấp, chuyển sang dùng **Qwen-plus** và **GPT-4o-mini** với cấu trúc hạ tầng ổn định hơn.
- **Kết quả:** Hệ thống đạt được sự cân bằng hoàn hảo giữa tốc độ (xử lý 50 câu trong ~3-4 phút) và độ tin cậy (Success Rate 100%, không còn lỗi 429).

---
*Ngày hoàn thành: 21/04/2026*
