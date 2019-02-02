/*!
 * Start Bootstrap - Grayscale Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery to collapse the navbar on scroll
function collapseNavbar() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
}

function doTheSlidieSlide() {
    var slidies = $(".slidie-slide");
    var $body = $('body');
    var top = document.scrollingElement.scrollTop; //$body.scrollTop();
    slidies.each(function(index, element) {
        var $this = $(element)
        //$this.css({'backgroundPositionY': Math.min(-($this.offset().top - top) * 0.172, 600) + 'px'});
        var offset = Math.max(($this.parent().offset().top - top) * 0.1 + 80, -600);
        $this.find('.slidie-slide-image').css({
            'transform': 'translate3d(0px, ' + offset + 'px, 0px)',
            'top': 'auto',
            'height': ($this.parent().outerHeight() * 1.3) + 'px'
        });
    });
}

$(window).scroll(collapseNavbar);
$(document).ready(collapseNavbar);
$(document).scroll(doTheSlidieSlide);

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
  if ($(this).attr('class') != 'dropdown-toggle active' && $(this).attr('class') != 'dropdown-toggle') {
    $('.navbar-toggle:visible').click();
  }
});

$(function() {
    if ($('#youtube-playlist').length) {
        var controller = new YTV('youtube-playlist', {
           //user: 'taperunsout',
           accent: '#337ab7',
           responsive: true,
           playlist: $('#youtube-playlist').data('playlist')
        });
    }
    doTheSlidieSlide();
});
