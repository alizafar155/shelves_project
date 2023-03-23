from django.urls import path
from shelves import views

app_name = 'shelves'

urlpatterns = [
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),

    path('contact_us/', views.contact_us, name='contact_us'),

    path('add_media/', views.add_media, name='add_media'),

    path('medias/', views.list_medias, name='medias'),

    path('<slug:media_title_slug>/', views.show_media, name='show_media'),

    path('<slug:media_title_slug>/add_book_details/', views.add_book_details, name='add_book_details'),

    path('<slug:media_title_slug>/add_movie_details/', views.add_movie_details, name='add_movie_details'),

    path('<slug:media_title_slug>/add_show_details/', views.add_show_details, name='add_show_details'),

    path('<slug:media_title_slug>/add_song_details/', views.add_song_details, name='add_song_details'),

]