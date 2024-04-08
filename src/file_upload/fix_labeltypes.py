import os

from dotenv import load_dotenv
from tqdm import tqdm

from src.file_upload.upload_prediction import create_client, get_project

if __name__ == "__main__":
    load_dotenv()
    client = create_client()
    project = get_project(client)
    storage_location = os.getenv("STORAGE_LOCATION")

    for task in tqdm(project.tasks,  desc="Updating task", unit="tasks"):

        for anno in task["annotations"]:

            id = anno["id"]

            results = []

            for result in anno["result"]:

                if result["type"] == "polygon":
                    result["type"] = "polygonlabels"

                if result["type"] == "keypoint":
                    result["type"] = "keypointlabels"

                results.append(result)

            project.update_annotation(annotation_id=id, result=results)