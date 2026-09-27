from pathlib import Path
import json, zipfile
root=Path(__file__).parent
data=json.loads((root/'hoh_graph.json').read_text(encoding='utf-8'))
template=(root/'graph-viewer.template.html').read_text(encoding='utf-8')
out=root/'haus-ohne-hueter-interaktiv.html'
out.write_text(template.replace('__GRAPH_DATA__',json.dumps(data,ensure_ascii=False).replace('<','\\u003c')),encoding='utf-8')
with zipfile.ZipFile(root/'haus-ohne-hueter-teilen.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(out,out.name)
print(out)
