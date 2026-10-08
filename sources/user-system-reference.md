# Auto Research × Self-improving Model：从技术闭环到产品系统

## 导读：这两个方向为什么其实是一件事

Auto Research 和 Self-improving Model 表面上是两个不同问题。

Auto Research 研究的是：

> 如何让 AI 像一个研究员一样，自主提出假设、设计实验、执行实验、分析结果，并不断推进研究。

Self-improving Model 研究的是：

> 如何让 AI 系统利用数据、反馈、实验或者自身产生的经验，使下一代 AI 比当前版本更强。

但如果把时间尺度拉长，两者实际上会逐渐汇合。

因为一旦 AI 能够自主完成研究，那么一个非常自然的研究课题就是：

> **如何制造一个更好的 AI？**

于是整个系统就会形成：

```text
当前 AI
   ↓
开展 AI Research
   ↓
发现更好的训练方法 / 数据 / Agent / 架构
   ↓
训练或构造新的 AI
   ↓
得到更强 AI
   ↓
更强 AI 开展更好的 AI Research
   ↓
继续迭代
```

这就是为什么像超衍这样的团队，会同时强调：

* Auto Research
* Autonomous Scientist
* Self-evolving Foundation Model

它们本质上属于一条技术路线的不同阶段。

---

# 第一章：从 Auto Research 到 Self-improvement，完整闭环是怎么形成的

## 1. Auto Research 最重要的变化：AI 不再只是“回答问题”

传统 LLM 产品基本遵循：

```text
用户提出问题
    ↓
模型推理
    ↓
输出答案
```

Deep Research 已经复杂了一步：

```text
问题
 ↓
搜索资料
 ↓
阅读
 ↓
比较
 ↓
综合
 ↓
输出报告
```

但 Deep Research 仍然存在一个非常重要的限制：

> **它主要从已经存在的信息中寻找答案。**

例如：

“Transformer 为什么有效？”

AI 可以：

* 搜论文
* 找实验结果
* 比较观点
* 最后综合答案

但是 Auto Research 面对的问题可能是：

> “能不能找到一个比现有 attention 更适合某类任务的方法？”

这个问题的答案可能根本还不存在。

AI 必须：

1. 提出新的 hypothesis；
2. 写代码；
3. 做实验；
4. 观察结果；
5. 发现假设不成立；
6. 提出新假设；
7. 再做实验。

因此 Auto Research 真正的跃迁是：

> 从 **Knowledge Retrieval**
> 变成 **Knowledge Creation**。

---

# 2. Auto Research 的最小闭环

把所有复杂细节拿掉以后，Auto Research 可以被抽象成五个步骤：

```text
Generate
   ↓
Execute
   ↓
Evaluate
   ↓
Select
   ↓
Iterate
```

也可以用科研语言表示：

```text
Hypothesis
   ↓
Experiment
   ↓
Evidence
   ↓
Conclusion
   ↓
Next Hypothesis
```

这五步里，每一步都有完全不同的技术问题。

---

## 2.1 Generate：提出值得尝试的方向

这一阶段不仅仅是“脑暴几个 Idea”。

一个好的 Research Agent 必须知道：

* 当前已经知道什么；
* 哪些方向已经失败；
* 哪些问题最值得解决；
* 哪个实验的信息增益最高；
* 哪种假设既新颖又可以验证。

因此 Generate 实际包含：

```text
Research Memory
+
Literature
+
Current Results
+
Search Strategy
↓
Next Hypothesis
```

---

## 2.2 Execute：真正让世界给你反馈

这是 Auto Research 和普通 Chat Agent 最大的区别之一。

Research Agent 不能永远停留在 language space。

它必须进入环境。

例如：

```text
写 Python
运行代码
训练模型
修改参数
调用 GPU
读取日志
分析数据
调用 simulator
```

所以 Research Agent 必然需要：

> Runtime + Sandbox + Tool System

如果没有 Environment：

AI 能做的仍然只是：

> “我觉得这个想法可能有效。”

有了 Environment：

它才能变成：

