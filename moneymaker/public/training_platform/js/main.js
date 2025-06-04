// intialization plugins
$(document).ready(function () {

    //animation icon toggler of navbar
    $(`.navbar-toggler`).click(function() {
        $(`.navbar-toggler`).toggleClass(`active`);
    });

    //Wow intit
    wow = new WOW({
        boxClass: 'wow',
        animateClass: 'animated',
        offset: 200,
        mobile: true,
        live: false
    });
    wow.init();

    //fancybox
    $("[data-fancybox]").fancybox({
        selector: '[data-fancybox="images"]',
        // loop: true
    });

    //  loader 
    // $(window).on("load", function() {
    //     $("#preloader").addClass("isdone");
    // });

    //more_butn  notifications_pg
    $(`.notifications_pg .item .p .more_butn`).click(function() {
        $(this).parent().toggleClass(`active`);
    });

    //more_butn courses_pg
    $(`.courses_pg .filter_box .show_more_butn `).click(function() {
        $(this).toggleClass(`active`);

        $(this).parent().find('.categs_inner').toggleClass(`active`);
    });


    //expandButn in course_cont_pg
    $(`.course_cont_pg #expandButn`).click(function() {
        $(`.course_cont_pg .lg_box`).removeClass(`col-lg-8`);
        $(`.course_cont_pg .lg_box`).addClass(`col-lg-12`);
        $(`.course_cont_pg .left_box`).removeClass(`col-lg-4`);
        $(`.course_cont_pg .left_box`).addClass(`beDrawer `);
        $(`.course_cont_pg .drawerButn`).addClass(`active `);

    });
    
    //drawerButn in course_cont_pg
    $(`.course_cont_pg .drawerButn`).click(function() {
        $(`.course_cont_pg .lg_box`).addClass(`col-lg-8`);
        $(`.course_cont_pg .lg_box`).removeClass(`col-lg-12`);
        $(`.course_cont_pg .left_box`).addClass(`col-lg-4`);
        $(`.course_cont_pg .left_box`).removeClass(`beDrawer `);
        $(`.course_cont_pg .drawerButn`).removeClass(`active `);
    });

});

// Swiper
$(document).ready(function () {

    //////////////////// Swiper  ////////////////////
    var swiper = new Swiper('.sponsors_sec2 .sponsors_swiper', {
        loop: true,
        speed: 3000,
        slidesPerView: 2,
        spaceBetween: 15,
        freeMode: true,
        loopAddBlankSlides:true,
        // cssMode:true,
        grabCursor: true,
        loopAdditionalSlides: 2,
        autoplay: {
            delay: 0,
            disableOnInteraction:false,
        },
        navigation: {
            nextEl: '.sponsors_sec2 .swiper-button-next',
            prevEl: '.sponsors_sec2 .swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 20,
            },
            1024: {
                slidesPerView: 6,
                spaceBetween: 20,
            },
        }
    });

    
    // ------------ courses tabs slider -----------
    var swiper = new Swiper(' .courses_sec .courses-tabs-slider', {
        slidesPerView: 2,
        spaceBetween: 50,
        // centeredSlides: true,
        speed: 1000,
        pagination: {
            el: ' .courses_sec .swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: ' .courses_sec .swiper-button-next',
            prevEl: ' .courses_sec .swiper-button-prev',
        },
        mousewheel: false,
        keyboard: true,
        // autoplay: {
        //     delay: 20000,
        // },
        loop: false,
        breakpoints: {
            0: {
                slidesPerView: 2,
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
                slidesPerView: 5,
            }
        }
    });

    //////////////////// Swiper  ////////////////////
    var swiper = new Swiper('.partners_sec .sponsors_swiper', {
        loop: true,
        speed: 3000,
        slidesPerView: 2,
        spaceBetween: 15,
        freeMode: true,
        loopAddBlankSlides:true,
        // cssMode:true,
        grabCursor: true,
        loopAdditionalSlides: 2,
        autoplay: {
            delay: 0,
            disableOnInteraction:false,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 20,
            },
            1024: {
                slidesPerView: 5,
                spaceBetween: 20,
            },
        }
    });


    //////////////////// Swiper  ////////////////////
    var swiper = new Swiper('.courses_sec .courses_swiper', {
        // loop: true,
        speed: 900,
        slidesPerView: 1,
        spaceBetween: 15,
        // autoplay: {
        //     delay: 2500,
        // },
        navigation: {
            nextEl: '.courses_sec .swiper-button-next',
            prevEl: '.courses_sec .swiper-button-prev',
        },
        pagination: {
            el: '.courses_sec .swiper-pagination',
            clickable: true
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 20,
            },
            1024: {
                slidesPerView: 3,
                spaceBetween: 20,
            },
        }
    });

    //////////////////// Swiper  ////////////////////
    // var swiper = new Swiper(' .swiper-container', {
    //     // loop: true,
    //     speed: 900,
    //     slidesPerView: 1,
    //     spaceBetween: 15,
    //     // autoplay: {
    //     //     delay: 2500,
    //     // },
    //     //In Tabs
    //     // observer: true,
    //     // observeParents: true,
    //     navigation: {
    //         nextEl: '.swiper-button-next',
    //         prevEl: '.swiper-button-prev',
    //     },
    //     pagination: {
    //         el: '.swiper-pagination',
    //         clickable: true
    //     },
    //     breakpoints: {
    //         640: {
    //             slidesPerView: 2,
    //             spaceBetween: 20,
    //         },
    //         768: {
    //             slidesPerView: 3,
    //             spaceBetween: 20,
    //         },
    //         1024: {
    //             slidesPerView: 5,
    //             spaceBetween: 20,
    //             // Prevent swiper in lg screens
    //             // allowTouchMove: false,
    //             // preventClicks: false
    //         },
    //     }
    // });

});


var x = document.getElementsByClassName("msg_data_box");
if(x && x.length > 0) {
    if (x == 1) {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
}


// ------------ SHOW HED PASS ----------
$(document).ready(function() {
    $(".show_hide_password .show_pass").on('click', function(event) {
        event.preventDefault();
        if($(this).siblings("input").attr("type") == "text"){
            $(this).siblings("input").attr('type', 'password');
            $(this).addClass( "fa-eye-slash" );
            $(this).removeClass( "fa-eye" );
        }else if($(this).siblings("input").attr("type") == "password"){
            $(this).siblings("input").attr('type', 'text');
            $(this).removeClass( "fa-eye-slash" );
            $(this).addClass( "fa-eye" );
        }
    });
});


// DARK MODE THEME
// function to set a given theme/color-scheme
function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
}

// function to toggle between light and dark theme
function toggleTheme() {
    if (localStorage.getItem('theme') === 'theme-dark') {
        setTheme('theme-light');
    } else {
        setTheme('theme-dark');
    }
}

// Immediately invoked function to set the theme on initial load
(function () {
    if (localStorage.getItem('theme') === 'theme-dark') {
        setTheme('theme-dark');
        document.getElementById('slider').checked = false;
    } else {
        setTheme('theme-light');
      document.getElementById('slider').checked = true;
    }
})();

// 
$(`.themeToggler .switch `).click(function() {
    $(`.form-switch`).toggleClass(`active`);
});