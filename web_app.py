from __future__ import annotations

from flask import Flask, jsonify, redirect, render_template, request, url_for

from orchestrator.hf_client import HuggingFaceGateway
from orchestrator.router import MultiAIOrchestrator
from orchestrator.settings import load_settings


app = Flask(__name__)
_orchestrator: MultiAIOrchestrator | None = None
_startup_error: str | None = None


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


def get_orchestrator() -> MultiAIOrchestrator:
    global _orchestrator
    global _startup_error

    if _orchestrator is not None:
        return _orchestrator

    try:
        settings = load_settings()
        gateway = HuggingFaceGateway(settings.hf_token, settings.config["models"])
        _orchestrator = MultiAIOrchestrator(gateway)
        _startup_error = None
        return _orchestrator
    except Exception as exc:
        _startup_error = str(exc)
        raise


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    try:
        get_orchestrator()
        return jsonify({"ok": True, "error": None})
    except Exception:
        return jsonify({"ok": False, "error": _startup_error}), 500


@app.post("/api/run")
def run_orchestrator():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()

    if not text:
        return jsonify({"ok": False, "error": "Metin bos olamaz."}), 400

    try:
        response = get_orchestrator().run(text)
        return jsonify(
            {
                "ok": True,
                "intent": response.intent,
                "sentiment": response.sentiment,
                "answer": response.answer,
            }
        )
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/api/run", methods=["OPTIONS"])
def run_orchestrator_options():
    return ("", 204)


@app.get("/api/run")
def run_orchestrator_get():
    # Friendly behavior for humans: if someone opens this URL in a browser,
    # redirect them to the HTML UI instead of returning "Method Not Allowed".
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7860, debug=False)
