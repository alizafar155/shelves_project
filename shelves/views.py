from django.shortcuts import render
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile
from shelves.forms import MediaForm, BookForm, MovieForm, ShowForm, SongForm, PostForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


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


def show_media(request, media_title_slug, media_type):
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
    
    response = render(request, 'shelves/media_collection.html', context=context_dict)

    return response


@login_required
def add_media(request):
    media_form = MediaForm()

    if request.method == 'POST':
        media_form = MediaForm(request.POST)

        if media_form.is_valid():
            media = media_form.save(commit=False)
            media.user = request.user
            media.save()
            return redirect(reverse('shelves:add_type_details', kwargs={'media_title_slug': media.slug}))

        else:
            print(media_form.errors)

    return render(request, 'shelves/add_media.html', {'form': media_form})


@login_required
def add_type_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))
    
    if media.type == "book":
        type_form = BookForm
    elif media.type == 'movie':
        type_form = MovieForm
    elif media.type == 'show':
        type_form = ShowForm
    elif media.type == 'song':
        type_form = SongForm

    if request.method == 'POST':
        type_form = type_form(request.POST)

        if type_form.is_valid():
            type = type_form.save(commit=False)
            type.media = media
            type.save()

            return redirect(reverse('shelves:show_media',
                                    kwargs={'media_title_slug':
                                            media_title_slug,
                                            'media_type':
                                            media.type}))
        else:
            print(type_form.errors)

    context_dict = {'form': type_form, 'media': media}
    return render(request, 'shelves/add_type_details.html', context=context_dict)


@login_required
def add_post(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect('/shelves/')

    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            if media:
                post = post_form.save(commit=False)
                post.media = media
                post.likes = 0
                post.user = request.user
                post.save()

                return redirect(reverse('shelves:show_media',
                                        kwargs={'media_title_slug':
                                                media_title_slug,
                                                'media_type':
                                                media.type}))
        else:
            print(post_form.errors)

    context_dict = {'form': post_form, 'media': media}
    return render(request, 'shelves/add_post.html', context=context_dict)


@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            
            return redirect(reverse('shelves:index'))
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'shelves/profile_registration.html', context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture,})
        user_posts = Post.objects.filter(user = user.id)
        user_collection = Media.objects.filter(user = user.id)

        my_dict = {}
        my_dict['books'] = user_collection.filter(type='book')
        my_dict['movies'] = user_collection.filter(type='movie')
        my_dict['shows'] = user_collection.filter(type='show')
        my_dict['songs'] = user_collection.filter(type='song')
        
        return (user, user_profile, form, user_posts, my_dict)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form, posts, media_collection) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('shelves:index'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form,
                        'posts': posts,
                        'media_collection': media_collection,
                        }
        
        return render(request, 'shelves/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('shelves:index'))

        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('shelves:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'shelves/profile.html', context_dict)


@login_required
def delete_account(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user.delete()
        return redirect('/')

    return render(request, 'profile.html', {'user': user})

class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()
        return render(request,
                    'shelves/list_profiles.html',
                    {'user_profile_list': profiles})

def about(request):
    pass

def contact_us(request):
    pass
