from django import template
from shelves.models import Book, Movie, Show, Song

register = template.Library()

@register.inclusion_tag('rango/medias.html')
def get_book_list(current_book=None):
    return {'books': Book.objects.all(),
            'current_book': current_book}

@register.inclusion_tag('rango/medias.html')
def get_movie_list(current_movie=None):
    return {'movies': Movie.objects.all(),
            'current_movie': current_movie}

@register.inclusion_tag('rango/medias.html')
def get_show_list(current_show=None):
    return {'shows': Show.objects.all(),
            'current_show': current_show}

@register.inclusion_tag('rango/medias.html')
def get_song_list(current_song=None):
    return {'songs': Song.objects.all(),
            'current_song': current_song}
