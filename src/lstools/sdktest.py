from typing import List

from console import console
from label_studio_sdk import Client, Project
from dotenv import load_dotenv
import os

# ----------------------------------------
load_dotenv()
api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")
# ----------------------------------------


# Connect to the Label Studio API and check the connection
def list_projects(ls: Client) -> None:
    """List available projects."""
    projects: List[Project] = ls.list_projects()

    project: Project
    for project in projects:
        console.print(f"{project}")


# Create new project
# project = ls.start_project(
#   title='Image Classification Project',
#   label_config='''
# <View>
# <Image name="image" value="$image"/>
# <Choices name="choice" toName="image">
# <Choice value="Dog"/>
# <Choice value="Cat" />
# </Choices>
# </View>
# '''
# )

# # Create new tasks; use additional columns for data
# project.import_tasks(
#     [
#         {'image': 'https://data.heartex.net/open-images/train_0/mini/0045dd96bf73936c.jpg'},
#         {'image': 'https://data.heartex.net/open-images/train_0/mini/0083d02f6ad18b38.jpg'}
#     ]
# )
# for t in project.get_tasks():
#     d = t['data']
#     if not 'source' in d:
#         d['source'] = 'data.heartex.net'
#         project.update_task(t['id'], data=d)
#
#
# # Bulk data exports

if __name__ == "__main__":
    # test connection
    ls = Client(url=api_url, api_key=api_key)
    ls.check_connection()
    console.print(f"Successful SDK connection to: {api_url}", style="blue")

    # list projects
    list_projects(ls=ls)
