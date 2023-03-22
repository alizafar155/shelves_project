from django.urls import path
from shelves import views

app_name = 'shelves'

urlpatterns = [
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),

    path('contact_us/', views.contact_us, name='contact_us'),

    path('medias/', views.list_medias, name='medias'),

    path('<slug:media_title_slug>/', views.show_media, name='show_media'),

]