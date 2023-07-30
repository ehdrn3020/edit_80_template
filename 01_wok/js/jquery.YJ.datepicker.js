/*
 * '+opt.nameSpace+' v1.1.2 - Custom calendar
 *
 * Copyright 2016, Newriver UI Development Team - Shin Yong Jun
 *
 * Webagency Newriver - http://newriver.co.kr/
 *
 */

;(function($){
	var defaults = {
		nameSpace : 'dp',
		format : 'yyyy-mm-dd',
		weekendDisable : false,
		button : {
			month : true,
			year : true,
			trigger : false,
			today : false
		},
		text : {
			thisMonth : '월',
			thisYear : '년',
			days : ['일', '월', '화', '수', '목', '금', '토'],
			month : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
			btnToday : '오늘로',
			btnPrevMonth : '이전달',
			btnNextMonth : '다음달',
			btnPrevYear : '이전해',
			btnNextYear : '다음해'
		},
		select : false,
		selectYear : {
			start : -100,
			end : 0
		},
		periodFrom : false,
		periodTo : false,
		date : {
			/* ex : [19910301, 1231] */
			disable : [],
			holiday : []
		},
		onChange : function(date){

		}
	}

	$.fn.YJdatepicker = function(options){
		if(!this.length){
			return false;
		}

		if(this.length > 1){
			this.each(function(){
				$(this).YJdatepicker(options);
			});
			return this;
		}

		var _ = this, opt = {}, obj = {}, sbj = {};

		var init = function(){
			setting(); /* 1번만 실행 */
		}

		var setting = function(){
			opt = $.extend({}, defaults, options);

			sbj.nodeType = _[0].tagName === 'DIV' ? 'block' : 'input';
			sbj.weekCount = 0;

			checkFormat();
			getTodayDate();
			setLayout();

			if(sbj.nodeType === 'input'){
				onClickInput();
			}
		}

		var setLayoutMarkup = function(){
			sbj.node = {}
			sbj.typeClass		= sbj.nodeType === 'block' ? opt.nameSpace+'-type-block' : opt.nameSpace+'-type-input';
			sbj.node.outer		= '<div class="'+opt.nameSpace+'-outer '+sbj.typeClass+'" />';
			sbj.node.trigger	= '<button type="button" class="'+opt.nameSpace+'-trigger" title="달력 열기">달력 열기</button>';
			sbj.node.viewer		= '<div class="'+opt.nameSpace+'-viewer" />';
			sbj.node.animate	= '<div class="'+opt.nameSpace+'-animate" />';
		}

		var checkFormat = function(){
			sbj.indexYS = opt.format.indexOf('y');
			sbj.indexYE = opt.format.lastIndexOf('y')+1;
			sbj.indexMS = opt.format.indexOf('m');
			sbj.indexME = opt.format.lastIndexOf('m')+1;
			sbj.indexDS = opt.format.indexOf('d');
			sbj.indexDE = opt.format.lastIndexOf('d')+1;

			sbj.formatY = String(opt.format.substring(sbj.indexYS, sbj.indexYE));
			sbj.formatM = String(opt.format.substring(sbj.indexMS, sbj.indexME));
			sbj.formatD = String(opt.format.substring(sbj.indexDS, sbj.indexDE));
		};

		var getTodayDate = function(){
			sbj.date = new Date();
			sbj.todayY = sbj.date.getFullYear();
			sbj.todayM = sbj.date.getMonth();
			sbj.todayD = sbj.date.getDate();
			sbj.todayDNA = String(sbj.todayY) + computeLength(sbj.todayM + 1) + computeLength(sbj.todayD);
			sbj.dateLeng = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
		}

		var setLayout = function(){
			setLayoutMarkup();

			if(sbj.nodeType === 'block'){
				obj.outer = _.html(sbj.node.outer).children('.'+opt.nameSpace+'-outer');
				
				obj.viewer = obj.outer.append(sbj.node.viewer).children('.'+opt.nameSpace+'-viewer');
				obj.animate = obj.viewer.append(sbj.node.animate).children('.'+opt.nameSpace+'-animate');

				setDatePicker();
			}else{
				obj.outer = _.wrap(sbj.node.outer).parent('.'+opt.nameSpace+'-outer');
				obj.input = _.addClass(opt.nameSpace+'-input');
				sbj.inputDNA = convertDNA(obj.input.val());

				if(opt.button.trigger){
					obj.trigger = obj.outer.append(sbj.node.trigger).children('.'+opt.nameSpace+'-trigger');
				}
				
				obj.viewer = obj.outer.append(sbj.node.viewer).children('.'+opt.nameSpace+'-viewer');
				obj.animate = obj.viewer.append(sbj.node.animate).children('.'+opt.nameSpace+'-animate');
			}
		}

		function computeLength(number){
			var result = String(number).length == 1 ? '0' + String(number) : String(number);

			return result;
		}

		var setData = function(){
			sbj.str = {};
			sbj.thisY = sbj.date.getFullYear();
			sbj.thisM = sbj.date.getMonth();
			sbj.prevM = sbj.thisM == 0 ? 11 : sbj.thisM - 1;
			sbj.str.thisM = computeLength(sbj.thisM + 1);
			sbj.dateLeng[1] = (sbj.thisY % 4 == 0 && sbj.thisY % 100 != 0) || sbj.thisY % 400 == 0 ? 29 : 28;

			sbj.thisDateLeng = sbj.dateLeng[sbj.thisM];
			sbj.titleYM = sbj.thisY + '. ' + sbj.str.thisM;
			sbj.str.thisYM = sbj.thisY + sbj.str.thisM;

			sbj.thisD = sbj.date.getDate();
			sbj.str.thisD = computeLength(sbj.thisD);
			sbj.thisDNA = sbj.str.thisYM + sbj.str.thisD;

			sbj.date.setDate(1);
			sbj.firstDay = sbj.date.getDay();

			if(sbj.nodeType === 'input'){
				sbj.inputDNA = convertDNA(obj.input.val());
			}

			if(opt.periodFrom){
				obj.from = $(opt.periodFrom);
				sbj.fromDNA = convertDNA(obj.from.val());
			}

			if(opt.periodTo){
				obj.to = $(opt.periodTo);
				sbj.toDNA = convertDNA(obj.to.val());
			}
		}

		var setHead = function(type){
			var typeClass = type ? type : '';

			obj.oldInner = obj.animate.children('.'+opt.nameSpace+'-inner');
			obj.inner = obj.animate.append('<div class="'+opt.nameSpace+'-inner '+typeClass+'" />').children('.'+opt.nameSpace+'-inner:last-child')
			obj.head = obj.inner.append('<div class="'+opt.nameSpace+'-head" />').children('.'+opt.nameSpace+'-head');
			obj.body = obj.inner.append('<div class="'+opt.nameSpace+'-body" />').children('.'+opt.nameSpace+'-body');
			obj.title = obj.head.append('<div class="'+opt.nameSpace+'-title" />').children('.'+opt.nameSpace+'-title');

			if(opt.select){
				setSelectYear();
				setSelectMonth();
				onChangeSelect();
			}else{
				obj.title.append('<div class="'+opt.nameSpace+'-title-year">'+sbj.thisY+opt.text.thisYear+'</div>');
				obj.title.append('<div class="'+opt.nameSpace+'-title-month">'+opt.text.month[sbj.thisM]+opt.text.thisMonth+'</div>');
			}

			if(opt.button.month){
				obj.btnPrevMonth = obj.head.append('<button type="button" class="'+opt.nameSpace+'-prev-month" title="'+opt.text.btnPrevMonth+'">'+opt.text.btnPrevMonth+'</button>').children('.'+opt.nameSpace+'-prev-month');
				obj.btnNextMonth = obj.head.append('<button type="button" class="'+opt.nameSpace+'-next-month" title="'+opt.text.btnNextMonth+'">'+opt.text.btnNextMonth+'</button>').children('.'+opt.nameSpace+'-next-month');
			}

			if(opt.button.year){
				obj.btnPrevYear = obj.head.append('<button type="button" class="'+opt.nameSpace+'-prev-year" title="'+opt.text.btnPrevYear+'">'+opt.text.btnPrevYear+'</button>').children('.'+opt.nameSpace+'-prev-year');
				obj.btnNextYear = obj.head.append('<button type="button" class="'+opt.nameSpace+'-next-year" title="'+opt.text.btnNextYear+'">'+opt.text.btnNextYear+'</button>').children('.'+opt.nameSpace+'-next-year');
			}

			if(opt.button.today){
				obj.btnToday = obj.head.append('<button type="button" class="'+opt.nameSpace+'-today" title="'+opt.text.btnToday+'">'+opt.text.btnToday+'</button>').children('.'+opt.nameSpace+'-today');
			}
		}

		var setDatePicker = function(type){
			setData();
			setHead(type);
			setTableHead();
			setTableBody();
			onClickButton();
			viewerAnimate(type);
		}

		var viewerAnimate = function(type){
			obj.viewer.css({'height' : obj.inner.outerHeight()});

			switch(type){
				case 'prev' :
					obj.animate.animate({'left' : '100%'}, 300, function(){
						obj.oldInner.remove();
						obj.animate.css({'left' : 0});
						obj.inner.removeClass('prev');
					});
					break;
				case 'next' :
					obj.animate.animate({'left' : '-100%'}, 300, function(){
						obj.oldInner.remove();
						obj.animate.css({'left' : 0});
						obj.inner.removeClass('next');
					});
					break;
				default :
					break;
			}
		}

		var convertFormat = function(dna){
			var f, y, m, d;

			y = sbj.formatY.length === 2 ? String(dna.substring(2, 4)) : String(dna.substring(0, 4));
			m = String(dna.substring(4, 6));
			d = String(dna.substring(6, 8));
			f = opt.format.replace(sbj.formatY, y).replace(sbj.formatM, m).replace(sbj.formatD, d);

			return f;
		}

		var convertDNA = function(format){
			var result = String(format.substring(sbj.indexYS, sbj.indexYE))+String(format.substring(sbj.indexMS, sbj.indexME))+String(format.substring(sbj.indexDS, sbj.indexDE));

			return result;
		}

		var setSelectYear = function(){
			sbj.selectYear = '<select class="'+opt.nameSpace+'-select-year">';
			sbj.selectYearStart = sbj.todayY + opt.selectYear.start;
			sbj.selectYearEnd = sbj.todayY + opt.selectYear.end;
			for(var i = sbj.selectYearEnd; i >= sbj.selectYearStart; i--){
				sbj.selectYear += i === sbj.thisY ? '<option value="'+i+'" selected>'+i+'</option>' : '<option value="'+i+'">'+i+'</option>';
			}
			sbj.selectYear += '</select>'+opt.text.thisYear;
			obj.selectYear = obj.title.append(sbj.selectYear).children('.'+opt.nameSpace+'-select-year');
			obj.selectYear.option = obj.selectYear.children('option');
		}

		var setSelectMonth = function(){
			sbj.selectMonth = '<select class="'+opt.nameSpace+'-select-month">';
			for(var i = 1; i < 13; i++){
				sbj.selectMonth += i === (sbj.thisM+1) ? '<option value="'+i+'" selected>'+i+'</option>' : '<option value="'+i+'">'+i+'</option>';
			}
			sbj.selectMonth += '</select>'+opt.text.thisMonth;
			obj.selectMonth = obj.title.append(sbj.selectMonth).children('.'+opt.nameSpace+'-select-month');
			obj.selectMonth.option = obj.selectMonth.children('option');
		}

		var getDisabledDate = function(target){
			if(sbj.fromDNA && target.dna < sbj.fromDNA){
				return true;
			}

			if(sbj.toDNA && target.dna > sbj.toDNA){
				return true;
			}

			for(var i = 0; i < opt.date.disable.length; i++){
				if(opt.date.disable[i].length === 4 && target.mad === opt.date.disable[i]){
					return true;
				}
				if(opt.date.disable[i].length === 8 && target.dna === opt.date.disable[i]){
					return true;
				}
			}
		}

		var setDateClass = function(){
			var classSunday = opt.weekendDisable ? 'sunday disabled' : 'sunday';
			var classSatday = opt.weekendDisable ? 'satday disabled' : 'satday';

			obj.date = obj.body.find('td').each(function(i){
				this.day = $(this).index();
				this.dna = $(this).attr('date');
				this.mad = String(this.dna).substring(4, 8);

				switch(this.day){
					case 0 :
						$(this).addClass(classSunday);
						break;
					case 6 :
						$(this).addClass(classSatday);
						break;
					default :
						break;
				}

				if(this.dna){
					if(this.dna === sbj.inputDNA || (sbj.fromDNA && this.dna === sbj.fromDNA) || (sbj.toDNA && this.dna === sbj.toDNA) || (sbj.inputDNA && sbj.fromDNA && this.dna > sbj.fromDNA && this.dna < sbj.inputDNA) || (sbj.inputDNA && sbj.toDNA && this.dna < sbj.toDNA && this.dna > sbj.inputDNA)){
						$(this).addClass('selected');
					}
				}

				if(this.dna === sbj.todayDNA){
					$(this).addClass('today');
				}

				if(getDisabledDate(this)){
					$(this).addClass('disabled');
				}

				if(opt.date.holiday){
					for(var i = 0; i < opt.date.holiday.length; i++){
						if((opt.date.holiday[i].length === 4 && this.mad === opt.date.holiday[i]) || (opt.date.holiday[i].length === 8 && this.dna === opt.date.holiday[i])){
							$(this).addClass('holiday');
						}
					}
				}
			});
		}

		var setTableHead = function(){
			sbj.markup = '<table><thead><tr>';
			for(var i = 0; i < 7; i++){
				sbj.markup += '<th>'+opt.text.days[i]+'</th>';
			}
			sbj.markup += '</tr></thead>';
		}

		var setTableBody = function(){
			var pmFirstDay = sbj.dateLeng[sbj.prevM] - sbj.firstDay;
			sbj.markup += '<tbody><tr>';

			for(var i = 1; i <= sbj.firstDay; i++){
				sbj.markup += '<td class="disabled">' + (pmFirstDay + i) + '</td>';
				sbj.weekCount++;
			}

			for(var i = 1; i <= sbj.thisDateLeng; i++){
				if(sbj.weekCount === 0){
					sbj.markup += '<tr>';
				}
				sbj.markup += '<td date="'+sbj.str.thisYM+computeLength(i)+'" title="'+convertFormat(sbj.str.thisYM+computeLength(i))+'">'+i+'</td>';
				sbj.weekCount++;
				if(sbj.weekCount === 7){
					sbj.markup += '</tr>';
					sbj.weekCount = 0;
				}
			}

			for(var i = 1; sbj.weekCount != 0; i++){
				if(sbj.weekCount === 7){
					sbj.markup += '</tr>';
					sbj.weekCount = 0;
				}else{
					sbj.markup += '<td class="disabled">'+i+'</td>';
					sbj.weekCount++;
				}
			}

			sbj.markup += '</tbody></table>';
			obj.body.html(sbj.markup);
			setDateClass();
			onClickDate();
		}

		var onChangeSelect = function(){
			obj.selectYear.on('change', function(){
				if($(this).val() < sbj.thisY){
					sbj.date.setFullYear($(this).val());
					setDatePicker('prev');
				}
				if($(this).val() > sbj.thisY){
					sbj.date.setFullYear($(this).val());
					setDatePicker('next');
				}
			});

			obj.selectMonth.on('change', function(){
				if($(this).val() - 1 < sbj.thisM){
					sbj.date.setMonth($(this).val() - 1);
					setDatePicker('prev');
				}
				if($(this).val() - 1 > sbj.thisM){
					sbj.date.setMonth($(this).val() - 1);
					setDatePicker('next');
				}
			});
		}

		var onClickInput = function(){
			function openDatepicker(){
				if(!obj.outer.hasClass('open')){
					setDatePicker();
					$('.'+opt.nameSpace+'-outer').removeClass('open');
					obj.outer.addClass('open');
				}
			}

			obj.input.on('click', function(e){
				e.stopPropagation();
				openDatepicker();
			});

			if(opt.button.trigger){
				obj.trigger.on('click', function(e){
					e.stopPropagation();
					openDatepicker();
				});
			}
		}

		var onClickButton = function(){
			if(opt.button.month){
				obj.btnPrevMonth.on('click', function(){
					sbj.date.setMonth(sbj.date.getMonth() - 1);
					if(opt.select && sbj.date.getFullYear() < sbj.selectYearStart){
						sbj.date.setMonth(sbj.date.getMonth() + 1)
						return false;
					}else{
						setDatePicker('prev');
					}
				});
				obj.btnNextMonth.on('click', function(){
					sbj.date.setMonth(sbj.date.getMonth() + 1);
					if(opt.select && sbj.date.getFullYear() > sbj.selectYearEnd){
						sbj.date.setMonth(sbj.date.getMonth() - 1)
						return false;
					}else{
						setDatePicker('next');
					}
				});
			}

			if(opt.button.year){
				obj.btnPrevYear.on('click', function(){
					sbj.date.setFullYear(sbj.date.getFullYear() - 1);
					if(opt.select && sbj.date.getFullYear() < sbj.selectYearStart){
						sbj.date.setFullYear(sbj.date.getFullYear() + 1);
						return false;
					}else{
						setDatePicker('prev');
					}
				});
				obj.btnNextYear.on('click', function(){
					sbj.date.setFullYear(sbj.date.getFullYear() + 1);
					if(opt.select && sbj.date.getFullYear() > sbj.selectYearEnd){
						sbj.date.setFullYear(sbj.date.getFullYear() - 1);
						return false;
					}else{
						setDatePicker('next');
					}
				});
			}

			if(opt.button.today){
				function goTodayMonth(type){
					sbj.date.setFullYear(sbj.todayY);
					sbj.date.setMonth(sbj.todayM);
					setDatePicker(type);
				}

				obj.btnToday.on('click', function(){
					if(sbj.todayY === sbj.thisY && sbj.todayM === sbj.thisM){
						return false;
					}else{
						if(sbj.todayY < sbj.thisY){
							goTodayMonth('prev');
						}else{
							if(sbj.todayY > sbj.thisY){
								goTodayMonth('next');
							}else{
								if(sbj.todayM < sbj.thisM){
									goTodayMonth('prev');
								}else{
									goTodayMonth('next');
								}
							}
						}
					}
				});
			}
		}

		var onClickDate = function(){
			obj.date.on('click', function(){
				if(sbj.nodeType === 'block' || $(this).hasClass('disabled')){
					return false;
				}else{
					obj.input.val(convertFormat(this.dna));
					opt.onChange(this.dna);
					obj.outer.removeClass('open');
				}
			});

			$(document).off('click.YJdatepicker').on('click.YJdatepicker', function(e){
				if(!$(e.target).closest('.'+opt.nameSpace+'-outer').length){
					$('.'+opt.nameSpace+'-outer').removeClass('open');
				}
			});
		}

		init();

		return this;
	}
})(jQuery);