import argparse
from pathlib import Path

import os
from nomad_sample_questionnaire.web_app import create_app


def main():
    parser = argparse.ArgumentParser(
        description="A service which hosts a webform allowing users to generate nomad metadata."
    )

    parser.add_argument(
        "--port",
        type=int,
        default=os.environ.get("NOMAD_EXPERIMENT_QUESTIONNAIRE_PORT", 5000),
        help="Port that the questionnare should be hosted on (default: from NOMAD_EXPERIMENT_QUESTIONNAIRE_PORT env var or 5000)",
    )

    parser.add_argument(
        "--questions-path",
        type=str,
        default=os.environ.get("NOMAD_QUESTIONS_PATH"),
        help="Directory that questions are read from (default: from NOMAD_QUESTIONS_PATH env var)",
    )

    parser.add_argument(
        "--answers-path",
        type=str,
        default=os.environ.get("NOMAD_ANSWERS_PATH"),
        help="Directory that answers are written to (default: from NOMAD_ANSWERS_PATH env var)",
    )

    args = parser.parse_args()
    create_app(Path(args.questions_path), Path(args.answers_path)).run(
        host="0.0.0.0", port=args.port
    )


if __name__ == "__main__":
    main()
