from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'tools/index.html')

def traits(request):
    return render(request, 'tools/traits.html')

def augments(request):
    return render(request, 'tools/augments.html')

def items(request):
    return render(request, 'tools/items.html')

def champions(request):
    return render(request, 'tools/champions.html')