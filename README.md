# CS329Z 中文学习笔记

按 Stanford CS329Z: Engineering AI Agents（2026 年秋季）的课程顺序，把每一讲的内容写成中文的网站。内容根据课程主页 https://cs329z.stanford.edu/ 公开的材料整理，配图来自课程材料，版权属于课程的作者。

## 现在有哪些讲

| 讲次 | 主题 | 页数 |
|---|---|---|
| 第 1 讲 | 导论：什么是 agent 系统 | 8 |
| 第 2 讲 | 给搭建者讲的 LLM | 9 |
| 第 3 讲 | 检索增强生成（RAG） | 8 |
| 第 4 讲 | 工具使用和函数调用 | 7 |
| 第 5 讲 | 框架与编排 | 8 |
| 第 6 讲 | agent 的设计模式和运行框架 | 8 |
| 第 7 讲 | agent 的记忆架构 | 8 |
| 第 8 讲 | 多 agent 系统 | 7 |
| 第 9 讲 | 优化 | 8 |
| 第 10 讲 | 嘉宾讲座：Terminal-Bench | 5 |
| 第 11 讲 | agent 需要什么数据 | 8 |
| 第 12 讲 | 数据的挑选和质量 | 7 |
| 第 13 讲 | 评估基础与基准测试设计 | 6 |
| 第 15 讲 | 用语言模型当评审，以及评估的基础设施 | 8 |

第 14 讲是一次对谈，没有可整理的材料。第 16 讲之后的材料发布后再补。

## 每一讲怎么写

- 像教材一样直接陈述内容。正文里不提讲义、幻灯片、讲者，也不写讲义页码。每页最后有一行小字说明内容和配图的来源，这一行来自 `lecture.json` 的 `credit`。
- 先定一句话的主线，每个页面回答一个问题。
- 事实和数字给出处链接。原始材料说得含糊或不准确的地方，直接写核对过的事实。估算的数写明「粗略估算」，没有查到的写明「论文里没有找到」。
- 三种颜色的框：蓝色是说明和提醒，绿色是延伸的资料（带出处链接），橙色是常见的说法和事实对不上的地方。
- 数字放在带完整列名的表格里，或者写成完整的句子。
- 有课程视频的讲次，用字幕补上口头讲的内容，同样直接写成正文。

## 目录

- `course.json`：首页的课程列表。某一讲整理好之后，给它加上 `"dir": "lectureNN"`。
- `lectures/lectureNN/lecture.json`：这一讲的导航、每页的标题和导语，以及页面最后那行来源说明。
- `lectures/lectureNN/content/*.html`：各页的正文，改这里。
- `lectures/lectureNN/img/pNN.jpg`：正文用到的配图。
- `assets/`：全站共用的样式和脚本。
- `build.py`：把上面这些生成到 `_site/`。
- `scripts/pdf_extract.py`：把课程 PDF 的每一页转成图片并提取文字，输出到 `src/`（不进仓库）。
- `scripts/check_site.py`：检查生成的网站里所有站内链接、锚点和图片。
- `scripts/check_text.py lectureNN`：检查一讲的正文有没有违反写法规则（提到讲义、破折号、强行对比的句式等）。
- `scripts/render_check.py`：在无界面的 Chromium 里打开一讲的每一页，报告脚本错误、坏图和超出边框的表格。
- `scripts/vtt_to_text.py`：把视频字幕文件转成带时间标记的纯文本。

正文里插图的写法：`{{fig 13 | 说明}}` 或 `{{figs 18 19 | 说明}}` 会插入 `img/p13.jpg` 这样的配图，说明文字原样显示。

## 怎么改和发布

```
python3 build.py
python3 scripts/check_site.py
python3 scripts/check_text.py lecture13
```

只构建一讲到单独的目录：`python3 build.py --out /tmp/out lecture13`。

推送之后，GitHub Actions 会重新生成并发布到 GitHub Pages。
