import argparse
from app import App


def _parse_args(args=None):
    """Parse command line arguments, provide usage help to users."""

    parser = argparse.ArgumentParser(
        description="Monitors websites' status"
    )

    parser.add_argument(
        "--poll_seconds",
        required=False,
        help="Override website status polling interval globally.",
        type=int
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    args = _parse_args()
    app = App()
    app.start(args)
