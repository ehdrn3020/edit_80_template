$(document).ready(function(){
	// tab menu
	$('.promotion_tab li').click(function(){
		$(this).parents().find('li').removeClass("selected");
		$(this).addClass("selected");
		$(".sort-box").removeClass('active');
		$('.sort-box').hide();
		$(".sort-box[data-id='"+$(this).find('a').attr('data-id')+"']").addClass("active");
		if($(".sort-box[data-id='"+$(this).find('a').attr('data-id')+"']").find("active")){
			$('.sort-box.active').slideDown();
		}
  });
	$('.promotion_tab_sub li').click(function(){
		$(this).parents().find('li').removeClass("selected_sub");
		$(this).addClass("selected_sub");
		$(".sort-box_sub").removeClass('active_sub');
		$('.sort-box_sub').hide();
		$(".sort-box_sub[data-id='"+$(this).find('a').attr('data-id')+"']").addClass("active_sub");
		if($(".sort-box_sub[data-id='"+$(this).find('a').attr('data-id')+"']").find("active_sub")){
			$('.sort-box_sub.active_sub').slideDown();
		}
  });

	//event tag
	$('.box_event span').click(function(){
		$(this).parents().find('span').removeClass("selected");
		$(this).addClass("selected");
		$(".clear").removeClass('active');
		$('.clear').hide();
		$(".clear[data-id='"+$(this).attr('data-id')+"']").addClass("active");
		if($(".clear[data-id='"+$(this).attr('data-id')+"']").find("active")){
			$('.clear.active').slideDown();
		}
  });
	$('.box_event_sub span').click(function(){
		$(this).parents().find('span').removeClass("selected_sub");
		$(this).addClass("selected_sub");
		$(".clear_sub").removeClass('active_sub');
		$('.clear_sub').hide();
		$(".clear_sub[data-id='"+$(this).attr('data-id')+"']").addClass("active_sub");
		console.log($(this).attr('data-id'));
		if($(".clear_sub[data-id='"+$(this).attr('data-id')+"']").find("active_sub")){
			console.log(123123);
			$('.clear_sub.active_sub').slideDown();
		}
  });

	//score btn focus
	$('.score_btn').click(function(){
		$(".comment_content").focus();
	});

	$(window).resize(function(){
		var width_size = window.outerWidth;
		if (width_size <= 660) {
			//$('.slide_mob .swiper-button-next').addClass("slide_btn_next");
			//$('.slide_mob .swiper-button-prev').addClass("slide_btn_prev");
		}
	});

	//slider
	var galleryThumbs = new Swiper('.gallery-thumbs', {
		slidesPerView: 3,
		freeMode: true,
		direction: 'vertical',
		watchSlidesProgress: true,
	});
	var galleryTop = new Swiper('.gallery-top', {
		autoplay: true,
		thumbs: {
			swiper: galleryThumbs
		},

		breakpointsInverse: true,
		breakpoints: {
			320:{
				navigation: {
					nextEl: '.swiper-button-next',
					prevEl: '.swiper-button-prev',
				},
			},
			640:{
				navigation: {
					nextEl: '.slide_btn_prev',
					prevEl: '.slide_btn_next',
				},
			}
		}
	});

	//reserve slide
	var galleryThumbs_ = new Swiper('.gallery-thumbs_', {
		direction: 'vertical',
		slidesPerView: 5,
		slidesPerColumn: 2,
		spaceBetween: 10,
		freeMode: true,
		watchSlidesVisibility: true,
		watchSlidesProgress: true,
		scrollbar : {
			el : '.swiper-scrollbar',
			draggable: true,
		},

	});
	var galleryTop_ = new Swiper('.gallery-top_', {
		effect: 'fade',
		loop: true,
		autoHeight : true,
		speed : 10,
		pagination: {
			el: '.swiper-pagination',
			type: 'fraction',
		 },
		navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev',
		},
		thumbs: {
			swiper: galleryThumbs_
		},

	});

	var swiper = new Swiper('.slide_reserv', {
      slidesPerView: 3,
	  slidesPerGroup : 3,
	  spaceBetween: 10,
	  freeMode: true,
	  breakpointsInverse: true,
	  breakpoints: {
		  320: {
			  slidesPerView: 1,
			  slidesPerGroup : 1,
			},
		  490: {
			  slidesPerView: 1,
			  slidesPerGroup : 1,
			},
		  501: {
			  slidesPerView: 3,
			  slidesPerGroup : 3,
			},
		  640: {
			  slidesPerView: 3,
			  slidesPerGroup : 3,
		  }
	  },

      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
    });

	$('.gallery_wrap').click(function(){
		$('.swipe_warp').css({"opacity": 0, "visibility": "visible"}).animate({opacity: '1'}, 'slow');
	});
	$('.lg-close').click(function(){
		$('.swipe_warp').css("visibility","hidden");

	});

	//bar
	var barProgress = $(".progressbar");
	barProgress.eq(0).progressbar({ value:parseFloat($('.progress .point').eq(0).text())*20 });
	barProgress.eq(1).progressbar({ value:parseFloat($('.progress .point').eq(1).text())*20 });
	barProgress.eq(2).progressbar({ value:parseFloat($('.progress .point').eq(2).text())*20 });
	barProgress.eq(3).progressbar({ value:parseFloat($('.progress .point').eq(3).text())*20 });
	barProgress.eq(4).progressbar({ value:parseFloat($('.progress .point').eq(4).text())*20 });
	barProgress.eq(5).progressbar({ value:parseFloat($('.progress .point').eq(5).text())*20 });
	barProgress.eq(6).progressbar({ value:parseFloat($('.progress .point').eq(6).text())*20 });

	//star
	$('.starRev span').click(function(){
	  $(this).parent().children('span').removeClass('on');
	  $(this).addClass('on').prevAll('span').addClass('on');
		var star_num = $(this).text();
		$(this).parent().children('input[type=hidden]').val(star_num);
	  return false;
	});

	// 영업시간 Old Value
	if($("#day_mon").prop('checked') == true){
		$("#day_mon").parent().addClass('on');
	}
	if($("#day_tue").prop('checked') == true){
		$("#day_tue").parent().addClass('on');
	}
	if($("#day_wed").prop('checked') == true){
		$("#day_wed").parent().addClass('on');
	}
	if($("#day_thu").prop('checked') == true){
		$("#day_thu").parent().addClass('on');
	}
	if($("#day_fri").prop('checked') == true){
		$("#day_fri").parent().addClass('on');
	}
	if($("#day_sat").prop('checked') == true){
		$("#day_sat").parent().addClass('on');
	}
	if($("#day_sun").prop('checked') == true){
		$("#day_sun").parent().addClass('on');
	}
	if($("#day_all").prop('checked') == true){
		$("#day_all").parent().addClass('on');
	}
	// 영업시간 클릭시
	$("#day_mon").click(function(){
		if($(this).prop('checked') == true){ $(this).parent().addClass('on'); }
		else{ $(this).parent().removeClass('on'); }
	});
	$("#day_tue").click(function(){
		if($(this).prop('checked') == true){ $(this).parent().addClass('on'); }
		else{ $(this).parent().removeClass('on'); }
	});
	$("#day_wed").click(function(){
		if($(this).prop('checked') == true){ $(this).parent().addClass('on'); }
		else{ $(this).parent().removeClass('on'); }
	});
	$("#day_thu").click(function(){
		if($(this).prop('checked') == true){ $(this).parent().addClass('on'); }
		else{ $(this).parent().removeClass('on'); }
	});
	$("#day_fri").click(function(){
		if($(this).prop('checked') == true){ $(this).parent().addClass('on'); }
		else{ $(this).parent().removeClass('on'); }
	});
	$("#day_sat").click(function(){
		if($(this).prop('checked') == true){ $(this).parent().addClass('on'); }
		else{ $(this).parent().removeClass('on'); }
	});
	$("#day_sun").click(function(){
		if($(this).prop('checked') == true){ $(this).parent().addClass('on'); }
		else{ $(this).parent().removeClass('on'); }
	});
	$("#day_all").click(function(){
		if($(this).prop('checked') == true){
			$('.pd_top > label').addClass('on');
			$('.pd_top > label > input:checkbox').prop('checked', true);
		}
		else{
			$('.pd_top > label').removeClass('on');
			$('.pd_top > label > input:checkbox').prop('checked', false);
		}
	});

	$('input.timepicker01').timepicker({});
	$('input.timepicker02').timepicker({});

	//편의시설 Old Value
	if($("#opt1").prop('checked') == true){ $("#opt1").parent().addClass('on'); }
	if($("#opt2").prop('checked') == true){ $("#opt2").parent().addClass('on'); }
	if($("#opt3").prop('checked') == true){ $("#opt3").parent().addClass('on'); }
	if($("#opt4").prop('checked') == true){ $("#opt4").parent().addClass('on'); }
	if($("#opt5").prop('checked') == true){ $("#opt5").parent().addClass('on'); }
	if($("#opt6").prop('checked') == true){ $("#opt6").parent().addClass('on'); }
	if($("#opt7").prop('checked') == true){ $("#opt7").parent().addClass('on'); }
	if($("#opt8").prop('checked') == true){ $("#opt8").parent().addClass('on'); }
	if($("#opt9").prop('checked') == true){ $("#opt9").parent().addClass('on'); }
	if($("#opt10").prop('checked') == true){ $("#opt10").parent().addClass('on'); }

	if($("#opt11").prop('checked') == true){ $("#opt11").parent().addClass('on'); }
	if($("#opt12").prop('checked') == true){ $("#opt12").parent().addClass('on'); }
	if($("#opt13").prop('checked') == true){ $("#opt13").parent().addClass('on'); }
	if($("#opt14").prop('checked') == true){ $("#opt14").parent().addClass('on'); }
	if($("#opt15").prop('checked') == true){ $("#opt15").parent().addClass('on'); }
	if($("#opt16").prop('checked') == true){ $("#opt16").parent().addClass('on'); }
	if($("#opt17").prop('checked') == true){ $("#opt17").parent().addClass('on'); }
	if($("#opt18").prop('checked') == true){ $("#opt18").parent().addClass('on'); }
	if($("#opt19").prop('checked') == true){ $("#opt19").parent().addClass('on'); }
	if($("#opt20").prop('checked') == true){ $("#opt20").parent().addClass('on'); }

	//편의시설 클릭시
	$('.reserve_btn').click(function(){
		if($(this).hasClass('on')){
			$(this).removeClass('on');
			// $(this).children('input[type=checkbox]').attr('value', 'N')
			$(this).children('input[type=checkbox]').prop('checked', false);
			console.log($(this).children('input[type=checkbox]').attr('value'));
		}else{
			$(this).addClass('on');
			// $(this).children('input[type=checkbox]').attr('value', 'Y')
			$(this).children('input[type=checkbox]').prop('checked', true);
			console.log($(this).children('input[type=checkbox]').attr('value'));
		}
	});

	//reserve page right box
	$(window).scroll(function(){
		var height = $(document).scrollTop();
		if(height > 700){
		  $('.move_menu').addClass('fixinner');
		}else if(height < 700){
		  $('.move_menu').removeClass('fixinner');
		}
	  });

	//이미지 선택
	$('.imgUpload_promotion, .imgUpload_promotion_rep').click(function(){
		var img = $(this).children('img');
		if(img.hasClass('on')){
			img.removeClass('on');
			img.css('border', '');
		}
		else{
			img.css('border', 'solid 3px #ff5a60');
			img.addClass('on');
		}
	});
});

