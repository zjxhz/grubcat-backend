from django.contrib.admin.widgets import AdminFileWidget
from easy_thumbnails.files import get_thumbnailer
import image_cropping
import settings

ADMIN_THUMBNAIL_SIZE = getattr(settings, 'IMAGE_CROPPING_THUMB_SIZE', (300, 300))
def thumbnail(image_path, thumbnail_size):
    if not thumbnail_size:
        thumbnail_size = ADMIN_THUMBNAIL_SIZE
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'size': thumbnail_size,
        #        'upscale':True
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb.url

def get_attrs(image, name, thumbnail_size):
    try:
        if not thumbnail_size:
            thumbnail_size = ADMIN_THUMBNAIL_SIZE
        thumbnailer = get_thumbnailer(image)
        thumbnail_options = {
            'detail': True,
            'size': thumbnail_size,
        }
        thumb = thumbnailer.get_thumbnail(thumbnail_options)

        return {
            'class': "crop-thumb",
            'data-thumbnail-url': thumb.url,
            'data-field-name': name,
            'data-org-width': image.width,
            'data-org-height': image.height,
            }
    except ValueError:
        # can't create thumbnail from image
        return {}

class ImageCropWidget(image_cropping.ImageCropWidget):

    def __init__(self, thumbnail_size=None):
        self.thumbnail_size = thumbnail_size
        super(ImageCropWidget, self).__init__()

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if value:
            attrs.update(get_attrs(value, name, self.thumbnail_size))
        return super(AdminFileWidget, self).render(name, value, attrs)