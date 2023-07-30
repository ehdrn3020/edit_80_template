from django.shortcuts import render

def index(request):
    return render(request, 'asks/index.html')

def show(request):
    return render(request, 'asks/show.html')

def create(request):
    return render(request, 'asks/create.html')

def edit(request):
    return render(request, 'asks/create.html')

def delete(request):
    return render(request, 'asks/index.html')
