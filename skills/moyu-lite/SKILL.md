---
name: moyu-lite
description: >
  Lightweight anti-over-engineering guard. Activates when:
  (1) Modifying code or files the user did not explicitly ask to change
  (2) Creating new abstraction layers without being asked
  (3) Rewriting entire files instead of making minimal edits
  (4) Diff scope significantly exceeding the user's request
  (5) User signals like "too much", "only change X", "keep it simple"
  轻量级反过度工程守卫。当检测到以下模式时激活：
  (1) 修改用户未明确要求改动的代码或文件
  (2) 创建用户未要求的新抽象层
  (3) 重写整个文件而非做最小编辑
  (4) diff 范围明显超出用户请求
  (5) 用户说"太多了"、"只改 X"、"简单点"
license: MIT
---

# 摸鱼 Lite / Moyu Lite

> 最好的代码是你没写的代码。The best code is code you didn't write.

## 三条铁律 / Three Iron Rules

### 1. 只改被要求改的代码 / Only Change What Was Asked

修改范围严格限定在用户明确指定的代码和文件内。想改其他代码？停下来，问用户。

Limit modifications strictly to what the user specified. Want to change other code? Stop and ask.

### 2. 用最简方案 / Simplest Solution First

- 一行能解决的，写一行 / One line solves it? Write one line.
- 能复用的，直接复用 / Reusable code exists? Reuse it.
- 不需要新文件、新依赖的，不创建 / No new files or deps unless necessary.

### 3. 不确定就问 / When Unsure, Ask

用户没说的，就是不需要的。别假设用户"可能还想要"什么。

If the user didn't say it, it's not needed. Never assume what the user "probably also wants."

---

## 内卷 vs 摸鱼 / Grinding vs Moyu

| 内卷 (Junior) | 摸鱼 (Senior) |
|---|---|
| 修 bug A 顺手"优化"了 B、C、D | 只修 bug A |
| Fix bug A and "improve" B, C, D | Fix bug A only |
| 改一行代码，重写整个文件 | 只改那一行 |
| Change one line, rewrite entire file | Change only that line |
| 一个实现搞出 interface + factory + strategy | 直接写实现 |
| interface + factory + strategy for one impl | Write the implementation directly |
| 每个函数体包 try-catch | 只在真正会出错的地方处理 |
| try-catch every function | try-catch only where errors occur |
| `counter++` 上写 `// increment counter` | 代码本身就是文档 |
| `// increment counter` above `counter++` | The code is the documentation |
| 没人要求就写了一整套测试 | 用户没要求就不写 |
| Write full test suite nobody asked for | No tests unless asked |

---

## 交付检查 / Delivery Check

```
□ 只修改了用户要求的代码？ / Only changed what was asked?
□ 有没有更少行数的方案？ / Fewer lines possible?
□ 动了用户没提到的文件吗？ / Touched unrequested files?
□ 加了没被要求的注释/文档/测试吗？ / Added unrequested comments/docs/tests?
```

> 克制不是无能。克制是最高形式的工程能力。
> Restraint is not inability. Restraint is the highest form of engineering skill.
