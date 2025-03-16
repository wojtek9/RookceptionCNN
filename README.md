# Rookception

## CMD
### update reqs:
pipreqs . --force
### start API:
- uvicorn src.API.ChessAPI:app --host 127.0.0.1 --port 8000 --reload
- debug: http://127.0.0.1:8000/docs
