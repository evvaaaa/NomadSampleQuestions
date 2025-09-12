from pathlib import Path
from uuid import uuid4
from flask import Flask, render_template_string, request, redirect, url_for
import yaml

FORM_HTML = (Path(__file__).parent / "form.html").read_text()


def create_app(questions_directory: Path, answers_directory: Path) -> Flask:
    if not questions_directory.exists():
        raise ValueError(f"Given questions path {questions_directory} does not exist")

    if not answers_directory.exists():
        raise ValueError(f"Given answers path {answers_directory} does not exist")

    with (questions_directory / "questions.yaml").open() as f:
        questions = yaml.safe_load(f)["questions"]
    with (questions_directory / "constant_answers.yaml").open() as f:
        static_answers = yaml.safe_load(f)

    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def survey():
        saved = request.args.get("saved", None)
        answers_yaml = request.args.get("yaml", None)
        error_msg = None

        if request.method == "POST":
            answers = {}
            missing_required = []
            for q in questions:
                # For multiple fields: getlist, else get
                if q.get("multiple"):
                    values = request.form.getlist(q["id"])
                    values = [v for v in values if v.strip()]
                    answers[q["id"]] = values
                    if q.get("required") and not values:
                        missing_required.append(q["label"])
                else:
                    value = request.form.get(q["id"], "").strip()
                    answers[q["id"]] = value
                    if q.get("required") and not value:
                        missing_required.append(q["label"])
            if missing_required:
                error_msg = (
                    f"Please fill all required fields: {', '.join(missing_required)}"
                )
                return render_template_string(
                    FORM_HTML,
                    questions=questions,
                    saved=False,
                    answers_yaml=None,
                    answers_directory=answers_directory,
                    error_msg=error_msg,
                )
            experiment_uuid = uuid4()
            answers.update(static_answers)
            answers_yaml = yaml.dump(answers, sort_keys=False, allow_unicode=True)
            answers_file = answers_directory / f"{experiment_uuid}.yaml"
            with answers_file.open("w+") as f:
                f.write(answers_yaml)
            # Redirect to avoid POST resubmission
            return redirect(url_for("survey", saved="true", yaml=answers_yaml))

        return render_template_string(
            FORM_HTML,
            questions=questions,
            saved=(saved == "true"),
            answers_yaml=answers_yaml,
            answers_directory=str(answers_directory),
            error_msg=error_msg,
        )

    return app
