import boto3
import json
from celery import Task
from .models import Text, session
from .imports import (
  AuthorImport,
  TextImport,
  PoetryFoundationDataImport
)

from pprint import pprint


class S3Task(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = boto3.client('s3', region_name='us-east-1')


class S3BucketPageImportTask(S3Task):
    name = "texts.S3BucketPageImportTask"

    def run(self, page, annotate):
        from poetaster.celery_app import app as celery_app
        annotate_task = celery_app.tasks.get("texts.AnnotateTextTask")

        for obj in page["Contents"]:
            key = obj["Key"]

            data = self.client.get_object(
              Bucket="poetry-collection",
              Key=key
            )

            data = json.loads(data["Body"].read())

            author = AuthorImport(session, data).process()

            text = TextImport(
                session, data, author_slug=author.slug
            ).process()

            poetry_foundation_data = PoetryFoundationDataImport(
                session, data, text=text, author=author
            ).process()

            text.poetry_foundation_data_id = poetry_foundation_data.id

            print("Created", text.title, author.name)

            if annotate:
                _, pk, _ = session.identity_key(instance=text)
                annotate_task.apply_async(args=(pk,))

        session.commit()


class S3BucketImportTask(S3Task):
    name = "texts.S3BucketImportTask"

    def run(self, annotate=False):
        paginator = self.client.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket="poetry-collection")

        from poetaster.celery_app import app as celery_app
        page_import_task = celery_app.tasks.get("texts.S3BucketPageImportTask")

        i = 1
        for page in page_iterator:
            print("Dispatching page %s of texts..." % i)
            page_import_task.apply_async(args=(page, annotate,))
            i += 1


class AnnotateTextTask(Task):
    name = "texts.AnnotateTextTask"

    def run(self, text_id):
        text = session.query(Text).get(text_id)
        text.generate_nlp_constructs(session=session)
        session.commit()

        print("Generated nlp constructs for", text.title)
