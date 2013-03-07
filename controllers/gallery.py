import utils
from models import *
import logging


class MainHandler(utils.BaseHandler):
    def get(self):
        """Get photos that need to be in the slide show"""
        query = CatalogPhoto.all()
        query.filter('in_slide_show =', True)
        in_slideshow = query.fetch(limit=10)
        self.context['photos'] = in_slideshow
        self.render('index.html')


class GalleryHandler(utils.BaseHandler):
    def get(self, art_type, art_subtype):
        logging.info(art_type)
        query = Artwork.all()
        if art_type != '':
            query.filter('art_medium =', art_type)
        if art_subtype != '':
            query.filter('art_medium_subtype =', art_subtype)

        artworks = query.fetch(limit=200)
        """ Need to fix this so that the Display text, not 'real' text value
        of art_type and art_subtype are send. have to get the actual ArtType
        to the view. """
        self.context['art_type'] = nullstring(art_type)
        self.context['art_subtype'] = nullstring(art_subtype)
        self.context['artworks'] = artworks
        self.render('gallery.html')


class GalleryItemHandler(utils.BaseHandler):
    def get(self, artwork_id):
        """Single item view of an artwork"""
        artwork = Artwork.get_by_id(int(artwork_id), parent=None)
        self.context['piece'] = artwork
        self.render('artwork.html')


class AboutHandler(utils.BaseHandler):
    def get(self):
        """Basic static about page"""
        q = About.all()
        about = q.get()
        self.context['about'] = about
        self.render('about.html')


def nullstring(s):
    """returns None if a string is empty, otherwise the value as a string"""
    return None if str(s) == '' else str(s)
