# Auto Research 与 Self-improving Model 学习手册

双击根目录的 `学习手册.html` 即可阅读；这是无需其他文件的独立版本。`course/index.html` 是便于继续编辑的多文件版本。页面、样式、课程和交互全部本地加载，不依赖 CDN、框架、账号或服务器。外部官方资料链接需要联网。

19 课按概念主线 → 系统与产品 → 项目例证 → 阅读与面试综合编排；核心问题采用直接可见的问答，含流程图、对比表、B1–B4 交互示例与折叠自测答案。

## 文件

- `course/index.html`：入口
- `course/lessons.js`：完整课程内容
- `course/integration.js`：概念主线、补充机制课程与课程重排
- `scripts/build_course.py`：生成独立 HTML
- `course/style.css`：响应式样式
- `course/app.js`：课程切换、层级示例
- `sources/`：本次核对的官方材料快照

## 内容边界

资料读取于 2026-09-22。官方仓库文档与实现事实、课程架构建议、假设案例分别标识。未运行 GPU 训练或 benchmark。论文摘要核对不等同于全文精读；详见“现在再读论文”一课。

用户原文末尾的 “Roll” 按 Rollback 理解，同时在模型发布课讨论灰度 rollout。

## 本次融合

吸收用户提供文档的系统讲解方式，增加研究搜索、评价职责、改进层次、递归证据、SEAL、R-Zero、DGM archive 和 Research OS。项目背景继续保留。旧链接使用稳定 ID，课程显示编号随阅读顺序重新排序。修改内容后运行 `python3 scripts/build_course.py` 同步独立版本。
