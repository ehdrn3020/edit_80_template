from django.shortcuts import render
import simplejson as json

#Main Page
def index(request):
    return render(request, 'mypages/index.html')

#User Info Tab
def userinfo(request, name):
    print(name)

    if name == 'index':
        return render(request, 'mypages/userinfo.html')
    elif name == 'profile':
        return render(request, 'mypages/userinfo_profile.html')
    elif name == 'rank':
        return render(request, 'mypages/userinfo_rank.html')
    elif name == 'phone':
        return render(request, 'mypages/userinfo_phone.html')
    elif name == 'edit':
        return render(request, 'mypages/userinfo_edit_info.html')
    elif name == 'pwd':
        return render(request, 'mypages/userinfo_edit_pwd.html')

#Activate Tab
def active(request, name):
    print(name)

    if name == 'index':
        return render(request, 'mypages/active.html')
    elif name == 'board':
        context = { 
            'title': '게시글'
        }
        return render(request, 'mypages/active_board.html', context)
    elif name == 'comment':
        context = { 
            'title': '댓글'
        }
        return render(request, 'mypages/active_board.html', context)
    elif name == 'scrap':
        context = { 
            'title': '스크랩'
        }
        return render(request, 'mypages/active_board.html', context)
    elif name == 'event':
        return render(request, 'mypages/active_event.html')