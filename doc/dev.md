# Development guide

## Test

```
source .venv/bin/activate
pip install -r requirements_dev.txt
python -m coverage run -m pytest -v --durations=50 test/test_*.py -W ignore::DeprecationWarning
python -m coverage html -i --omit=conf/settings.py
```
