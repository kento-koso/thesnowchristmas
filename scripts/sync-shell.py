#!/usr/bin/env python3
"""Compatibility entry point. The full build now owns shared HTML and asset versions."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('build.py')), run_name='__main__')
