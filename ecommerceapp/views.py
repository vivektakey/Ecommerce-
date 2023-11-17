from django.shortcuts import render
from .models import Contact,Product
from django.contrib import messages
from math import ceil

# Create your views here.

def index(request):
    allproducts = []
    catproducts =Product.objects.values('category','id')
    cats = {item['category'] for item in catproducts}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4)-(n // 4)) 
        allproducts.append([prod, range(1, nSlides), nSlides])
    params = {'allproducts':allproducts}
    return render(request,'index.html',params)

def contact(request):
    if request.method == "POST":
        try:
            name = request.POST['name']
            email = request.POST["email"]
            phone = request.POST["phone"]
            desc = request.POST["desc"]
            data =Contact(name=name,email=email,phone=phone,desc=desc)
            data.save()
            messages.success(request,"Request submitted")
            return render(request,'contact.html')
        except Exception as identifier:
            pass
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def shop(request):
    return render(request,'shop.html')
