import sys
import os
import importlib.util

_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'backend'))
sys.path.insert(0, _root)

_spec = importlib.util.spec_from_file_location("backend_main", os.path.join(_root, "backend", "main.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
app = _mod.app
