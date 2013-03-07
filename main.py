#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *
from controllers import gallery
from controllers import contact
from controllers import admin
from controllers import images


def main():
    application = webapp.WSGIApplication([
            ('/', gallery.MainHandler),
            ('/about', gallery.AboutHandler),
            ('/contact', contact.ContactHandler),
            ('/thanks', contact.ContactCompleteHandler),
            ('/admin/list', admin.ListArtHandler),
            ('/admin', admin.AdminHomeHandler),
            ('/admin/create', admin.CreateArtHandler),
            (r'/admin/artwork/(.*)/edit', admin.EditFormHandler),
            (r'/admin/artwork/(.*)', admin.ArtItemHandler),
            (r'/admin/slideshow', admin.SlideshowAdminHandler),
            (r'/admin/about', admin.AboutAdmin),
            (r'/admin/seed', admin.SeedData),
            (r'/photo/(.*)', images.PhotoHandler),
            (r'/img/(.*)', images.Image),
            (r'/gallery/(.*)', gallery.GalleryItemHandler),
            (r'/(.*)/(.*)', gallery.GalleryHandler)
        ],
        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
