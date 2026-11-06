from pathlib import Path
import csv
import ollama

models = [
    "gemma4:e2b",
    "qwen2.5-coder:7b",
    "llama3.1:8b",
]

prompt = """
Forecast how the adoption of electric vehicles in Sweden might change over the next five years.
Clearly separate facts from assumptions. Identify the main factors that could speed up or slow down adoption and describe optimistic, middle, and pessimistic scenarios, and explain what evidence would change your prediction. Finally state which of the three scenarios you believe to be most likely and motivate why. Finish with a concise summary. You are free to speculate, but do not present it as certainty.
""".strip()

output_file = Path("model_responses.md")
csv_file = Path("model_responses.csv")

def seconds(ns):
    return ns / 1_000_000_000

print("LLM Model comparison: Three increasingly complex local ollama models, same prompt.")
print("---")
print("Prompt:")
print("---")
print(prompt)
print("---")

# Start a fresh output file for each run
with output_file.open("w", encoding="utf-8") as responses_file:
    responses_file.write("# Model responses\n\n")

    for i, model in enumerate(models, start=1):
        print(f"Now running local model {i}/{len(models)}: {model}")
        print("---")

        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )

            answer = response["message"]["content"]

            # also write to a CSV file
            with csv_file.open("a", encoding="utf-8", newline="") as f:
                csv.writer(f).writerow([model, answer])

            # write the model response to an output file, not to stdout (noise supression)
            responses_file.write(f"## Response {i}: {model}\n\n")
            responses_file.write(answer)
            responses_file.write("\n\n")
            responses_file.flush()

            # store usage metrics (these will be printed to stdout)
            metrics = []
            for key, label in [
                ("total_duration", "Total time"),
                ("load_duration", "Model load time"),
                ("prompt_eval_duration", "Prompt processing time"),
                ("eval_duration", "Generation time"),
            ]:
                value = response.get(key)
                if value is not None:
                    metrics.append(f"{label}: {seconds(value):.2f} s")

            prompt_tokens = response.get("prompt_eval_count")
            generated_tokens = response.get("eval_count")

            if prompt_tokens is not None:
                metrics.append(f"Prompt tokens: {prompt_tokens}")
            if generated_tokens is not None:
                metrics.append(f"Generated tokens: {generated_tokens}")

            generation_time = response.get("eval_duration")
            if generation_time and generated_tokens:
                speed = generated_tokens / seconds(generation_time)
                metrics.append(f"Generation speed: {speed:.2f} tokens/s")

            # report usage metrics to stdout
            print("Stats:")
            if metrics:
                for metric in metrics:
                    print(f"- {metric}")
            else:
                print("Usage metrics not returned.")

            print("---")

        except Exception as e:
            print(f"Error running model nr.{i} {model}: {e}")

print(f"\nRun complete. Responses saved to {output_file}")