// 선택된이미지 삭제
function del_img(){
	var arrimg = new Array();
	var arrpimg = new Array();
	var idx = 0;
	var img = $('.imgUpload_promotion');
	// 클릭된것 지우기
	for(i=0; i<img.length; i++){
		if(img.eq(i).children('img').hasClass('on')){
			$('.img'+(i+1)).attr('src','');
			$('.pimg'+(i+1)).attr('value','');
			img.eq(i).children('img').removeClass('on');
			img.eq(i).children('img').css('border', '');
		}
		// 클릭되지않은것 따로 배열저장
		else if($('.img'+(i+1)).attr('src')!=''){
			arrimg[idx] = $('.img'+(i+1)).attr('src');
			arrpimg[idx] = $('.pimg'+(i+1)).attr('value');
			idx++;
		}
	}
	// 앞으로땡기기
	for(i=0; i<img.length; i++){
		if(arrimg[i]){
			$('.img'+(i+1)).attr('src',arrimg[i]);
			$('.pimg'+(i+1)).attr('value',arrpimg[i]);
		}else{
			$('.img'+(i+1)).attr('src','');
			$('.pimg'+(i+1)).attr('value','');
			img.eq(i).css('display','none');
		}
	}
}
// 선택된 대표이미지 삭제
function del_img_rep(){
	var arrimg = new Array();
	var arrpimg = new Array();
	var arrtxt = new Array();
	var idx = 0;
	var img = $('.imgUpload_promotion_rep');
	// 클릭된것 지우기
	for(i=0; i<img.length; i++){
		if(img.eq(i).children('img').hasClass('on')){
			$('.img'+(i+1)+'_second').attr('src','');
			$('.pimg'+(i+1)+'_second').attr('value','');
			img.eq(i).children('img').removeClass('on');
			img.eq(i).children('img').css('border', '');
		}
		// 클릭되지않은것 따로 배열저장
		else if($('.img'+(i+1)+'_second').attr('src')!=''){
			arrimg[idx] = $('.img'+(i+1)+'_second').attr('src');
			arrpimg[idx] = $('.pimg'+(i+1)+'_second').attr('value');
			arrtxt[idx] = $('.rep_img'+(i+1)+'_txt').attr('value');
			idx++;
		}
	}
	// 앞으로땡기기
	for(i=0; i<img.length; i++){
		if(arrimg[i]){
			$('.img'+(i+1)+'_second').attr('src',arrimg[i]);
			$('.pimg'+(i+1)+'_second').attr('value',arrpimg[i]);
			$('.rep_img'+(i+1)+'_txt').attr('value',arrtxt[i]);
		}else{
			$('.img'+(i+1)+'_second').attr('src','');
			$('.pimg'+(i+1)+'_second').attr('value','');
			img.eq(i).css('display','none');
			// 상품설명지우기
			$('.rep_img'+(i+1)+'_txt').attr('value','');
			$('.rep_img'+(i+1)+'_txt').css('display','none');
		}
	}
}

function openZipSearch() {
	new daum.Postcode({
		oncomplete: function(data) {
			//$('[name=zip]').val(data.zonecode); // 우편번호 (5자리)
			$("#cstAddre").val(data.address);
			//$('[name=addr2]').val(data.buildingName);
		}
	}).open();
}
