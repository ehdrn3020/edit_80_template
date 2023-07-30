from django.shortcuts import render

def index(request):
    return render(request, 'gallerys/index.html')

def show(request):
    return render(request, 'gallerys/show.html')

def create(request):
    return render(request, 'gallerys/create.html')

def edit(request):
    return render(request, 'gallerys/create.html')

def delete(request):
    return render(request, 'gallerys/index.html')
