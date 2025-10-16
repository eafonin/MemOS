---
source_url: https://memos-docs.openmem.net/overview/quick_start/mem_recall
section: Overview
scraped_date: 2025-10-16
title: Memory Recall and Instruction Completion
has_images: yes
has_tables: yes
---

# Memory Recall and Instruction Completion
 [ In MemOS, memory is not just about archiving information, but also about being dynamically retrieved when needed and transformed into executable input. This process is achieved through two closely connected steps: Memory Recall and Instruction Completion. 
## 1. Capability Overview
 
### 1.1 Memory Recall
 
[Memory recall is responsible for quickly retrieving the most relevant memory fragments when the user initiates a new request.]
 
- [**Role**: Ensures that the model does not start âfrom scratchâ when generating responses, but instead integrates the user's history, preferences, and context.]
- [**Returned Results**: The recalled content is presented as plaintext facts.Traceable: Each memory is accompanied by its source, timestamp, and confidence level.Highly controllable: Developers have full control over which memories enter downstream logic.]
 
 
### 1.2 Instruction Completion (Coming Soon)
 
[It is important to note that âfactsâ are not the same as âinstructions.â If developers only obtain plaintext memory, they must write additional rules to translate this information into prompts that large models can directly execute.] **The role of instruction completion** is to automatically generate instructions of different granularity based on recall results. - [**In most systems, developers can only get âmemory factsâ and then manually piece together prompts. This leads to several challenges:**Task awareness: The same memory may require different phrasing under different tasks;Personalization: User style and habits need to be instantly supplemented;Dynamic optimization: Different models require different optimal prompt formulations;Efficient compression: Redundancy must be removed to reduce token consumption.]
 
 
- [**MemOS instruction completion helps developers cover this âlast mileâ:**Saves the cost of rules assembly and tuning;Ensures that recalled memories are effectively utilized;Provides three modes: matches / instruction / full_instruction, to meet different levels of control needs.Memory facts (matches): Recall relevant memories for the current query.Semi-finished instruction (instruction): Combine recalled memories with the userâs current question to form a basic prompt, upon which developers can add business logic.Full instruction (full_instruction): Based on the semi-finished version, integrate context, preferences, compliance constraints, etc., to generate a terminal prompt directly executable by the model.] Instruction completion works through both **offline chain** and **real-time chain** . <table><thead><tr><th>Chain</th><th>Description</th></tr></thead><tbody><tr><td>Offline Chain (Accumulation &amp; Preparation)</td><td>Extract user preferences to form a profile.Build a few-shot sample library.Solidify long-term rules such as brand, compliance, and style.</td></tr><tr><td>Real-time Chain (Dynamic Decision)</td><td>Select which memories and templates to activate based on task intent.Resolve conflicts (e.g., âlikes poetic openingsâ vs. ârequires concisenessâ).Perform compression and degradation based on token budget and model characteristics.</td></tr></tbody></table>
 
 
## 2. Example (Try after instruction completion is launched) â Personalized Tutoring in AI Education
 
### 2.1 Historical Dialogue Input (Raw Material)
 
```
2025-06-10
 Student: Hello teacher, my name is Xiao Ming, I am in 9th grade 
 Teacher: Hello Xiao Ming, nice to meet you
 â¦â¦

2025-08-01
 Student: Teacher, I really canât solve this problem, can you explain more clearly? 
 Teacher: Sure, I will explain step by step. 
 â¦â¦

2025-09-03
 â¦â¦
 Student: You just explained too long, I couldnât keep up. Can you make it simpler? 
 Teacher: Okay, Iâll tell you in a simpler way.
 â¦â¦

2025-10-09
 Student: I still canât distinguish between linear and quadratic functionsâ¦ 
 Teacher: The graph of a linear function is a straight line, while a quadratic function is a parabola. You need to remember this difference.
 â¦â¦

```
 
 
### 2.2 MemOS Instruction Preference Modeling (Offline Chain)
 
- [**Preference Extraction**Likes step-by-step explanations (from âcan you explain step by stepâ).Prefers concise answers (from âyou just explained too longâ).Easily confuses similar concepts (from âI still canât distinguish between linear and quadratic functionsâ).]
- [**Few-shot Selection**: Pick dialogues with step-by-step, concise explanations, and concept clarification.]
- [**Strategy Summary**: Summarized as âstep-by-step + concise + clarify common confusionsâ.]
 
```
user_teaching_template_u123:
 audience: "9th grade student"
 task: "Solve math problems"
 structure:
 - "Step-by-step explanation (3â4 steps)"
 - "Correct confusion between linear and quadratic functions when necessary"
 constraints:
 - "Keep explanations concise, not too long"
 - "Highlight key points, avoid lengthy formula derivations"

fewshot_examples_u123:
 - id: "fs-step-01"
 user: "Teacher, I really canât solve this problem, can you explain more clearly?"
 assistant: "Sure, I will explain step by stepâ¦"
 tag: "Step-by-step explanation"

 - id: "fs-brief-02"
 user: "You just explained too long, I couldnât keep up. Can you make it simpler?"
 assistant: "Okay, Iâll tell you in a simpler wayâ¦"
 tag: "Concise expression"

 - id: "fs-contrast-03"
 user: "I still canât distinguish between linear and quadratic functionsâ¦"
 assistant: "The graph of a linear function is a straight line, while a quadratic function is a parabola. You need to remember this differenceâ¦"
 tag: "Concept clarification"

```
 
 
### 2.3 Real-time Chain (Instruction Completion) User query: Teacher, can you teach me how to solve this problem? 2xÂ² - 3x - 5 = 0 - [**Recalled matches:** Only returns facts, unprocessed. Developers need to piece together the prompt and decide how to guide the student.]
 
```
matches:
 - value: "9th grade student"
 score: 0.95
 source: "Dialogue record#2025-06-10"
 
 - value: "Prefers step-by-step explanations"
 score: 0.94
 source: "Dialogue record#2025-08-01"
 
 - value: "Likes concise explanations"
 score: 0.92
 source: "Dialogue record#2025-09-03"
 
 - value: "Confuses linear and quadratic functions"
 score: 0.90
 source: "Dialogue record#2025-10-09"

user_query: "Teacher, can you teach me how to solve this problem? 2xÂ² - 3x - 5 = 0"

```
 
 
- [**Semi-finished instruction:** Translate facts into structured requirements: task / audience / steps / constraints]
 
```
instruction: |
 Task: Help student solve a quadratic equation problem 
 Audience: 9th grade student 
 Requirements: 
 - Explain in 3â4 steps 
 - Correct common confusion between linear/quadratic functions during explanation 
 - Keep it concise, avoid lengthy derivations 
 Note: If the question is incomplete, please ask for clarification first

user_query: "Teacher, can you teach me how to solve this problem? 2xÂ² - 3x - 5 = 0"

```
 
 
- [**Full instruction:** Further refined from the semi-finished versionConvert âoften confusesâ into explicit teaching action (must emphasize difference between quadratic and linear functions during explanation).Translate âprefers step-by-step explanationsâ into a clear problem-solving method (use step-by-step explanation).Rewrite â9th grade studentâ into the teaching role relationship (you are the math teacher of a 9th grade student).Select few-shot examples from historical dialogue and include them in the final instruction to help the model learn explanation and clarification patterns.]
 
> Semi-finished instructions are more structured for developer customization; full instructions are closer to natural language and directly executable by models.
 
```
final_prompt_to_model:
 - role: system
 content: |
 You are the math teacher of a 9th grade student. 
 The student often confuses linear and quadratic functions, and prefers concise, step-by-step explanations. 
 Please follow the style of the following historical examples: 

 [Example 1] 
 Student: Teacher, I really canât solve this problem, can you explain more clearly? 
 Teacher: Sure, I will explain step by step. 

 [Example 2] 
 Student: You just explained too long, I couldnât keep up. Can you make it simpler? 
 Teacher: Okay, Iâll tell you in a simpler way. 

 [Example 3] 
 Student: I still canât distinguish between linear and quadratic functionsâ¦ 
 Teacher: The graph of a linear function is a straight line, while a quadratic function is a parabola. You need to remember this difference. 

 Now please answer the studentâs question: âSolve 2xÂ² - 3x - 5 = 0.â 
 Requirements: 
 - Solve the problem step-by-step (3â4 steps); 
 - Point out the difference between linear and quadratic functions during the explanation; 
 - Keep the answer concise and clear, avoid lengthy derivations; 
 - If the problem statement is incomplete, please ask for clarification first.
 - role: user
 content: "Teacher, can you teach me how to solve this problem? 2xÂ² - 3x - 5 = 0"

```
 
> Case Summary: In the â9th grade student solving quadratic equationâ scenario, instruction completion provides the following benefits over returning raw memory only:
 
- [**From facts to executable**Raw memory only has âstudent often confuses linear and quadratic functions,â developers must convert this into a teaching action.Instruction completion directly generates âmust emphasize the key difference during explanation,â avoiding extra developer rules.]
- [**Context integration**Raw memory is fragmented; developers must decide how to place them into prompts.Instruction completion automatically merges memories with the user query into a coherent task description for direct model use.]
- [**Optimization and pruning**If developers directly concatenate memories, the result is often redundant or conflicting.Instruction completion compresses into concise step-by-step requirements, reducing token consumption and improving focus.]
- [**Robustness assurance**If developers only get memories, they must consider âwhat if the question is incomplete.âInstruction completion includes clarification strategies, making outputs more robust without reinventing the wheel.]
 
 
## 3. Advanced: Deep Customization
 
[In MemOS, recall and completion are not achieved through a single path, but through combinations of multiple strategies and components. Different scenarios may require different configurations. This section lists the main steps and customizable points for you to flexibly choose according to business needs.]
 
<table><thead><tr><th>Layer</th><th>Customizable Points</th><th>Example</th></tr></thead><tbody><tr><td>Memory Recall</td><td>Adjust recall strategy</td><td>Raise similarity threshold to only return memories with confidence â¥0.9</td></tr><tr><td></td><td>Set filters</td><td>Only retrieve the last 30 days of conversations; only preference memories, not factual ones</td></tr><tr><td>Semi-finished Instructioninstruction</td><td>Extend structured fields</td><td>Add extra fields such as âOutput format: Markdownâ, âMust include: Safety reminderâ</td></tr><tr><td></td><td>Custom concatenation template</td><td>Replace default concatenation logic to generate semi-finished instructions with brand tone</td></tr><tr><td>Full Instructionfull_instruction</td><td>Few-shot strategy</td><td>Replace default historical messages with your own example library, fix to 2 examples each time</td></tr><tr><td></td><td>Role and tone control</td><td>Force setting to âFinancial Advisorâ, output style as âformal professionalâ</td></tr><tr><td></td><td>Token cost optimization</td><td>Define compression rules: keep core preferences, prune redundant background information</td></tr><tr><td></td><td>Multi-model adaptation</td><td>For GPT output with LaTeX, for LLaMA output plain text, auto-switch</td></tr><tr><td>Output Governance &amp; Audit</td><td>Compliance fallback</td><td>Automatically prepend âAnswer must comply with regulationsâ before completion</td></tr><tr><td></td><td>Logging &amp; traceability</td><td>Record used memories and few-shot selection each call</td></tr><tr><td></td><td>A/B testing</td><td>Run two concatenation templates simultaneously, compare user satisfaction differences</td></tr></tbody></table>
 
 
## 4. Next Steps
 
[Learn more about MemOS core capabilities:]
 
- [[Memory Lifecycle Management](/overview/quick_start/mem_lifecycle)]
