# habitat-py

Scripts for the home

## setup

```bash
python3 -m venv habitat.venv 
source habitat.venv/bin/activate
pip install wheel
pip install -r requirements.txt   
```

## develop

```bash
source habitat.venv/bin/activate
uvicorn main:app --reload
```

## serve

```bash
uvicorn main:app --host 0.0.0.0 --port 5001 --root-path /habitat
```

## clockify hooks

any timer started | https://sf8do.mooo.com/habitat/clockify/start
any timer stopped | https://sf8do.mooo.com/habitat/clockify/stop
