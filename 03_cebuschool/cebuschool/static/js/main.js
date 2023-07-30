$(document).ready(function(){
	var show = false;
	$(".sec_btn_left1").click(function(){
		show = !show
		if(show){
				$(this).find("+.sec_menu").slideDown("");
				$(this).find(".all_view_btn").addClass("active");
				$(this).find(".all_view_btn").find("a").html("<i class='fas fa-times'></i>");
				return false;
			}else{
				$(this).find("+.sec_menu").slideUp(""); 	
				$(this).find(".all_view_btn").removeClass("active");
				$(this).find(".all_view_btn").find("a").html("<i class='fas fa-bars'></i>");
				return false;
			}
	});
	var showshow = false;
	$(".sec_btn_left2").click(function(){
		showshow = !showshow
		if(showshow){
				$(this).find("+.sec_menu").slideDown("");
				$(this).find(".all_view_btn").addClass("active");
				$(this).find(".all_view_btn").find("a").html("<i class='fas fa-times'></i>");
				return false;
			}else{
				$(this).find("+.sec_menu").slideUp(""); 	
				$(this).find(".all_view_btn").removeClass("active");
				$(this).find(".all_view_btn").find("a").html("<i class='fas fa-bars'></i>");
				return false;
			}
	});
	// 탭기능 - 메인 세부 여행후기 섹션
		$('ul.tab > li').eq(0).addClass('selected'); 
		$('.tab_content').hide();
		$('.tab_content').eq(0).show(); 
		$('ul.tab > li').click(function(){
			$('ul.tab > li').removeClass('selected'); 
			$(this).addClass('selected'); 
			$('.tab_content').hide();
			$('.tab_content').eq($(this).index()).show(); 	
				return false; 
		});

		// 탭기능 - 모바일 메인 세부 여행후기 섹션
		$('.tab > div').eq(0).addClass('selected'); 
		$('.tab_content').hide();
		$('.tab_content').eq(0).show(); 
		$('.tab > div').click(function(){
			$('.tab > div').removeClass('selected'); 
			$(this).addClass('selected'); 
			$('.tab_content').hide();
			$('.tab_content').eq($(this).index()).show(); 	
				return false; 
		});
		
		// 탭기능 - 메인 로그인 박스
		$('.main_login_box').hide();
		$('.main_login_btm ul li').click(function(){ 
			$('.main_login_btm ul li').removeClass('selected'); 
			$(this).addClass('selected'); 
			$('.main_login_box').hide();
			$('.main_login_box').eq($(this).index()).show(); 	
				return false; 
		});
		$(document).click(function(){
				$('.main_login_btm ul li').removeClass('selected'); 
				$('.main_login_box').hide();
		});

		// 탭기능 - 메인 쇼핑 섹션
		$('ul.tab2 > li').eq(0).addClass('selected'); 
		$('.tab2_content').hide();
		$('.tab2_content').eq(0).show(); 
		$('ul.tab2 > li').click(function(){ 
			$('ul.tab2 > li').removeClass('selected'); 
			$(this).addClass('selected'); 
			var swiper11= new Swiper('.swiper11');
			var swiper12= new Swiper('.swiper12');
			var swiper13= new Swiper('.swiper13');
			$('.tab2_content').hide();
			$('.tab2_content').eq($(this).index()).show(); 	
				return false; 
		});

		/* quick 메뉴 */
		var quickID = $('.quick_menu');
		var offset = quickID.offset();
		$(window).scroll(function(){
			if($(window).scrollTop() > offset.top){ 
				quickID.stop().animate({
					marginTop : $(window).scrollTop() 
				},1000);
			}else{
					quickID.stop().animate({
					marginTop:0 
				},200);
			}
		});
});

