"""society URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from pages.views import home_view , password_reset_view , log_out , validate_otp , new_password , print_view
from members.views import onemember_record
from adminapp.views import adminmainpage_view , remove_form_view , confirmform_view , loan_form_view , paid_form_view , join_form_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view ),
    path('logout' , log_out),
    path('adminmainpage/', adminmainpage_view ),
    path('membersrecord/<str:name>' , onemember_record),
    path("remove" , remove_form_view),
    path("confirmform/<str:name>" , confirmform_view),
    path("loanform" , loan_form_view),
    path("paidform" , paid_form_view),
    path("joinform" , join_form_view),
    path("resetpassword" , password_reset_view),
    path("otpvalidation" , validate_otp),
    path("changepassword" , new_password),
    path("printlayout" , print_view)
]
