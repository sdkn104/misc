"""
openai_sub.yaml内で$ref:で記述されているパスの末尾セルをm.txtに出力する。
次にopenai_sub.yamlのcomponentsのschemasの要素で、m.txtに記載された名前と一致しないものを削除する。
以上を行うpythonコードを生成して。
"""

import yaml
import re

yaml_file = "openapi_sub.yaml"
m_file = "m.txt"
output_yaml = "openapi_sub_filtered.yaml"

# 1. $ref: のパス末尾セルを m.txt に出力
ref_names = set()
ref_pattern = re.compile(r'\$ref:\s*["\']?#/components/schemas/([^"\']+)["\']?')

with open(yaml_file, "r", encoding="utf-8") as f:
    for line in f:
        match = ref_pattern.search(line)
        if match:
            ref_names.add(match.group(1))
            print(match.group(1))

with open(m_file, "w", encoding="utf-8") as f:
    for name in sorted(ref_names):
        f.write(f"{name}\n")

# 2. m.txtに記載された名前と一致しないものを削除
with open(m_file, "r", encoding="utf-8") as f:
    valid_names = set(line.strip() for line in f if line.strip())

with open(yaml_file, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

schemas = data.get("components", {}).get("schemas", {})
if schemas:
    for name in list(schemas.keys()):
        if name not in valid_names:
            del schemas[name]

with open(output_yaml, "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True, sort_keys=False)