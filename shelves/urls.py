from django.urls import path
from shelves import views

app_name = 'shelves'

urlpatterns = [
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('media_collection/', views.list_media, name='list_media'),

    path('<str:media_type>/<slug:media_title_slug>/show_media', views.show_media, name='show_media'),

    path('add_media/', views.add_media, name='add_media'),

    path('<str:media_type>/<slug:media_title_slug>/add_details/', views.add_details, name='add_details'),

    path('<str:media_type>/<slug:media_title_slug>/add_post/', views.add_post, name='add_post'),

    path('register_profile/', views.register_profile, name='register_profile'),

    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),

    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),

    path('delete/<username>', views.delete_account, name='delete_account'),

    path('<username>/send_friend_request/', views.send_friend_request, name='send_friend_request'),

    path('<username>/accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),

]
