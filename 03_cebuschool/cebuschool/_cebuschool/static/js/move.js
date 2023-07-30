$(function(){ // jQuery 준비


		// 화면 높이가 200px 이동시 go top 버튼 보임
		var offset = 200;
		$(window).scroll(function(){
			var st=$(this).scrollTop();
			if(st > offset){ // 윈도우 스크롤 탑이 offset(200) 이상일때
				$('.go_top').fadeIn(500); // 점점 나타나라
			}else{
				$('.go_top').fadeOut(500); //스크롤 탑이 offset(200) 이하일때 점점사라져라
			}
		

		//마지막 콘텐츠 영역에 도달시 메뉴 스타일 적용
		if(st >= $('.content').height()-$(window).height()){
				$('ul.sub_navi > li > a').removeClass('on');
				$('ul.sub_navi > li:last').find('a').addClass('on');
		}

		}); //end : scroll

		// 맨위로 화면 스크롤
		$('.go_top').click(function(){
			$('html,body').animate({
				scrollTop:0
			},500);
			return false;
		});

				
}); //jQuery 종료