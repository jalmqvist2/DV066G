### TL/DR

Check to folder `example_output` to view the output artifacts from a complete run.

### Purpose

This python script tests three different local `ollama` LLM models:

```bash
ollama list
NAME                SIZE
gemma4:e2b          4.6 GB
qwen2.5-coder:7b    4.7 GB
llama3.1:8b         4.9 GB
```

All models receive the same prompt. Usage statistics is reported and the responses for each model are persisted to an output file (`model_responses.md`).

It is not intended to be a rigorous benchmark but rather a *quick-and-dirty test of local LLM model performance*. For a more serious benchmark, increase the number of model runs and aggregate the statistics. 

### What to expect

Even a single run should indicate that:

- prompt processing time increases with model complexity
- generation speed decreases with model complexity
- prompt tokens differ

The first two observations make sense intuitively, and the models also handle token processing differently.

---

### Usage (Linux/BSD/Mac):

```python
# launch the script
python -u test.py > test.log 2>&1 &

# view the model statistcs
tail -f test.log

# read the responses produced by the models
cat model_responses.md | more
```

---

### Example run

On my humble local workstation (6 GB nvidia card, 8 i7 cores, 32 GB RAM) total time ranges from 30-60 seconds per model. Generated tokens / Total time decrease as model complexity increases, generation speed increases.

For the smaller model `gemma4:e2b` my GPU VRAM suffices:

```bash
ollama ps
NAME          ID              SIZE      PROCESSOR    CONTEXT    RUNNER      UNTIL              
gemma4:e2b    b37049369adf    224 MB    100% GPU     4096       llamacpp    4 minutes from now    
```

 But for the largest model `llama3.1:8b`, requiring 8 GB of VRAM, the CPU and RAM has to contribute:

```bash
ollama ps
NAME           ID              SIZE      PROCESSOR          CONTEXT    RUNNER      UNTIL              
llama3.1:8b    46e0c10c039e    5.6 GB    14%/86% CPU/GPU    4096       llamacpp    4 minutes from now    
```

---

### Ideas for future versions:

- Increase runs per model

- Let an independent local model review the responses and score them based on prompt-adherence, factual correctness and degree of referenced statements. Build two summary response models: `political` (consensus-based) and `research` (competitive/ensemble-based).

---