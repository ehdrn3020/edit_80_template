;(function($, window, undefined){

	'use strict';


	$(document).ready(function(){
		//
	});


	NrvPub.UI = {
		GnbAction : function(){
			var $header = $('#header');
			var $depth1 = $('#gnb > ul > li');

			$depth1.on('mouseover focusin', function(){
				$header.addClass('depth2');
				$(this).addClass('on').siblings().removeClass('on');
			});

			$header.on('mouseleave focusout', function(){
				$header.removeClass('depth2');
				$depth1.removeClass('on');
			});
		},

		HeaderActive : function(){
			var $header  = $('#header');
			var $gnb	 = $('#gnb > ul');
			var $depth1  = $('#gnb > ul > li');
			var $showGnb = $('#showGnb');
			var x, y;
			var supportPageOffset = window.pageXOffset !== undefined;

			$header.on({
				'mouseover' : function(){
					$(this).addClass('active');
				},
				'mouseleave' : function(){
					if(y == 0){
						$(this).removeClass('active open');
					}
				}
			});

			$depth1.on('mouseover focusin', function(){
				$header.addClass('active open');
				$showGnb.children('.type').eq($(this).index()).addClass('on').siblings().removeClass('on');
			});

			$gnb.on('mouseleave focusout', function(){
				$header.removeClass('open');
			});

			$(window).on('load scroll', function(){
				x = supportPageOffset ? window.pageXOffset : isCSS1Compat ? document.documentElement.scrollLeft : document.body.scrollLeft;
				y = supportPageOffset ? window.pageYOffset : isCSS1Compat ? document.documentElement.scrollTOp : document.body.scrollTop;

				$header.css({'left':-x});
				
				if(y > 0){
					$header.addClass('active');
				}else{
					$header.removeClass('active');
				}
			});
		},

		QuickActive : function(){
			var $quickBtn = $('#quickBar > ol > li > a');
			var headerH = $('#header').height();

			$quickBtn.on('click', function(event){
				event.preventDefault();
				$('html, body').stop().animate({scrollTop:$(this.hash).offset().top - headerH}, 500);
			});

//			$(window).on('scroll', function(){
//				$quickBtn.each(function(){
//					var btn = $(this);
//					if($(window).scrollTop() >= $(this.hash).offset().top - headerH){
//						btn.parent().addClass('on').siblings().removeClass('on');
//					} else {
//						btn.parent().removeClass('on');
//					}
//				});
//			});
		},

		FaqList : function(){
			var $trg = $('#faq_list .qbox');

			$trg.on('click', function(){
				$(this).parent('li').toggleClass('on');
			});
		},

		ConsultActive : function(){
			$(window).on('scroll', function(){
				var scrTop = $(this).scrollTop();
				var $footer = $('#footer');
				var $consult = $('#simpleConsult');

				if(scrTop >= $(document).height() - $(window).height() - $footer.height()) {
					var btmH = $(document).height() - scrTop - $(window).height();
					$consult.css({
						'bottom' : $footer.height() - btmH
					});
				} else {
					$consult.css({
						'bottom' : '0'
					});
				}
			});			
		}
	}


	NrvPub.Slider = {
		BMainVisual : function(){
			var $slider = $('#bmain #mainvisual .slick-wrap');

			$slider.slick({
				arrows : true,
				dots : true,
				infinite : true,
				autoplay : true,
				autoplaySpeed : 5000,
				slidesToShow : 1,
				slidesToScroll : 1,
                appendArrows : $('#bmain #mainvisual .arrows_wrap'),
                appendDots : $('#bmain #mainvisual .dots_wrap')
			});
		},

		FMainVisual : function(){
			var $slider = $('#fmain #mainvisual .slick-wrap');

			$slider.slick({
				arrows : true,
				dots : true,
				infinite : true,
				autoplay : true,
				autoplaySpeed : 5000,
				slidesToShow : 1,
				slidesToScroll : 1,
                appendArrows : $('#fmain #mainvisual .arrows_wrap'),
                appendDots : $('#fmain #mainvisual .dots_wrap')
			});
		},

		MainSns : function(){
			var $slider = $('#snsWrap .slick-wrap');

			$slider.slick({
				arrows : true,
				dots : false,
				infinite : true,
				autoplay : true,
				autoplaySpeed : 4000,
				slidesToShow : 7,
				slidesToScroll : 1,
				swipe : false
			});
		},

		StoreVisual : function(){
			var $slider = $('#storeVisual .slick-wrap');

			$slider.slick({
				arrows : true,
				dots : false,
				infinite : true,
				autoplay : true,
				autoplaySpeed : 3000,
				slidesToShow : 1,
				slidesToScroll : 1
			});
		},

		SetMenu : function(){
			var $slider = $('#setMenu .slick-wrap');
			var iScrollPos = 0;
			var _scrollTimeout = null;
			var speed = 600;
			var flag = false;

			$slider.slick({
				arrows : false,
				speed : speed,
				dots : true,
                dotsClass: 'slick-dots',
				infinite : false,
				autoplay : false,
				vertical : true,
				verticalSwiping : true,
				slidesToShow : 1,
				slidesToScroll : 1
			});

			$(window).on('mousewheel', function(e){
				if(e.originalEvent.wheelDelta /120 > 0){
					if($(window).scrollTop() === 0){
						if(flag){
							return;
						}else{
							flag = true;
							$slider.slick('slickPrev');
							clearTimeout(_scrollTimeout);
							_scrollTimeout = setTimeout(function(){
								flag = false;
							}, speed);
						}
					}
				}else{
					if($slider.slick('slickCurrentSlide') < 3 || flag){
						e.preventDefault();
					}
					if(flag){
						return;
					}else{
						flag = true;
						$slider.slick('slickNext');
						clearTimeout(_scrollTimeout);
						_scrollTimeout = setTimeout(function(){
							flag = false;
						}, speed);
					}
				}
			});

			return $slider;
		}
	}


})(jQuery, window);