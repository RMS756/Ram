"""Build the supplement of the sixth edition (DOCX + PDF) from supplement/SUPPLEMENT_R6.md and its own reference list.

usage: python3 REM_FINAL_SUBMISSION/thesis_r6/tools/build_supplement.py
Uses the pinned pandoc and LibreOffice of the main build; no page-number lists (the supplement is indexed by unit number).
"""
import os
import subprocess

import pypandoc

HERE = os.path.dirname(os.path.abspath(__file__))
TH = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(TH, '..', '..'))
SUP = os.path.join(TH, 'supplement')
md = open(os.path.join(SUP, 'SUPPLEMENT_R6.md'), encoding='utf-8').read() + '\n\n' + \
    open(os.path.join(SUP, 'REFERENCES_SUPPLEMENT.md'), encoding='utf-8').read()
tmp = os.path.join(TH, 'build', 'supplement_all.md')
open(tmp, 'w', encoding='utf-8').write(md)
out = os.path.join(SUP, 'REM_THESIS_R6_SUPPLEMENT.docx')
pypandoc.convert_file(tmp, 'docx', outputfile=out, extra_args=[
    '--reference-doc=' + os.path.join(TH, 'build', 'reference.docx'), '--resource-path=' + ROOT,
    '--metadata=title:Supplement to the Sixth Edition of the REM Thesis (indexed; R5 numbering with prefix S-)'])
prof = os.path.join(TH, 'build', 'lo_profile_supplement')
subprocess.run(['soffice', '-env:UserInstallation=file://' + prof, '--headless', '--convert-to', 'pdf', '--outdir', SUP, out],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=dict(os.environ, SAL_USE_VCLPLUGIN='svp'))
pdf = out[:-5] + '.pdf'
pages = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
print('supplement:', out, os.path.getsize(out), 'bytes;', [l for l in pages.split('\n') if l.startswith('Pages')])
