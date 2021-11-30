import os
import boto3

env = os.environ.get
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

session = boto3.Session(
    aws_access_key_id=env("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=env("AWS_SECRET_ACCESS_KEY"),
)
s3 = session.client("s3", region_name="ap-northeast-2")


with open("data/food_nutrient.csv", "r") as csvfile:
    idx = 0
    for lines in csvfile.readlines():
        name = lines.split("|")[0]
        if idx != 0:
            folder_path = f"data/downloads/{name}"
            for i, filename in enumerate(os.listdir(folder_path)):
                extension = filename.split(".")[-1]
                s3.upload_file(
                    os.path.join(BASE_DIR, f"data/downloads/{name}/{filename}"),
                    "reviewkingwordcloud",
                    f"food/{idx}/{i+1}.{extension}",
                )
        idx += 1
