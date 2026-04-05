import os
import sys
import tempfile
from pathlib import Path

_BACKEND = Path(__file__).resolve().parent.parent
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

_data = tempfile.mkdtemp(prefix="nutri_pytest_")
os.environ["DB_PATH"] = os.path.join(_data, "chat_history.db")
os.environ["CHROMA_PATH"] = os.path.join(_data, "chroma")
os.environ["RATE_LIMIT_ENABLED"] = "false"
