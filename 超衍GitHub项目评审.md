# 超衍智能 GitHub 项目：用途、证据与改进空间

审阅日期：2026-09-22。公司确认来自另一个任务《制定 Auto Research 学习路线》及会话《超衍面试学习资料》中的链接，官方组织为 [apexin-ai](https://github.com/apexin-ai)。范围为组织 API 返回的全部 7 个公开仓库，不包括私有仓库、Hugging Face 数据全集或论文中承诺将来公开的资产。

**总体判断：这是一组围绕“自动科研 → 评价 → 产生改进”的公开资产。公开材料最能证明的是科研任务评测的工程投入，以及若干可检查的研究产出；尚不能据此证明一个基础模型已经实现持续、递归、可泛化的自我提升。**

这不是对公司内部能力的否定。要区分“内部可能已经做到什么”和“第三方现在能从公开仓库验证什么”。

## 1. 先看全景

| 项目 | 实际是什么 | 解决的问题 | 当前公开材料的主要边界 |
|---|---|---|---|
| [ASI-Bench](https://github.com/apexin-ai/ASI-Bench) | 科研 Agent 基准、执行与评分框架 | 判断 AI 在减少人类方法指导后能否完成科研任务 | 固定任务和评价契约不等于开放式发现；官方私有参考评分依赖服务端 |
| [Apex-Tune-results](https://github.com/apexin-ai/Apex-Tune-results) | 自动研究得到的训练脚本、公式与 GPU kernel | 展示训练效率、性能预测与计算内核优化成果 | 公开的是候选成果及复现脚本，未见完整自动研究系统和搜索历史 |
| [apex-research-report](https://github.com/apexin-ai/apex-research-report) | 4 页研究报告与介绍 | 用真实同行评审作为自动科研质量的外部信号 | 不是完整科研 Agent 源码，也不是 34 篇论文及全量实验档案 |
| [Evaluation-Self-Evolve-AI-System](https://github.com/apexin-ai/Evaluation-Self-Evolve-AI-System) | 评价体系综述设计、文献库和写作辅助材料 | 系统解释评价如何指导、证明和审计自进化 | 不是已经实现的 evaluator 平台 |
| [Math-Paper](https://github.com/apexin-ai/Math-Paper) | 5 篇数学手稿 | 展示 Apex Math 的数学研究成果并征求验证 | 作者明确标为待独立验证；仓库未附证明器源码和完整检查资产 |
| [dashboard](https://github.com/apexin-ai/dashboard) | Volcano 集群管理仪表盘的 fork | 查看和管理计算任务、队列、Pod 等资源 | 上游是 volcano-sh/dashboard；不能将整套软件计为超衍原创 |
| [.github](https://github.com/apexin-ai/.github) | 组织首页 | 介绍定位、研究与招聘 | 不是软件项目，宣传主张应回到具体证据核查 |

可以用下面这条线理解它们之间的关系。这是本次分析的概念归纳，不表示仓库已经实现彼此的系统集成：

```text
研究执行与搜索（核心系统未在这些仓库中完整公开）
    ├─ 产生研究论文          → apex-research-report
    ├─ 产生数学证明候选      → Math-Paper
    └─ 产生训练/公式/kernel  → Apex-Tune-results

测量科研任务能力            → ASI-Bench
设计进化评价原则            → Evaluation-Self-Evolve-AI-System
管理底层计算资源            → dashboard（上游 fork）
对外说明定位                → .github
```

## 2. ASI-Bench：最值得优先研究的系统项目

补充阅读：[ASI-Bench 评分机制详解：真实题目、规则与 LLM 混合评分](/Users/peizhengma/Documents/ChatGPT/RSI/ASI-Bench评分机制详解.md)。


### 它做什么，为什么有价值？

它让同一个科研目标处于四种指导条件下：B1 给完整方法和步骤；B2 给方法但省去具体流程；B3 只给目标、数据、约束与输出要求；B4 在 B3 基础上加入正确但无关的信息。目标和评分标准保持一致，因此更容易分辨系统究竟依赖了多少人的指导。

例如，普通评测会问“这套算法实现对了吗”；这里进一步问“没有告诉你算法名字，你还能自己选方法并完成任务吗”。这很适合判断 Research Agent 从执行助手走向自主研究的程度。

仓库声明包含 60 个正式项目级任务、11 个领域，另有 5 个公开示例。实现覆盖 Agent adapters、Docker/namespace 沙箱、任务输入与产物管理、数值与模型裁判、结果溯源、提交与本地评分。seed31415 有公开参考，可本地评分；seed42 的参考保留在官方评分端。后者有防泄漏价值，但公开侧无法完全独立复刻官方评测。

**值得肯定的细节：** 它区分“Agent 做错”和“评分器坏了”，评分器内部失败会记录空分数、错误计数并使命令非零退出；还区分未观测到的模型调用信息与真实的零值。这些比单纯给一个榜单更接近可用基础设施。

### 局限与可以更好的地方

1. **测量自主完成既定任务，与产生新的科学知识仍有距离。** B3 可以用已有方法解决预先定义、已有参考的任务。这样的成功很有价值，却不自动意味着发现了未知规律。建议把复现、方法选择、跨领域迁移、开放假设生成分开报告，增加需要新证据的长期挑战。
2. **任务筛选会影响低分的含义。** 贡献规范要求 B3/B4 平均分严格小于 40。这样能避免题库过早饱和，也会偏向筛选时模型的弱点。建议记录筛选模型、版本、预算和淘汰任务，另保留未按模型表现筛选的外部任务集，防止把“刻意挑难题上的低分”解释成整个科学领域的能力比例。
3. **指导梯度并不能单独证明因果机制。** B1→B3 同时改变了信息量、搜索空间和执行成本。建议配对比较同一模型、同一 harness、相同预算，并加做等长度无关文本控制；报告每个领域和任务的差值、方差，而不只报一个总体均分。先前会话强调 B2→B3 的概念意义，但论文摘要给出的平均分下降更大的是 B1→B2（50.91→29.10），B2→B3 是 29.10→26.62；概念分界与实测最大瓶颈不能混为一谈。
4. **多个 Judge 调用不一定是多个独立判断者。** `llm_judge.py` 的 `num_judges` 循环对同一个解析后的 model 重复调用，默认温度为 0。它有助于处理输出解析波动，却不等于跨模型共识。建议显式配置异构裁判，报告裁判间分歧，并用领域专家抽检校准。
5. **长产物的裁判可见范围有限。** 默认每个文件只取前 10,000 字符，后文可能包含关键实验、错误或结论。代码会提示截断，因此这不是隐藏行为；问题是局部内容能否支持总体分数。建议按结构提取证据、分节评分，记录被读取的覆盖率，把低覆盖结果送人工复核。
6. **需要把模型联网与自由外网访问分开。** Docker 执行代码为了 CLI Agent 的模型 API 开放网络，默认这一层没有限定只连模型域名。工具禁用也不等于 OS 层禁止网络。建议采用出口代理与目的地址允许列表，并分别设置闭网研究和开放检索赛道。这是根据运行配置推导的评测边界风险，本次未实际尝试绕过。
7. **可维护性已有压力。** `ai4sci_bench/cli.py` 约 4,800 行。后续按运行、评分、提交、任务作者四个命令组拆分，更容易验证“本地非官方评分”和“官方提交”之间的契约。

证据入口：[README](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/README.md)、[Judge 实现](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/ai4sci_bench/scorers/llm_judge.py)、[Docker 沙箱](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/ai4sci_bench/runner/os_sandbox.py)、[CLI](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/ai4sci_bench/cli.py)。

**面试时值得问：** “如果把筛选时没见过的新模型和新领域加入，怎样判断分数下降来自科研方法选择、工具执行，还是预算不足？”

## 3. Apex-Tune-results：最适合检查“AI 到底发现了什么”

### 四类成果分别做什么？

| 子项目 | 用普通话解释 | 公开结果及边界 |
|---|---|---|
| NanoChat autoresearch | 固定 300 秒，在单张 B200 上把语言模型训练得更好 | 10 seed 平均 val_bpb 为 0.8927922；越低越好。这是固定小预算训练实验，不是通用模型能力的全面测量 |
| MLS fused attention | 把 Transformer 的注意力计算写得更快 | H100 上三个给定 shape 的前向吞吐提升；不能直接等同于完整模型端到端提速 |
| SLDBench | 从已有训练实验中拟合规律，预测新规模/配置的表现 | 四任务平均分约 0.8846；需要区分当前 held-out 划分和真正换模型家族后的泛化 |
| GPUMode TriMul | 优化类似 AlphaFold 的三角更新计算 | H100 上 7 个性能 shape、18 个正确性测试；已公布材料中也列出了略快的 K-Search 对照 |

这些结果比单纯的“系统会研究”口号具体：有候选代码、评测脚本、数据版本和逐 seed 指标。本次重算 NanoChat 的 10 个数，均值与标准差和公布结果一致。但这是对已发布数据的一致性核查，没有重新训练模型，也没有独立确认外部 SOTA 排名。

### 已复现的工程问题

**A. SLDBench 可能把不完整评测算成漂亮均分。** `run_subtask` 即使进程非零退出，只要 stdout 出现 `Combined Score` 就仍返回该分数；主流程对有分数的任务求均值，不把剩余失败任务计入分母，且不会因此非零退出。本次模拟四项中三项失败、一项 0.999989，脚本仍生成 `suite_mean=0.999989` 并正常返回。

建议：单任务同时满足退出码为零、结果结构合法、分数有限才有效；完整四任务报告必须带 expected/completed/failed 数量，不完整时不发布可与四任务均值直接比较的分数，并返回非零状态。可借用 ASI-Bench 已实现的“评测无效”状态体系。

**B. MLS 的异常报告路径会再次崩溃。** 当 kernel 进程在产生指标前失败，`run_one` 返回 `crash`，但汇总代码直接访问所有结果的 `r['max_diff']`。本次用模拟进程失败复现了 `KeyError: max_diff`。建议用明确的成功/失败结果类型，缺失指标保留 null，避免丢掉最初的失败原因。

证据：[SLDBench runner](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/Apex-Tune-results/sldbench/evaluate.py:60)、[MLS 汇总](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/Apex-Tune-results/mls-bench_fused_attention/bench.py:114)、[本次复现脚本](/Users/peizhengma/Documents/ChatGPT/RSI/review-evidence/check_findings.py)、[复现输出](/Users/peizhengma/Documents/ChatGPT/RSI/review-evidence/check-results.json)。这些发现没有用于断言已公布实验实际遭遇同样错误。

### 更重要的研究与产品边界

**数值稳定性需要明确适用条件。** Fused Attention 候选直接计算指数，再把未归一化权重转为 FP16，省去常见的减最大值稳定处理。这对基准的随机输入可能很快，但输入幅度变大时存在溢出风险。例如 d=64、q=k=2，则缩放后的点积为 32，exp(32) 约 7.9×10¹³，远大于 FP16 的 65504。这里是针对计算路径的数学反例，未在 H100 上执行。建议增加大幅值、极端分布、不同长度与 dtype 的正确性测试，并对安全输入域之外走稳定实现。

其 harness 还只用 `max_diff > threshold` 判错，没有显式拒绝 NaN。Python 中 `NaN > threshold` 为 False；外层 parser 的限制可能使结果无法解析，所以不能说 NaN 已经拿到官方有效分数，但内层判定应加入 `isfinite`，防止错误的 `correct=1` 输出。见 [候选与 harness](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/Apex-Tune-results/mls-bench_fused_attention/submission.py:85)。

**公开赢家不足以复现发现过程。** 当前可看到“找到了什么”，但看不到完整候选数量、失败轨迹、人类介入、搜索费用和选择策略。因此不能据此分辨：优势有多少来自更好的研究 Agent，有多少来自更多尝试或人工筛选。建议公开至少一个从基线到最终方案的完整 campaign，包含所有候选、预算、拒绝原因、独立验证和消融。

**比较口径要收紧。** NanoChat 混合展示竞品均值与最佳值，SLDBench 明确说明 baseline 是 previous evaluator artifact 而非 SimpleTES 论文 5-seed 方法级均值；TriMul 同一表也有 1030 μs 的 K-Search，比 1036.1 μs 更低。建议“SOTA”声明附榜单时间、资格规则、硬件、依赖版本、选择预算，避免表格被理解成对所有方法的统一比较。

**复杂候选应变成可解释产品资产。** 训练脚本约 7,385 行，混合了许多实验分支。先发布一版最小获胜配置、明确依赖和机制消融，再保留探索版，会更有利于复用和定位收益来源。

**面试时值得问：** “最终模型训练只用了 300 秒，发现这个配置一共用了多少 GPU 小时？提升来自模型结构、数据配方还是 kernel，分别做过哪些消融？”

## 4. apex-research-report：有价值的外部信号，证据链仍不完整

报告称 34 个 AI 生成项目提交到 ARR，平均评分 2.60，对照人类分布均值为 2.63；8 篇超过 3.0，2 篇为 3.67；消耗 1,286 allocated GPU-days，并称人类消息轮数占 0.38%。

**价值：** 相比模型自己给自己打分，真实领域审稿意见提供了更独立的质量信号，也把科研评价落到了可以讨论的论文成果。

**需要保留判断的地方：**

- “预计 11 篇可录用”依据历史分数与录用关系估计，不是 11 篇已录用；仓库同时说所有 AI 投稿将在评审后撤回。
- “通过科研图灵测试”是作者对结果的概括。报告没有给出审稿者判断“作者是不是 AI”的识别率，因此不宜把它当作严格的作者识别实验结论。
- 0.38% 是消息轮数占比，不是劳动时间、决策价值或因果贡献占比。一次选题或淘汰决定也可能很关键。
- 2026 投稿对照 2025 分数分布、2024 录用历史存在跨年度比较限制。样本、领域和稿件选择过程也会影响结论。
- 当前仓库只有 README、logo 和 4 页 PDF；未见报告承诺公开的全套 34 篇手稿、实验协议和 reviews，因此无法复查选样与全量分数。
- allocated GPU-days 不能直接等同于设备实际满载时间、统一硬件 FLOPs 或美元成本；缺少 GPU 类型、利用率和模型 API 费用会使成本比较失真。

**改进优先级：** 发布逐项目台账：题目、版本、原始 reviews、人工干预、耗时与费用、实验重现材料、撤稿/接受状态；再找独立团队抽样复现。核心产品指标可以从“产出多少论文”前移到“每单位总成本产生多少可独立验证的新结果”。

证据：[仓库说明](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/apex-research-report/README.md)、[报告原文](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/apex-research-report/Apex_Research_Report.pdf)。

## 5. Evaluation-Self-Evolve-AI-System：理论框架好，距离执行系统还有一步

它把评价分成三种功能：Control 指导并选择下一次改进，Proof 独立证明是否真的变好，Meta 审计与升级评价器自身。进一步把评价对象从单次答案扩展到过程、组件更新、系统版本和长期进化轨迹。

**对产品负责人很有帮助：** 这意味着产品不能只有一个“分数”字段。内部搜索分数、上线准入判断、外部能力证据需要不同权限与来源；更新 Judge 后，还必须知道新旧系统是否仍然可比。

**主要局限：**

1. 当前主要是综述设计和资料收集，没有发现可直接运行的 evaluator 服务、标准评测数据或 promotion gate 实现。应把它视为思想材料。
2. `data/research-report.md` 明确限制为英文同行评议期刊，排除了无期刊版本的相关会议论文。这个范围可以成立，但会系统性漏掉 AI 前沿的重要一部分；需要说明它是“期刊文献子集”，或增加会议/预印本证据轨道。
3. 报告保留了无法在 GitHub 解析的 `cite...` 标记，还链接到 `sandbox:/mnt/data/...xlsx`，但仓库没有该工作簿。读者无法顺着部分论断完成核查。这是具体的证据可追溯性缺口，不代表其中所有论文都不真实。
4. 架构分类很全面，但还缺“最小落地案例”：例如连续 20 次 Agent 更新，如何区分短期得分上涨、旧能力遗忘和裁判偏移。

**建议的最小产品化版本：** 定义 Candidate、Snapshot、Evaluation、Decision 四个对象；把独立测试集与内部反馈隔开；每次更新记录收益、遗忘、成本和失败原因；再加入 evaluator 版本变更审批与回滚。用一段真实迭代轨迹展示三类评价如何相互约束，比继续扩展术语更有说服力。

证据：[综述设计](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/Evaluation-Self-Evolve-AI-System/README.md)、[文献研究报告](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/Evaluation-Self-Evolve-AI-System/data/research-report.md:29)。

## 6. Math-Paper：应评审“命题与证明”，不能只评审论文外观

五篇手稿分别涉及：四变量五次齐次多项式的 Gordan–Noether 问题、Kakimizu 不可压 Seifert 曲面复形、Kari–Moutot excess 上界、五穿孔射影平面的 Markoff–Hurwitz 关系，以及 genus-two 曲线复形的可缩性。

这类工作的重要意义是：科研 Agent 的产物可以是数学命题及证明，而不只有在已有数据集上提分。仓库明确邀请独立审查，全部标为 `Open for independent verification`，这种状态表达是恰当的。

**最需要补足的证据：** Kari–Moutot 手稿摘要声称部分结论已在 Lean 4/mathlib 中形式化、无 sorry 和新增公理；Gordan–Noether 手稿提到 exact frozen checker。但当前仓库只含 5 个 PDF 和 README，没有对应 `.lean`、检查器代码或可重建环境。外部读者目前只能读这些声明，无法在仓库内重跑验证。

**改进建议：**

- 逐条定理提供机器证明或计算证书、Lean/mathlib 版本、构建命令与哈希；说明机械检查覆盖了全文哪些步骤。
- 每篇提供 LaTeX 源码、版本变化和问题台账，把“已验证、存在缺口、已修复、仍未知”细化到具体 lemma。
- 将专家审稿与形式化检查结合：证明器确认形式命题推导正确，不自动保证形式化命题与自然语言研究目标完全一致。
- 记录研究过程中的错误路线和反例，才能评价系统是否有可靠的自纠错能力。

本次读取了全部 5 篇摘要并定位相关验证声明，没有逐条验算这些高级数学证明，因此不对命题真伪下结论。证据：[仓库验证状态](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/Math-Paper/README.md)。

## 7. dashboard：资源管理基础设施，不是自动科研系统本身

这是 [volcano-sh/dashboard](https://github.com/volcano-sh/dashboard) 的 fork，采用 Next.js、React、tRPC 与 Kubernetes 客户端，对 Jobs、Queues、Pods 等资源提供管理界面。它可以作为 Research OS 的算力管理底座，但缺少科研层面的 Hypothesis、Experiment、Evidence、Candidate 等核心对象。没有逐 commit 比较上游，因此本次不判断超衍究竟贡献了哪些修改。

**具体问题与改进：**

1. **高优先级：公开代码没有用户级认证授权闭环。** API handler 创建 `session: null`；`procedure` 是原始 tRPC procedure；删除 Job 等 mutation 直接使用服务端 Kubernetes 凭据。默认部署又给该 service account 集群级 Job/Queue 修改权限。因此，只要网络可达且没有外部认证代理拦截，客户端就可能继承服务端操作权限。README 还提供监听 `0.0.0.0` 的 port-forward 示例。建议默认只读、只监听本机，写操作要求登录、命名空间授权和审计；K8s service account 也按租户缩小权限。本次只做静态核查，未连接真实集群。
2. **界面能力和部署权限不匹配。** 存在 Pod 新增、更新、删除接口，默认 YAML 对 Pod 却只有 get/list/watch。结果可能是界面可点、操作被 K8s 拒绝。不要简单把权限全加上；应按服务器实际授权显示可用动作，并默认禁用不需要的写权限。
3. **设计文档与实现漂移。** `docs/design.md` 仍写 Express、Material-UI、React Router，实际目录是 Next.js/tRPC 等。建议从当前边界重写架构图，明确哪些权限在 UI、API 和 K8s 分别生效。
4. **向科研产品延伸时，需要从资源状态走向实验状态。** 除了“GPU 是否忙”，还应回答“哪个假设用了多少预算、哪个实验可恢复、失败产物是否保留、何时应该停”。这是合理的产品扩展方向，不是当前通用 Volcano 仪表盘必须承担的缺陷。

证据：[API 路由](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/dashboard/apps/web/src/app/api/trpc/[trpc]/route.ts:9)、[tRPC procedure](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/dashboard/packages/trpc/server/trpc.ts:10)、[Job 删除接口](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/dashboard/packages/trpc/server/router/jobs/jobs.ts:151)、[部署权限](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/dashboard/deployment/volcano-dashboard.yaml:69)。这些观察适用于这份 fork 快照，不代表问题由超衍引入。

## 8. .github：对外定位需要与证据状态同步

仓库只有组织介绍和 logo，主张是 self-evolving foundation models，并链接到 Apex Research 报告。它的作用是传播，不需要按软件架构评价。

最值得改进的是增加“声明—证据—状态—更新日期”表：把模型权重改进、Agent 软件改进、科研产出分别写清；研究报告的预期录用、数学手稿的待验证状态也应在首页保持一致。让读者一眼找到能运行的项目、能复现的成果、尚待验证的主张。

## 9. 如果从产品负责人视角选改进方向

我会优先推进三个方向：

**第一，建立统一的研究证据链。** 将 ASI-Bench 的运行溯源、Apex-Tune 的成果、Math-Paper 的证明和研究报告的项目台账连起来。核心不是增加一个展示页面，而是让每个结论都能找到输入、代码版本、运行环境、原始结果、验证者和决策记录。

**第二，把独立验证做成正式发布门槛。** 搜索时可以快速试错，但获胜候选应在未参与选择的任务、seed、硬件或领域上复验，同时报告成本与旧能力回归。数学结论则给出可执行证明证书和专家核查状态。

**第三，证明“下一轮研究变得更好”。** 现在较多材料在展示某次产出不错。要支持递归改进，还需要连续版本实验：在相同总预算下，M(t+1) 是否比 M(t) 更快提出有效假设、减少无效实验、产生更多独立验证的改进？最终分数提升和研究生产率提升应分开测。

阅读建议：先看 ASI-Bench 的任务和评分契约，再看 Apex-Tune 的具体产出，然后用 Evaluation 综述组织自己的观点，最后审视报告与数学论文的证据强度。dashboard 放在计算资源与产品运维这一层理解即可。

## 10. 本地交付与验证范围

全部仓库位于 `/Users/peizhengma/Documents/ChatGPT/RSI/repositories/`。由于 GitHub 主站的 Git 连接超时，使用 GitHub 官方 API 下载默认分支完整文件快照；**不包含 Git 提交历史，不是已完成的 git clone**。版本和压缩包 SHA-256 见 [快照清单](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/snapshot-manifest.json)。大规模数据集、模型权重和外部服务没有下载。

审查包括所有仓库文件清单与 README、报告全文、数学摘要及部分验证声明、ASI-Bench 的关键执行/评分代码、Apex-Tune 的 runner 和候选 kernel、dashboard 的 API 和部署权限。另执行了独立的 CPU 评审探针并重算公开统计量。未运行 GPU 训练、H100 kernel、完整 ASI-Bench 付费模型评测或 Kubernetes 部署；没有修改第三方项目实现，没有上传、投稿或联系作者。
