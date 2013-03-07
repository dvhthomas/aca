from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
import jinja2
from models import *


def rescale(blob_info, width, height, halign='middle', valign='middle'):
    """Resize then optionally crop a given image.

    Attributes:
        blob_info: BlobInfo associated with a stored Blobstore object
        width: The desired width
        height: The desired height
        halign: Acts like photoshop's 'Canvas Size' function, horizontally
                aligning the crop to left, middle or right
        valign: Verticallly aligns the crop to top, middle or bottom

    from: http://stackoverflow.com/questions/1944112/app-engine-cropping-to-a-specific-width-and-height/2555121#2555121
  """
    blob_key = str(blob_info.key())
    reader = blobstore.BlobReader(blob_key)
    data = reader.read()
    image = images.Image(data)

    """ Stop scaling up in either dimension if the requested w/h is
    bigger than the source image """
    if width > image.width:
        width = image.width

    if height > image.height:
        height = image.height

    desired_wh_ratio = float(width) / float(height)
    wh_ratio = float(image.width) / float(image.height)

    if desired_wh_ratio > wh_ratio:
    # resize to width, then crop to height
        image.resize(width=width)
        image.execute_transforms()
        trim_y = (float(image.height - height) / 2) / image.height
    if valign == 'top':
        image.crop(0.0, 0.0, 1.0, 1 - (2 * trim_y))
    elif valign == 'bottom':
        image.crop(0.0, (2 * trim_y), 1.0, 1.0)
    else:
        image.crop(0.0, trim_y, 1.0, 1 - trim_y)

    # resize to height, then crop to width
    image.resize(height=height)
    image.execute_transforms()
    trim_x = (float(image.width - width) / 2) / image.width

    if halign == 'left':
        image.crop(0.0, 0.0, 1 - (2 * trim_x), 1.0)
    elif halign == 'right':
        image.crop((2 * trim_x), 0.0, 1.0, 1.0)
    else:
        image.crop(trim_x, 0.0, 1 - trim_x, 1.0)

    return image.execute_transforms()


class BaseHandler(webapp.RequestHandler):
    context = {}

    def initialize(self, request, response):
        """docstring for __init__"""
        self.populateContext()
        super(BaseHandler, self).initialize(request, response)

    def populateContext(self):
        """Load up the stuff that every web handler will need"""
        self.context['artwork'] = Artwork
        self.context['art_types'] = MenuBuilder()
        self.context['logged_in'] = False
        user = users.get_current_user()

        if user:
            self.context['logged_in'] = True
            self.context['is_admin'] = users.is_current_user_admin()

    def render(self, template_name):
        """Rending a template in a base directory by passing the name of the template"""
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('views'))
        template = env.get_template(template_name)
        self.response.out.write(template.render(self.context))


class BlobBaseHandler(blobstore_handlers.BlobstoreUploadHandler):
    """This is tiresome, but need another base class to load some stuff
        specific to Blob uploads"""
    context = {}

    def initialize(self, request, response):
        """docstring for __init__"""
        self.populateContext()
        super(BlobBaseHandler, self).initialize(request, response)

    def populateContext(self):
        """Load up the stuff that every web handler will need"""
        self.context['artwork'] = Artwork
        self.context['art_types'] = MenuBuilder()

    def render(self, template_name):
        """Rending a template in a base directory by passing the name of the template"""
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('views'))
        template = env.get_template(template_name)
        self.response.out.write(template.render(self.context))


def MenuBuilder():
    """docstring for MenuBuilder"""
    menu = []
    art_types = ArtType.all().order('display_order').fetch(limit=1000)
    top_levels = filter(lambda atype: atype.parent_type == None, art_types)
    children = filter(lambda stype: stype.parent_type != None, art_types)

    for top_level in top_levels:
        submenu = []
        submenu.append((top_level.name, top_level.display_name))
        sub_items = filter(lambda stype: stype.parent_type.name == top_level.name, children)
        submenu.append([(child.name, child.display_name) for child in sub_items])
        menu.append(submenu)

    return menu
