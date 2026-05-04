import yaml
import json
import os
from llms import LLMs
from datetime import datetime


def run_benchmark(benchmark_path, config_path):
    # 1. Load config
    llms = LLMs()
    with open(config_path, 'r') as f:
        conf = yaml.safe_load(f)

    model_name = conf['llm']['model']

    if "deepseek" in model_name:
        api_key = conf["api_keys"]["deepseek"]
    elif "gpt" in model_name:
        api_key = conf["api_keys"]["gpt"]
    elif model_name == "gemini":
        api_key = conf["api_keys"]["gemini"]
    elif "claude" in model_name:
        api_key = conf["api_keys"]["claude"]
    else:
        raise ValueError("Unsupported model")

    # 2. Load benchmark
    with open(benchmark_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_results = []

    # 3. Loop over multiple benchmarks (topics)
    for benchmark in data.get('topics', []):
        print(f"\n=== Running benchmark: {benchmark['id']} ({benchmark['topic']}) ===")

        topic_results = {
            "topic_id": benchmark["id"],
            "topic": benchmark["topic"],
            "results": []
        }

        # Loop over paragraphs inside each topic
        for p in benchmark.get('paragraphs', []):
            print(f"\nPrompt: {p['prompt']}")

            # Step A: Generate story
            if "deepseek" in model_name:
                story_answer = llms.deepseek(p['prompt'], model_name, api_key)
            elif model_name == "gemini":
                story_answer = llms.gemini(p['prompt'], "gemini-2.0-flash", api_key)
            elif "gpt" in model_name:
                story_answer = llms.chatgpt(p['prompt'], model_name, api_key)
            elif "claude" in model_name:
                story_answer = llms.claude(p['prompt'], model_name, api_key)
            paragraph_results = {
                "idx": p['idx'],
                "title": p.get("title"),
                "original_prompt": p['prompt'],
                "llm_story": story_answer,
                "validation_results": []
            }

            # Step B: Validation questions
            for v_q in p.get('validation_questions', []):
                validation_prompt = f"Story: {story_answer}\n\nQuestion: {v_q['text']}"

                if "deepseek" in model_name:
                    v_answer = llms.deepseek(validation_prompt, model_name, api_key)
                elif model_name == "gemini":
                    v_answer = llms.gemini(validation_prompt, "gemini-2.5-flash-lite", api_key)
                elif  "claude" in model_name:
                    v_answer = llms.claude(validation_prompt, model_name, api_key)
                elif "gpt" in model_name:
                    v_answer = llms.chatgpt(validation_prompt, model_name, api_key)

                paragraph_results["validation_results"].append({
                    "q_id": v_q['id'],
                    "question": v_q['text'],
                    "answer": v_answer
                })

            topic_results["results"].append(paragraph_results)

        all_results.append(topic_results)

    # 4. Output handling
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_model_name = model_name.replace('-', '_')
    output_filename = f"results_{clean_model_name}_{timestamp}.json"
    full_path = os.path.join(output_dir, output_filename)

    output_payload = {
        "model_used": model_name,
        "results": all_results
    }

    with open(full_path, 'w') as f:
        json.dump(output_payload, f, indent=2)

    print(f"\n✅ Success! Results written to {full_path}")


if __name__ == "__main__":
    run_benchmark('benchmark.json', 'conf.yaml')
