from flask import Flask, render_template, request
import os
from ..core.client import upload_video, get_result


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

TMP_ROOT = "./tmp"
os.makedirs(TMP_ROOT, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def up_video():
    if "video" not in request.files:
        return "No file", 400

    file = request.files["video"]

    job_id = upload_video(file)
    result = get_result(job_id)
    while result is None:
        result = get_result(job_id)
    print(result)
    return "Video uploaded successfully!"

@app.route("/result/<job_id>")
def get_result_route(job_id):
    result = get_result(job_id)
    if result is None:
        return "", 204
    return result, 200


if __name__ == "__main__":
    app.run(debug=True)

