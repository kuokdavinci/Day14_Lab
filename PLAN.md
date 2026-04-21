# 📋 Kế hoạch Triển khai Lab 14: AI Evaluation Factory

## 1. Mục tiêu Dự án (Project Objectives)
Xây dựng một **Hệ thống đánh giá tự động (Evaluation Factory)** chuyên nghiệp để benchmark AI Agent. Hệ thống phải chứng minh được bằng con số cụ thể: *"Agent đang tốt ở đâu và tệ ở đâu"* (Trích dẫn từ **README.md**).

## 2. Các chỉ số then chốt (Key Metrics)
Dựa trên yêu cầu từ **README.md** và **GRADING_RUBRIC.md**, hệ thống cần đo lường:
- **Retrieval Metrics:** Hit Rate và MRR (Mean Reciprocal Rank) cho ít nhất 50 test cases.
- **Generation Metrics:** Điểm số từ **Multi-Judge Consensus Engine**.
- **Agreement Metrics:** Agreement Rate (Hệ số đồng thuận) giữa các Judge models.
- **System Metrics:** Cost (Giá tiền/lần Eval), Token Usage, và Latency (Async execution).
- **Regression Metrics:** Delta Analysis (So sánh V1 vs V2).

## 3. Phân chia Nhiệm vụ & Lộ trình Thực hiện (Timeline)
Tổng thời gian thực hiện: **4 Tiếng**.

### Giai đoạn 1: Data & Synthetic Data Generation (SDG) - (45 phút)
*Nhiệm vụ trọng tâm: Thiết kế Golden Dataset.*
- **Công việc cụ thể:**
    - Chạy `data/synthetic_gen.py` để tạo ra ít nhất **50 test cases** chất lượng.
    - Phải bao gồm **Ground Truth IDs** của tài liệu để tính toán Hit Rate (Yêu cầu từ **GRADING_RUBRIC.md**).
    - Tạo các bộ dữ liệu **"Red Teaming"** đặc biệt để thử thách và phá vỡ hệ thống.
- **Đầu ra:** File `data/golden_set.jsonl`.

### Giai đoạn 2: Engine Development & Async Runner - (90 phút)
*Nhiệm vụ trọng tâm: Xây dựng Eval Engine đa tầng.*
- **Công việc cụ thể:**
    - **Multi-Judge Engine:** Triển khai ít nhất **2 model Judge** khác nhau (VD: GPT-4o, Claude 3.5).
    - **Consensus Logic:** Lập trình logic xử lý xung đột điểm số và tính toán độ đồng thuận (Agreement Rate).
    - **Async Runner:** Tối ưu hóa pipeline để chạy song song. Mục tiêu: **< 2 phút cho 50 cases** (Yêu cầu từ **GRADING_RUBRIC.md**).
    - **Calibration:** Đảm bảo hệ thống đánh giá khách quan và tin cậy.

### Giai đoạn 3: Benchmark & Phân tích lỗi (Failure Analysis) - (60 phút)
*Nhiệm vụ trọng tâm: Tìm ra nguyên nhân gốc rễ.*
- **Công việc cụ thể:**
    - Chạy Benchmark toàn diện qua `main.py`.
    - **Failure Clustering:** Phân cụm các lỗi thường gặp.
    - **Phân tích "5 Whys":** Truy vết lỗi nằm ở đâu (Ingestion pipeline, Chunking strategy, Retrieval, hay Prompting - Theo **README.md**).
    - **Cost Analysis:** Lập báo cáo chi tiết về chi phí và đề xuất cách giảm 30% chi phí eval.

### Giai đoạn 4: Tối ưu & Hoàn thiện báo cáo - (45 phút)
*Nhiệm vụ trọng tâm: Cải thiện Agent & Đóng gói.*
- **Công việc cụ thể:**
    - Tối ưu hóa Agent dựa trên dữ liệu benchmark vừa thu thập.
    - **Regression Analysis:** So sánh kết quả phiên bản mới (V2) với phiên bản cũ (V1).
    - **Auto-Gate:** Viết logic tự động quyết định "Release" hoặc "Rollback" dựa trên các ngưỡng (Threshold) chất lượng/chi phí.
    - Hoàn thiện file `analysis/failure_analysis.md`.

## 4. Bảng đối chiếu Tiêu chí Chấm điểm (Grading Alignment)