> “我跑了 12 个实验，其中 Experiment #7 在相同计算预算下提高了 4.3%。”

这两个东西的可信度完全不同。

---

# 3. Karpathy autoresearch：为什么一个很小的 repo 能把这件事讲得很清楚

Karpathy 2026 年发布的 `autoresearch` 是一个特别适合理解这个闭环的项目。

它故意把系统压缩得非常简单：

```text
prepare.py
train.py
program.md
```

其中：

* `prepare.py`：固定环境和评估；
* `train.py`：Agent 可以修改的研究对象；
* `program.md`：告诉 Agent 如何进行研究。

Agent 会：

```text
读取当前代码
 ↓
提出 modification
 ↓
修改 train.py
 ↓
训练 5 分钟
 ↓
测 val_bpb
 ↓
如果更好 → 保留
如果更差 → 回滚
 ↓
提出下一个 idea
```

官方 README 明确设计为固定 5 分钟 wall-clock budget，并使用 validation bits-per-byte 作为统一指标，从而让不同实验更容易比较。

为什么这件事情值得特别理解？

因为它把 Auto Research 的四个关键组成部分拆得非常干净：

### Search Space

Agent 可以修改：

> `train.py`

也就是说它有一个明确的研究空间。

### Budget

所有实验统一：

> 五分钟。

所以 Agent 必须思考：

> 在固定算力下怎么获得最好结果。

### Evaluator

统一 metric：

> val_bpb。

所以它知道：

> 怎样算 better。

### Selection

结果：

```text
better → keep
worse → revert
```

于是研究第一次变成一个机器可以持续运行的搜索过程。

---

# 4. 为什么 Auto Research 本质上也是 Search

这其实是理解整个方向的关键。

科研看起来像：

> 灵感、创造力、发现。

但从系统视角看，很大一部分可以抽象成：

```text
Candidate Space
        ↓
Generate Candidates
        ↓
Evaluate Candidates
        ↓
Keep promising candidates
        ↓
Explore nearby candidates
```

因此：

> **Research = Search under uncertainty and resource constraints**

问题变成：

### Search Space

AI 到底允许改什么？

例如：

* architecture
* optimizer
* loss
* data
* prompt
* Agent workflow
* tool
* hyperparameter

### Search Policy

下一步尝试什么？

### Evaluator

如何判断好坏？

### Budget

可以尝试多少次？

### Memory

过去试过什么？

这几个东西组合起来，就是 Auto Research 的核心。

---

# 第二章：为什么 Evaluator 可能比 Research Agent 本身更重要

Auto Research 初看很容易让人关注：

> AI 能不能提出很聪明的 Idea？

但一个更深的问题是：

> **你怎么知道这个 Idea 是真的好？**

这是整个 self-improvement 领域的核心问题。

---

# 5. Generator 决定搜索空间，Evaluator 决定进化方向

假设 AI 一晚上可以产生 10,000 个 Idea。

如果 Evaluator 非常准确：

```text
10,000 candidate
↓
Evaluation
↓
筛出真正有价值的 10 个
```

这是强大的研究系统。

但如果 Evaluator 错了：

```text
AI 产生 candidate
↓
发现 evaluator 的漏洞
↓
学会优化漏洞
↓
score 越来越高
↓
真实能力没有提高
```

系统反而可能越进化越坏。

所以可以记住一句话：

> **Generator 决定系统能探索什么，Evaluator 决定整个系统朝哪个方向进化。**

---

# 6. Evaluator 实际上承担六种不同角色

很多人会把 Evaluator 简单理解成：

> 一个 benchmark。

其实不是。

一个真正的 self-improvement 系统至少需要六种 evaluation 能力。

---

## 6.1 Objective：定义“什么叫更好”

比如 autoresearch 里：

```text
lower val_bpb = better
```

这是一个非常明确的 Objective。

但现实中：

> “更好的 Research Agent”

根本没有这么简单。

它可能同时要求：

* research quality
* novelty
* correctness
* cost
* speed
* reproducibility
* robustness
* safety

于是变成：

