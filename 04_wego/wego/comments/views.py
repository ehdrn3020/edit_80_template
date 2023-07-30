from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import simplejson as json
from .models import Comment_After, Comment_Ask, Comment_Info, Comment_Community, Comment_Course, Comment_Gallery, Comment_Promotion, Comment_Notice, Comment_CustomerCenter
from afters.models import After
from asks.models import Ask
from infos.models import Info
from communitys.models import Community
from courses.models import Course
from pages.models import Point, Exprience
from gallerys.models import Gallery
from promotions.models import Promotion
from centers.models import Notice, CustomerCenter
from msgboxs.models import Alarm_Addcommentlike
from decimal import Decimal

# 후기 댓글 작성
def create_after(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    after = get_object_or_404(After, pk=content_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_after = Comment_After.objects.create(
        user=request.user, comment_table=after, content = comment_content
    )
    c_after.save()

    # 후기댓글증가
    after.comments += 1
    after.save()

    # 댓글쓴 사람에게 포인트,경험치
    p = Point.objects.filter(title='후기댓글').values('point').first()
    e = Exprience.objects.filter(title='후기댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'comment', likefrom=request.user, comment_user=after.user, comment_id=c_after.id, comment_table = '후기댓글',
        board_name='후기', board_url='afters/show/'+str(content_id)+'/'+str(c_after.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('afters:show', content_id, c_after.id)

# 후기 대댓글 작성
def create_after_re(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    after = get_object_or_404(After, pk=content_id)
    parent_comment = get_object_or_404(Comment_After, pk=comment_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_after = Comment_After.objects.create(
        user=request.user, comment_table=after, content = comment_content, parent_id=parent_comment
    )
    c_after.save()

    # 후기댓글증가
    after.comments += 1
    after.save()

    # 댓글쓴 사람에게 포인트
    p = Point.objects.filter(title='후기댓글').values('point').first()
    e = Exprience.objects.filter(title='후기댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 're_comment', likefrom=request.user, comment_user=parent_comment.user, comment_id=c_after.id, comment_table = '후기댓글',
        board_name='후기', board_url='afters/show/'+str(content_id)+'/'+str(c_after.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('afters:show', content_id, c_after.id)

# 후기 댓글 삭제
def delete_after(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    # 댓글삭제
    comment = get_object_or_404(Comment_After, pk=comment_id)
    chk_parent_id = Comment_After.objects.filter(parent_id=comment_id).count()
    # 댓글에 대댓글이 있으면 내용만바꾸기
    if chk_parent_id > 0:
        comment.content = '[이미 삭제된 댓글입니다.]'
        comment.save()
    else:
        comment.is_published = False
        comment.save()

    # 후기 댓글수 -1
    after = get_object_or_404(After, pk=content_id)
    after.comments -= 1
    after.save()

    return redirect('afters:show', content_id)

# 질문답변 댓글 작성
def create_ask(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    ask = get_object_or_404(Ask, pk=content_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_ask = Comment_Ask.objects.create(
        user=request.user, comment_table=ask, content = comment_content
    )
    c_ask.save()

    # 질답댓글증가
    ask.comments += 1
    ask.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='질답댓글').values('point').first()
    e = Exprience.objects.filter(title='질답댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'comment', likefrom=request.user, comment_user=ask.user, comment_id=c_ask.id, comment_table ='질답댓글',
        board_name='질문답변', board_url='asks/show/'+str(content_id)+'/'+str(c_ask.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('asks:show', content_id, c_ask.id)

# 질문답변 대댓글 작성
def create_ask_re(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    ask = get_object_or_404(Ask, pk=content_id)
    parent_comment = get_object_or_404(Comment_Ask, pk=comment_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_ask = Comment_Ask.objects.create(
        user=request.user, comment_table=ask, content = comment_content, parent_id=parent_comment
    )
    c_ask.save()

    # 질답댓글증가
    ask.comments += 1
    ask.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='질답댓글').values('point').first()
    e = Exprience.objects.filter(title='질답댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 're_comment', likefrom=request.user, comment_user=parent_comment.user, comment_id=c_ask.id, comment_table ='질답댓글',
        board_name='질문답변', board_url='asks/show/'+str(content_id)+'/'+str(c_ask.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('asks:show', content_id, c_ask.id)

# 질문답변 댓글 삭제
def delete_ask(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    # 댓글삭제
    comment = get_object_or_404(Comment_Ask, pk=comment_id)
    chk_parent_id = Comment_Ask.objects.filter(parent_id=comment_id).count()
    # 댓글에 대댓글이 있으면 내용만바꾸기
    if chk_parent_id > 0:
        comment.content = '[이미 삭제된 댓글입니다.]'
        comment.save()
    else:
        comment.is_published = False
        comment.save()

    # 질답 댓글수 -1
    ask = get_object_or_404(Ask, pk=content_id)
    ask.comments -= 1
    ask.save()

    return redirect('asks:show', content_id)

# 정보공유 댓글 작성
def create_info(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    info = get_object_or_404(Info, pk=content_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_info = Comment_Info.objects.create(
        user=request.user, comment_table=info, content = comment_content
    )
    c_info.save()

    # 정보공유댓글증가
    info.comments += 1
    info.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='정보공유댓글').values('point').first()
    e = Exprience.objects.filter(title='정보공유댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'comment', likefrom=request.user, comment_user=info.user, comment_id=c_info.id, comment_table='정보공유댓글',
        board_name='정보공유', board_url='inofs/show/'+str(content_id)+'/'+str(c_info.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('infos:show', content_id, c_info.id)

# 정보공유 대댓글 작성
def create_info_re(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    info = get_object_or_404(Info, pk=content_id)
    parent_comment = get_object_or_404(Comment_Info, pk=comment_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_info = Comment_Info.objects.create(
        user=request.user, comment_table=info, content = comment_content, parent_id=parent_comment
    )
    c_info.save()

    # 정보공유댓글증가
    info.comments += 1
    info.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='정보공유댓글').values('point').first()
    e = Exprience.objects.filter(title='정보공유댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 're_comment', likefrom=request.user, comment_user=parent_comment.user, comment_id=c_info.id, comment_table='정보공유댓글',
        board_name='정보공유', board_url='inofs/show/'+str(content_id)+'/'+str(c_info.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('infos:show', content_id, c_info.id)

# 정보공유 댓글 삭제
def delete_info(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    # 댓글삭제
    comment = get_object_or_404(Comment_Info, pk=comment_id)
    chk_parent_id = Comment_Info.objects.filter(parent_id=comment_id).count()
    # 댓글에 대댓글이 있으면 내용만바꾸기
    if chk_parent_id > 0:
        comment.content = '[이미 삭제된 댓글입니다.]'
        comment.save()
    else:
        comment.is_published = False
        comment.save()

    # 후기 댓글수 -1
    info = get_object_or_404(Info, pk=content_id)
    info.comments -= 1
    info.save()

    return redirect('infos:show', content_id)

# 커뮤니티 댓글 작성
def create_community(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    community = get_object_or_404(Community, pk=content_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_community = Comment_Community.objects.create(
        user=request.user, comment_table=community, content = comment_content
    )
    c_community.save()

    # 후기댓글증가
    community.comments += 1
    community.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='커뮤니티댓글').values('point').first()
    e = Exprience.objects.filter(title='커뮤니티댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'comment', likefrom=request.user, comment_user=community.user, comment_id=c_community.id, comment_table='커뮤니티댓글',
        board_name='커뮤니티', board_url='communitys/show/'+str(content_id)+'/'+str(c_community.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('communitys:show', content_id, c_community.id)

# 커뮤니티 대댓글 작성
def create_community_re(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    community = get_object_or_404(Community, pk=content_id)
    parent_comment = get_object_or_404(Comment_Community, pk=comment_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_community = Comment_Community.objects.create(
        user=request.user, comment_table=community, content = comment_content, parent_id=parent_comment
    )
    c_community.save()

    # 커뮤니티댓글증가
    community.comments += 1
    community.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='커뮤니티댓글').values('point').first()
    e = Exprience.objects.filter(title='커뮤니티댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 're_comment', likefrom=request.user, comment_user=parent_comment.user, comment_id=c_community.id, comment_table='커뮤니티댓글',
        board_name='커뮤니티', board_url='communitys/show/'+str(content_id)+'/'+str(c_community.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('communitys:show', content_id, c_community.id)

# 커뮤니티 댓글 삭제
def delete_community(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    # 댓글삭제
    comment = get_object_or_404(Comment_Community, pk=comment_id)
    chk_parent_id = Comment_Community.objects.filter(parent_id=comment_id).count()
    # 댓글에 대댓글이 있으면 내용만바꾸기
    if chk_parent_id > 0:
        comment.content = '[이미 삭제된 댓글입니다.]'
        comment.save()
    else:
        comment.is_published = False
        comment.save()

    # 커뮤니티 댓글수 -1
    community = get_object_or_404(Community, pk=content_id)
    community.comments -= 1
    community.save()

    return redirect('communitys:show', content_id)

# 여행코스 댓글 작성
def create_course(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    course = get_object_or_404(Course, pk=content_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_course = Comment_Course.objects.create(
        user=request.user, comment_table=course, content = comment_content
    )
    c_course.save()

    # 여행코스댓글증가
    course.comments += 1
    course.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='여행코스댓글').values('point').first()
    e = Exprience.objects.filter(title='여행코스댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'comment', likefrom=request.user, comment_user=course.user, comment_id=c_course.id, comment_table='여행코스댓글',
        board_name='여행코스', board_url='courses/show/'+str(content_id)+'/'+str(c_course.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('courses:show', content_id, c_course.id)

# 여행코스 대댓글 작성
def create_course_re(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    course = get_object_or_404(Course, pk=content_id)
    parent_comment = get_object_or_404(Comment_Course, pk=comment_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_course = Comment_Course.objects.create(
        user=request.user, comment_table=course, content = comment_content, parent_id=parent_comment
    )
    c_course.save()

    # 여행코스댓글증가
    course.comments += 1
    course.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='여행코스댓글').values('point').first()
    e = Exprience.objects.filter(title='여행코스댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 're_comment', likefrom=request.user, comment_user=parent_comment.user, comment_id=c_course.id, comment_table='여행코스댓글',
        board_name='여행코스', board_url='courses/show/'+str(content_id)+'/'+str(c_course.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('courses:show', content_id, c_course.id)

# 여행코스 댓글 삭제
def delete_course(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    # 댓글삭제
    comment = get_object_or_404(Comment_Course, pk=comment_id)
    chk_parent_id = Comment_Course.objects.filter(parent_id=comment_id).count()

    # 댓글에 대댓글이 있으면 내용만바꾸기
    if chk_parent_id > 0:
        comment.content = '[이미 삭제된 댓글입니다.]'
        comment.save()
    else:
        comment.is_published = False
        comment.save()

    # 여행코스 댓글수 -1
    course = get_object_or_404(Course, pk=content_id)
    course.comments -= 1
    course.save()

    return redirect('courses:show', content_id)

# 실시간세부 댓글 작성
def create_gallery(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    gallery = get_object_or_404(Gallery, pk=content_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_gallery = Comment_Gallery.objects.create(
        user=request.user, comment_table=gallery, content = comment_content
    )
    c_gallery.save()

    # 실시간세부댓글증가
    gallery.comments += 1
    gallery.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='실시간세부댓글').values('point').first()
    e = Exprience.objects.filter(title='실시간세부댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'comment', likefrom=request.user, comment_user=gallery.user, comment_id=c_gallery.id, comment_table='실시간세부댓글',
        board_name='실시간세부', board_url='gallerys/show/'+str(content_id)+'/'+str(c_gallery.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('gallerys:show', content_id, c_gallery.id)

# 실시간세부 댓글 삭제
def delete_gallery(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    # 댓글삭제
    comment = get_object_or_404(Comment_Gallery, pk=comment_id)
    comment.is_published = False
    comment.save()

    # 실시간세부 댓글수 -1
    gallery = get_object_or_404(Gallery, pk=content_id)
    gallery.comments -= 1
    gallery.save()

    return redirect('gallerys:show', content_id)

# 여행사홍보 댓글 작성
def create_promotion(request):
    print(request.POST)
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    star_total = request.POST['star_total']
    star_response = request.POST['star_response']
    star_price = request.POST['star_price']
    star_clean = request.POST['star_clean']
    star_service = request.POST['star_service']
    star_kindness = request.POST['star_kindness']
    star_quality = request.POST['star_quality']
    star_location = request.POST['star_location']
    promotion = get_object_or_404(Promotion, pk=content_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_promotion = Comment_Promotion.objects.create(
        user=request.user, comment_table=promotion, content = comment_content,
        star_total=star_total, star_response=star_response, star_price=star_price,
        star_clean=star_clean, star_service=star_service, star_kindness=star_kindness,
        star_quality=star_quality, star_location=star_location
    )
    c_promotion.save()

    # 별점 평균계산
    num = promotion.star_participate
    promotion.star_participate = num + 1
    promotion.star_total = round((((promotion.star_total*num) + Decimal(star_total)) / (num+1)),2)
    promotion.star_response = round((((promotion.star_response*num) + Decimal(star_response)) / (num+1)),2)
    promotion.star_price = round((((promotion.star_price*num) + Decimal(star_price)) / (num+1)),2)
    promotion.star_clean = round((((promotion.star_clean*num) + Decimal(star_clean)) / (num+1)),2)
    promotion.star_service = round((((promotion.star_service*num) + Decimal(star_service)) / (num+1)),2)
    promotion.star_kindness = round((((promotion.star_kindness*num) + Decimal(star_kindness)) / (num+1)),2)
    promotion.star_quality = round((((promotion.star_quality*num) + Decimal(star_quality)) / (num+1)),2)
    promotion.star_location = round((((promotion.star_location*num) + Decimal(star_location)) / (num+1)),2)
    promotion.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='여행사홍보댓글').values('point').first()
    e = Exprience.objects.filter(title='여행사홍보댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'comment', likefrom=request.user, comment_user=promotion.user, comment_id=c_promotion.id, comment_table='여행사홍보댓글',
        board_name='여행사홍보', board_url='promotions/show/'+str(content_id)+'/'+str(c_promotion.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('promotions:show', content_id, c_promotion.id)

# 여행사홍보 대댓글 작성
def create_promotion_re(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    promotion = get_object_or_404(Promotion, pk=content_id)
    parent_comment = get_object_or_404(Comment_Promotion, pk=comment_id)

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 댓글저장
    c_promotion = Comment_Promotion.objects.create(
        user=request.user, comment_table=promotion, content = comment_content, parent_id=parent_comment
    )
    c_promotion.save()

    # 여행사홍보댓글증가
    promotion.comments += 1
    promotion.save()

    # 댓글쓴 사람에게 포인트, 경험치
    p = Point.objects.filter(title='여행사홍보댓글').values('point').first()
    e = Exprience.objects.filter(title='여행사홍보댓글').values('exprience').first()
    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 're_comment', likefrom=request.user, comment_user=parent_comment.user, comment_id=c_promotion.id, comment_table='여행사홍보댓글',
        board_name='여행사홍보', board_url='promotions/show/'+str(content_id)+'/'+str(c_promotion.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('promotions:show', content_id, c_promotion.id)

# 여행사홍보 댓글 삭제
def delete_promotion(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    # 댓글삭제
    comment = get_object_or_404(Comment_Promotion, pk=comment_id)
    comment.is_published = False
    comment.save()

    # 여행사홍보 댓글수 -1
    promotion = get_object_or_404(Promotion, pk=content_id)
    promotion.star_participate -= 1
    promotion.save()

    return redirect('promotions:show', content_id)

# 위고센터 댓글 작성
def create_center(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    kind = request.POST['kind']

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 글, 댓글, 포인트, 경험치
    obj = ''
    c_obj = ''
    p = ''
    e = ''
    # 공지사항일때
    if kind == 'notice':
        # 공지사항댓글증가
        obj = get_object_or_404(Notice, pk=content_id)
        obj.comments += 1
        obj.save()
        #댓글저장
        c_obj = Comment_Notice.objects.create(
            user=request.user, comment_table=obj, content = comment_content
        )
        obj.save()
        # 댓글쓴 사람에게 포인트, 경험치
        p = Point.objects.filter(title='공지사항댓글').values('point').first()
        e = Exprience.objects.filter(title='공지사항댓글').values('exprience').first()

    # 고객센터일때
    elif kind == 'customerCenter':
        # 고객센터댓글증가
        obj = get_object_or_404(CustomerCenter, pk=content_id)
        obj.comments += 1
        obj.save()
        #댓글저장
        c_obj = Comment_CustomerCenter.objects.create(
            user=request.user, comment_table=obj, content = comment_content
        )
        obj.save()
        # 댓글쓴 사람에게 포인트, 경험치
        p = Point.objects.filter(title='고객센터댓글').values('point').first()
        e = Exprience.objects.filter(title='고객센터댓글').values('exprience').first()

    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    comment_table = ''
    board_name = ''
    if kind == 'notice':
        comment_table = '공지사항댓글'
        board_name = '공지사항'
    elif kind == 'customerCenter':
        comment_table = '고객센터댓글'
        board_name = '고객센터'
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'comment', likefrom=request.user, comment_user=obj.user, comment_id=c_obj.id, comment_table=comment_table,
        board_name=board_name, board_url='centers/show/'+kind+'/'+str(content_id)+'/'+str(c_obj.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('centers:show', kind, content_id, c_obj.id)

# 위고센터 대댓글 작성
def create_center_re(request):
    comment_content = request.POST['comment_content']
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']
    kind = request.POST['kind']

    # 유효성
    val_message = validation(comment_content)
    if val_message != '유효성검사성공':
        messages.error(request, val_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # 글, 댓글, 부모댓글, 포인트, 경험치
    obj = ''
    c_obj = ''
    parent_comment = ''
    p = ''
    e = ''
    # 공지사항일때
    if kind == 'notice':
        # 공지사항댓글증가
        obj = get_object_or_404(Notice, pk=content_id)
        obj.comments += 1
        obj.save()
        #댓글저장
        parent_comment = get_object_or_404(Comment_Notice, pk=comment_id)
        c_obj = Comment_Notice.objects.create(
            user=request.user, comment_table=obj, content = comment_content, parent_id=parent_comment
        )
        obj.save()
        # 댓글쓴 사람에게 포인트, 경험치
        p = Point.objects.filter(title='공지사항댓글').values('point').first()
        e = Exprience.objects.filter(title='공지사항댓글').values('exprience').first()

    # 고객센터일때
    elif kind == 'customerCenter':
        # 고객센터댓글증가
        obj = get_object_or_404(CustomerCenter, pk=content_id)
        obj.comments += 1
        obj.save()
        #댓글저장
        parent_comment = get_object_or_404(Comment_CustomerCenter, pk=comment_id)
        c_obj = Comment_CustomerCenter.objects.create(
            user=request.user, comment_table=obj, content = comment_content, parent_id=parent_comment
        )
        obj.save()
        # 댓글쓴 사람에게 포인트, 경험치
        p = Point.objects.filter(title='고객센터댓글').values('point').first()
        e = Exprience.objects.filter(title='고객센터댓글').values('exprience').first()

    request.user.point += p['point']
    request.user.exprience += e['exprience']
    request.user.save()

    # 댓글알람생성
    comment_table = ''
    board_name = ''
    if kind == 'notice':
        comment_table = '공지사항댓글'
        board_name = '공지사항'
    elif kind == 'customerCenter':
        comment_table = '고객센터댓글'
        board_name = '고객센터'
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 're_comment', likefrom=request.user, comment_user=parent_comment.user, comment_id=c_obj.id, comment_table=comment_table,
        board_name=board_name, board_url='centers/show/'+kind+'/'+str(content_id)+'/'+str(c_obj.id), content_id = content_id
    )
    c_alarm.save()

    return redirect('centers:show', kind, content_id, c_obj.id)

# 공지사항 댓글 삭제
def delete_center(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']
    kind = request.POST['kind']

    # 댓글삭제
    if kind == 'notice' :
        comment = get_object_or_404(Comment_Notice, pk=comment_id)
        chk_parent_id = Comment_Notice.objects.filter(parent_id=comment_id).count()
        # 댓글에 대댓글이 있으면 내용만바꾸기
        if chk_parent_id > 0:
            comment.content = '[이미 삭제된 댓글입니다.]'
            comment.save()
        else:
            comment.is_published = False
            comment.save()
        #글오브젝트 댓글수 -1
        obj = get_object_or_404(Notice, pk=content_id)
        obj.comments -= 1
        obj.save()
    elif kind == 'customerCenter':
        comment = get_object_or_404(Comment_CustomerCenter, pk=comment_id)
        chk_parent_id = Comment_CustomerCenter.objects.filter(parent_id=comment_id).count()
        # 댓글에 대댓글이 있으면 내용만바꾸기
        if chk_parent_id > 0:
            comment.content = '[이미 삭제된 댓글입니다.]'
            comment.save()
        else:
            comment.is_published = False
            comment.save()
        #글오브젝트 댓글수 -1
        obj = get_object_or_404(CustomerCenter, pk=content_id)
        obj.comments -= 1
        obj.save()

    return redirect('centers:show', kind, content_id)

# 글자수 유효성검사
def validation(text):
    if len(text) > 20000:
        return '글자 수는 1,000자 내로 작성해주세요!'
    else:
        return '유효성검사성공'
