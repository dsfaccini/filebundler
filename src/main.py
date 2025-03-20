# main.py
import os
import sys
import signal
import atexit
import logging

import app

logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    """Handle keyboard interrupt and other termination signals"""
    logger.info(f"Received signal {sig}, shutting down...")
    app.cleanup()
    sys.exit(0)


def main():
    """Entry point function for the package."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Terminal closing

    # Register app.cleanup to be called on normal exit
    atexit.register(app.cleanup)

    # When called as an installed package, we need to run Streamlit with this file
    import streamlit.web.cli as stcli

    # Get the absolute path to this file
    current_file = os.path.abspath(__file__)

    try:
        # Set up Streamlit arguments to run this file
        sys.argv = ["streamlit", "run", current_file, "--global.developmentMode=false"]

        # Run Streamlit CLI with this file
        sys.exit(stcli.main())
    except KeyboardInterrupt:
        # Handle Ctrl+C at the top level
        logger.info("Keyboard interrupt received, exiting...")
        app.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers here too for development mode
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(app.cleanup)

    try:
        app.main()
    except KeyboardInterrupt:
        sys.exit(0)
