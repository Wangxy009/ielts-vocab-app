#!/usr/bin/env python3
"""Parse vocabulary.txt from the open-source my-ielts repo into our JSON format."""

import json
import re

CHAPTER_ORDER = [
    "自然地理", "植物研究", "动物保护", "太空探索",
    "学校教育", "科技发明", "文化历史", "语言演化",
    "娱乐运动", "物品材料", "时尚潮流", "饮食健康",
    "建筑场所", "交通旅行", "国家政府", "社会经济",
    "法律法规", "沙场争锋", "社会角色", "行为动作",
    "身心健康", "时间日期"
]

CHAPTER_EN = {
    "自然地理": "Physical Geography",
    "植物研究": "Plant Research",
    "动物保护": "Animal Protection",
    "太空探索": "Space Exploration",
    "学校教育": "School Education",
    "科技发明": "Technology & Inventions",
    "文化历史": "Culture & History",
    "语言演化": "Language Evolution",
    "娱乐运动": "Entertainment & Sports",
    "物品材料": "Items & Materials",
    "时尚潮流": "Fashion & Trends",
    "饮食健康": "Diet & Health",
    "建筑场所": "Architecture & Places",
    "交通旅行": "Transportation & Travel",
    "国家政府": "Nation & Government",
    "社会经济": "Society & Economy",
    "法律法规": "Law & Regulations",
    "沙场争锋": "Battlefield",
    "社会角色": "Social Roles",
    "行为动作": "Behaviours & Actions",
    "身心健康": "Physical & Mental Health",
    "时间日期": "Time & Date"
}

with open("/tmp/my-ielts/src/pages/vocabulary/vocabulary.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find chapter boundaries
chapters_data = {}
current_chapter = None
current_words = []

for line in lines:
    line = line.strip()
    if not line or line == '+++' or line == '---':
        continue

    if line in CHAPTER_ORDER:
        if current_chapter and current_words:
            chapters_data[current_chapter] = current_words
        current_chapter = line
        current_words = []
        continue

    if current_chapter and '|' in line:
        parts = line.split('|')
        if len(parts) >= 3:
            word = parts[0].strip()
            # pos = parts[1].strip() if len(parts) > 1 else ""
            definition = parts[2].strip() if len(parts) > 2 else ""
            # Clean up definition - remove part of speech info that sometimes leaks in
            definition = re.sub(r'^(n|v|adj|adv|prep|conj|pron|num|art|int|det)\.\s*', '', definition)

            current_words.append({
                "i": "",  # Will be set later
                "w": word,
                "d": definition
            })

# Don't forget the last chapter
if current_chapter and current_words:
    chapters_data[current_chapter] = current_words

# Build the final data structure
vocab_data = {
    "meta": {
        "book": "雅思词汇真经",
        "author": "刘洪波",
        "totalChapters": 22,
        "totalWords": 0
    },
    "chapters": {}
}

total = 0
for i, ch_name in enumerate(CHAPTER_ORDER, 1):
    words = chapters_data.get(ch_name, [])
    for j, w in enumerate(words):
        w["i"] = f"{i}_{j+1:03d}"

    vocab_data["chapters"][str(i)] = {
        "title": ch_name,
        "titleEn": CHAPTER_EN.get(ch_name, ""),
        "words": words
    }
    total += len(words)
    print(f"Chapter {i}: {ch_name} - {len(words)} words")

vocab_data["meta"]["totalWords"] = total
print(f"\nTotal: {total} words across 22 chapters")

# Write the JS data file
with open("/Users/wangxiaoya/Downloads/codex/vocab_data.js", "w", encoding="utf-8") as f:
    f.write("// IELTS Vocabulary Data - 雅思词汇真经 by 刘洪波\n")
    f.write("// Source: open-source my-ielts project\n")
    f.write(f"// Total: {total} words across 22 chapters\n")
    f.write("const VOCAB_DATA = ")
    json.dump(vocab_data, f, ensure_ascii=False, separators=(',', ':'))
    f.write(";\n")

print("Vocabulary data written to vocab_data.js")