```text
Utility =
Quality
+ Novelty
+ Generalization
- Compute Cost
- Error
- Risk
```

这件事情本身就是产品和技术设计。

---

# 7. 为什么 ASI-Bench 很值得看

超衍自己的 ASI-Bench，本质上就是在解决：

> 怎么衡量 Research Agent 到底“会不会研究”。

ASI-Bench 目前包含 60 个 project-level 科研任务，覆盖 11 个科学领域，并通过 B1 到 B4 逐渐减少人类给出的 methodological guidance。

最有意思的其实不是 benchmark 分数，而是：

> B1 → B4 的设计哲学。

---

## B1：我把方法告诉你

给 AI：

* scientific background
* method
* equations
* full procedure

AI 主要做：

> implementation。

这更像执行 Agent。

---

## B2：我告诉你方法，但不告诉你怎么具体做

例如：

> “用 PCA 做这个问题。”

但是完整 pipeline 由 Agent 自己完成。

于是 AI 开始承担：

> Workflow Construction。

---

## B3：我只告诉你目标

给：

* Objective
* Data
* Constraint
* Required Output

但是：

> 不告诉你应该采用什么方法。

于是 AI 必须：

```text
理解问题
↓
选择方法
↓
设计 workflow
↓
实现
↓
执行
↓
验证
```

这一层才真正出现：

> Scientific Decision Making。

---

## B4：再加入干扰信息

现实科研里不会有人把所有信息整理得干干净净。

所以系统还要判断：

> 什么信息重要，什么不重要。

因此 B4 开始测试：

> Robust Autonomous Research。

---

# 8. “会执行科研”与“会做科研”为什么完全不是一回事

这是你面试时可以形成的一个很明确的观点。

今天大量 Agent benchmark 实际测试的是：

> 给定任务以后，AI 能否执行。

例如：

```text
Implement algorithm X
```

但真正的研究问题是：

```text
Solve problem Y
```

两者差异非常巨大。

前者：

> Solution Space 已经由人类定义。

后者：

> Solution Space 本身也需要 AI 探索。

所以：

> **B2 → B3 很可能比模型 benchmark 从 70 分到 80 分更重要。**

因为 AI 的角色从：

> Executor

变成：

> Researcher。

---

# 第三章：Self-improvement 到底有哪些层级

“Self-improving AI”这个词现在使用得非常混乱。

很多系统只要会：

> Reflection

就号称 Self-improving。

但实际上不同方法改变的是完全不同的东西。

最清楚的办法是分四层。

---

# 9. 第一层：Context-level Improvement

比如 Agent 做错了一个任务以后写：

```text
上一次失败原因：
调用 API 之前没有检查 schema。

以后：
先 inspect schema，再调用工具。
```

然后把它存在 memory。

下次任务时表现可能真的更好。

但是：

> Model weights 没有变化。

这属于：

> **Behavioral adaptation**

而不是严格意义上的 Model Self-improvement。

---

# 10. 第二层：Harness-level Improvement

进一步，AI 可以修改：

* Prompt
* Workflow
* Tools
* Agent Code
* Planning Strategy

此时 Agent 系统真的发生了变化。

但：

> Foundation Model 本身可能还是原来的模型。

Darwin Gödel Machine 就是一个非常典型的例子。

---

# 11. Darwin Gödel Machine：不是训练模型，而是进化 Agent

DGM 让 Coding Agent：

> 读取并修改自己的 Agent codebase。

例如它可以自己发现：

* 文件查看方式不好；
* patch validation 不够；
* 只有一个 solution candidate 不够；
* 应该记住过去失败。

然后直接改自己的系统代码。

新版本再去 SWE-bench 等 benchmark 上评估。

Sakana AI 报告其系统在 SWE-bench 中从 20.0% 提升到 50.0%，同时在 Polyglot 上从 14.2% 提升到 30.7%。更重要的是，他们发现只有 self-modification 不够，开放式 archive/search 也很关键。

---

# 12. 为什么 DGM 不只保留“目前最强的 Agent”

这是 DGM 特别值得理解的地方。

最简单的进化算法可能是：

