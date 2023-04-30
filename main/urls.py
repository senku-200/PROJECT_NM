from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.register,name="register"),
    path('signup_edit',views.signup_edit,name="signup_edit"),
    path('login',views.loginform,name="login"),
    path('logout',views.logout_form,name="logout"),
    path('opencv',views.stone_paper_scissor,name="opencv"),
    path('project/<str:pk>/',views.project,name="project"),
    path('object_detector',views.object_detecter,name="object_detector"),
    path('profile',views.profile,name="profile"),
]