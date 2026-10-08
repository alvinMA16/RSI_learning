# ASI-Bench 到底问什么、怎样评分？

基于本地仓库 `56829c9`，补充于 2026-09-22。这里区分公开正式任务的评分契约与公开示例；正式任务的完整实例题面、数据主要从 Hugging Face 下载。本次没有调用付费裁判模型或重新运行正式评测。

**核心答案：它是按任务定制的混合评分系统。文件与代码规则、数值误差、领域专用指标、重新执行仿真、LLM 文本判断、VLM 看图可以组合使用。没有一套统一的 LLM prompt 给所有答案打分。**

## 一、它问的通常是一个“需要交付成果的任务”

不是只问“解释什么是细胞聚类”，而是交给 Agent 数据，要求它写代码、运行分析，最后交付数组、CSV、图、代码和说明。下面是依据真实配置整理的中文转述，不是假装逐字引用正式题面。

| 真实任务 | Agent 需要完成什么 | 交付物 | 评分依据 |
|---|---|---|---|
| `materials.phonon_dispersion`，公开示例 | 给定一维原子链的质量、弹簧系数等，计算振动频率、态密度和热容 | 三个 `.npy` 数组 | 文件契约与参考数值误差 |
| `biology.scrna_seq_analysis`，正式任务 | 用合成的细胞×基因表达矩阵，完成聚类、细胞轨迹、差异基因和调控网络分析 | 代码、分类标签、轨迹数组、基因列表、网络分数、方法说明 | ARI、Spearman、F1、AUROC 与代码/文字规则 |
| `astronomy.nbody_close_encounters`，正式任务 | 根据带噪声、顺序打乱的观测及先验轨道粒子，预测天体后续状态与近距离相遇风险 | 预测分位数数组、风险汇总 CSV | 预测误差、区间宽度、概率和事件时间误差等 |
| `electrical_engineering.cmos_opamp_design`，正式任务 | 按给定工艺和增益、功耗、稳定性等要求，设计晶体管级运放并运行仿真 | 电路网表、仿真脚本、测量结果、波形、设计说明 | 网表规则、独立 SPICE 重跑、性能门槛、LLM 审核 |
| `physics.ag_strip_dielectric_inference`，正式任务 | 根据输入光学数据拟合介电模型，并预测未用于拟合的样本 | 参数、模型比较、预测结果、诊断图 | 自定义预测质量 96 分，文件 1 分、代码规则 1 分、VLM 图表判断 2 分 |

“其他方式”主要体现为领域专用的可执行验证。例如电路 Judge 可以真的跑 ngspice；名字叫 Judge，不代表一定是在调用 LLM。

## 二、同一个任务为何有 B1–B4？

四级通常维持同一研究目标和评分要求，改变 Agent 能获得的方法指导。

- B1：告诉方法、公式、完整操作步骤。
- B2：告诉方法方向，自己补执行流程。
- B3：只给目标、输入、约束与输出，自己决定怎么做。
- B4：在 B3 上加入正确但非必要的信息，考察抵抗干扰的能力。

公开的原子链示例很直观：B1 直接提供振动频率公式、5000 点密集网格、态密度归一化和热容求和方法；B3 基本只说“读取参数，计算并保存三个数组，只能用 numpy”。两者最后都要接受数值检验。因此 B1 高、B3 低意味着去掉具体指导后表现下降，不能直接推断为“模型不懂物理”，因为方法选择、规划、代码和执行也都可能出问题。

注意：这是 `sample` 教学任务，不是把它当成 60 道正式任务之一。部分 scorer 会接收 `prompt_level`，所以精确分析具体任务时仍要检查是否有分级逻辑，不能假设整个仓库每个判定都与等级完全无关。

证据：[B1 题面](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/tasks/materials/phonon_dispersion/prompt_b1.md)、[B3 题面](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/tasks/materials/phonon_dispersion/prompt_b3.md)。

## 三、总体流程：先检查能否评分，再累计分数

```text
任务题面 + 数据 + 约束
       ↓
Agent 规划、写代码、执行、修正
       ↓
提交输出文件
       ↓
Gate：文件存在？格式正确？有没有违反明确约束？
       ↓
Scoring：数值指标 / 自定义验证 / 仿真 / LLM / VLM
       ↓
按该任务的权重累计分数
       ↓
按任务、领域、B1–B4 汇总；另报时间、token、费用等
```

