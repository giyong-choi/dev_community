// Prallax script
$(window).scroll(function () {
    var scrollTop = $(this).scrollTop();
    $('.parallax-bg').css('top', -(scrollTop / 3) + 'px');
});
