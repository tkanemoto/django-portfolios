import os

from django.conf import settings
from django.core.files.uploadhandler import MemoryFileUploadHandler
from PIL import Image

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


JPEG_QUALITY = getattr(settings, 'JPEG_QUALITY', 70)
COMPRESSED_TYPES = ['image/jpeg']


class CompressImageUploadHandler(MemoryFileUploadHandler):
    def file_complete(self, file_size):
        if not self.content_type is None and self.content_type in COMPRESSED_TYPES:
            self.file.seek(0)
            newfile = StringIO()
            img = Image.open(self.file)
            img.save(newfile, 'JPEG', quality=JPEG_QUALITY)
            self.file = newfile
            name, ext = os.path.splitext(self.file_name)
            self.file_name = '{0}.{1}'.format(name, 'jpg')
            self.content_type = 'image/jpeg'

        return super(CompressImageUploadHandler, self).file_complete(file_size)