```text
Agent A
 ↓
改造
 ↓
Agent B
 ↓
B 更好
 ↓
保留 B
 ↓
继续改 B
```

这叫：

> Hill Climbing。

问题是非常容易掉入：

> Local Optimum。

---

## DGM 的做法

它保留：

> 一个不断扩张的 Agent Archive。

于是：

```text
Agent A
 ├── B
 │   ├── D
 │   └── E
 └── C
     ├── F
     └── G
```

未来的 Agent 可以从：

> A / B / C / D / E / F / G

任意一个节点继续探索。

这件事特别重要。

因为一个今天表现一般的 Agent：

```text
score = 60
```

可能拥有一个非常有价值的新机制。

它的 descendant：

```text
score = 80
```

可能正是通过这个中间版本才被发现。

DGM 的实验也观察到最终最好 agent 的 lineage 中经过过一些比父版本更差的中间节点，因此 archive 可以避免简单 hill-climbing 过早丢失有价值的 stepping stone。

---

# 13. 这给 Auto Research 一个非常重要的启发

研究不能永远是：

> “保留当前最佳方案。”

因为科研很多突破来自：

> 暂时看起来没有优势，但开辟了新方向。

因此未来 Auto Research 系统很可能不只是：

```text
Best Experiment
```

而是维护：

```text
Research Tree

Hypothesis A
├── Experiment A1
├── Experiment A2
│
Hypothesis B
├── Experiment B1
│   └── Hypothesis B1.1
│
Hypothesis C
```

这和 Git branch 非常类似。

我认为未来 Research Agent 一个很重要的产品对象可能不是：

> Conversation。

而是：

> **Research Lineage / Research Tree。**

---

# 第四章：Model-level Self-improvement——模型本身开始变化

第三层才是真正的：

> Model Self-improvement。

也就是：

```text
Training Data
Reward
Weights
Training Strategy
```

发生变化。

---

# 14. SEAL：模型如何学会“给自己制作教材”

SEAL——Self-Adapting Language Models——提出的一个非常关键概念叫：

> **Self-edit**

官方定义里，模型通过 RL 学习生成供自身使用的 fine-tuning data 和其他 update directives。

传统 fine-tuning 是：

```text
Human
 ↓
准备 Dataset
 ↓
Training
 ↓
Model improves
```

模型本身是：

> 被动学习。

---

## SEAL 做的事情

变成：

```text
New Information
     ↓
Model
     ↓
Generate Self-edit
     ↓
Convert into training material
     ↓
Finetune
     ↓
Evaluate future performance
```

比如模型得到一份知识材料。

它可能自己决定：

> “我要把这个知识重新组织成 Question/Answer pair。”

或者：

> “我要生成几个推理题训练自己。”

也就是说：

> AI 不只是学习数据。

它开始学习：

> **如何把经验变成适合自己学习的数据。**

---

# 15. 为什么这件事很接近“Learning to Learn”

真正关键的是：

SEAL 不只训练：

> 怎么回答问题。

它还训练：

> **什么样的 self-edit 能让未来的自己表现更好。**

所以目标变成：

```text
Current Model
 ↓
Generate Learning Strategy
 ↓
Update
 ↓
Future Model Performance
```

Reward 不只是来自：

> 当前回答对不对。

而是来自：

> **这次自我编辑有没有让后续模型变强。**

这已经属于 meta-learning 的味道。

---

# 16. R-Zero：连训练题都不让人类提供

R-Zero 又进一步。

它试图减少：

> human-curated training data。

系统由两个角色组成：

```text
Challenger
    ↓
Generate Problem
    ↓
Solver
    ↓
Solve
    ↓
Verifier
    ↓
Training
```

官方描述把它定义为 Challenger 与 Solver 的 co-evolutionary loop：Challenger 不断寻找 Solver 当前能力边界附近的问题，而 Solver 在这些逐渐变难的任务上改进，从而形成 adaptive curriculum。

---

# 17. 为什么“题目的难度”特别重要

如果 Challenger 永远出：

```text
1 + 1 = ?
```

