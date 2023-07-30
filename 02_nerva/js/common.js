$(document).ready(function(){
	// gnb
	$('.c-gnb__link').on('mouseenter', function(){
		var idx = $(this).parent().index();
		$('.c-gnb__item').removeClass('c-gnb__item--active');
		$(this).parent().addClass('c-gnb__item--active');
		
		$('.c-menus').addClass('c-menus--active');
		$('.c-menu').removeClass('c-menu--active');
		$('.c-menu').eq(idx).addClass('c-menu--active');
	});
	
	$('.c-header').on('mouseleave', function(){
		$('.c-menus').removeClass('c-menus--active');
		$('.c-menu').removeClass('c-menu--active');
		$('.c-gnb__item').removeClass('c-gnb__item--active');	
	});
	
	// menu close
	$('.c-menu .c-menu__close').on('click', function(){
		$('.c-menus').removeClass('c-menus--active');
		$('.c-menu').removeClass('c-menu--active');
		$('.c-gnb__item').removeClass('c-gnb__item--active');

		return false;
	});
	
	// navi
	$('.c-navi__link').on('click', function(){
		var idx = $(this).parent().index();
			$('.n-menus').removeClass('n-menus--active');
			$('.n-menus .n-menu').removeClass('n-menu--active');

			$('.n-country__link').removeClass('n-country__link--active');
			$('.n-country__name').removeClass('n-country__name--active');
			$('.n-country__link').eq(3).addClass('n-country__link--active');
			$('.n-country__name').eq(3).addClass('n-country__name--active');

		if ( $(this).parent().hasClass('c-navi__item--active')){
			$(this).parent().removeClass('c-navi__item--active');
		}else {
			$('.c-navi__item').removeClass('c-navi__item--active');
			$(this).parent().addClass('c-navi__item--active');
			$('.n-menus').addClass('n-menus--active');
			$('.n-menus .n-menu').eq(idx).addClass('n-menu--active');
		}

		return false;
	});

	$('.n-menus .c-menu__close').on('click', function(){
		$('.n-menus').removeClass('n-menus--active');
		$('.n-menus .n-menu').removeClass('n-menu--active');
		$('.c-navi__item').removeClass('c-navi__item--active');

		return false;
	});
	
	// navi > country
	$('.n-country__link').on('mouseenter', function(){
		var idx = $(this).index();
		
		$('.n-country__link').removeClass('n-country__link--active');
		$(this).addClass('n-country__link--active');

		$('.n-country__name').removeClass('n-country__name--active');
		$('.n-country__name').eq(idx).addClass('n-country__name--active');
	});

});