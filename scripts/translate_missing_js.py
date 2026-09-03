#!/usr/bin/env python3
"""planka client/src/locales/ja-JP/core.js に無いキーをローカルgemma4(think:false)で翻訳。ICU/{{x}}/{x}プレースホルダ逐語保持を検証。"""
import json,os,re,requests,sys,time
SRC=sys.argv[1]; DST=sys.argv[2]; URL=os.environ.get("OLLAMA_URL","http://localhost:11434")+"/api/generate"; MODEL="gemma4:12b-it-qat"
en={}; 
for ln in open(SRC,encoding='utf-8'):
    k,_,v=ln.rstrip('\n').partition('\t'); 
    if k: en[k]=v
PH=re.compile(r'\{\{?[^}]+\}\}?'); out={}; keys=list(en)
def ph(s): return sorted(PH.findall(s))
for i in range(0,len(keys),14):
    chunk={k:en[k] for k in keys[i:i+14]}
    prompt=("Translate these UI strings of a Kanban project app (PLANKA) from English to natural, concise Japanese for business users (です/ます). "
            "Keep placeholders like {{name}} or {count} EXACTLY. Keys ending with _title are headings; _body are sentences. Output ONLY a JSON object with the same keys.\n\n"+json.dumps(chunk,ensure_ascii=False,indent=1))
    for attempt in range(3):
        try:
            r=requests.post(URL,json={"model":MODEL,"prompt":prompt,"stream":False,"think":False,"format":"json","options":{"temperature":0.2,"num_predict":1800}},timeout=300).json()
            j=json.loads(r.get("response","{}"))
            ok={k:v for k,v in j.items() if k in chunk and isinstance(v,str) and v.strip() and ph(v)==ph(chunk[k])}
            out.update(ok); bad=[k for k in chunk if k not in ok]
            if not bad: break
            chunk={k:chunk[k] for k in bad}
        except Exception as e: print("retry",attempt,str(e)[:60],flush=True); time.sleep(3)
    print(f"{min(i+14,len(keys))}/{len(keys)} done={len(out)}",flush=True)
    json.dump(out,open(DST,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print("FINISHED",len(out),"/",len(keys))
