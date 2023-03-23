from django.shortcuts import render
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile
from shelves.forms import MediaForm, BookForm, MovieForm, ShowForm, SongForm, PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    context_dict = {}

    try:
        media_list = Media.objects.order_by('-avgScore')[:10]
        post_list = Post.objects.order_by('-likes')[:10]

        context_dict['medias'] = media_list
        context_dict['posts'] = post_list
    
    except Media.DoesNotExist:
        context_dict['medias'] = None
        context_dict['posts'] = None

    response = render(request, 'shelves/index.html', context=context_dict)

    return response


def show_media(request, media_title_slug):
    context_dict = {}
    
    try:
        media = Media.objects.get(slug=media_title_slug)
        posts = Post.objects.filter(media=media)
        
        context_dict['media'] = media
        context_dict['posts'] = posts
    
    except Media.DoesNotExist:
        context_dict['media'] = None
        context_dict['posts'] = None

    return render(request, 'shelves/media.html', context=context_dict)


def list_medias(request):
    media_collection = {}

    book_list = Book.objects.all()
    movie_list = Movie.objects.all()
    show_list = Show.objects.all()
    song_list = Song.objects.all()

    media_collection['books'] = book_list
    media_collection['movies'] = movie_list
    media_collection['shows'] = show_list
    media_collection['songs'] = song_list

    context_dict = {}
    context_dict['media_collection'] = media_collection
    
    response = render(request, 'shelves/medias.html', context=context_dict)

    return response


def add_media(request):
    media_form = MediaForm()

    if request.method == 'POST':
        media_form = MediaForm(request.POST)

        if media_form.is_valid():
            media = media_form.save(commit=True)
            
            if media.type == "Book":
                return redirect(reverse('shelves:add_book_details', kwargs={'media_title_slug': media.slug}))
            elif media.type == "Movie":
                return redirect(reverse('shelves:add_movie_details', kwargs={'media_title_slug': media.slug}))
            elif media.type == "Show":
                return redirect(reverse('shelves:add_show_details', kwargs={'media_title_slug': media.slug}))
            elif media.type == "Song":
                return redirect(reverse('shelves:add_song_details', kwargs={'media_title_slug': media.slug}))

        else:
            print(media_form.errors)

    return render(request, 'shelves/add_media.html', {'form': media_form})


def add_book_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))
    
    book_form = BookForm()

    if request.method == 'POST':
        book_form = BookForm(request.POST)

        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.media = media
            book.save()

            return redirect(reverse('shelves:show_media',
                                    kwargs={'media_title_slug':
                                            media_title_slug}))
        else:
            print(book_form.errors)

    context_dict = {'form': book_form, 'media': media}
    return render(request, 'shelves/add_book_details.html', context=context_dict)


def add_movie_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))
    
    movie_form = MovieForm()

    if request.method == 'POST':
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.media = media
            movie.save()

            return redirect(reverse('shelves:show_media',
                            kwargs={'media_title_slug':
                                    media_title_slug}))
        else:
            print(movie_form.errors)
    
    context_dict = {'form': movie_form, 'media': media}
    return render(request, 'shelves/add_movie_details.html', context=context_dict)


def add_show_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))
    
    show_form = ShowForm()

    if request.method == 'POST':
        show_form = ShowForm(request.POST)

        if show_form.is_valid():
            show = show_form.save(commit=False)
            show.media = media
            show.save()
            
            return redirect(reverse('shelves:show_media',
                            kwargs={'media_title_slug':
                                    media_title_slug}))
        else:
            print(show_form.errors)

    context_dict = {'form': show_form, 'media': media}
    return render(request, 'shelves/add_show_details.html', context=context_dict)


def add_song_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))
    
    song_form = SongForm()

    if request.method == 'POST':
        song_form = SongForm(request.POST)

        if song_form.is_valid():
            song = song_form.save(commit=False)
            song.media = media
            song.save()
            
            return redirect(reverse('shelves:show_media',
                            kwargs={'media_title_slug':
                                    media_title_slug}))
        else:
            print(song_form.errors)

    context_dict = {'form': song_form, 'media': media}
    return render(request, 'shelves/add_song_details.html', context=context_dict)


def about(request):
    pass

def contact_us(request):
    pass
