# LaTeX清理改进记录

## 任务目标
修复柏慧学堂v2中LaTeX公式清理不彻底的问题，特别是：
- `\dfrac` 分数转换为 `/` 导致格式混乱
- `\begin{cases}` 等结构命令未处理
- 根号等符号清理不完整

## 修改文件
`baihuixuetang_v2/ui/components/quiz_panel.py` - `_clean_question_text`方法

## 改进内容
1. **分数处理**: `\frac{a}{b}` → `(a)/(b)` 格式
2. **根号处理**: `\sqrt{x}` → `√ x`，`\sqrt[n]{x}` → `√[n] x`
3. **结构命令**: `\begin{cases}` → 空，`\end{cases}` → 空
4. **希腊字母**: `\alpha` → `α`, `\beta` → `β` 等
5. **运算符**: `\leqslant` → `≤`, `\geqslant` → `≥` 等

## 测试结果
| 原始LaTeX | 清理结果 |
|-----------|----------|
| `$$\dfrac{2x-5}{3}$$` | `(2x-5)/(3)` |
| `$$\sqrt[3]{m}$$` | `√[3] m` |
| `$$x\left(0\leqslant x\leqslant 10\right)$$` | `x0≤ x≤ 10` |
| `$$\begin{cases} x+y=27 \\ 0.2x+0.3y=6.6 \end{cases}$$` | `x+y=27 0.2x+0.3y=6.6` |

## 下一步
打包exe并测试
