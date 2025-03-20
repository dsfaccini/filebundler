# filebundler/main.py
import os
import sys
import signal
import atexit
import logging

from filebundler.app import run, cleanup

logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    """Handle keyboard interrupt and other termination signals"""
    logger.info(f"Received signal {sig}, shutting down...")
    cleanup()
    sys.exit(0)


def main():
    """Entry point function for the package."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Terminal closing

    # Register cleanup to be called on normal exit
    atexit.register(cleanup)

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
        cleanup()
        sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers here too for development mode
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(cleanup)

    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)
