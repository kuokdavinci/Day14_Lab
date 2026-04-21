from typing import List, Dict

class ExpertEvaluator:
    def __init__(self):
        pass

    def calculate_retrieval_metrics(self, test_cases: List[Dict], results: List[Dict]) -> Dict:
        """
        Tính Hit Rate và MRR
        Hit: Nếu source_id của ground truth nằm trong danh sách contexts tìm được.
        """
        hits = 0
        mrr_score = 0
        total = len(test_cases)
        
        for i in range(total):
            gt_source = test_cases[i]["metadata"].get("source_id")
            retrieved_sources = results[i].get("agent_metadata", {}).get("sources", [])
            
            # Hit Rate
            if gt_source in retrieved_sources:
                hits += 1
                
                # MRR: Reciprocal Rank
                # Giả sử chúng ta lấy index từ metadata trả về
                # Ở đây chúng ta tạm dùng check trong metadata.retrieved_metadata
                retrieved_metadata = results[i].get("retrieved_metadata", [])
                for rank, meta in enumerate(retrieved_metadata):
                    if meta.get("source_id") == gt_source:
                        mrr_score += 1 / (rank + 1)
                        break
        
        return {
            "hit_rate": round(hits / total, 4) if total > 0 else 0,
            "mrr": round(mrr_score / total, 4) if total > 0 else 0,
            "total_samples": total
        }

    def calculate_quality_metrics(self, evaluation_results: List[Dict]) -> Dict:
        """
        Tính điểm trung bình và Agreement Rate
        """
        total_score = 0
        agreed_count = 0
        total = len(evaluation_results)
        
        if total == 0: return {}

        for res in evaluation_results:
            total_score += res["final_score"]
            if res["is_agreed"]:
                agreed_count += 1
        
        return {
            "avg_quality_score": round(total_score / total, 2),
            "agreement_rate": round(agreed_count / total, 4),
            "total_evaluated": total
        }
