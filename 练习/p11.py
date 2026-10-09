# p11.py —— JSON：让字典和文字互相变身
import json

d = {"name": "龙", "age": 24}

# ① 字典 → 文字（打包）
print(json.dumps(d))
print(json.dumps(d, ensure_ascii=False))

# ② 文字 → 字典（拆包）
text = json.dumps(d, ensure_ascii=False)
back = json.loads(text)
print(back)
print(type(back))
print(back["name"])
