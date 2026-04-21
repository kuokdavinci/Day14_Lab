# 📝 LAB 14 CHECKLIST - AI EVALUATION FACTORY

Dưới đây là tiến độ hoàn thành bài Lab 14 dựa trên hướng dẫn của giáo viên và tiêu chuẩn Expert Level.

## 🏗️ PHASE 1 — DATASET (Quan trọng nhất)
- [x] **Bước 1: Chuẩn bị source data** (Đã có 3 văn bản: Policy, Security, IT Support).
- [x] **Bước 2: Chunk dữ liệu** (Đã phân mảnh dữ liệu với chunk_id và metadata đầy đủ).
- [x] **Bước 3: Thiết kế prompt tạo dataset** (Sử dụng `synthetic_gen.py` với cơ chế gợi ý Hard Cases).
- [x] **Bước 4: Dùng LLM tạo Golden Dataset** (Đã tạo 50 câu hỏi đa dạng: Easy, Medium, Hard).
- [x] **Bước 5: Manual Review Dataset** (Đã lọc trùng và bổ sung 10 câu hỏi "cực khó" về Prompt Injection và Finance).

## 🤖 PHASE 2 — AGENT VERSION
- [x] **Bước 6: Tạo Version 1** (Phiên bản `HELPFUL` - Dễ bị lừa, hay đoán mò).
- [x] **Bước 7: Tạo Version 2** (Phiên bản `STRICT` - Theo chuẩn Expert, an toàn, từ chối đúng chỗ).

## ⚖️ PHASE 3 — TRUST / JUDGE
- [x] **Bước 8: Tạo LLM Judge** (Triển khai Multi-model Judge: Qwen + GPT-4o-mini).
- [x] **Bước 9: Verify lại Judge** (Đã kiểm tra Agreement Rate đạt trên 94%, đảm bảo tính khách quan).

## 📊 PHASE 4 — BENCHMARK
- [x] **Bước 10: Chạy benchmark cho V1** (Lưu kết quả tại `reports/v1/`).
- [x] **Bước 11: Chạy benchmark cho V2** (Lưu kết quả tại `reports/v2/`).
- [x] **Bước 12: Tính metric** (Đầy đủ: Hit Rate, MRR, Quality, Tokens, Latency).

## 🔍 PHASE 5 — ANALYSIS
- [x] **Bước 13: Phân tích nguyên nhân** (Đã hoàn thiện file `analysis/failure_analysis.md` với kỹ thuật 5 Whys).

## 📜 PHASE 6 — REPORT
- [x] **Bước 14: Làm Final Report** (Đã có `reports/summary.json` và `FINAL_REPORT.md`).

---

### 🏁 TRẠNG THÁI CUỐI CÙNG (FINAL DELIVERABLE)
- [x] **Dataset (50 câu)**
- [x] **Agent V1 & V2 Logic**
- [x] **Multi-Model Judge Engine**
- [x] **Benchmark Results (JSON)**
- [x] **Final Report & Failure Analysis (Markdown)**

**KẾT LUẬN:** Bài làm đã sẵn sàng 100% để nộp và bảo vệ (Expert Level). 🚀🏁