Solver 永远得 100%。

但是：

> 没有 learning signal。

如果 Challenger 永远出：

```text
Solver 完全无法解决的问题
```

Solver 永远得 0。

也：

> 没有 useful signal。

理想状态是：

```text
Solver 当前能力
        │
        │
     frontier
        │
        ↓
Challenger 在这里出题
```

也就是：

> **Goldilocks Zone**

不太简单，也不太难。

---

# 18. 这实际上就是自动 Curriculum Learning

传统训练：

```text
Human Dataset
 ↓
固定训练课程
 ↓
Model
```

R-Zero：

```text
Current Model Capability
         ↓
Generate appropriate challenge
         ↓
Train
         ↓
Capability improves
         ↓
Generate harder challenge
```

课程本身会随着能力动态变化。

所以这里出现：

> **Co-evolution**

Challenger 变强：

> 更会发现 Solver 的 weakness。

Solver 变强：

> 更能解决 Challenger 的题。

两边互相推动。

---

# 第五章：什么时候才真正出现 Recursive Self-improvement

这里必须区分两个概念。

## Self-improvement

例如：

```text
Model A
 ↓
训练
 ↓
Model B
```

B 比 A 强。

这是 Self-improvement。

但它不一定 recursive。

---

# 19. Recursive 的关键是“能力增强本身能增强下一轮增强能力”

真正 Recursive 的结构必须是：

```text
AI(t)
 ↓
Improve itself
 ↓
AI(t+1)
 ↓
Because AI(t+1) is stronger,
it can discover better improvements
 ↓
AI(t+2)
 ↓
Even better improvement ability
```

换句话说：

> **Improvement Capability itself must improve.**

---

# 20. 举个反例

假设：

```text
AI
 ↓
生成100万条 synthetic data
 ↓
训练
 ↓
benchmark +5%
```

虽然：

> AI improved itself。

但是下一次生成训练数据的能力：

> 并没有因此明显提高。

那么这更多是：

> Iterative Self-training。

并不能直接称为强意义上的 Recursive Self-improvement。

---

# 21. Auto Research 为什么恰好提供了 recursive 的可能性

现在把两条线合起来。

假设 Auto Research 系统研究：

> “如何让模型 reasoning 更强。”

它提出：

```text
新的 RL algorithm
```

然后训练：

```text
Model v2
```

v2 推理能力更强。

接下来：

> v2 成为新的 Research Agent。

于是 v2：

* 更会读论文；
* 更会提出 hypothesis；
* 更会写代码；
* 更会判断实验；
* 更会设计 training method。

于是：

```text
Better AI
↓
Better Research
↓
Better AI
↓
Better Research
```

到这里才真正出现：

> Recursive Loop。

---

# 第六章：完整系统架构——未来的 Auto Research Platform 应该长什么样

现在可以把前面的东西整合成一个完整系统。

```text
                    Human / Research Goal
                              ↓
                    Problem Formulation
                              ↓
                      Research Planner
                              ↓
          ┌───────────────────┴──────────────────┐
          ↓                                      ↓
 Literature / Knowledge                    Research Memory
          ↓                                      ↓
          └──────────→ Hypothesis Generator ←────┘
                              ↓
                      Experiment Designer
                              ↓
                       Execution Runtime
                              ↓
                     Sandbox / Compute
                              ↓
                         Experiment
                              ↓
                     Evaluator / Verifier
                              ↓
                     Evidence / Findings
                              ↓
                      Research Selector
                     ↙                  ↘
              Explore                 Exploit
                 ↓                      ↓
             New Branch             Improve Best
                     ↘              ↙
                      Research Archive
                              ↓
                         Next Cycle
```

这才是真正完整的 Research Agent。

---

# 22. 为什么它已经不是一个“聊天机器人”

Chat 的核心对象是：

```text
Message
```

Auto Research 的核心对象应该逐渐变成：

```text
Research Project
Hypothesis
Experiment
Artifact
Evidence
Finding
Research Branch
```

所以产品的信息结构也应该变化。

未来不应该是：

