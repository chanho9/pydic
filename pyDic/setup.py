# -*- coding: utf-8 -*-
from setuptools import setup
import py2exe

setup(name="test_py2xxx",
      description="myPyDic",
      version="0.0.1",
      windows=[{"script": "run.py"}],
      options={"py2exe": {bundle_files : 1, "includes": ["PySide.QtCore", "PySide.QtGui"]}})