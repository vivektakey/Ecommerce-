from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.handlelogin,name="handleloginlogin"),
    path('logout/',views.handlelogout,name="handlelogout"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name="activate"),

]
