import json
import os

def cleanup_dataset(file_path: str):
    if not os.path.exists(file_path):
        return

    all_standardized_cases = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            try:
                data = json.loads(line)
                
                # Trường hợp 1: Dữ liệu bị bọc trong list "questions"
                if "questions" in data and isinstance(data["questions"], list):
                    for q in data["questions"]:
                        case = {
                            "question": q.get("question"),
                            "expected_answer": q.get("expected_answer"),
                            "type": q.get("type", data.get("metadata", {}).get("category", "unknown")),
                            "difficulty": q.get("difficulty", "medium"),
                            "context": data.get("context"),
                            "metadata": data.get("metadata", {})
                        }
                        if case["question"] and case["expected_answer"]:
                            all_standardized_cases.append(case)
                
                # Trường hợp 2: Dữ liệu đã phẳng {"question": "..."}
                elif "question" in data:
                    # Đảm bảo có metadata
                    if "metadata" not in data:
                        data["metadata"] = {}
                    all_standardized_cases.append(data)
            except:
                continue

    # Lưu lại file sạch
    with open(file_path, "w", encoding="utf-8") as f:
        for case in all_standardized_cases:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
            
    print(f"✅ Cleaned up dataset. New total: {len(all_standardized_cases)} valid cases.")

if __name__ == "__main__":
    cleanup_dataset("data/golden_set.jsonl")
