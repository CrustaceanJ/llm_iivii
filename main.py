import argparse
import logging

import uvicorn

from src.lib.app import create_app
from src.lib.config import Config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", type=str, default="configs/config.json")
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8994)

    return parser.parse_args()


def main(
    config_file: str,
    host: str | None,
    port: int | None,
) -> None:
    try:
        config = Config.load(config_file)
        app = create_app(config)
        uvicorn.run(app, host=host, port=port)
    except Exception as e:
        logging.exception(f"Exception: {e}")
        raise e


if __name__ == "__main__":
    args = parse_args()
    main(args.config_file, args.host, args.port)