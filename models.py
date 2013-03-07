from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import images
import datetime


class About(db.Model):
    description = db.TextProperty(required=True)


class ArtType(db.Model):
    name = db.StringProperty(required=True)
    display_name = db.StringProperty(required=True)
    display_order = db.IntegerProperty(required=True)
    parent_type = db.ReferenceProperty(collection_name='subtypes')


class Artwork(db.Model):
    CURRENCIES = ['GBP', 'USD', 'EUR']
    title = db.StringProperty(required=True)
    artist = db.StringProperty(required=True, default='Autumn Christie')
    description = db.TextProperty()
    art_medium = db.StringProperty(default='paint')
    art_medium_subtype = db.StringProperty(default='other')
    art_medium_details = db.TextProperty()
    year_completed = db.IntegerProperty(default=datetime.date.today().year)
    price = db.FloatProperty(default=0.00)
    currency = db.StringProperty(choices=CURRENCIES, default='GBP')
    for_sale = db.BooleanProperty(default=True)
    dimensions = db.StringProperty()

    def hasPhotos(self):
        count = 0
        for photo in self.photos:
            count += 1
        return count

    def setYearCompleted(self, year):
        """Handle empty years"""
        if (year == ''):
            self.year_completed = datetime.date.today().year
        else:
            self.year_completed = int(year)

    def formatted_price(self):
        """docstring for get_formatted_price"""
        currency = "&pound;"
        if self.currency == 'USD':
            currency = '&#36;'
        elif self.currency == 'EUR':
            currency = '&euro;'

        return "%s%.2f" % (currency, self.price)

    def delete(self):
        """Override the base class so we can remove all associated
        CatalogPhotos"""
        for photo in self.photos:
            photo.delete()

        db.delete(self)


class CatalogPhoto(db.Model):
    """Each artwork can have many photos for use in the gallery"""
    artwork = db.ReferenceProperty(Artwork, collection_name='photos')
    in_slide_show = db.BooleanProperty(default=False)
    picture_key = blobstore.BlobReferenceProperty()

    def delete(self):
        """handle deleting cleanly for blobinfos"""
        #picture_info = blobstore.delete(self.picture_key.key())
        db.delete(self)

    def url(self):
        return images.get_serving_url(str(self.picture_key.key()))
