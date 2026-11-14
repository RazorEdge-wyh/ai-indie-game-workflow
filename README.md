# ai-indie-game-workflow

> A gate-based production workflow for AI-assisted indie game development.
> **The human decides. The AI reviews from a target-player and a picky-player perspective (no invented personas) plus a light scope check. Every step ends with a freeze card.**

一个给 AI 编码代理用的「独立游戏串行闸门」skill。不是教你"用 AI 做游戏"的教程，而是一套**约束 AI、逼人拍板、每步留下证据**的工作流。

## 为什么需要它

AI 让"生成"变便宜之后，独立游戏最容易死于三件事：范围膨胀、风格漂移、以及一堆"做完了但没人验"的内容。

这个 skill 用四个机制对抗它们：

| 机制 | 作用 |
|---|---|
| **串行闸门** | 一次只推进一个模块；上一步没冻结，不许开下一步 |
| **双视角评审** | AI 用目标玩家 / 挑剔玩家两种视角，再加一个轻量范围检查；不虚构角色，每轮 ≤400 字，禁止夸 |
| **A/B/C 决策分级** | 主题/玩法/结局/美术总调必须人定；小配角/占位文本 AI 自主，每周抽查 |
| **冻结卡** | 每步留半页纸：已定 / 待定 / 风险 / 下一步验证 / 签字；改已冻结内容必须开变更单 |

## 里面有什么

```
SKILL.md                    主指令：触发条件、五条铁律、双视角协议、决策分级、模块库
references/
  gates.md                  10 个模块的完整闸门卡（输入/产出/通过标准/失败模式/AI 边界）
  templates.md              冻结卡、变更单、state.md、决策流水、测试记录、资产台账
  prompts.md                P1–P8 提示词（评审、冻结、变更、C 级清单、美术方式二、叙事审查、类型预设）
  scaling.md                1–30 人适配：签字矩阵、会议节奏、人多人少的坑
  quality-bar.md            10 条质量红线、失败模式、发送前五问
scripts/
  init_workflow.py          在游戏项目里初始化 .gameworkflow/
  check_gates.py            校验闸门卡（缺章节 / 空章节 / 已定不足 / 待定没写何时定 / 无 A 级签字）
LICENSE                     Apache License 2.0（不是 MIT）
NOTICE                     版权与归属声明
```

## 安装

**DSH（本 skill 的原生环境）**

```bash
git clone https://github.com/<your-name>/ai-indie-game-workflow.git ~/.dsh/skills/ai-indie-game-workflow
```

Windows 下就是 `C:\Users\<you>\.dsh\skills\ai-indie-game-workflow`。用户级目录意味着**任何工作区的新对话都能加载它**；如果只想在某个项目里用，放到 `<项目>/.dsh/skills/`。

**Claude Code / Codex / Cursor 等其他代理**

把 `SKILL.md` 作为系统提示的一部分，或在 `AGENTS.md` / `CLAUDE.md` 里引用：

```markdown
## Game production workflow
Read `skills/ai-indie-game-workflow/SKILL.md` before planning any game work.
```

**任何 LLM**

直接把 `SKILL.md` 正文贴进系统提示；参考资料按需加载。

## 快速开始

```bash
# 1. 在游戏项目里初始化
python scripts/init_workflow.py /path/to/your-game --preset narrative

# 2. 从 G0 开始：让代理按双视角协议问 3–5 个问题
# 3. 你回答后，写 .gameworkflow/gates/G0.md
# 4. 自检
python scripts/check_gates.py /path/to/your-game
```

`--preset` 四选一：

| preset | 顺序 | 适合 |
|---|---|---|
| `narrative` | G0 → N → A → L → C → P → T? → V → M → R | 恐怖 / 冒险 / RPG |
| `gameplay` | G0 → C → A → L → P → N? → V → M → R | 消消乐 / Roguelike / 竞技 |
| `experience` | G0 → A → N → L → P → C → V → M → R | 步行模拟 / 氛围向 |
| `multiplayer` | G0 → C → T → A → L → P → N? → V → M → R | 合作 / 派对 |

模块含义：G0 种子、N 叙事、A 美术基调、L 空间关卡、C 核心玩法、P 表现氛围、T 技术骨架、V 纵向小样、M 量产、R 收敛发布。

## 质量契约（写死在 skill 里）

- 每轮评审 **≤400 字**，冻结卡 **≤200 字**；
- 每轮必须有一句具体的「我担心……」，**禁止全肯定**；
- 一次只问 3–5 个问题，每个带选项和推荐；
- 不替用户写主线、不做大规模资产、不做技术架构评审；
- 不编造销量/数据/案例；
- 每步必须有落地物（文档 / 图 / 可走灰盒），只在对话里不算完成。

## 校验示例

```text
$ python scripts/check_gates.py ./my-game
Checking: ./my-game/.gameworkflow
Gate cards: 1 (G0.md)
Result: PASS
```

缺章节或没签字时会返回非零退出码，并列出具体问题；`--strict` 把警告也当错误。

## 开发与测试

```bash
python -m py_compile scripts/*.py
python scripts/init_workflow.py /tmp/demo
python scripts/check_gates.py /tmp/demo
```

脚本输出刻意保持 ASCII，避免中文终端/CI 乱码；游戏项目里的内容仍然是中文。

## 许可证

**Apache License 2.0**，不是 MIT。可以商用、修改、再分发，但需保留版权与 NOTICE，并附带许可证副本；同时包含专利授权条款。详见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)。

## 状态

v1.0.0，脚本已在 Windows + Python 3.12 实测：初始化、通过、缺章节失败、`--strict` 失败四种路径均验证。

## 贡献

欢迎提 issue / PR。改动请遵守两条：闸门卡保持"可被第三方检查"的通过标准；不要为了显得完整而增加无用的模块。
