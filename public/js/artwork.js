var app = app || {};
app.Artwork = function () {

  var pad = 200; // pixels
  var padBottom = 150; //pixels

  function buildImageUrl (photoId, width, height) {
    return "/img/" + photoId + "?w=" + width + "&h=" + height;
  }

  return {
    Images: function () {
      return {
        mainImageWidth: 520, mainImageHeight: 400,
        thumbWidth: 160,
        thumbHeight: 120,
        lightboxPadding: pad,
        padBottom: padBottom };
    }(),

    maxImageSize: function() {
      var maxwidth = $(window).width() - pad;
      var maxheight = $(window).height() - padBottom;
      return { width: maxwidth, height: maxheight };
    },

    ResetAllThumbUrls: function () {
      $('.thumbnail').each(function () {
        $id = $(this).attr('data-id');
        var max = app.Artwork.maxImageSize();
        var url = buildImageUrl($id, max.width, max.height);
        $(this).attr('href', url);
      });
    }
  };
}();

$(document).ready(function() {
  // Fix the lightbox URLs on load to take account of current browser window size
  app.Artwork.ResetAllThumbUrls();

  // Make sure the picture sizes we request for the lightbox
  // are never bigger than the browser viewport
  $(window).resize(function() {
    app.Artwork.ResetAllThumbUrls();
  });

  var $id = $('#piece-id').val();
  $('#backnav').attr('href', document.referrer + "#" + $id);
});

