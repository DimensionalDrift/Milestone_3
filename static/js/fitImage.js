// This function is used to correctly display dynamically loaded images that can be of any size in a html 'frame'
fitImage = function(pic) {
  // Find the image width and height
  var h = $(pic).height(),
    w = $(pic).width();

  // If the image already has one of the below classes it is removed
  $(pic).removeClass("portrait landscape square circle");
  var m;
  // If the image is portrait
  if (h > w) {
    $(pic).addClass("portrait");
    // Calculate how much to shift the image to center it in the frame
    m = -((h / w) * 100 - 100) / 2;
    $(pic).css("margin-top", m + "%");
  }
  // If the image is landscape
  else if (w > h) {
    $(pic).addClass("landscape");
    // Calculate how much to shift the image to center it in the frame
    m = -((w / h) * 100 - 100) / 2;
    $(pic).css("margin-left", m + "%");
  }
  // If it is neither then it must be a square
  else {
    $(pic).addClass("square");
  }
};
