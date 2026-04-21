import json
import os
import random

def downsample(file_path: str, target_total: int = 50, target_hard: int = 15):
    if not os.path.exists(file_path):
        return

    cases = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                cases.append(json.loads(line))

    # Phân nhóm theo độ khó
    hard_cases = [c for c in cases if c.get("difficulty") == "hard"]
    other_cases = [c for c in cases if c.get("difficulty") != "hard"]

    print(f"[*] Original: {len(hard_cases)} hard, {len(other_cases)} other.")

    # Lấy 15 câu khó (vượt mức tối thiểu 10 câu bạn yêu cầu)
    final_hard = random.sample(hard_cases, min(len(hard_cases), target_hard))
    
    # Lấy số còn lại từ nhóm khác
    needed_others = target_total - len(final_hard)
    final_others = random.sample(other_cases, min(len(other_cases), needed_others))

    final_set = final_hard + final_others
    random.shuffle(final_set)

    # Lưu lại
    with open(file_path, "w", encoding="utf-8") as f:
        for case in final_set:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
            
    print(f"✅ Downsampled to {len(final_set)} cases (Hard: {len(final_hard)}, Others: {len(final_others)})")

if __name__ == "__main__":
    downsample("data/golden_set.jsonl")
