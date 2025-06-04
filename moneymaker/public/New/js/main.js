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

});

// Swiper
$(document).ready(function () {

    //////////////////// partners_swiper  ////////////////////
    var swiper = new Swiper('.partners_sec .partners_swiper', {
        loop: true,
        speed: 900,
        slidesPerView: 1,
        spaceBetween: 15,
        // centeredSlides: true,
        // autoplay: {
        //     delay: 2500,
        // },
        navigation: {
            nextEl: '.partners_sec .swiper-button-next',
            prevEl: '.partners_sec .swiper-button-prev',
        },
        pagination: {
            el: '.partners_sec .swiper-pagination',
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
                slidesPerView: 4,
                spaceBetween: 20,
            },
        }
    });

    //////////////////// feedback_swiper  ////////////////////
    var swiper = new Swiper('.feedback_sec .feedback_swiper', {
        loop: true,
        speed: 900,
        slidesPerView: 1,
        spaceBetween: 15,
        centeredSlides: true,
        // autoplay: {
        //     delay: 2500,
        // },
        navigation: {
            nextEl: '.feedback_sec .swiper-button-next',
            prevEl: '.feedback_sec .swiper-button-prev',
        },
        pagination: {
            el: '.feedback_sec .swiper-pagination',
            clickable: true
        },
        breakpoints: {
            1024: {
                slidesPerView: 1.7,
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


// ------------ gsap scripts -----------
// $(function () {

//     gsap.registerPlugin(ScrollTrigger, ScrollSmoother);

//     const smoother = ScrollSmoother.create({
//         content: "#scrollsmoother-container",
//         smooth: 1.5,
//         normalizeScroll: true,
//         ignoreMobileResize: true,
//         effects: true,
//     });

//     gsap.timeline({ scrollTrigger: { 
//         trigger: ".about_sec",  start: "-600 top",  scrub: !0 
//     } }).to(".about_sec .secImg", {
//             x: -50, y: 0, scale: 1, duration: 20, ease: "linear", delay: 0 
//         }
//     ),
//     gsap.timeline({ scrollTrigger: { 
//         trigger: ".service_sec",  start: "-600 top",  scrub: !0 
//     } }).from(".service_sec .serv_box" , 
//         { x: 0,y: 0, scale: 0.8,duration: 15, ease: "none",delay: 0,
//     }).to(".service_sec .serv_box", {
//             x: 0,y: 0, scale: 1,duration: 15, ease: "none",delay: 0
//         }
//     ),
//     gsap.timeline({ scrollTrigger: { 
//         trigger: ".header",  start: "-600 top",  scrub: !0 
//     } }).to(".header .heroImg", {
//         x: 20,
//         y: 0,
//         scale: 1,
//         duration: 20,
//         ease: "none",
//         delay: 0,
//         // rotationZ: -90,
//         }
//     );



// });
