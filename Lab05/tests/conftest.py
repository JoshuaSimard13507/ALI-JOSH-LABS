import os
import sys
import pathlib
import builtins
import time
import pytest

@pytest.fixture(autouse=True)
def no_blocking_io(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    monkeypatch.setattr(time, "sleep", lambda *a, **k: None)


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

@pytest.fixture
def temp_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path

@pytest.fixture
def mock_print(monkeypatch):
    lines = []
    def fake_print(*args, **kwargs):
        lines.append(" ".join(str(a) for a in args))
    monkeypatch.setattr(builtins, "print", fake_print)
    return lines

@pytest.fixture
def fake_dice(values):
    from src.dice import Die
    dice = [Die() for _ in values]
    for d, v in zip(dice, values):
        d.value = v
    return dice

@pytest.fixture
def values():
    return lambda seq: seq
