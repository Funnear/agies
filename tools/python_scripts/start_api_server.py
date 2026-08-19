"""Start the AGIES REST API Server."""

import argparse
from pathlib import Path
import sys
import uvicorn

# Ensure src is in pythonpath
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))


def main():
    parser = argparse.ArgumentParser(description="Start the AGIES REST API Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    print(f"Starting AGIES REST API on http://{args.host}:{args.port}")
    print(f"Interactive Swagger Docs: http://{args.host}:{args.port}/docs")
    print(f"ReDoc Documentation: http://{args.host}:{args.port}/redoc")
    print("Default Sandbox API Key: agies_test_key_123")
    print("Default Master Admin Key: agies_dev_master_key_999\n")

    uvicorn.run("agies.api.app:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
