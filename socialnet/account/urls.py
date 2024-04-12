from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("register/", views.RegisterUser.as_view(), name="register_user"),
    path("login/", views.LoginUserForm.as_view(), name="login_user"),
    path("logout/", views.UserLogoutForm.as_view(), name="logout_user"),
    path(
        "profile/<int:user_id>/", views.UserProfileView.as_view(), name="profile_user"
    ),
    path("reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/done/",
        views.UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "confirm/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "confirm/complete/",
        views.UserPasswordResetCompeleteView.as_view(),
        name="password_reset_compelete",
    ),
    path('follow/<int:user_id>',views.UserFollowView.as_view(),name='user_follow'),
    path('unfollow/<int:user_id>',views.UserUnFollowView.as_view(),name='user_unfollow'),
    path('edit_user/',views.UserEditView.as_view(),name='edit_user')


]
