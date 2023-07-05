import os
import csv

from django.core.management.base import BaseCommand
from django.core.files.base import File
from django.db.utils import IntegrityError

from upload.models import Image


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
                    Image(alt=alt[:50], name=name[:50],
                          file=path, tags=tags[:3]).save()
            except IntegrityError as error:
                #  ~ Image.objects.get()
                #  ~ print(dir(error))
                #  ~ print(error.args)
                image = Image(
                    alt=alt[:50], name=name[:50],
                    file=path, tags=tags[:3]
                )
                orig = Image.objects.get(md5hash=image.calc_md5(image.file))
                print(orig)
                print(image)
                return
            except Exception as error:
                print(error)
