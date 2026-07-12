#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1];PORTFOLIO=ROOT/'images'/'portfolio';OUTPUT=ROOT/'data'/'gallery.json';EXT={'.jpg','.jpeg','.png','.webp','.avif'}
def humanize(s):
 t=re.sub(r'[-_]+',' ',s).strip();return t[:1].upper()+t[1:]
def meta(folder):
 f=folder/'product.json'
 if not f.exists(): return {}
 try:return json.loads(f.read_text(encoding='utf-8'))
 except json.JSONDecodeError as e:raise RuntimeError(f'Błędny JSON w {f}: {e}')
def rel(p):return p.relative_to(ROOT).as_posix()
def valid_model(value,name):
 value=str(value or '').strip()
 if not value:return ''
 f=ROOT/Path(value)
 if f.suffix.lower()!='.glb':print(f'OSTRZEŻENIE: {name}: model nie ma rozszerzenia .glb: {value}')
 if not f.is_file():print(f'OSTRZEŻENIE: {name}: nie znaleziono modelu: {f}');return ''
 return rel(f)
def build_gallery():
 if not PORTFOLIO.exists():raise RuntimeError(f'Nie istnieje katalog: {PORTFOLIO}')
 out=[]
 for folder in sorted(p for p in PORTFOLIO.iterdir() if p.is_dir()):
  m=meta(folder)
  if m.get('status','published')!='published':continue
  images=sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in EXT)
  model=valid_model(m.get('model',''),folder.name)
  if not images and not model:print(f'Pominięto {folder.name}: brak zdjęć i poprawnego modelu.');continue
  out.append({'slug':folder.name,'title':m.get('title',humanize(folder.name)),'category':m.get('category','Realizacje'),'description':m.get('description',''),'featured':bool(m.get('featured',False)),'order':int(m.get('order',9999)),'cover':rel(images[0]) if images else '','images':[rel(i) for i in images],'model':model})
 out.sort(key=lambda i:(i['order'],i['title'].lower()));return out
def main():
 try:
  g=build_gallery();OUTPUT.parent.mkdir(parents=True,exist_ok=True);OUTPUT.write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8');print(f'Gotowe: {OUTPUT}');print(f'Liczba opublikowanych produktów: {len(g)}');return 0
 except Exception as e:print(f'Błąd: {e}',file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
