# 🎯 Task Breakdown: Evaluation Factory Setup

Dự án xây dựng hệ thống đánh giá AI Agent tự động sử dụng ChromaDB, Jina Reranker và Multi-Judge (GPT+Gemini).

## 📊 Overview
- **Project Type:** BACKEND / AI ENGINE
- **Primary Goal:** Đạt 100đ Lab 14 với hệ thống Evaluation chuyên nghiệp.
- **Key Modules:** SDG, Real RAG (Chroma), Multi-Judge, Regression Gate.

---

## 🚀 Task List

### Phase 1: Foundation & Data Preparation
| ID | Task | Agent | Skill | Dependency |
|---|---|---|---|---|
| T1.1 | Khởi tạo thư mục `data/source/` và 3 file chính sách mẫu (Markdown). | `project-planner` | `clean-code` | - |
| T1.2 | Migrate class `MarkdownLegalChunker` từ workspace `A20-App-036`. | `code-archaeologist` | `clean-code` | T1.1 |
| T1.3 | Hoàn thiện `data/synthetic_gen.py` tích hợp "Hard Cases" prompts. | `backend-specialist` | `python-patterns` | T1.2 |
| T1.4 | Chạy SDG để tạo ra file `data/golden_set.jsonl` (50+ cases). | `backend-specialist` | `behavioral-modes` | T1.3 |

### Phase 2: RAG Engine with ChromaDB & Jina
| ID | Task | Agent | Skill | Dependency |
|---|---|---|---|---|
| T2.1 | Thiết lập class `ChromaStore` hỗ trợ lưu trữ và truy vấn local. | `database-architect` | `database-design` | T1.2 |
| T2.2 | Viết script Ingestion nạp dữ liệu từ `data/source/` vào ChromaDB. | `backend-specialist` | `python-patterns` | T2.1 |
| T2.3 | Implement `LegalRetrievalEngine` tích hợp Jina Reranker. | `backend-specialist` | `api-patterns` | T2.2 |
| T2.4 | Kết nối Agent thực tế (`MainAgent`) với `LegalRetrievalEngine`. | `backend-specialist` | `python-patterns` | T2.3 |

### Phase 3: Evaluation & Multi-Judge Logic
| ID | Task | Agent | Skill | Dependency |
|---|---|---|---|---|
| T3.1 | Implement `ExpertEvaluator` tính toán Hit Rate và MRR thực tế. | `test-engineer` | `testing-patterns` | T2.3 |
| T3.2 | Xây dựng `MultiModelJudge` gọi song song OpenAI và Gemini. | `backend-specialist` | `api-patterns` | T1.4 |
| T3.3 | Implement logic tính **Agreement Rate** và **Cost Tracking**. | `test-engineer` | `testing-patterns` | T3.2 |

### Phase 4: Runner & Analysis
| ID | Task | Agent | Skill | Dependency |
|---|---|---|---|---|
| T4.1 | Hoàn thiện `main.py` với Async Runner và Automated Release Gate. | `devops-engineer` | `nodejs-best-practices` | T3.3 |
| T4.2 | Chạy Benchmark V1 vs V2 và tạo reports. | `orchestrator` | `behavioral-modes` | T4.1 |
| T4.3 | Thực hiện Failure Clustering và hoàn thiện `failure_analysis.md`. | `debugger` | `systematic-debugging` | T4.2 |

---

## ✅ Phase X: Final Verification
- [ ] Chạy `python check_lab.py` PASS 100%.
- [ ] So sánh V1/V2 có kết quả Delta rõ ràng.
- [ ] Pipeline 50 cases chạy dưới 120 giây.
- [ ] Không lộ API Key trong repo.
