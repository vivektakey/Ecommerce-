from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def signup(request):
    # print("success")
    if request.method == "POST":
       email = request.POST['email']
       password = request.POST['password']
       password2 = request.POST['password2']
       if password != password2:
            messages.warning(request,"password dosn't match")
            return render(request,'signup.html')
       try:
           if User.objects.get(username=email):
                messages.warning(request,"Email already exists")
                return render(request,'signup.html')
       except Exception as identifier:
           pass
       user = User.objects.create_user(email,email,password)
       user.is_active=False
       user.save()
       email_subject="Activate your account"
       message=render_to_string('activate.html',{
           'user':user,
           'domain':'http://127.0.0.1:8000',
           'uid':urlsafe_base64_encode(force_bytes(user.pk)),
           'token':generate_token.make_token(user)
       })
       email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
       messages.success(request,"Please activate your account by clicking the link in your gmail!")
       email_message.send()
    #    return redirect('/auth/login')
    return render(request,'signup.html')


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account activated successfully!")
            return redirect('/auth/login')
        return render(request,'activatefail.html')


def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        userpassword = request.POST['password']
        myuser = authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            # messages.success(request,"login successful!")
            return redirect('/')
        else:
            messages.error(request,"Invalid credetials!")
            return redirect('/auth/login')

    return render(request,'login.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"logout successful!")
    return redirect('/auth/login')

    