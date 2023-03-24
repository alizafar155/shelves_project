from django.urls import path
from shelves import views

app_name = 'shelves'

urlpatterns = [
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),

    path('contact_us/', views.contact_us, name='contact_us'),

    path('register_profile/', views.register_profile, name='register_profile'),

    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),

    path('delete/<username>', views.delete_account, name='delete_account'),

    path('add_media/', views.add_media, name='add_media'),

    path('media_collection/', views.list_medias, name='media_collection'),

    path('media/<str:media_type>/<slug:media_title_slug>/', views.show_media, name='show_media'),

    path('<slug:media_title_slug>/add_type_details/', views.add_type_details, name='add_type_details'),

    path('<slug:media_title_slug>/add_post/', views.add_post, name='add_post'),


]