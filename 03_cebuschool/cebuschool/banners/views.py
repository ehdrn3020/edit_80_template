from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import simplejson as json
from .models import Banner

def index(request):
    banner_id = request.POST['banner_id']
    banner = get_object_or_404(Banner, pk=banner_id)

    #클릭시 숫자증가
    banner.click_number += 1
    banner.save()
    
    # Ajax성공시 링크 Url을 반환
    context = {
        'url': banner.link_url
    }

    return HttpResponse(json.dumps(context), content_type="application/json")