```text
Chat 1
Chat 2
Chat 3
Chat 4
```

而更可能是：

```text
Research Project

Goal

Research Plan

Hypotheses
 ├── H1
 │   ├── Experiment 1
 │   └── Experiment 2
 │
 ├── H2
 │   └── Experiment 3

Findings

Artifacts

Research Memory
```

这其实正好和你之前一直思考的：

> Agent 是否应该从 session-centric 变成 goal/task-centric

属于同一个趋势。

---

# 第七章：产品负责人真正要设计的不是 Agent，而是“Research Operating System”

如果你去面超衍，我觉得这是最值得形成的产品判断。

一个成熟 Auto Research 产品，本质上不是：

> 一个 Agent UI。

而更像：

> **Research OS。**

---

# 23. Research OS 的六类核心对象

## Goal

我要解决什么问题？

例如：

> 在相同 FLOPs 下，把语言模型 validation loss 降低 5%。

---

## Hypothesis

我认为：

> 使用新的 optimizer 配置可能提高 convergence efficiency。

---

## Experiment

具体如何验证？

```text
Model
Dataset
Code
Config
Compute
Random Seed
Metric
```

---

## Evidence

实验产生：

```text
Logs
Metrics
Plots
Checkpoint
Output
```

---

## Finding

系统形成：

> Hypothesis supported / rejected / uncertain。

---

## Artifact

最终：

* code
* dataset
* model
* paper
* report
* chart

---

# 24. 为什么 Experiment Lineage 会变成非常重要的产品能力

假设 AI 做了 500 个实验。

用户真正想知道：

> 为什么现在选择方案 B？

系统必须回答：

```text
Experiment 147
↓
发现 optimizer X 不稳定

Experiment 163
↓
改变 warmup

Experiment 182
↓
发现 loss 降低

Experiment 216
↓
增加新的 schedule

Experiment 241
↓
最终提高 6.2%
```

这就是：

> **Lineage。**

没有 Lineage：

Research Agent 就变成：

> 一个黑箱。

有 Lineage：

你才能：

* audit；
* reproduce；
* debug；
* trust。

---

# 25. Research Memory 也不能只是向量数据库

Research Memory 至少应该分四类。

### Episodic Memory

过去发生过什么？

> Experiment 37 使用 AdamW，失败。

### Semantic Memory

目前已经知道什么？

> Batch size 超过 X 会导致 instability。

### Procedural Memory

什么方法有效？

> 做 optimizer comparison 时统一 training budget。

### Failure Memory

哪些方向不要重复？

> Architecture X 已经尝试过三次，没有 improvement。

这比单纯：

> embedding → vector search

复杂得多。

---

# 第八章：Human-in-the-loop 应该怎么设计

Agent 自主性越强：

> Human approval 就越不应该简单地“每一步弹窗”。

否则 Auto Research 根本无法 scale。

理想模式更像：

```text
Human 设置 Policy
↓
Agent 在 Policy 范围内自主工作
↓
超过阈值才 escalation
```

例如：

```text
单实验 <$5
自动跑

$5–50
允许批量预算

>$50
请求批准
```

再比如：

```text
读数据
自动

修改代码
自动

修改 evaluator
需要审批

发布论文
需要审批
```

未来 Agent Product 很重要的一层不是：

> permission button。

而是：

> **Delegation Policy。**

---

# 第九章：Compute 本身会成为产品的一部分

传统 SaaS 产品通常不需要用户思考：

> 这次点击消耗多少 GPU。

但 Auto Research 不一样。

它本质是：

> Search under Compute Constraint。

假设有：

```text
Experiment A
预计成功概率 50%
成本 $100

Experiment B
预计成功概率 20%
成本 $5
```

Agent 要决定：

> 先跑哪个？

所以 Research Planner 未来实际还承担：

> Resource Allocation。

可以把一个实验价值抽象成：

```text
Expected Research Value
=
Expected Information Gain
×
Probability of Success
×
Potential Impact
÷
Compute Cost
```

不需要真的用这个公式计算。

但产品思维要有这个意识：

