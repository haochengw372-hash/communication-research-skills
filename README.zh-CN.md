> 使用请引用：Haocheng Wang (2026). *Communication Research Skills for Codex*. https://github.com/haochengw372-hash/communication-research-skills。机器可读引用信息见 [`CITATION.cff`](CITATION.cff)。引用属于学术署名请求，不是 Apache-2.0 的额外使用条件。

# Communication Research Skills for Codex（计算传播学版）

面向传播学与计算传播学研究的可维护 Codex Skill 套件。它和通用 CS / 计算社科 / 生物类科研 Skill 的区别在于：所有研究请求都先经过一条传播学推理链——现象 → 文献 → 理论 → 构念 → 机制 → RQ/H → 操作化 → 测量 → 设计/识别 → 证据 → 理论贡献——并强制执行七道领域门禁。

## 套件内容

`skills/` 下共有 18 个可直接安装的 Skill，一个目录对应一个 Skill：

| Skill | 作用 |
|---|---|
| `communication-research-workflow` | 编排器：controller/executor/auditor、任务契约、窗口计划、门禁与路由 |
| `communication-literature` | 传播学文献检索、筛选、证据矩阵 |
| `communication-theory` | 理论-机制匹配与竞争解释审计 |
| `communication-construct` | 构念查重、消歧与定义锁定 |
| `communication-scale` | 已发表量表、跨文化改编、CFA 与测量不变性 |
| `communication-method-router` | 先定研究目标再选方法 |
| `communication-experiment` | 问卷/在线/HMC/AI 披露类实验设计 |
| `communication-content-analysis` | 语料、编码本、人机编码、信度与验证 |
| `communication-network-analysis` | 图边界、社群、扩散、ERGM、SAOM、关系事件 |
| `communication-causal-inference` | 估计量、DAG、自然/准实验、诊断与敏感性分析 |
| `communication-temporal-analysis` | 时间序列、面板、事件史、生存与序列分析 |
| `communication-multimodal-analysis` | 图像、视频、音频、OCR/ASR、计算机视觉与多模态验证 |
| `communication-spatial-analysis` | GIS、地理编码、空间依赖、地理扩散与地图完整性 |
| `communication-simulation` | ABM、观点动力学、生成式/LLM 智能体校准与验证 |
| `communication-writing` | 传播学/社会科学的证据写作、修订、同步、rebuttal 与终稿 |
| `communication-prose-revision` | 减少模板化与防御性表达，同时保持科学含义并拒绝检测规避 |
| `communication-reviewer` | 七道门禁式评审与审计输出 |
| `scholarly-access` | 合规的五层全文获取与归档 |

## 研究流程

```mermaid
flowchart LR
    P["现象"] --> L["文献"]
    L --> T["理论"]
    T --> C["构念"]
    C --> M["机制"]
    M --> R["RQ / 假设"]
    R --> O["操作化"]
    O --> S["测量"]
    S --> D["设计 / 识别"]
    D --> E["证据"]
    E --> G["理论贡献"]
```

七道门禁分布在该链条上：理论、构念、测量、设计/识别、新颖性、贡献、证据-结论一致性。每道门禁由对应域 Skill 负责，编排器在下一次跳转前强制执行。

## 安装

把整个套件装进 Codex Skills 目录：

```bash
scripts/install.sh                 # 安装到 ~/.codex/skills
scripts/install.sh --dest /tmp/x   # 安装到测试目录
scripts/uninstall.sh               # 移除已安装的十八个文件夹
```

手动安装等价：把 `skills/` 下的每个文件夹复制到 `~/.codex/skills/<folder-name>/`。安装后需要刷新或重启 Codex，新 Skill 才会出现在目录中。

编排器位于 `skills/communication-research-workflow/`，其余域 Skill 位于 `skills/` 下的同级文件夹。

## 快速开始

把真实研究请求交给编排器：

```text
$communication-research-workflow

只要做计划。题目：比较某一环境风险在两个数字平台上的责任框架如何随时间变化。
先分类研究目标，再选择方法；给出研究生命周期，路由专业 Skill，并列出进入分析前
必须通过的证据与测量门禁。
```

窄任务可直接调用域 Skill，例如 `$communication-theory`、`$communication-content-analysis`、`$communication-network-analysis`、`$communication-causal-inference`、`$communication-writing`，或带 DOI 清单调用 `$scholarly-access`。

## 项目控制层

长期项目不需要搬动已有文件。编排器沿用上游的非侵入式 `.codex-research/` 控制层：

```text
research-project/
├── 已有数据、代码、论文与产出
└── .codex-research/
    ├── project.yaml
    ├── state.yaml
    ├── windows.yaml
    ├── decisions.md
    ├── contracts/
    ├── handoffs/
    ├── audits/
    └── snapshots/
```

只有 controller 能写权威治理状态；executor 与 auditor 返回带哈希与最新验证的不可变交接包。

## 个性化与完整案例

通用 Skill 不内嵌个人研究默认值。私人偏好与项目特有信息应放在个人衍生 Skill 或项目 `AGENTS.md` 中，规则见 `references/personalization-guide.md`；角色与交接生命周期的完整案例见 `references/complete-case-study.md`。

## 统一方法论、CSS 层与 Demo

- `METHODOLOGY.md` 是套件落地的那一套统一方法论：推理链、七道门禁、目标先行的方法路由、证据-结论纪律、五层全文政策，以及端到端工作流。
- 计算社会科学位于传播学层之下。通用 CSS 理论锚点见 `skills/communication-theory/references/css-theory.md`，通用 CSS 方法族见 `skills/communication-method-router/references/css-methods.md`。
- `demo/RESEARCH_DEMO.md` 提供三个合成、可替换的通用示例，分别覆盖计算内容分析、网络/扩散分析和传播实验；`demo/plans/` 展示 archetype 级窗口图，不内嵌某个项目、题目或私人语料。网络、因果、时间、多模态、空间与仿真均有独立的专业 Skill。

## 许可证

Haocheng Wang 的原创贡献采用 Apache-2.0。上游衍生部分保留原 MIT
版权及许可声明，具体范围、署名与方法学启发来源见 `LICENSE` 与 `NOTICE.md`。
