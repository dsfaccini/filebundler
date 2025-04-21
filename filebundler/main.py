# filebundler/main.py
import logging
import os
import sys
import atexit
import argparse

from filebundler import app


def main():
    """Entry point function for the package."""

    # Register app.cleanup to be called on normal exit
    atexit.register(app.cleanup)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="File Bundler App")

    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level (default: info)",
    )
    parser.add_argument(
        "--theme",
        default="dark",
        choices=["light", "dark"],
        help="Set the Streamlit theme (light or dark)",
    )
    args = parser.parse_args()

    if args.log_level:
        os.environ["LOG_LEVEL"] = args.log_level

    if "ANTHROPIC_API_KEY" not in os.environ:
        logging.warning(
            "\033[93mAnthropic API key not found in environment variables. "
            "Some features may not work as expected. "
            "(Color might not be supported in all terminals)\033[0m"
        )

    # When called as an installed package, we need to run Streamlit with this file
    import streamlit.web.cli as stcli

    # Get the absolute path to this file
    current_file = os.path.abspath(__file__)

    try:
        # Set up Streamlit arguments to run this file
        st_args = ["streamlit", "run", current_file, "--global.developmentMode=false"]
        if args.headless:
            st_args.append("--server.headless=true")
        if args.theme:
            st_args.append(f"--theme.base={args.theme}")

        sys.argv = st_args

        # Run Streamlit CLI with this file
        sys.exit(stcli.main())
    except KeyboardInterrupt:
        # Handle Ctrl+C at the top level
        logging.info("Keyboard interrupt received, exiting...")
        app.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    atexit.register(app.cleanup)

    try:
        app.main()
    except KeyboardInterrupt:
        sys.exit(0)
