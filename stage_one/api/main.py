from datetime import datetime
from flask import Flask, request


app = Flask(__name__)


@app.get('/api')
def index() -> dict:
    """
    returns a JSON response with the details passed
    """
    slack_name = request.args.get("slack_name")
    track = request.args.get("track")

    return {
        "slack_name": slack_name,
        "utc_time": f'{datetime.utcnow().isoformat(timespec="seconds")}Z',
        "current_day": datetime.now().strftime("%A"),
        "track": track,
        "github_file_url": "https://github.com/DrOncogene/hngx-2023/blob/main/stage_one/main.py",
        "github_repo_url": "https://github.com/DrOncogene/hngx-2023",
        "status_code": 200
    }


if __name__ == '__main__':
    app.run(port=8080)
