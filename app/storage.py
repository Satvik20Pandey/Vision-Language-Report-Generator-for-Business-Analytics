import os
from typing import BinaryIO
from .config import settings
class Storage:
	def __init__(self):
		self.local_dir = settings.storage_dir
		os.makedirs(self.local_dir, exist_ok=True)
		self.s3 = None
		if settings.aws_access_key_id and settings.aws_secret_access_key and settings.s3_bucket:
			try:
				import boto3  # type: ignore
				self.s3 = boto3.client("s3", aws_access_key_id=settings.aws_access_key_id, aws_secret_access_key=settings.aws_secret_access_key, region_name=settings.aws_region)
				self.bucket = settings.s3_bucket
			except:
				self.s3 = None
	def save(self, filename: str, content: bytes) -> str:
		if self.s3:
			key = filename
			self.s3.put_object(Bucket=self.bucket, Key=key, Body=content)
			return f"s3://{self.bucket}/{key}"
		path = os.path.join(self.local_dir, filename)
		with open(path, "wb") as f:
			f.write(content)
		return path

