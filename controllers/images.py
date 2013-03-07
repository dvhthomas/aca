import json
from models import *
from google.appengine.ext import webapp
import utils


class Image(webapp.RequestHandler):
    def get(self, photo_id):
        width = int(self.request.get('w'))
        height = int(self.request.get('h'))
        photo = CatalogPhoto.get_by_id(int(photo_id), parent=None)
        image = utils.rescale(photo.picture_key, width=width, height=height)
        self.response.headers.add_header("Expires", "Thu, 01 Dec 2014 16")
        self.response.headers["Cache-Control"] = "public, max-age=3660000"
        self.response.headers['Content-Type'] = photo.picture_key.content_type
        self.response.out.write(image)


class PhotoHandler(utils.BaseHandler):
    def delete(self, photo_id):
        """Deleting photos of artwork"""
        photo = CatalogPhoto.get_by_id(int(photo_id), parent=None)
        photo.delete()

    def put(self, photo_id):
        """Update a photo: is it in the slideshow or not"""
        decoder = json.JSONDecoder()
        data = decoder.decode(self.request.body)
        photo = CatalogPhoto.get_by_id(int(photo_id), parent=None)
        in_show = data['in_show']
        photo.in_slide_show = in_show
        db.put(photo)