| Hạng mục | Yêu cầu đạt điểm tối đa (Theo **GRADING_RUBRIC.md**) | Trọng số |
| :--- | :--- | :---: |
| **Retrieval Eval** | Tính Hit Rate & MRR; Giải thích được mối liên hệ giữa Retrieval và Answer Quality. | 10đ |
| **Dataset & SDG** | 50+ cases kèm Ground Truth; Có bộ "Red Teaming" phá vỡ hệ thống. | 10đ |
| **Multi-Judge** | 2+ model Judge; Tính Agreement Rate; Logic xử lý xung đột tự động. | 15đ |
| **Regression** | So sánh V1 vs V2 thành công; Có logic "Release Gate" tự động. | 10đ |
| **Performance** | Chạy Async (< 2 phút); Báo cáo chi tiết Cost & Token usage. | 10đ |
| **Failure Analysis**| Phân tích "5 Whys" cực sâu, chỉ rõ lỗi hệ thống (Chunking, Ingestion, ...). | 5đ |

## 5. Checklist Chi tiết Công việc (Detailed Implementation Checklist)

### Phase 1: Data & Retrieval Optimization
- [ ] Xây dựng bộ dataset 50+ cases bằng `data/synthetic_gen.py`.
- [ ] Gắn Ground Truth IDs cho từng case để đánh giá Retrieval.
- [ ] Thiết kế ít nhất 5 cases "Red Teaming" (Input lắt léo, jailbreak, hoặc ngoài phạm vi kiến thức).
- [ ] Viết script tính toán **Hit Rate** và **MRR** cho Vector DB.

### Phase 2: Eval Engine & Performance
- [ ] Cấu hình ít nhất 2 model Judge (VD: 1 model to như GPT-4o và 1 model nhỏ hơn hoặc khác hãng).
- [ ] Triển khai logic tính **Agreement Rate** (độ đồng thuận giữa các Judge).
- [ ] Xây dựng hàm Async Runner để chạy song song toàn bộ pipeline.
- [ ] Tích hợp tính toán Cost (USD) và Token Usage cho mỗi lần chạy.
- [ ] Đảm bảo toàn bộ 50+ cases chạy xong trong **< 2 phút**.

### Phase 3: Regression & Analysis
- [ ] Thực hiện Benchmark lần 1 (V1) để lấy baseline.
- [ ] Cập nhật Agent (Prompting/Model) và chạy Benchmark lần 2 (V2).
- [ ] Hoàn thiện script **Delta Analysis** so sánh V1 và V2.
- [ ] Implement **Auto-Gate logic**: Chỉ cho phép release nếu V2 tốt hơn V1 (hoặc chi phí giảm mà chất lượng giữ nguyên).
- [ ] Thực hiện phân loại lỗi (Clustering) và viết báo cáo **5 Whys Analysis**.

### Phase 4: Finalization
- [ ] Chạy lệnh `python check_lab.py` để kiểm tra lỗi định dạng.
- [ ] Tổng hợp file `reports/summary.json` và `reports/benchmark_results.json`.
- [ ] Mọi thành viên hoàn thiện file Reflection cá nhân.
- [ ] Kiểm tra lại file `.gitignore` để chắc chắn không lộ API Key.

## 6. Danh mục nộp bài (Submission Checklist)
Cần kiểm tra kỹ các thành phần sau trước khi push:
- [ ] **Mã nguồn:** Đầy đủ các module trong `agent/`, `engine/`, `data/`.
- [ ] **Reports:** File `reports/summary.json` (phải chứa kết quả Regression) và `reports/benchmark_results.json`.
- [ ] **Analysis:** File `analysis/failure_analysis.md` đã điền đầy đủ thông tin.
- [ ] **Individual:** File Reflection của từng thành viên (`analysis/reflections/`).
- [ ] **Validation:** Chạy `python check_lab.py` và đảm bảo 100% Passed.

---
> [!IMPORTANT]
> **Lưu ý về bảo mật:** File `.env` chứa API Key tuyệt đối **KHÔNG** được push lên GitHub.
> 
> **Cảnh báo điểm liệt:** Theo **GRADING_RUBRIC.md**, nếu chỉ dùng 1 Judge duy nhất hoặc thiếu Metrics Retrieval, điểm nhóm sẽ bị **giới hạn ở mức 30/60 điểm**.
