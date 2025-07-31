
import requests
import logging
from .config import settings

def push_to_benchling(file_path: str, project_id: str = "PLACEHOLDER"):
    """Upload a file to Benchling as an attachment.

    Replace `project_id` with a real project UUID or modify this to use
    the endpoints you need.
    """
    token = settings.benchling_api_token
    if not token:
        logging.warning("BENCHLING_API_TOKEN not set; skipping Benchling push.")
        return False

    url = f"https://api.benchling.com/v2/attachments?projectId={project_id}"
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as fh:
        files = {"file": fh}
        response = requests.post(url, headers=headers, files=files, timeout=60)
    if response.ok:
        logging.info("Uploaded to Benchling")
    else:
        logging.error("Benchling upload failed: %s – %s", response.status_code, response.text)
    return response.ok
