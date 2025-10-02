# AI 应用工程师（LLM Application Engineer）专业课程最终大纲

**课程代码**：AI-APP-101  
**学时**：96 学时（理论 32h + 实践 64h）  
**学分**：6 学分  
**课程性质**：职业技能培训课程  
**适用对象**：有 Python 基础的在校生/在职转型开发者/应届生  
**版本**：v2.1 | 2025-10-02

—

## 一、课程定位与简介

本课程采用成果导向教育（OBE）理念，面向大语言模型（LLM）应用开发岗位，培养学员从模型微调、Prompt 优化、RAG 系统到 Agent 编排与服务端工程化的全栈能力。课程强调底层原理与生产级工程实践，不依赖 LangChain/LlamaIndex 等封装框架，确保对关键组件的可控与可解释。

—

## 二、课程目标（CO）

学完本课程，学员将能够：

1. CO1｜理解与应用 LLM 核心技术：讲解 Transformer/Attention/KV Cache/RoPE 原理；实现采样与困惑度计算，绘制训练/推理数据流。
2. CO2｜完成小模型微调与量化部署：用 LoRA/QLoRA 完成 SFT 微调并量化为 int4，在 Apple Silicon/GPU 部署，评测集效果较基座提升 ≥10%。
3. CO3｜掌握系统化 Prompt 工程：设计 Few‑Shot/CoT/JSON Schema，构建 A/B 与自动化评估，效果提升 ≥15%。
4. CO4｜开发企业级 RAG 系统：Milvus Hybrid 检索 + Cross‑Encoder 重排，引用对齐与冷热分层，较纯生成 Faithfulness/Answer Relevance 提升 ≥20%。
5. CO5｜构建高可用 Agent：纯 Python 状态机实现多工具编排（ReAct/Plan‑Execute），端到端成功率 ≥85%，具备回放与故障恢复。
6. CO6｜开发生产级 FastAPI 服务：SSE 流式、鉴权、限流、可观测（日志/指标/追踪），本机 QPS ≥30，错误率 <1%。
7. CO7｜建立数据质量门控：用 pandas/polars 完成清洗与规则门控，拦截 ≥90% 已知脏样本，指标稳定提升。
8. CO8｜理解业务闭环：构建效果/效率/成本/风险指标树，设计灰度与回滚方案并完成业务汇报。

—

## 三、先修要求

| 必备技能 | 说明 |
|---|---|
| Python 编程 | 熟悉函数、类、模块、虚拟环境 |
| Linux/终端 | 常用命令（cd/ls/vim/git） |
| 英语阅读 | 能读英文文档与报错信息 |
| 数学基础 | 概率/线性代数基本概念 |

可选加分：有 FastAPI/Web 经验、基础 ML 知识、Docker 使用经验。

—

## 四、职业路径与薪资（参考）

岗位：AI 应用工程师、Prompt 工程师、RAG 开发工程师、AI 产品工程师。  
一线城市参考：初级 15–25K/月；中级 25–40K/月；高级 40–60K/月。

—

## 五、课程内容与学时分配（总计 96h）

说明：统一采用“每模块 12 小时（讲解 4h + 实践 8h）”的结构与口径。

### 模块 1（12h）：Python 工程化与 FastAPI 服务端开发（CO6）
- 教学内容（4h）：
  - 工程化：uv/Poetry、Ruff、MyPy、pytest、`src/` 布局、`pyproject.toml`
  - FastAPI：路由、依赖注入、Pydantic 校验、异常处理
  - SSE 流式；异步与并发（asyncio、超时、重试）
  - 可观测：结构化日志、OpenTelemetry、Prometheus
- 实践项目（8h）：
  - Lab 1.1：实现 `/chat` SSE 流式接口
  - Lab 1.2：API Key 鉴权与 IP 限流
  - Lab 1.3：结构化日志与 `/metrics` 指标
- 验收标准：`/chat` + `/health` 正常；QPS ≥30；覆盖率 ≥70%；Ruff/MyPy 无错误。

### 模块 2（12h）：LLM 基础原理与推理优化（CO1）
- 教学内容（4h）：
  - Transformer：Self‑Attention、Multi‑Head、RoPE、残差与归一化
  - 推理优化：KV Cache、Flash Attention、Continuous Batching
  - 训练范式：Pretrain/SFT/DPO/RLHF；量化：int8/int4、GGUF、PTQ vs QAT
  - 采样策略：Temperature/Top‑p/Top‑k，困惑度（PPL）
- 实践项目（8h）：
  - Lab 2.1：实现 Temperature + Top‑p 采样
  - Lab 2.2：计算 PPL 并对比模型
  - Lab 2.3：绘制训练/推理数据流（Mermaid）
- 验收标准：10 分钟讲解 Attention/KV Cache；代码通过单测；1 页 A4 数据流图。

### 模块 3（12h）：小模型微调（SFT/LoRA/QLoRA）（CO2）
- 教学内容（4h）：
  - 数据准备：JSONL、分词与模板、去重与质量过滤
  - PEFT：LoRA/QLoRA 原理与超参；Trainer API 与监控
  - 量化与部署：bitsandbytes、MLX（Apple Silicon）
