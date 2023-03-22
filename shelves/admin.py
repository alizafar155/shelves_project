from django.contrib import admin
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile

admin.site.register(Media)
admin.site.register(Book)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Song)
admin.site.register(Post)
admin.site.register(UserProfile)
