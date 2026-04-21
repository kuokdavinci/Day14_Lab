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
    batch_size = 50 
    batch_delay = 0 # s (Mức an toàn để tránh Rate Limit cho Qwen/DashScope)
    
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

    # --- EXPERT RELEASE GATE LOGIC ---
    # Ngưỡng chất lượng (Thresholds)
    MIN_QUALITY = 8.5
    MIN_HIT_RATE = 0.9
    MAX_FAILURES = 0
    
    is_passed = (
        quality_stats['avg_quality_score'] >= MIN_QUALITY and 
        retrieval_stats['hit_rate'] >= MIN_HIT_RATE and
        len(failures) <= MAX_FAILURES
    )
    
    summary["gate_status"] = "PASSED" if is_passed else "FAILED"
    summary["release_recommendation"] = "🚀 READY FOR PRODUCTION" if is_passed else "🛑 ROLLBACK: Quality below threshold"
    summary["thresholds"] = {
        "min_quality": MIN_QUALITY,
        "min_hit_rate": MIN_HIT_RATE,
        "max_failures": MAX_FAILURES
    }
    
    # Ensure reports directory exists for the current version
    version = os.getenv("BENCHMARK_VERSION", "v2")
    output_dir = f"reports/{version}"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    # Standard summary for check_lab script (Expert Version)
    summary_short = {
        "hit_rate": retrieval_stats['hit_rate'],
        "mrr": retrieval_stats['mrr'],
        "avg_quality_score": quality_stats['avg_quality_score'],
        "agreement_rate": quality_stats['agreement_rate'],
        "failures": len(failures),
        "total_tokens": sum(r["agent_metadata"].get("tokens_used", 0) for r in results),
        "total_latency_sec": sum(r["agent_metadata"].get("latency_sec", 0) for r in results),
        "gate_status": summary["gate_status"],
        "recommendation": summary["release_recommendation"]
    }
    with open(f"{output_dir}/summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_short, f, indent=2, ensure_ascii=False)
        
    print("\n" + "="*40)
    print("🏆 BENCHMARK COMPLETE!")
    print(f"📊 Hit Rate: {retrieval_stats['hit_rate']*100}%")
    print(f"📉 MRR: {retrieval_stats['mrr']}")
    print(f"🎯 Avg Quality: {quality_stats['avg_quality_score']}/10")
    print(f"🤝 Agreement: {quality_stats['agreement_rate']*100}%")
    print(f"❌ Failures: {len(failures)}")
    print("-" * 40)
    if is_passed:
        print("✅ RELEASE GATE: PASSED")
        print("🚀 RECOMMENDATION: READY FOR PRODUCTION")
    else:
        print("❌ RELEASE GATE: FAILED")
        print("🛑 RECOMMENDATION: ROLLBACK & RE-TUNE PROMPT")
    print("="*40)
    print(f"✅ Báo cáo chi tiết: {output_dir}/benchmark_results.json")
    print(f"✅ Bản tóm tắt: {output_dir}/summary.json")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
