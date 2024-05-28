import json
import os
from pathlib import Path
from typing import List, Dict, Optional

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
    filtered = list(filter(lambda p: p.params["title"] == project_name, client.list_projects()))

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
        Path(task["data"]["img"]).name: task
        for task in tasks
    }


def get_storage_location_path(task: Dict) -> Path:
    return Path(task["data"]["img"]).parent


class DataUpload:
    def __init__(self):
        load_dotenv()
        self.client = create_client()
        self.project = get_project(self.client)
        self.data_source = get_data_source()
        self.storage_location = os.getenv("STORAGE_LOCATION")

    def upload_datasets(self, datasets: Optional[Dict[str, str]]) -> None:
        for dataset_dir in self.data_source.iterdir():
            if datasets and dataset_dir.name not in datasets:
                continue
            self.upload_dataset(dataset_dir, datasets[dataset_dir.name])

    def upload_dataset(self, dataset_dir: Path, remote_name: str) -> None:
        with open(dataset_dir / "data_config.json", "r") as f:
            data_config = json.load(f)

        if len(data_config) == 0:
            console.print(f"The data_config.json is empty", style="red")

        self.create_or_update_tasks(data_config, remote_name)

        self.create_predictions(dataset_dir, data_config)

    def create_data_dict(self, entry: Dict, remote_name: str) -> Dict:
        return {
            "img": f"{self.storage_location}/?d={remote_name}/image/{entry['image']}",
            "image": entry["image"],
            "subject": entry["subject"],
            "species": entry["species"],
            "group": entry["group"],
            "dataset": entry["dataset"],
            "tile": str(entry["tile"]),
            "diet weeks": str(entry["diet weeks"])
        }

    def create_or_update_tasks(self, data_config: List[Dict], remote_name: str) -> None:
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
            to_create.append(self.create_data_dict(entry, remote_name))

        if len(to_create) > 0:
            console.print(f"Creating {len(to_create)} new tasks", style="green")
            self.project.import_tasks(to_create)

        # update data dict for existing tasks
        for image, entry in tqdm(existing.items(), desc=f"Updating {len(existing)} tasks", unit="tasks"):
            task = image_task_dict[image]
            data_dict = self.create_data_dict(entry, remote_name)

            # check if task is already up-to-date
            if task["data"] == data_dict:
                continue

            self.project.update_task(
                task["id"],
                data=data_dict
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

            task = image_task_dict[image.name]

            # delete existing predictions
            if len(task["predictions"]) != 0:
                for prediction in task["predictions"]:
                    if prediction["model_version"] == "initial_import":
                        prediction_id = prediction["id"]
                        self.client.make_request("DELETE", f"/api/predictions/{prediction_id}")

            self.project.create_prediction(task_id=task["id"], result=results, model_version="initial_import")


if __name__ == "__main__":
    """Requires the following information:
    
    - predictions: predictions by algorithm
    - data_config.json: meta data for predictions/tasks
    """


    data_upload = DataUpload()
    # map local folder to remote folder
    datasets = {"steatosis_2024-05-28": "steatosis_2024-05-28"}
    data_upload.upload_datasets(datasets)