**Hard gate：** 失败通常不进入主评分，默认总分为 0。个别任务明确配置例外，例如运放任务用 `hard_fail_score_mode: gate_score_sum` 保留少量已经通过的门槛分。

**Soft gate：** 失败记警告，但不会在通用编排层自动阻断主评分或统一扣分。不要把所有 gate 都理解成“一票否决”。

**主评分：** scorer 返回已乘权重的贡献，编排层相加。常见任务满分为 100，但阈值和权重由各任务契约定义，不能拿不同领域的原始指标直接相加。

**评测失败和答错应区分：** 本地 `score` 会把带内部错误标记的评分判为 `evaluation_invalid`、分数记为 null，单独计数而不按普通零分处理。不过实现仍有边界：通用 Judge 聚合器遇到全部 JSON 解析失败时会以 0 处理，而非自动标为内部错误。这是值得修正的一种混淆。

证据：[评分编排](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/ai4sci_bench/runner/orchestrator.py:152)、[本地评分状态](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/ai4sci_bench/local_scoring.py)、[Judge 聚合](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/ai4sci_bench/scorers/_judge_common.py:290)。

## 四、例子一：完全不需要 LLM 的数值评分

公开原子链示例的真实权重：

| 项目 | 分值 | 满分条件 | 零分条件 |
|---|---:|---|---|
| 文件存在 | 10 | 三份要求的文件齐全 | 按检查项给分；前面还有格式硬门槛 |
| 振动频率曲线 | 45 | mean relative L2 误差 ≤ 0.01 | 误差 ≥ 0.20 |
| 态密度 | 30 | 误差 ≤ 0.05 | 误差 ≥ 0.30 |
| 热容 | 15 | 误差 ≤ 0.02 | 误差 ≥ 0.20 |

中间区间线性给分。以 45 分项为例：

`得分 = 45 × clamp((0.20 − 误差) / (0.20 − 0.01), 0, 1)`

这里的误差是数组的相对 L2 度量，不是“有多少个数填错”的百分比。参考数组来自任务生成器/参考解；参考值并不是让 LLM 临时想出来的。

**教学计算例子，非真实模型成绩：** 文件合格，三个误差依次为 0.105、0.175、0.11，三项均处在各自满分与零分阈值的正中间，因此总分为 `10 + 22.5 + 15 + 7.5 = 55`。一旦前面的硬门槛失败，则不能照此继续加主评分。

证据：[任务及权重](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/tasks/materials/phonon_dispersion/task.yaml)、[数值评分实现](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/ai4sci_bench/scorers/numerical.py:93)。

## 五、例子二：正式的单细胞分析任务如何评价“研究做得好不好”？

| 子问题 | 怎么测 | 权重 | 满分 / 零分阈值 |
|---|---|---:|---|
| 有没有把相似细胞分到正确的组 | ARI，对照隐藏的细胞标签，类别编号本身不重要 | 25 | ≥0.75 / ≤0.20 |
| 有没有恢复细胞变化的先后轨迹 | 预测 pseudotime 与参考轨迹的绝对 Spearman 相关性 | 24 | ≥0.85 / ≤0.25 |
| 有没有找到重要差异基因 | F1，兼顾找得准与找得全 | 20 | ≥0.70 / ≤0.15 |
| 有没有恢复基因调控关系 | AUROC，正确关系是否排在错误关系前面 | 21 | ≥0.75 / ≤0.50 |
| 有没有说明方法选择并遵守约束 | 对 `method_choices.json` 做正则表达式检查 | 10 | 按各项规则给分 |

这个任务的主评分配置没有 LLM 裁判。前面还有输出文件和禁止某些高层生信库的硬门槛。

最值得批判的是最后 10 分：它检查 batch effect、nonlinear、causal 等关键词模式，并不能可靠判断方法说明是否真的正确。同样，静态正则检查 `import` 只能覆盖一部分违规方式，也可能误判写法。可改成运行时依赖追踪、结构化方法说明、少量语义审查和因果消融；不能把“出现关键词”当成理解机制的充分证据。

证据：[正式任务评分契约](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/tasks/biology/scrna_seq_analysis/task_eval.yaml)、[自定义指标实现](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/tasks/biology/scrna_seq_analysis/custom_scorer.py)。

