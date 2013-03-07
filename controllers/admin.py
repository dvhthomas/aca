from google.appengine.ext import blobstore
from google.appengine.ext import db
from models import *
import utils


class CreateArtHandler(utils.BlobBaseHandler):
    def get(self):
        """form to upload new artwork"""
        self.context['blob_url'] = blobstore.create_upload_url('/admin/create')
        self.render('admin/create.html')

    def post(self):
        """ creating new artwork """
        """ handle the uploaded picture and other arty stuff """
        artwork = Artwork(title=self.request.get('title'))
        artwork.description = self.request.get('description')
        art_type = self.request.get('art_type').split('|')
        artwork.art_medium = art_type[0]
        artwork.art_medium_subtype = art_type[1]
        artwork.art_medium_details = self.request.get('medium_details')
        artwork.artist = self.request.get('artist')
        artwork.dimensions = self.request.get('dimensions')
        artwork.price = float(self.request.get('price'))
        artwork.currency = self.request.get('currency')
        artwork.for_sale = bool(self.request.get('for_sale'))
        artwork.setYearCompleted(self.request.get('created'))
        db.put(artwork)

        for upload in self.get_uploads():
            if upload.filename != '':
                photo = CatalogPhoto(picture_key=upload.key(), artwork=artwork)
                db.put(photo)

        self.redirect('/admin/list')


class ListArtHandler(utils.BaseHandler):
    def get(self):
        """List all artworks"""
        self.context['artworks'] = Artwork.all()
        self.render('admin/list.html')


class ArtItemHandler(utils.BlobBaseHandler):
    def get(self, artwork_id):
        """View a single piece of art"""
        artwork = Artwork.get_by_id(int(artwork_id), parent=None)
        self.context['piece'] = artwork
        self.render('admin/item.html')

    def post(self, artwork_id):
        method = self.request.get('_method')

        if method == 'put':
            """ updating existing artwork """
            """ handle the uploaded picture and other arty stuff """
            artwork = Artwork.get_by_id(int(artwork_id), parent=None)
            artwork.title = self.request.get('title')
            artwork.description = self.request.get('description')
            art_type = self.request.get('art_type').split('|')
            artwork.art_medium = art_type[0]
            artwork.art_medium_subtype = art_type[1]
            artwork.art_medium_details = self.request.get('medium_details')
            artwork.artist = self.request.get('artist')
            artwork.dimensions = self.request.get('dimensions')
            artwork.price = float(self.request.get('price'))
            artwork.currency = self.request.get('currency')
            artwork.for_sale = bool(self.request.get('for_sale'))
            artwork.setYearCompleted(self.request.get('created'))
            db.put(artwork)

            for upload in self.get_uploads():
                if upload.filename != '':
                    photo = CatalogPhoto(picture_key=upload.key(), artwork=artwork)
                    db.put(photo)

            self.redirect('/admin/list')

        elif method == 'delete':
            """handle delete through a form post: delete a single artwork"""
            artwork = Artwork.get_by_id(int(artwork_id), parent=None)
            artwork.delete()
            self.redirect('/admin/list')

        else:
            self.error(405)  # METHOD NOT ALLOWED


class EditFormHandler(utils.BaseHandler):
    def get(self, artwork_id):
        """Edit page for one artwork"""
        self.context['piece'] = Artwork.get_by_id(int(artwork_id), parent=None)
        self.context['blob_url'] = blobstore.create_upload_url('/admin/artwork/%s' % artwork_id)
        self.render('admin/edit.html')


class AdminHomeHandler(utils.BaseHandler):
    def get(self):
        """Home page for admin"""
        self.render('admin/index.html')


class SlideshowAdminHandler(utils.BaseHandler):
    def get(self):
        query = CatalogPhoto.all()
        query.filter('in_slide_show =', True)
        in_slideshow = query.fetch(limit=200)
        query_out = CatalogPhoto.all()
        query_out.filter('in_slide_show =', False)
        not_in_slideshow = query_out.fetch(limit=200)
        self.context['in_show'] = in_slideshow
        self.context['not_in_show'] = not_in_slideshow
        self.render('admin/slideshow.html')


class AboutAdmin(utils.BaseHandler):
    def get(self):
        q = db.Query(About)
        about = q.get()
        self.context['about'] = about
        self.render('admin/about.html')

    def post(self):
        """update or create"""
        d = self.request.get('description')
        q = db.Query(About)
        about = q.get()

        if about:
            about.description = d
        else:
            about = About(description=d)

        db.put(about)
        self.redirect('/admin/about')


class SeedData(utils.BaseHandler):
    def post(self):
        mediums = ArtType.all().fetch(40)

        if len(mediums) > 0:
            for m in mediums:
                db.delete(m)

        paint = ArtType(name='paint', display_name='Paint', display_order=0)
        db.put(paint)
        abstract = ArtType(name="abstract", display_name="Abstract", display_order=2, parent_type=paint)
        db.put(abstract)
        pother = ArtType(name="other", display_name="Other", display_order=3, parent_type=paint)
        db.put(pother)

        sculpture = ArtType(name='sculpture', display_name='Sculpture', display_order=1)
        db.put(sculpture)
        fig = ArtType(name="fig", display_name="Figurative", display_order=0, parent_type=sculpture)
        sother = ArtType(name="other", display_name="Other", display_order=1, parent_type=sculpture)
        db.put(fig)
        db.put(sother)

        mixed = ArtType(name='mixed', display_name='Mixed media', display_order=2)
        db.put(mixed)
        mother = ArtType(name="other", display_name="Other", display_order=0, parent_type=mixed)
        db.put(mother)

        archive = ArtType(name='archive', display_name='Archive', display_order=3)
        db.put(archive)
        oother = ArtType(name="other", display_name="Other", display_order=0, parent_type=archive)
        db.put(oother)

        self.redirect('/admin')
