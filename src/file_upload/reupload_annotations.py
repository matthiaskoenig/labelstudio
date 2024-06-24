import json
import os

from dotenv import load_dotenv
from tqdm import tqdm

from src.file_upload.upload_prediction import create_client, get_project

if __name__ == "__main__":
    load_dotenv()
    client = create_client()
    project = get_project(client)
    storage_location = os.getenv("STORAGE_LOCATION")

    tasks = project.tasks

    with open("/media/jkuettner/Extreme Pro/exchange/labelstudio/labelstudio_10-04-2024.json", "r") as f:
        annos = json.load(f)

    for task in project.tasks:
        for anno in annos:
            if task["data"]["image"] == anno["data"]["image"]:
                for annotation in anno["annotations"]:
                    annotation["last_updated_by"] = 2
                    annotation["project"] = 1
                    annotation["task"] = task["id"]
                    annotation["completed_by"] = 2
                    annotation["parent_prediction"] = None
                    project.create_annotation(task["id"],
                                              **annotation)

                break

