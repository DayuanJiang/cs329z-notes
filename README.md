# CS329Z 中文学习笔记

Stanford CS329Z: Engineering AI Agents（2026 年秋季）各讲讲义的中文学习笔记网站。讲义和视频来自课程主页 https://cs329z.stanford.edu/ ，版权属于讲者。

## 现在有哪些讲

| 讲次 | 主题 | 状态 |
|---|---|---|
| 第 8 讲 | 多 agent 系统 | 已整理，7 页 |
| 第 13 讲 | 评估基础与基准测试设计 | 已整理，6 页 |
| 第 1 至 7、9 至 12、15 讲 | 见 `course.json` | 待整理 |

## 每一讲怎么写

- 先定一句话的主线，每个页面回答一个问题。
- 讲义说的、论文原文说的、整理者自己的判断，在正文里分开写明。表格下面写清每一列来自哪里。
- 三种颜色的框：蓝色是对讲义内容的说明和提醒，绿色是讲义之外的资料（带出处链接），橙色是讲义的说法和后来的事实对不上的地方。
- 关键的页面插入讲义原图。数字放在带完整列名的表格里，或者写成完整的句子。
- 有课堂视频的讲次，用字幕补上讲者口头讲的内容。

## 目录

- `course.json`：首页的课程列表。某一讲整理好之后，给它加上 `"dir": "lectureNN"`。
- `lectures/lectureNN/lecture.json`：这一讲的导航和每页的标题、导语。
- `lectures/lectureNN/content/*.html`：各页的正文，改这里。
- `lectures/lectureNN/img/pNN.jpg`：正文用到的讲义原图。
- `assets/`：全站共用的样式和脚本。
- `build.py`：把上面这些生成到 `_site/`。
- `scripts/pdf_extract.py`：把讲义 PDF 的每一页转成图片并提取文字，输出到 `src/`（不进仓库）。
- `scripts/check_site.py`：检查生成的网站里所有站内链接、锚点和图片。

正文里的两个简写：

- `<section class="sec" id="x" data-p="7-15">` 会在小节标题右边显示「讲义第 7 至 15 页」。
- `{{slide 13 | 说明}}` 或 `{{slides 18 19 | 说明}}` 会插入对应页的讲义原图。

## 怎么改和发布

```
python3 build.py
python3 scripts/check_site.py
```

推送之后，GitHub Actions 会重新生成并发布到 GitHub Pages。
