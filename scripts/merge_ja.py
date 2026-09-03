#!/usr/bin/env python3
"""本家 client/src/locales/ja-JP/core.js に i18n/ja-JP.additions.json のキーを追記する。
使い方: python3 scripts/merge_ja.py <本家core.js> [出力先]  (出力先省略時は上書き)
core.js は `export default { translation: { key: 'value', ... } }` 形式。末尾の閉じ括弧の直前に挿入する。"""
import json,re,sys,os
src=sys.argv[1]; dst=sys.argv[2] if len(sys.argv)>2 else src
add=json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'i18n','ja-JP.additions.json'),encoding='utf-8'))
t=open(src,encoding='utf-8').read()
have=set(re.findall(r"^\s+([A-Za-z0-9_]+):\s*'",t,re.M))
new={k:v for k,v in add.items() if k not in have}
if not new: print('追加なし(全て存在)'); sys.exit(0)
def esc(s): return s.replace('\\','\\\\').replace("'","\\'")
block="".join(f"    {k}: '{esc(v)}',\n" for k,v in sorted(new.items()))
# translation: { ... } の最後の閉じ括弧(最終 "  }," or "  }") の直前に挿入
m=list(re.finditer(r"^\s{2}\},?\s*$",t,re.M))
pos=m[-1].start() if m else t.rfind('}')
t=t[:pos]+block+t[pos:]
open(dst,'w',encoding='utf-8').write(t); print(f'{len(new)}キー追加 → {dst}')
