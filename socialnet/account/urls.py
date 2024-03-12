from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('register/',views.RegisterUser.as_view(),name='register_user'),
    path('login/',views.LoginUserForm.as_view(),name='login_user')

]