> **Research Agent 不只是 planning tasks，也是在 planning compute。**

---

# 第十章：用户为什么应该相信 Auto Research

最终，Auto Research 产品的竞争力很可能不是：

> “我的 AI 看起来比你的聪明。”

而是：

> **我的研究结果比你的可信。**

Research Result 应该携带：

```text
Claim
↓
Evidence
↓
Experiment
↓
Code
↓
Dataset
↓
Environment
↓
Metric
↓
Uncertainty
```

甚至进一步：

```text
Counter Evidence
Alternative Explanation
Known Limitation
```

所以可以把 Auto Research 的产品价值分成两部分：

### Intelligence

能不能发现东西？

### Epistemic Trust

用户为什么相信这个发现？

很多 AI 产品只重视第一点。

科研产品第二点可能更加重要。

---

# 第十一章：六个代表项目分别应该怎么理解

到这里再回去看项目，就会容易很多。

## autoresearch

核心学习：

> **Minimal Research Loop**

重点：

* bounded search space
* fixed budget
* objective evaluation
* keep/revert
* experiment history

---

## AI Scientist

核心学习：

> **Full Research Lifecycle**

不仅做 experiment，还覆盖 idea、novelty、experiment、visualization、paper 等环节。官方项目明确定位为让 foundation model 独立完成科学发现流程，并提供 NanoGPT、2D Diffusion、Grokking 三类初始模板。

你应该把它理解成：

> Research Workflow Automation。

---

## ASI-Bench

核心学习：

> **What does autonomous research actually mean?**

重点不是 leaderboard。

而是：

> B1 → B4 如何逐渐把 methodology 从人手里拿走。

---

## SEAL

核心学习：

> **Model learns how to update itself。**

关键：

> Self-edit。

---

## R-Zero

核心学习：

> **Automatic Curriculum + Co-evolution**

一个系统：

> 出题。

一个系统：

> 解题。

双方一起变强。

---

## Darwin Gödel Machine

核心学习：

> **Agent Harness Evolution + Open-ended Search**

尤其要理解：

> Archive 为什么比 Best Agent 更重要。

---

# 第十二章：把六个项目放在同一张地图上

你可以这样记：

| Project      | 它主要解决什么     | 什么东西在变化            |
| ------------ | ----------- | ------------------ |
| autoresearch | 自动实验循环      | Research Candidate |
| AI Scientist | 自动科研全流程     | Research Workflow  |
| ASI-Bench    | 衡量自主科研      | Evaluation         |
| DGM          | 自动优化 Agent  | Agent / Harness    |
| SEAL         | 模型生成自己的学习材料 | Model Weights      |
| R-Zero       | 自动产生训练课程    | Data + Model       |

然后往上抽象：

```text
Auto Research
│
├── autoresearch
├── AI Scientist
└── ASI-Bench


Self Improvement
│
├── Harness Evolution
│       └── DGM
│
├── Model Adaptation
│       └── SEAL
│
└── Curriculum Evolution
        └── R-Zero
```

最后：

```text
Auto Research
      +
Self Improvement
      ↓
Recursive AI R&D
```

---

# 第十三章：面试前应该真正掌握的四个层次

如果时间有限，不需要平均学习所有论文。

按四层推进。

## 第一层：概念

必须能讲清：

```text
Deep Research
≠
Auto Research
≠
Self-improvement
≠
Recursive Self-improvement
```

---

## 第二层：系统

必须能画出来：

```text
Goal
↓
Plan
↓
Hypothesis
↓
Experiment
↓
Execution
↓
Evaluation
↓
Selection
↓
Memory
↓
Next Experiment
```

---

## 第三层：机制

必须理解：

```text
Search
Evaluation
Selection
Exploration
Exploitation
Archive
Curriculum
Self-edit
```

这几个词比记 50 篇论文更重要。

---

## 第四层：产品

最后要回答：

> 怎么把以上东西做成一个人类真的愿意使用的系统？

关注：

```text
Research Project
Experiment UI
Long-running Task
Research Memory
Compute Budget
Human Delegation
Trust
Artifact
```

