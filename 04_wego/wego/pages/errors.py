from django.shortcuts import render, render_to_response
from django.template import RequestContext

def error400(request, exception):
    return render(request, 'errors/400.html', status = 400)

def error404(request, exception):
    return render(request, 'errors/404.html', status = 404)

def error500(request):
    return render(request, 'errors/500.html', status = 500)
