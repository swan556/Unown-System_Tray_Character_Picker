import json
import pandas as pd
from collections import defaultdict

TAG_TO_EMOTION = {
    # Positive
    "happy": {"happy"},
    "smiling": {"happy"},
    "blush": {"happy", "shy"},
    "sparkles": {"happy", "excited"},

    # Negative
    "sad": {"sad"},
    "crying": {"sad"},
    "anger": {"angry"},

    # Romance
    "heart": {"love"},
    "kiss": {"love"},
    "hug": {"love", "comfort"},

    # Excitement
    "dancing": {"excited"},
    "music": {"excited"},

    # Confidence / Attitude
    "smirk": {"smug"},
    "middle finger": {"angry", "rude"},
    "gun": {"aggressive"},
    "fight": {"aggressive"},
    "flex": {"confident"},

    # Thinking
    "shrug": {"confused"},
    "pointing": {"thinking"},
    "writing": {"thinking"},

    # Cute
    "flower": {"cute"},
    "cat": {"cute"},
    "bear": {"cute"},
    "koala": {"cute"},
    "angel": {"cute"},
    "devil": {"mischievous"},

    # Misc
    "food": {"hungry"},
    "running": {"active"},
    "proposal": {"love"},
    "wand": {"magic"},
    "glasses": {"cool"},
    "lenny": {"mischievous"},
    "donger": {"meme"},
    "archery": {"action"},
    "cheerleader": {"excited"},
}

kaomoji_data = {}
with open("assets/emoticon_dict.json", 'r', encoding='utf-8') as f:
    kaomoji_data = json.load(f)

tag_buckets = defaultdict(list)

for kaomoji, info in kaomoji_data.items():
    if len(kaomoji) > 8:
        continue

    tags = info["new_tags"]

    for tag in tags:
        tag_buckets[tag].append({
            "char": kaomoji,
            "tags": tags
        })

def score(item):
    return (
        len(item["tags"]) * 10
        - len(item["char"]) * 0.5
    )
LIMITS = {
    "smiling": 80,
    "heart": 80,
    "sad": 60,
    "crying": 50,
    "anger": 50,
    "kiss": 40,
    "hug": 40,
    "blush": 60,
    "dancing": 30,
    "music": 20,
    "flower": 20,
    "sparkles": 20,
    "cat": 20,
    "bear": 20,
    "koala": 10,
    "pointing": 20,
    "shrug": 20,
    "running": 15,
    "food": 15,
    "gun": 15,
    "middle finger": 10,
}

selected = {}

for tag, items in tag_buckets.items():

    items.sort(key=score, reverse=True)

    limit = LIMITS.get(tag, 15)

    for item in items[:limit]:
        selected[item["char"]] = item

complete_data = pd.DataFrame(columns=['char', 'tags', 'cateogory'])

rows = []
for item in selected.values():
    rows.append({
        "char": item["char"],
        "tags": " ".join(item["tags"]),
        "category": "kaomoji"
    })

complete_data = pd.DataFrame(rows)

emoji_data = pd.read_csv('assets/full_emoji.csv', usecols=['emoji', 'name'])

emoji_data['cateogory'] = "emoji"
emoji_data.columns = ['char', 'tags', 'cateogory']

print(emoji_data.head())
complete_data = pd.concat([complete_data, emoji_data], ignore_index=True, axis=0)

complete_data.to_csv('assets/complete_data.csv')
print("successfully created complete data")