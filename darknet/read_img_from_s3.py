import os

import boto3


def read_img_from_s3(filename):
    # aws CLI configure - profile을 이용하여 credential 해결
    # 추후 배포시 VM에 AWS 관련 configure 필요함
    os.environ["AWS_PROFILE"] = "S3_Admin"

    s3 = boto3.resource(
        "s3",
        region_name="ap-northeast-2",
    )
    bucket = s3.Bucket("reviewkingwordcloud")
    object = bucket.Object(filename)
    response = object.get()
    file_stream = response["Body"].read()

    return file_stream


if __name__ == "__main__":

    print("called: read_img_from_s3")
