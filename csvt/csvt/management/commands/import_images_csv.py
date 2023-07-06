import os
import csv

from django.core.management.base import BaseCommand
from django.core.files.base import File
from django.db.utils import IntegrityError

from upload.models import (Image, UploadFile)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv_file",
            type=str,
            help="csv file")

    def handle(self, *args, **options):
        csv_file = options.get("csv_file")
        for (alt, path) in csv.reader(open(csv_file)):
            name, ext = os.path.splitext(os.path.basename(path))
            if not ext:
                continue
            tags = os.path.dirname(path).split('/')[1:]
            if not alt:
                alt = name

                try:

                    with open(f"media/{path}", "rb") as f:
                        file = UploadFile(file=path)
                        try:
                            file = UploadFile.objects.get(md5hash=file.calc_md5(file.file))
                        except UploadFile.DoesNotExist:
                            file.save()

                        if not Image.objects.filter(translations__alt=alt[:50], name=name[:50]).exists():
                            Image(
                                alt=alt[:50], name=name,
                                file=file, tags=tags
                            ).save()

                except Exception as error:
                    print(Exception, error)
