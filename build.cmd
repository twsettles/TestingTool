@echo off
mypy %1
ECHO --- End Mypy ---
python -i %1
