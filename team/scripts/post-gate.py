#!/usr/bin/env python3
"""CLI entry point for the hard pre-post gate. Logic lives in post_gate.py (importable). Exit 0 = allowed, 2 = refused."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from post_gate import main
sys.exit(main())
