from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path("<int:id>", views.index, name = "index"),
    path("", views.home, name = "home1"),
    path("create/", views.create, name = "create"),
    path("home/", views.home, name="home"),
    path("view/", views.view, name="view"),
    re_path(r'^webpush/', include('webpush.urls')),

]
