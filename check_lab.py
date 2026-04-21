import os
import json
import sys

def check():
    print("🔍 [CHECK] Bắt đầu kiểm tra định dạng bài nộp Lab 14...")
    
    required_files = [
        "data/golden_set.jsonl",
        "reports/summary.json",
        "reports/benchmark_results.json",
        "analysis/failure_analysis.md",
        "main.py",
        "requirements.txt",
        ".env"
    ]
    
    missing = []
    for f in required_files:
        if not os.path.exists(f):
            if f == ".env":
                print("⚠️ [WARN] Thiếu .env (Đúng quy định, không được nộp key)")
            else:
                missing.append(f)
        else:
            print(f"✅ [OK] Tìm thấy {f}")
            
    # Validate JSON formats
    json_files = ["reports/summary.json", "reports/benchmark_results.json"]
    for jf in json_files:
        if os.path.exists(jf):
            try:
                with open(jf, "r") as f:
                    json.load(f)
                print(f"✅ [OK] JSON hợp lệ: {jf}")
            except Exception as e:
                print(f"❌ [FAIL] JSON lỗi tại {jf}: {e}")
                sys.exit(1)

    if missing:
        print("\n❌ [FAIL] Bài nộp thiếu các file sau:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)
    else:
        print("\n🚀 [SUCCESS] Bài nộp đã sẵn sàng 100%! Bạn có thể nén folder và nộp.")

if __name__ == "__main__":
    check()
