### TL/DR

Check the folder `example_output` to view the output artifacts from a complete run.

### Purpose

This python script tests three different local `ollama` LLM models:

```bash
ollama list
NAME                SIZE
gemma4:e2b          4.6 GB
qwen2.5-coder:7b    4.7 GB
llama3.1:8b         4.9 GB
```

All models receive the same prompt. Usage statistics is reported and the responses for each model are persisted to a output files (`model_responses.md`, `model_reponses.csv`).

The study is not intended as a rigorous benchmark but rather a *quick-and-dirty test of local LLM model performance*. For a more serious benchmark, increase the number of model runs and aggregate the statistics. 

### What to expect

Even a single run should indicate that:

- prompt processing time increases with model complexity
- generation speed decreases with model complexity
- prompt tokens differ

The first two observations make sense intuitively, and the models also handle token processing differently.

---

### Usage (Linux/BSD/Mac):

```python
# enter the directory
cd assignment_1 

# install required packages
python -m pip install -r requirements.txt

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

### Evaluation

The prompt given to the models was:

```
Forecast how the adoption of electric vehicles in Sweden might change over the next five years.

Clearly separate facts from assumptions.

Identify the main factors that could speed up or slow down adoption and describe optimistic, middle, and pessimistic scenarios, and explain what evidence would change your prediction.

Finally state which of the three scenarios you believe to be most likely and motivate why. 

Finish with a concise summary.

You are free to speculate, but do not present it as certainty.

```

#### Were the models correct?

This is actually unknowable. The ground truth will not be available until five years from now.

#### How does this compare to commercial models?

This question is interesting and deserves a separate study. Because the model responses involve a large degree of reasoning, metrics would need to be designed carefully to define what constitutes a good model. Performance-wise the local models could be anticipated to be slower and less accurate than commercial models, due to local hardware limitations and much less training.

---

### Ideas for future versions:

- Increase runs per model. This is necessary to carry out statistical evaluation.

- Let an independent local model review the responses and score them based on prompt-adherence, factual correctness and degree of referenced statements. Build two summary response models: `political` (consensus-based) and `research` (competitive/ensemble-based).

- Add commercial models to the benchmarks

---