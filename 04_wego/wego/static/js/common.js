$(function(){ 
	// 모바일 - 맨위로 화면 스크롤
		$('.gotop').click(function(){
			if($(window).width() <=1119){
			$('html,body').animate({
				scrollTop:0
			},500);
			return false;
			}
		});
	/* 
	탭기능 - 모바일 마이페이지 메뉴
		$('.m_mypage_nav').hide();
		$('.mypage_nav ul li').click(function(){ 
			 if($(window).width() <=1119){
               $('.mypage_nav ul li').removeClass('selected'); 
				$(this).addClass('selected'); 
				$('.m_mypage_nav').hide();
				$('.m_mypage_nav').eq($(this).index()).show(); 	
					return false; 
            }
		}); 
	*/
	//모바일 - 검색 버튼
		var search_show = false;
		$(".util_icon li.search ").click(function(){
			search_show  = !search_show 
			if(search_show){
				$(".hd_sch_wr").slideDown();
			}else{
				$(".hd_sch_wr").slideUp();
			}
		});

	//상단 유틸메뉴 중 썸네일 버튼
		var my_info_show = false;
		$(".hd_my_info a").click(function(){
		my_info_show = !my_info_show
		if(my_info_show){
				$(this).find("+ul").slideDown("");
				$(this).find(".my_thum").addClass("active");
				return false;
			}else{
				$(this).find("+ul").slideUp(""); 	
				$(this).find(".my_thum").removeClass("active");
				return false;
			}
	});
	// 리뷰 사이드 베스트 섹션 탭기능
		$('.best_tab li a').eq(0).addClass('selected'); 
		$('.best_tab_content').hide();
		$('.best_tab_content').eq(0).show(); 
		$('.best_tab li').click(function(){
			$('.best_tab li a').removeClass('selected'); 
			$(this).find("a").addClass('selected'); 
			$('.best_tab_content').hide();
			$('.best_tab_content').eq($(this).index()).show(); 	
				return false; 
		});

});