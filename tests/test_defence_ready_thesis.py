"""The defence-ready thesis edition: printed numbers match the raw-record recomputation, and assembly is clean."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'REM_DEFENCE_READY_THESIS'

pytestmark = pytest.mark.skipif(not (D / 'src' / 'CHAPTER_04_FINAL.md').exists(), reason='defence-ready sources not assembled')


def test_printed_numbers_match_recomputation():
    r = subprocess.run([sys.executable, str(D / 'tools' / 'check_thesis_numbers.py')], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    out = json.loads((D / 'audit' / 'thesis_number_check.json').read_text())
    assert out['cells_checked'] >= 150 and out['mismatches'] == []


def test_assembly_reported_no_problems():
    assert (D / 'audit' / 'r9_check.txt').read_text().strip() == 'no problems'


def test_five_layers_and_no_live_claim():
    ch4 = (D / 'src' / 'CHAPTER_04_FINAL.md').read_text(encoding='utf-8')
    assert '## 4.4 Comparison with Existing Security Frameworks' in ch4
    assert '## 4.5 Ablation Study of the REM Layers' in ch4
    assert 'sixth layer' not in ch4.replace('no sixth layer', '')
    assert '**No experiment with a live agent or a language model was executed, and no result in this chapter is a live result.**' in ch4


def test_status_page_claims_no_approval():
    fm = (D / 'text_front' / 'front_matter.md').read_text(encoding='utf-8')
    assert 'It has not been formally approved, and no approval is implied.' in fm


def test_no_prevented_672_misstatement_and_no_22_backbones():
    import re
    texts = [p.read_text(encoding='utf-8') for p in list((D / 'src').glob('*.md')) + list((D / 'text_front').glob('*.md'))]
    joined = '\n'.join(texts)
    assert '672 prevented' not in joined and '661 of the 672 attacks that REM' not in joined
    assert not re.search(r'\b22 (recorded )?backbones', joined)
    assert 'ablated as whole functional units' not in joined
