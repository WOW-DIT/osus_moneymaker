$(document).ready(function() {

    var wind = $(window);

    wow = new WOW({
        boxClass: 'wow',
        animateClass: 'animated',
        offset: 200,
        mobile: false,
        live: false
    });
    wow.init();




    // ---------- to top -----------
    $('.to-top').click(function() {
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
        return false;
    });


});


// ------------ swiper sliders -----------
$(document).ready(function() {

    // ------------ courses tabs slider -----------
    var swiper = new Swiper('.courses .courses-tabs-slider', {
        slidesPerView: 4,
        spaceBetween: 50,
        // centeredSlides: true,
        speed: 1000,
        pagination: {
            el: '.courses .swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.courses .swiper-button-next',
            prevEl: '.courses .swiper-button-prev',
        },
        mousewheel: false,
        keyboard: true,
        autoplay: {
            delay: 20000,
        },
        loop: false,
        breakpoints: {
            0: {
                slidesPerView: 1,
            },
            480: {
                slidesPerView: 2,
            },
            787: {
                slidesPerView: 3,
            },
            991: {
                slidesPerView: 4,
            },
            1200: {
                slidesPerView: 4,
            }
        }
    });


    // ------------ sponsors slider -----------
    var swiper = new Swiper('.sponsors-slider', {
        slidesPerView: 3,
        spaceBetween: 30,
        // centeredSlides: true,
        speed: 1000,
        pagination: {
            el: '.sponsors-slider .swiper-pagination',
            clickable: true,
        },
        navigation: false,
        mousewheel: false,
        keyboard: true,
        autoplay: {
            delay: 5000,
        },
        loop: true,
        breakpoints: {
            0: {
                slidesPerView: 1,
            },
            480: {
                slidesPerView: 2,
            },
            787: {
                slidesPerView: 3,
            },
            991: {
                slidesPerView: 3,
            },
            1200: {
                slidesPerView: 4,
            }
        }
    });


    // ------------ courses tabs slider -----------
    var swiper = new Swiper('.customers .customers-slider', {
        slidesPerView: 4,
        spaceBetween: 30,
        // centeredSlides: true,
        speed: 1000,
        pagination: {
            el: '.customers .swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.customers .swiper-button-next',
            prevEl: '.customers .swiper-button-prev',
        },
        mousewheel: false,
        keyboard: true,
        autoplay: {
            delay: 20000,
        },
        loop: true,
        breakpoints: {
            0: {
                slidesPerView: 1,
            },
            480: {
                slidesPerView: 2,
            },
            787: {
                slidesPerView: 3,
            },
            991: {
                slidesPerView: 4,
            },
            1200: {
                slidesPerView: 4,
            }
        }
    });



});


$(document).ready(function() {
    
})
