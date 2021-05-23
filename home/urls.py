from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.signup, name="signup"),
    path('login', views.Login, name="Login"),
    path('logout', views.Logout_view, name="Logout_view"),
    path('Buy', views.Purchase_course, name="Purchase_course"),
    path('success', views.Success, name='success'),
    path('enrolledcourse', views.Student_profile, name="student_profile"),
    path('forgot_mobile', views.Forgot_mobile, name='forgot_mobile'),
    path('forgot_password', views.Forgot_password, name='forgot_password'),


]
