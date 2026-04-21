import json
import asyncio
import os
from tqdm import tqdm
from agent.main_agent import MainAgent
from engine.judge import MultiModelJudge
from engine.evaluator import ExpertEvaluator
import litellm
import os
from dotenv import load_dotenv

load_dotenv()
# os.environ['LITELLM_LOG'] = 'DEBUG' # Bật lại nếu muốn soi kỹ
litellm.set_verbose = False # Tắt bớt spam để tập trung vào progress bar

async def run_benchmark():
    # 1. Setup
    agent = MainAgent()
    judge = MultiModelJudge()
    evaluator = ExpertEvaluator()
    
    # 2. Load Golden Set
    test_cases = []
    with open("data/golden_set.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                test_cases.append(json.loads(line))
    
    print(f"🚀 Starting Benchmark for {len(test_cases)} cases...")
    
    results = []
    eval_results = []
    
    # 3. Process in Batches
    batch_size = 5
    batch_delay = 45 # s (Hơi mạo hiểm nhưng để nhanh hơn 60s)
    
    print(f"🚀 Processing {len(test_cases)} cases in batches of {batch_size}...")
    pbar = tqdm(total=len(test_cases), desc="Evaluating")
    
    async def process_case(case):
        # Step A: Agent Query
        agent_resp = await agent.query(case["question"])
        
        # Step B: Judge Evaluation
        eval_resp = await judge.evaluate(
            question=case["question"],
            expected=case["expected_answer"],
            agent_ans=agent_resp["answer"],
            context="\n".join(agent_resp["contexts"])
        )
        
        return {
            "question": case["question"],
            "expected": case["expected_answer"],
            "agent_answer": agent_resp["answer"],
            "agent_metadata": agent_resp["metadata"],
            "eval": eval_resp,
            "category": case["metadata"].get("category", "unknown"),
            "gt_source": case["metadata"].get("source_id"),
            "retrieved_metadata": agent_resp.get("retrieved_metadata", [])
        }

    for i in range(0, len(test_cases), batch_size):
        batch = test_cases[i:i + batch_size]
        # Chạy song song cả batch
        batch_tasks = [process_case(case) for case in batch]
        batch_results = await asyncio.gather(*batch_tasks)
        
        for res in batch_results:
            results.append(res)
            eval_results.append(res["eval"])
            pbar.update(1)
            
        # Nếu chưa phải batch cuối, nghỉ để reset TPM
        if i + batch_size < len(test_cases):
            await asyncio.sleep(batch_delay)
            
    pbar.close()

    # 4. Calculate Final Metrics
    retrieval_stats = evaluator.calculate_retrieval_metrics(test_cases, results)
    quality_stats = evaluator.calculate_quality_metrics(eval_results)
    
    # 5. Summary Report
    summary = {
        "project": "Lab 14: AI Evaluation Factory",
        "total_cases": len(test_cases),
        "metrics": {
            "retrieval": retrieval_stats,
            "quality": quality_stats
        },
        "details": results
    }
    
    # Identify Failures (Score < 5)
    failures = [r for r in results if r["eval"]["final_score"] < 5]
    summary["failure_count"] = len(failures)
    
    with open("benchmark_report.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print("\n" + "="*40)
    print("🏆 BENCHMARK COMPLETE!")
    print(f"📊 Hit Rate: {retrieval_stats['hit_rate']*100}%")
    print(f"📉 MRR (Mean Reciprocal Rank): {retrieval_stats['mrr']}")
    print(f"🎯 Avg Quality Score: {quality_stats['avg_quality_score']}/10")
    print(f"🤝 Agreement Rate: {quality_stats['agreement_rate']*100}%")
    print(f"❌ Failures: {len(failures)}")
    print("="*40)
    print("Chi tiết báo cáo lưu tại: benchmark_report.json")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
