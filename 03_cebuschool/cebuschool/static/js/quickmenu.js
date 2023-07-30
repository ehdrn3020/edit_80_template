$(function(){ 
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