- 实践项目（8h）：
  - Lab 3.1：清洗 1k 条指令数据为 JSONL
  - Lab 3.2：用 LoRA 微调小模型并评测
  - Lab 3.3：int4 量化并本地推理
- 验收标准：评测集效果 ≥ 基座 +10%；int4 成功推理、显存 <8GB；复现文档齐全。

### 模块 4（12h）：Prompt Engineering 系统化方法（CO3）
- 教学内容（4h）：
  - 模式库：System Prompt、Few‑Shot、CoT、ReAct
  - 结构化输出：JSON Schema + Pydantic 验证，容错与纠偏
  - 自动化评估与 A/B 设计：LLM‑as‑Judge、规则评估、人机混合
- 实践项目（8h）：
  - Lab 4.1：两套 Prompt 模板设计与迁移
  - Lab 4.2：离线评估与对比报告
- 验收标准：模板 B 相对 A 提升 ≥15%；可迁移；含失效案例分析。

### 模块 5（12h）：RAG 全链路开发（Milvus）（CO4）
- 教学内容（4h）：
  - 文档预处理：分块策略（固定/递归/语义）、Embedding 选择（bge‑m3）
  - Milvus：Schema、索引（HNSW/IVF）、过滤表达式与向量度量
  - Hybrid 检索：Dense + Sparse（BM25/TF‑IDF）+ RRF 融合；Cross‑Encoder 重排
  - 引用对齐与冷热分层策略
- 实践项目（8h）：
  - Lab 5.1：`/ingest` 文档导入接口
  - Lab 5.2：`/ask` Hybrid + Rerank + 引用对齐
  - Lab 5.3：用 Ragas 评估 RAG 效果
- 验收标准：Faithfulness/Answer Relevance ≥ +20%；P99 <500ms；支持冷热分层。

### 模块 6（12h）：Agent 编排（纯 Python 状态机）（CO5）
- 教学内容（4h）：
  - 范式：ReAct、Plan‑Execute、状态机；工具调用与参数校验
  - 记忆管理：短/长期记忆、压缩（摘要/滑窗）
  - 容错：超时/重试/回退与降级；任务回放日志（JSON Lines）
- 实践项目（8h）：
  - Lab 6.1：多工具 Orchestrator（检索 + API + 计算器）
  - Lab 6.2：故障注入测试（超时/失败/降级）
- 验收标准：端到端成功率 ≥85%；异常可降级；回放可复现每个决策点。

### 模块 7（12h）：数据分析与清洗（CO7）
- 教学内容（4h）：
  - Profiling：pandas‑profiling，缺失/唯一值/分布
  - 质量门控：Great Expectations 规则与自动化
  - 清洗：异常值（Z‑score/IQR）、去重（精确/模糊）、填充策略；分布对齐与增强
- 实践项目（8h）：
  - Lab 7.1：构建质量门控并重跑训练/检索对比
- 验收标准：门控拦截 ≥90% 已知脏样本；指标稳定提升并提交报告。

### 模块 8（12h）：业务理解与上线闭环（CO8）
- 教学内容（4h）：
  - PRD 解读与优先级；技术可行性评估
  - 指标体系：效果/效率/成本/风险的指标树与北极星指标
  - 灰度与回滚：分流策略、AB 实验与应急预案；成本建模与优化（Token/存储/推理）
- 实践项目（8h）：
  - Lab 8.1：灰度方案设计与成本模型
  - Lab 8.2：准备 Capstone 答辩材料（PRD/指标/成本/灰度/回放/评估）
- 验收标准（Capstone）：15 分钟讲解 + 5 分钟 Q&A；Demo 功能完整无重大 Bug；材料齐全。

—

## 六、教学方法与策略

| 环节 | 时间占比 | 形式 |
|---|---|---|
| 理论讲解 | 20% | 直播/录播 + PPT |
| 案例分析 | 20% | 错误案例库/最佳实践 |
| 动手实操 | 40% | Lab + 代码审阅 |
| 项目复盘 | 20% | 分享会 + Q&A |

—

## 七、技术与环境

### 7.1 技术栈（避免黑盒）

| 类别 | 技术选型 | 版本 |
|---|---|---|
| 编程语言 | Python | 3.11+ |
| 包管理 | uv | latest |
| API 框架 | FastAPI | 0.115+ |
| 向量库 | Milvus | 2.4+ |
| Embedding | Sentence‑Transformers（bge‑m3） | 3.0+ |
| 重排 | Cross‑Encoder（bge‑reranker‑base） | - |
| 微调 | Transformers + PEFT | 4.45+ / 0.12+ |
| 量化 | bitsandbytes / MLX | - |
| 测试 | pytest | 8.0+ |
| Linter | Ruff | 0.6+ |
| 类型检查 | MyPy | 1.11+ |
| RAG 评估 | Ragas | 0.1+ |
| 可观测 | OpenTelemetry + Prometheus | 1.26+ |

