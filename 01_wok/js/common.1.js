$(function(){
    function header(){
        var $header = $('.header');
        $header.on('mouseover focusin', function(){
            $header.addClass('on');
        });
        $header.on('mouseleave focusout', function(){
            $header.removeClass('on');
        }); 
        $(window).on('scroll', function(){
            var headerH = $('.header').offset().top;
            if (headerH == 0) {
                $header.removeClass('on');
            } else {
                $header.addClass('on');
            }
        });
    };
    function mobile_open_close(){
        $('.aside_open').click(function(){
            $('html').addClass('on');
        })
        $('.aside_close').click(function(){
            $('html').removeClass('on');
        })
        $('.gnb_bg').click(function(){
            $('html').removeClass('on');
        })
    };
    function slick(){
        $('.main_visual .slick_wrap').slick({
            arrows: true,
            dots: true,
            infinite: true,
            autoplay: true,
            autoplaySpeed: 5000,
            slidesToShow: 1,
            slidesToScroll: 1,
            appendArrows: $('.main_visual .arrows_wrap'),
            appendDots: $('.main_visual .dots_wrap')
        });
        $('.sub02 .con_1 .slick_wrap').slick({
            arrows: true,
            dots: true,
            infinite: true,
            autoplay: true,
            autoplaySpeed: 5000,
            slidesToShow: 1,
            slidesToScroll: 1,
            appendArrows: $('.sub02 .con_1 .arrows_wrap'),
            appendDots: $('.sub02 .con_1 .dots_wrap')
        });
        $('.sns_wrap .slick_wrap').slick({
            arrows : true,
            dots : false,
            infinite : true,
            autoplay : true,
            autoplaySpeed : 4000,
            slidesToShow : 5,
            slidesToScroll : 1,
            swipe : false,
            appendArrows: $('.sns_wrap .arrows_wrap'),
            responsive: [
                {
                    breakpoint: 1024,
                    settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                    }
                },
                {
                    breakpoint: 480,
                    settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                    }
                }
            ]
        });
    };
    header();
    mobile_open_close();
    slick();
});