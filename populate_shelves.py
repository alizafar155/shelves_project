import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                    'shelves_project.settings')

import django
django.setup()
import datetime
from shelves.models import Media, Book, Movie, Show, Song, Post
from django.contrib.auth.models import User

def populate():
    testUser = User.objects.create(username='testUser', email='', password='testPassword')
    testUser.save()

    testBook = {'isbn': 9784809238130}  
    testBookPost = [
                {'title': 'Really enjoyed this book',
                'rating': 10,
                'comment': 'The story was very interesting. I loved reading it.',
                'publishDate': datetime.date(2021, 5, 5),
                'likes': 43, },
                ]

    testMovie = {'duration': datetime.timedelta(hours = 3, minutes = 45)}
    testMoviePost = [
                {'title': 'The movie was too long',
                'rating': 3,
                'comment': 'Nice visuals but it was too long and boring.',
                'publishDate': datetime.date(2021, 6, 5),
                'likes': 120, },
                ]
    
    testShow = {'episodes': 30,
               'seasons': 1,}
    testShowPost = [
                {'title': 'Medicore.',
                'rating': 5,
                'comment': '',
                'publishDate': datetime.date(2021, 7, 5),
                'likes': 4, },
                ]
    
    testSong = {'duration': datetime.timedelta(hours = 3, minutes = 45)}
    testSongPost = [
                {'title': 'I listen to this everyday',
                'rating': 9,
                'comment': 'Great to listen to when I am working or studying!',
                'publishDate': datetime.date(2021, 7, 5),
                'likes': 55, },
                ]


    medias = {'Harry Potter': 
             {'type': 'book',
              'concreteMedia': testBook,
              'posts': testBookPost, 
              'coverImage': None, 
              'writer': 'J.K. Rowling', 
              'language': 'English',
              'releaseDate': datetime.date(2015, 7, 5)},
             
             'Fast and Furious':
             {'type': 'movie',
              'concreteMedia': testMovie,
              'posts': testMoviePost, 
              'coverImage': None, 
              'writer': 'Steven Spielberg', 
              'language': 'English',
              'releaseDate': datetime.date(1985, 7, 5)},
             
             'SpongeBob SquarePants': 
             {'type': 'show',
              'concreteMedia': testShow,
              'posts': testShowPost, 
              'coverImage': None, 
              'writer': 'Dan Schneider', 
              'language': 'English',
              'releaseDate': datetime.date(2002, 7, 5)},
             
             
             'Whats My Name?': 
             {'type': 'song',
              'concreteMedia': testSong,
              'posts': testSongPost, 
              'coverImage': None, 
              'writer': 'Rihanna', 
              'language': 'English',
              'releaseDate': datetime.date(2014, 7, 5)},
             }

    for media, media_data in medias.items():
        m = add_media(media, 
            media_data['type'],
            media_data['coverImage'],
            media_data['writer'], 
            media_data['language'],
            media_data['releaseDate'],)
        
        for p in media_data['posts']:
            add_post(m, testUser, p['title'], p['rating'], p['comment'], p['publishDate'], p['likes'],)

        if media_data['type'] == 'book':
            isbn = media_data['concreteMedia']['isbn']
            add_book(m, isbn)
        elif media_data['type'] == 'movie':
            duration = media_data['concreteMedia']['duration']
            add_movie(m, duration)
        elif media_data['type'] == 'show':
            seasons = media_data['concreteMedia']['seasons']
            episodes = media_data['concreteMedia']['episodes']
            add_show(m, seasons, episodes)
        else:
            duration = media_data['concreteMedia']['duration']
            add_song(m, duration)


    # Print out the medias we have added.
    for m in Media.objects.all():
       for p in Post.objects.filter(media=m):
           print(f'- {m}: {p}')
           

def add_post(media, user, title, rating, comment, publishDate, likes):
    p = Post.objects.get_or_create(media=media, user=user, title=title)[0]
    p.title=title
    p.rating=rating
    p.comment=comment
    p.publishDate=publishDate
    p.likes=likes
    p.save()

def add_media(title, type, coverImage, writer, language, releaseDate):
    m = Media.objects.get_or_create(title=title,
        type=type,
        coverImage=coverImage, 
        writer=writer, 
        language=language, 
        releaseDate=releaseDate,)[0]
    m.save()
    return m

def add_book(media, isbn):
    b = Book.objects.get_or_create(media=media,
        isbn=isbn,)[0]
    b.save()

def add_movie(media, duration):
    m = Movie.objects.get_or_create(media=media,
        duration=duration,)[0]
    m.save()

def add_show(media, episodes, seasons):
    s = Show.objects.get_or_create(media=media,
        episodes=episodes,
        seasons=seasons,)[0]
    s.save()

def add_song(media, duration):
    s = Song.objects.get_or_create(media=media,
        duration=duration,)[0]
    s.save()

# Start execution here!
if __name__ == '__main__':
    print('Starting Shelves population script...')
    populate()