不使用：LangChain、LlamaIndex 等高度封装框架。

### 7.2 硬件要求与云服务

| 配置 | 最低 | 推荐 |
|---|---|---|
| CPU | 4 核 | 8 核 |
| 内存 | 16GB | 32GB |
| 存储 | 100GB | 256GB SSD |
| GPU | - | Apple Silicon 或 NVIDIA RTX 3060+ |

云服务（资源不足时）：AutoDL/恒源云（A100，约 3 元/小时）、Zilliz Cloud（Milvus 托管）、OpenAI/百炼/智谱 API。

—

## 八、考核与评估

### 8.1 评估结构

| 类型 | 权重 | 形式 |
|---|---|---|
| 过程性评估 | 60% | 每模块 Lab 与代码审阅 |
| 终结性评估 | 40% | Capstone 答辩 + 作品集 |

### 8.2 过程性评估（60 分）

| 模块 | 交付物 | 评分要点 | 分值 |
|---|---|---|---|
| 1 | FastAPI 服务 | 功能/性能/测试/质量 | 8 |
| 2 | 图解 + 代码 | 讲解清晰/正确性 | 6 |
| 3 | 微调报告 | 效果/复现 | 10 |
| 4 | Prompt 报告 | A/B 与迁移 | 8 |
| 5 | RAG 系统 | 指标/性能 | 10 |
| 6 | Agent 系统 | 成功率/容错 | 10 |
| 7 | 清洗报告 | 门控质量/提升 | 8 |

### 8.3 终结性评估（40 分）

| 维度 | 评分标准 | 分值 |
|---|---|---|
| 作品质量 | 3 个项目完整、代码规范、文档齐全 | 15 |
| 指标达成 | RAG +20%、Agent 85%、QPS 30 | 10 |
| 答辩表现 | 逻辑清晰、表达流畅、回答准确 | 10 |
| 创新性 | 独特优化或扩展功能 | 5 |

### 8.4 等级标准

| 等级 | 总分 | 要求 |
|---|---|---|
| 不及格 | <60 | - |
| 及格 | 60–69 | 基本完成所有 Lab |
| 良好 | 70–84 | 通过所有验收标准 |
| 优秀 | 85–100 | 指标达标 + 答辩优秀 + 创新 |

—

## 九、课程产出（Portfolio）

1. 企业知识库 RAG 系统：Milvus + bge‑m3 + bge‑reranker + FastAPI；指标：Faithfulness/Answer Relevance +20%、P99 <500ms。
2. 多工具 Agent 编排：纯 Python 状态机 + ReAct/Plan‑Execute；成功率 ≥85%，具备回放与降级。
3. 小模型微调与量化：Transformers + PEFT + bitsandbytes/MLX；效果 +10%，显存 <8GB，可复现。

—

## 十、能力评估矩阵（节选）

| 能力项 | Level 1 | Level 3 | Level 5（达标） |
|---|---|---|---|
| LLM 原理 | 复述 Transformer | 解释 Attention/KV Cache | 画数据流并做训练/推理权衡 |
| 模型微调 | 跑通示例 | 完成一次 SFT | 完整训练‑评估‑部署，+10%，int4 量化，复现文档 |
| Prompt | 写基础 Prompt | Few‑Shot/CoT/JSON | 自动化评估与 A/B，迁移到新任务 |
| RAG | Top‑K 检索 | Hybrid + Rerank + 引用 | +20%，冷热分层，P99 <500ms |
| Agent | 单工具 | 多工具编排 | 成功率 ≥85%，超时/重试/回退，回放完整 |
| 服务端 | 简单 API | SSE + 鉴权 | QPS ≥30、错误率 <1%，日志/指标/限流/灰度 |
| 数据清洗 | 手工清洗 | 脚本规则 | 门控体系拦截 ≥90%，指标有证明 |
| 业务理解 | 功能导向 | 写 PRD | 指标树 + ROI + 灰度方案 |

—

## 十一、学习资源与数据集

必读：
- Attention Is All You Need（Transformer）
- LoRA: Low‑Rank Adaptation
- FastAPI 官方文档
- Milvus 官方文档

推荐：
- The Illustrated Transformer
- Prompt Engineering Guide
- Ragas 文档

数据集：BELLE 指令（SFT）、MS MARCO（RAG 评估）、HotpotQA（多跳/Agent）。

—

## 十二、团队与版本

**课程负责人**：[你的名字]  
**教学团队**：[团队成员]  
**技术顾问**：[行业专家]

**版本历史**：
- v2.1（2025‑10‑02）：统一学时至 96h；命名口径（CO）；整合方法论与模块内容；明确技术栈版本与验收指标。
- v2.0（2025‑10）：首版对外发布。

**版权**：CC BY‑NC‑SA 4.0  
**联系方式**：[课程网站]｜[GitHub]｜[Issues]｜[邮箱/社群]

—

> 本最终大纲为对外版本；内部“技能分析与课程设计方案”用于教研与持续迭代，不随课件公开。

