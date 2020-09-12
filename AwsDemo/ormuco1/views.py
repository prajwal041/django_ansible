# Author : Prajwal Shetty

from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt,csrf_protect,ensure_csrf_cookie
from .models import Domain
# Create your views here.

def logout(request):
    return render_to_response('logout.html')

@ensure_csrf_cookie
@csrf_exempt
def ansviews(request, template_name='mypage.html'):
    if request.method == "POST":  # checking POST request
        name = request.POST.get('name', '')  # get the input from front end text box
        favcolor = request.POST.get('favcolor', '')
        pet = request.POST.get('pet', '')
        print(name, favcolor, pet)
        Domain.objects.create(name=name, favcolor=favcolor, pet=pet)
        context = {
            'name': name,
            'favcolor': favcolor,
            'pet': pet
        }
        return render(request, template_name, context)
    else:
        print("GET Type")
        return render(request, template_name)