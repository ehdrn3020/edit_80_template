from django.shortcuts import render

def index(request):
    return render(request, 'afters/index.html')

def show(request):
    return render(request, 'afters/show.html')

def create(request):
    return render(request, 'afters/create.html')

def edit(request):
    return render(request, 'afters/create.html')

def delete(request):
    return render(request, 'afters/index.html')