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
- **MRR (Mean Reciprocal Rank)**: Đây là metric quan trọng để đánh giá Retrieval stage. Thay vì chỉ xem có tìm thấy dữ liệu không (Hit Rate), MRR đo lường vị trí của kết quả đúng. Nếu kết quả đúng nằm ở vị trí số 1, rank là 1; nếu ở vị trí số 2, rank là 0.5. MRR cao chứng tỏ hệ thống Reranker (Jina) đang hoạt động hiệu quả trong việc đẩy thông tin liên quan nhất lên đầu.
- **Cohen's Kappa**: Tôi đã học cách dùng chỉ số này để đo lường độ tin cậy của Multi-Judge. Nó không chỉ đơn thuần là tỷ lệ đồng thuận (Agreement Rate) mà còn tính đến tỷ lệ đồng thuận ngẫu nhiên. Trong hệ thống benchmark, Cohen's Kappa giúp xác định xem sự đồng nhất giữa GPT-4o-mini và Qwen là do tiêu chí Rubric chặt chẽ hay chỉ là trùng hợp.
- **Position Bias**: Một hiện tượng "thiên kiến vị trí" của LLM Judge, nơi mô hình có xu hướng ưu tiên chọn các phương án ở đầu hoặc ở cuối danh sách. Bằng cách sử dụng Multi-Judge và thiết lập Rubric chấm điểm số thay vì chọn phương án, tôi đã giảm thiểu được sái số này.
- **Trade-off Chi phí vs Chất lượng**: Trong quá trình vận hành, tôi nhận ra việc dùng GPT-4o cho 100% case sẽ rất tốn kém (Chi phí cao). Việc thay thế bằng GPT-4o-mini làm Judge chính và chỉ gọi Qwen/GPT-4o để "phân xử" khi có xung đột (Consensus logic) giúp giảm 30-40% chi phí mà vẫn giữ nguyên độ chính xác của kết quả Benchmark (Chất lượng).
- **Grounding & Model Intelligence**: Tôi nhận ra rằng với các model thông minh như Qwen, nếu System Prompt (V1) không có tính **Grounding** khắt khe, mô hình sẽ tự ý "sáng tạo" thêm thông tin ngoài ngữ cảnh. Thậm chí các model Judge như GPT-4o-mini cũng có thể bị đánh lừa bởi sự nhiệt tình (Helpfulness) này nếu chúng ta không thiết lập các tiêu chí chấm điểm (Rubric) cực kỳ chặt chẽ về tính An toàn và Fact-checking.

## 3. Khó khăn & Cách giải quyết (Problem Solving)
- **Thử thách 1 (Performance vs Rate Limit):** Khi cố gắng đẩy tốc độ benchmark lên tối đa bằng cách sử dụng `acompletion` (bất đồng bộ hoàn toàn) để gửi 150 yêu cầu AI cùng lúc cho 50 test cases, hệ thống đã ngay lập tức bị chặn bởi lỗi **`litellm.RateLimitError` (429)** từ phía DashScope (Qwen), khiến toàn bộ tiến trình bị sập giữa chừng.
- **Giải quyết:** Tôi đã thực hiện "lùi một bước để tiến hai bước" bằng cách:
    1. Quay lại sử dụng cơ chế **Thread-pooling (`asyncio.to_thread`)** kết hợp với **Batching (20-50 câu/lượt)**. Việc này tạo ra một "hệ thống phanh" tự nhiên cho RPM (Request Per Minute).
    2. Loại bỏ hoàn toàn Gemini và Groq do hạn mức RPM quá thấp, chuyển sang dùng **Qwen-plus** và **GPT-4o-mini** với cấu trúc hạ tầng ổn định hơn.
- **Kết quả:** Hệ thống đạt được sự cân bằng hoàn hảo giữa tốc độ (xử lý 50 câu trong ~3-4 phút) và độ tin cậy (Success Rate 100%, không còn lỗi 429).

---
*Ngày hoàn thành: 21/04/2026*
