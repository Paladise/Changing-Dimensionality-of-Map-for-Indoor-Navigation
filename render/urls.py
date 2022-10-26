from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<id>/copy', views.copy_images, name='copy'),
    path('<id>/create', views.create_bash_script, name='create'),
    path('<id>/process', views.process_images, name='process'),
    path('<id>/check', views.check_if_finished, name='check'),
    path('<id>/', views.model, name='model')
]

app_name = "render"