import uvicorn
import signal

from app.database import create_tables
from app.main import app


def handle_shutdown(*args):
    raise KeyboardInterrupt()


if __name__ == "__main__":
    create_tables()
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        pass