这才最接近你面试岗位真正需要的东西。

---

# 第十四章：三天的学习顺序

## Day 1：先把 Auto Research 学透

先读：

1. autoresearch
2. AI Scientist
3. ASI-Bench

不要一开始读代码细节。

第一天最重要的是建立：

```text
Research Loop
```

最终要能不看资料画：

```text
Goal
↓
Hypothesis
↓
Experiment
↓
Environment
↓
Evidence
↓
Evaluator
↓
Selection
↓
Next Hypothesis
```

重点理解：

> 为什么科研 Agent 必须有 Environment 和 Evaluator。

---

## Day 2：理解 Self-improvement

顺序：

1. DGM
2. SEAL
3. R-Zero

这里有意不按照论文发布时间，而按照“什么东西在变”来学：

```text
Agent System
↓
Model
↓
Curriculum
```

最终你脑子里应该形成：

```text
Context
Harness
Data
Weights
Curriculum
Research Capability
```

这几个层级。

---

## Day 3：不要再继续读论文

第三天转向：

> Product Synthesis。

自己画一套：

> Apex Research Product Architecture。

至少设计：

```text
Home / Projects

Research Project
├── Goal
├── Plan
├── Hypotheses
├── Experiments
├── Findings
├── Artifacts
└── Research Memory
```

并进一步思考：

```text
什么时候需要用户 approve？

什么时候 AI 应该自己决定？

Compute 怎么控制？

失败实验怎么沉淀？

用户为什么相信结果？

多个 Research Agent 怎么协作？
```

---

# 第十五章：最后应该形成的几个核心判断

学完以后，我建议不要背项目，而是形成下面这些判断。

## 判断一

**Auto Research 不是 Deep Research Plus。**

区别不是：

> 搜索能力更强。

而是：

> 是否能够通过 Environment 创造新的 Evidence。

---

## 判断二

**科研 Agent 的核心对象不是 Conversation，而是 Experiment。**

Chat 只是交互方式。

真正的 state 是：

> Goal / Hypothesis / Experiment / Evidence。

---

## 判断三

**Auto Research 本质是一个 Search System。**

因此最重要的四个东西是：

```text
Search Space
Search Policy
Evaluator
Compute Budget
```

---

## 判断四

**Self-improvement 最大的难点并不是产生修改，而是判断修改是不是 improvement。**

所以：

> Evaluation 很可能是整个 self-evolving system 的 control plane。

---

## 判断五

**Model Self-improvement 与 Agent Self-improvement 是完全不同的问题。**

DGM 主要改：

> Harness。

SEAL 主要改：

> Model。

R-Zero 主要改：

> Curriculum + Model。

不能混为一谈。

---

## 判断六

**真正 Recursive 的条件不是“不断训练”，而是 improvement capability 本身不断增强。**

也就是：

```text
Better AI
↓
Better ability to create Better AI
↓
Even Better AI
```

---

## 判断七

**未来 Auto Research 产品很可能更像 Research OS，而不是 Chatbot。**

它需要：

* project
* experiment
* lineage
* artifact
* memory
* compute
* permission
* evaluation
* collaboration

完整的对象体系。

---

# 结语

如果把这整套东西压缩成一句话：

> **Auto Research 是把科研变成一个可执行、可评估、可迭代的 Agent Loop；Self-improving Model 是把 AI 自身也放进这个 Loop 的优化对象里。**

而两者真正汇合时：

```text
AI
↓
Research
↓
Improve AI
↓
Better AI
↓
Better Research
↓
Improve AI again
```

这时候出现的就不再只是一个 Research Agent。

而是一套：

> **能够持续搜索“下一代自己应该长什么样”的 AI R&D System。**

从产品角度看，真正困难的地方也不是给它做一个漂亮聊天框，而是：

> **如何把长期自主研究、实验分支、计算资源、证据、评价、记忆、权限和人类判断，组织成一个用户可以理解、干预、复现并信任的系统。**

我认为这才是“Auto Research 下一代智能产品形态”这个 JD 背后真正值得你准备的东西。
