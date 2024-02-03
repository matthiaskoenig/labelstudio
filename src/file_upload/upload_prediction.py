import json
import os
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv
from label_studio_sdk import Client, Project
from tqdm import tqdm

from src.lstools.console import console


def create_client() -> Client:
    api_key = os.getenv("API_KEY")
    api_url = os.getenv("API_URL")
    return Client(url=api_url, api_key=api_key)


def get_project(client: Client) -> Project:
    project_name = os.getenv("PROJECT")
    filtered = list(filter(lambda p: p["name"] == project_name, client.list_projects()))

    if len(filtered) == 0:
        raise NameError(f"No project with name '{project_name}' found")

    return filtered[0]


def get_data_source():
    data_source_dir = Path(os.getenv("DATA_SOURCE"))
    if not data_source_dir.exists():
        raise FileNotFoundError("The data source directory does not exist")

    return data_source_dir


def get_image_task_dict(tasks: List[Dict]) -> dict:
    return {
        Path(task["data"]["image"]).name: task
        for task in tasks
    }


def get_storage_location_path(task: Dict) -> Path:
    return Path(task["data"]["image"]).parent


def create_data_dict(entry: Dict) -> Dict:
    return {
        "project": entry["project"],
        "subject": entry["subject"],
        "species": entry["species"],
        "group": entry["group"],
        "dataset": entry["dataset"],
        "sample": entry["sample"]
    }


class DataUpload:
    def __init__(self):
        load_dotenv()
        self.client = create_client()
        self.project = get_project(self.client)
        self.data_source = get_data_source()
        self.storage_location = os.getenv("STORAGE_LOCATION")

    def upload_datasets(self) -> None:
        for dataset_dir in self.data_source.iterdir():
            self.upload_dataset(dataset_dir)

    def upload_dataset(self, dataset_dir: Path) -> None:
        with open(dataset_dir / "data_config.json", "r") as f:
            data_config = json.load(f)

        if len(data_config) == 0:
            console.print(f"The data_config.json is empty", style="red")

        self.create_or_update_tasks(data_config, dataset_dir.stem)

        self.create_predictions(dataset_dir, data_config)

    def create_or_update_tasks(self, data_config: List[Dict], dataset: str) -> None:
        image_task_dict = get_image_task_dict(self.project.get_tasks())

        existing = {}
        new = []

        for entry in data_config:
            image = entry["image"]
            if image in image_task_dict:
                existing[image] = entry
            else:
                new.append(entry)

        to_create = []

        # create non-existing tasks
        for entry in new:
            to_create.append(
                {
                    "image": f"{self.storage_location}/?d={dataset}/{entry['image']}",
                }.update(create_data_dict(entry))
            )

        if len(to_create) > 0:
            console.print(f"Creating {len(to_create)} new tasks", style="green")
        self.project.import_tasks(to_create)

        # update data dict for existing tasks
        for image, entry in tqdm(existing.items(), desc=f"Updating {len(existing)} tasks", unit="tasks"):
            task = image_task_dict[image]
            self.project.update_task(
                task["id"],
                data=task["data"].update(create_data_dict(entry))
            )

    def create_predictions(self, dataset_dir: Path, data_config: List[Dict]) -> None:
        image_task_dict = get_image_task_dict(self.project.get_tasks())

        for entry in tqdm(data_config, desc="Creating predictions", unit="tasks"):
            image = Path(entry["image"])
            polygon_path = dataset_dir / "predictions" / f"{image.stem}.json"

            if not polygon_path.exists():
                raise FileNotFoundError(f"No polygon data found for image {image}")

            with open(polygon_path, "r") as f:
                results: List[Dict] = json.load(f)

            task = image_task_dict[image]

            # delete existing predictions
            if len(task["predictions"]) != 0:
                for prediction in task["predictions"]:
                    if prediction["model_version"] == "initial_import":
                        prediction_id = prediction["id"]
                        self.client.make_request("DELETE", f"/api/predictions/{prediction_id}")

            self.project.create_prediction(task_id=task["id"], result=results, model_version="initial_import")


if __name__ == "__main__":
    data_upload = DataUpload()
    data_upload.upload_datasets()
