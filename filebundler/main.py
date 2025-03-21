# main.py
import os
import sys
import atexit
import logging
import argparse

from filebundler import app

logger = logging.getLogger(__name__)


def main():
    """Entry point function for the package."""

    # Register app.cleanup to be called on normal exit
    atexit.register(app.cleanup)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="File Bundler App")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    args = parser.parse_args()

    # When called as an installed package, we need to run Streamlit with this file
    import streamlit.web.cli as stcli

    # Get the absolute path to this file
    current_file = os.path.abspath(__file__)

    try:
        # Set up Streamlit arguments to run this file
        st_args = ["streamlit", "run", current_file, "--global.developmentMode=false"]
        if args.headless:
            st_args.append("--server.headless=true")
            logger.info("Running in headless mode")

        sys.argv = st_args

        # Run Streamlit CLI with this file
        sys.exit(stcli.main())
    except KeyboardInterrupt:
        # Handle Ctrl+C at the top level
        logger.info("Keyboard interrupt received, exiting...")
        app.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    atexit.register(app.cleanup)

    try:
        app.main()
    except KeyboardInterrupt:
        sys.exit(0)
