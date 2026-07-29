from pathlib import Path
import os
import uvicorn

from .api import create_app

root = Path(os.environ.get("LIFEOS_V2_REPOSITORY_ROOT", Path.cwd())).resolve()
state = Path(os.environ.get("LIFEOS_V2_PERSISTENCE_PATH", root / ".lifeos-v2/runtime.json"))
app = create_app(root, state)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8765)
