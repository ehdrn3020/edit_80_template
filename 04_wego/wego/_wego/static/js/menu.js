	var $ = jQuery; 

		$(function(){ // jQuery 준비
		/* 메뉴 */
	var $menu = $('.m_nav'), $menulink = $('#spinner-form');
	$menulink.click(function (e) {
		$menulink.toggleClass('active');
		$menu.toggleClass('active');
	});

	}); //jQuery 종료