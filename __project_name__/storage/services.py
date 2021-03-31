from typing import BinaryIO

import boto3

from __project_name__.config import config


class StorageServices:

    bucket_folder = config.STORAGE_BUCKET_FOLDER
    bucket_name = config.STORAGE_BUCKET_NAME
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=config.STORAGE_REGION,
                            endpoint_url=config.STORAGE_BUCKET_ENDPOINT,
                            aws_access_key_id=config.STORAGE_ACCESS_KEY_ID,
                            aws_secret_access_key=config.STORAGE_SECRET_ACCESS_KEY)

    def put_url(self, file_key: str) -> str:

        return self.client.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': self.bucket_name,
                    'Key': f'{self.bucket_folder}/{file_key}'},
            ExpiresIn=300)

    def get_url(self, file_key: str) -> str:

        return self.client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket':  self.bucket_name,
                    'Key': f'{self.bucket_folder}/{file_key}'},
            ExpiresIn=300)

    def delete_object(self, file_key: str) -> None:
        self.client.delete_object(Bucket=self.bucket_name,
                                  Key=f'{self.bucket_folder}/{file_key}')

    def delete_objects(self, keys) -> None:
        self.client.delete_objects(Bucket=self.bucket_name,
                                   Delete={'Objects': keys,
                                           'Quiet': True})

    def upload(self, file_key: str, body: BinaryIO) -> None:

        self.client.put_object(Bucket=self.bucket_name,
                               Key=f'{self.bucket_folder}/{file_key}',
                               Body=body,
                               ContentType='image/jpeg',
                               ACL='private')


storage = StorageServices()