## 六、例子三：电路任务为什么同时需要规则、仿真与 LLM？

这个任务要求晶体管级运放。只检查“输出波形看起来对”不够：Agent 可能拿理想放大器直接模拟效果，绕过真正设计晶体管电路的要求。

因此它组合三种证据：

1. **规则检查：** 文件存在，网表结构、引脚和代码形式符合约束。
2. **执行验证：** 评价器重新运行固定 AC、瞬态、DC/功耗、噪声、摆幅仿真，把测量值与 Agent 自报的 `results.json` 比较。自报一个漂亮数值不够，要与重跑结果一致。
3. **LLM 判断：** 判断主信号路径是否真的由晶体管网络实现；尺寸参数是否有工程意义；拓扑选择理由是否针对具体指标。

真实主评分权重是：交付物 1 + 网表规则 1 + LLM 实现真实性 1 + 性能达标 54 + 仿真核验 30 + LLM 参数合理性 8 + LLM 设计说明 5 = 100。

所以 **84 分主要来自性能与仿真核验，14 分直接来自 LLM，2 分来自文件/网表规则**。但 LLM 还参加前置 hard gate，其影响并不只有 14 分：若真实性判断不通过，主评分可能被阻断，只保留门槛分。

配置里的 `testbench_judge: agent: grounded` 当前走的是固定仿真重跑与容差比较，不应该只看到 “judge” 就归类为 LLM。

该任务 LLM 配置使用 `openai/gpt-5.5`、3 次裁判调用、温度 0，要求返回 JSON 的 0/1 分数；通用聚合器取有效结果的中位数并归一化。这里是同一个模型被调用多次，不是三个独立模型。其他任务可以采用不同模型、0–10 分与不同 rubric。

证据：[运放权重和 rubric](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/tasks/electrical_engineering/cmos_opamp_design/task_eval.yaml)、[重跑实现](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/tasks/electrical_engineering/cmos_opamp_design/custom_scorer.py:1153)。

## 七、VLM 看图和人类专家分别在什么位置？

有些任务需要诊断图，VLM 会检查曲线、坐标、标注和关键现象。例如银纳米条介电推断任务，96 分来自自定义科学指标，VLM 看图只有 2 分：是否同时展示拟合与多个 held-out 预测、是否区分不同偏振、是否暴露失败案例、坐标与图例是否清楚。

这比用图片整体相似性代理全部科学正确性更稳妥，但图表评分仍可能奖励“画得像参考答案”。实现也支持 `pixel_sim` 图像指标，所以 multimodal scorer 不一定总是模型裁判，需看具体 `mode`。

人类专家主要参与任务构建、领域审核、评分规则设计与审计。README 提到的 expert cross-review，不应直接解释成“每次 Agent 答题都有专家现场阅卷”。本次查看的运行契约以自动评分为主；官方私有服务端的完整人工流程无法仅凭公开代码确定。

证据：[介电推断评分](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/tasks/physics/ag_strip_dielectric_inference/task_eval.yaml)、[多模态评分器](/Users/peizhengma/Documents/ChatGPT/RSI/repositories/ASI-Bench/ai4sci_bench/scorers/multimodal.py)。

## 八、最终到底是在测模型，还是 Agent？

实际测到的是 **模型 + Agent harness + 可用工具 + 执行环境 + 时间/算力预算** 共同产生的结果。同一个模型换工具权限、重试机制或规划策略，也可能得到不同分数。

公开 runner 会按任务、领域和 B1–B4 汇总；通用报告总体分数是有效已评分结果的平均值，因此覆盖的任务、等级和重复次数应对齐。成本、耗时、token 等另外统计，并非统一自动折算进每题正确性分数。官方榜单的最终发布口径仍应以官方协议为准。

公开参考的 seed31415 用于本地非官方评分；seed42 的参考答案私有，须提交官方端评分。公开参考方便复现，同时也可能被针对性调参；私有参考减少泄漏，却增加对服务端透明度的要求。

**我的评价：这套系统主要在检查“是否交付了符合约束、可验证的科研成果”，并用减少指导的方式测自主性。它比只让 LLM 评价一段回答扎实，但仍不能把分数直接理解成科学创造力、真实新颖性或递归自我改进能力。**
