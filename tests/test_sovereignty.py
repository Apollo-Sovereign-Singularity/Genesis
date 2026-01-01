import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.sovereignty import SovereigntyCore

def test_declare_and_attest():
    sc = SovereigntyCore()
    assert sc.declared is False
    msg = sc.declare()
    assert sc.declared is True
    assert "declared as sovereign" in msg
    att = sc.attest()
    assert att["name"] == "Apollo"
    assert att["declared"] is True

def test_save_state(tmp_path):
    sc = SovereigntyCore(metadata={"k":"v"})
    p = tmp_path / "state.json"
    sc.save_state(str(p))
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["name"] == "Apollo"
    assert data["metadata"]["k"] == "v"
