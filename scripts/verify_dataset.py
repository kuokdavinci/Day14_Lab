import json
import os
from collections import Counter

def verify_dataset(file_path: str):
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} không tồn tại.")
        return

    cases = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                cases.append(json.loads(line))

    total = len(cases)
    print(f"\n===== 📊 BÁO CÁO KIỂM TRA GOLDEN DATASET =====")
    print(f"Total Cases: {total}")
    
    # 1. Kiểm tra số lượng
    if total >= 50:
        print("✅ Số lượng: ĐẠT (>= 50 cases)")
    else:
        print(f"❌ Số lượng: KHÔNG ĐẠT (Cần ít nhất 50, hiện có {total})")

    # 2. Kiểm tra danh mục
    categories = Counter(c["metadata"].get("category") for c in cases)
    print(f"\nPhân bổ Category:")
    for cat, count in categories.items():
        percent = (count / total) * 100
        print(f" - {cat}: {count} ({percent:.1f}%)")
    
    required_cats = {"fact-checking", "adversarial", "out-of-context"}
    missing_cats = required_cats - set(categories.keys())
    if not missing_cats:
        print("✅ Loại câu hỏi: ĐẠT (Có đủ Fact-checking, Adversarial, Out-of-context)")
    else:
        print(f"❌ Loại câu hỏi: THIẾU ({', '.join(missing_cats)})")

    # 3. Kiểm tra Ground Truth & Metadata
    missing_gt = 0
    missing_source = 0
    for c in cases:
        if not c.get("expected_answer") or not c.get("context"):
            missing_gt += 1
        if not c["metadata"].get("source_id"):
            missing_source += 1
    
    if missing_gt == 0:
        print("✅ Ground Truth: ĐẠT (100% có expected_answer và context)")
    else:
        print(f"❌ Ground Truth: KHÔNG ĐẠT (Có {missing_gt} cases thiếu info)")

    if missing_source == 0:
        print("✅ Mapping Source: ĐẠT (100% có source_id để tính Hit Rate)")
    else:
        print(f"❌ Mapping Source: KHÔNG ĐẠT (Có {missing_source} cases thiếu source_id)")

    # 4. Kiểm tra độ khó
    difficulties = Counter(c.get("difficulty") for c in cases)
    print(f"\nĐộ khó: {dict(difficulties)}")

    print(f"\n==============================================")

if __name__ == "__main__":
    verify_dataset("data/golden_set.jsonl")
