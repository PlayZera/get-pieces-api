import sys
from pathlib import Path
# Adiciona o diretório pai ao PYTHONPATH
sys.path.append(str(Path(__file__).parent))

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)