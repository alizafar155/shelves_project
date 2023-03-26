from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User


class IndexViewTests(TestCase):
    def test_index_view_with_no_media_status(self):
        response = self.client.get(reverse('shelves:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_with_no_media_string(self):
        response = self.client.get(reverse('shelves:index'))
        self.assertContains(response, 'No media has been uploaded to the website.')
    
    def test_index_view_with_no_media_context(self):
        response = self.client.get(reverse('shelves:index'))
        self.assertQuerysetEqual(response.context['medias'], [])
    
    def test_index_view_with_media_status(self):
        date = "2002-03-02"
        type = 'Book'
        test_user = create_user("bob", "bobpassword123", self)
        add_media('Frozen', test_user, date, type)
        add_media('Matilda', test_user, date, type)
        add_media('Macbeth', test_user, date, type)
        response = self.client.get(reverse('shelves:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_with_media_titles(self):
        date = "2002-03-02"
        type = 'Book'
        test_user = create_user("bob", "bobpassword123", self)
        add_media('Frozen', test_user, date, type)
        add_media('Matilda', test_user, date, type)
        add_media('Macbeth', test_user, date, type)
        response = self.client.get(reverse('shelves:index'))
        self.assertContains(response, "Frozen")
        self.assertContains(response, "Matilda")
        self.assertContains(response, "Macbeth")

    def test_index_view_with_media_count(self):
        date = "2002-03-02"
        type = 'Book'
        test_user = create_user("bob", "bobpassword123", self)
        add_media('Frozen', test_user, date, type)
        add_media('Matilda', test_user, date, type)
        add_media('Macbeth', test_user, date, type)
        response = self.client.get(reverse('shelves:index'))
        num_medias = len(response.context['medias'])
        self.assertEquals(num_medias, 3)


class ShowMediaViewTests(TestCase):
    def test_show_media_view_displays_correct_avgscore_status(self):
        date = "2002-03-02"
        type = 'Book'
        test_user_one = create_user("bob", "bobpassword123", self)
        test_user_two = create_user("duncan", "bobpassword123", self)
        test_media = add_media('Frozen', test_user_one, date, type)
        add_post(test_media, test_user_one, "I enjoyed it", 3)
        add_post(test_media, test_user_two, "I did not enjoy it", 5)
        response = self.client.get(reverse('shelves:show_media', kwargs={'media_type': type,
                                                                         'media_title_slug': test_media.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_show_media_view_displays_correct_avgscore(self):
        date = "2002-03-02"
        type = 'book'
        test_user_one = create_user("bob", "bobpassword123", self)
        test_user_two = create_user("duncan", "bobpassword123", self)
        test_media = add_media('Frozen', test_user_one, date, type)
        add_post(test_media, test_user_one, "I enjoyed it", 3)
        add_post(test_media, test_user_two, "I did not enjoy it", 2)
        response = self.client.get(reverse('shelves:show_media', kwargs={'media_type': type,
                                                                         'media_title_slug': test_media.slug}))
        num_posts = len(response.context['posts'])
        self.assertEqual(num_posts, 2)


class ListProfilesViewTests(TestCase):
    def test_list_profiles_view_with_users_status(self):
        create_user_profile("bob", "bobpassword123", self)
        create_user_profile("duncan", "duncanpassword123", self)
        response = self.client.get(reverse('shelves:list_profiles'))
        self.assertEqual(response.status_code, 200)

    def test_list_profiles_view_with_users_count(self):
        create_user_profile("bob", "bobpassword123", self)
        create_user_profile("duncan", "duncanpassword123", self)
        response = self.client.get(reverse('shelves:list_profiles'))
        num_profiles = len(response.context['user_profile_list'])
        self.assertEquals(num_profiles, 2)

    def test_list_profiles_view_with_users_names(self):
        create_user_profile("bob", "bobpassword123", self)
        create_user_profile("duncan", "duncanpassword123", self)
        response = self.client.get(reverse('shelves:list_profiles'))
        self.assertContains(response, "bob")
        self.assertContains(response, "duncan")


class ProfileViewTests(TestCase):
    def test_user_profile_view_with_posts_status(self):
        date = "2002-03-02"
        type = 'Book'
        test_user = create_user("bob", "bobpassword123", self)
        test_media = add_media('Frozen', test_user, date, type)
        add_post(test_media, test_user, "I enjoyed it", 3)
        response = self.client.get(reverse('shelves:profile', kwargs={'username': test_user.username}))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view_with_posts_count(self):
        date = "2002-03-02"
        type = 'Book'
        test_user = create_user("bob", "bobpassword123", self)
        test_media_one = add_media('Frozen', test_user, date, type)
        test_media_two = add_media('Matilda', test_user, date, type)
        add_post(test_media_one, test_user, "I enjoyed it", 3)
        add_post(test_media_two, test_user, "I did not enjoy it", 2)
        response = self.client.get(reverse('shelves:profile', kwargs={'username': test_user.username}))
        num_posts = len(response.context['posts'])
        self.assertEquals(num_posts, 2)

    def test_user_profile_view_with_friends_with_status(self):
        test_user_one = create_user_profile("bob", "bobpassword123", self)
        test_user_two = create_user_profile("duncan", "duncanpassword123", self)
        test_user_three = create_user_profile("james", "duncanpassword123", self)
        add_friends(test_user_one, test_user_two)
        add_friends(test_user_one, test_user_three)
        response = self.client.get(reverse('shelves:profile', kwargs={'username': test_user_one.user.username}))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view_with_friends_count(self):
        test_user_one = create_user_profile("bob", "bobpassword123", self)
        test_user_two = create_user_profile("duncan", "duncanpassword123", self)
        test_user_three = create_user_profile("james", "duncanpassword123", self)
        add_friends(test_user_one, test_user_two)
        add_friends(test_user_one, test_user_three)
        response = self.client.get(reverse('shelves:profile', kwargs={'username': test_user_one.user.username}))
        num_friends = len(response.context['selected_user_friends'])
        self.assertEqual(num_friends, 2)


class ListMediasViewTests(TestCase):
    def test_list_media_view_with_media_status(self):
        date = "2002-03-02"
        type = 'Book'
        test_user = create_user("bob", "bobpassword123", self)
        add_media('Frozen', test_user, date, type)
        response = self.client.get(reverse('shelves:list_media'))
        self.assertEqual(response.status_code, 200)
    
    def test_list_media_view_with_media_title(self):
        date = "2002-03-02"
        type = 'Book'
        test_user = create_user("bob", "bobpassword123", self)
        test_media = add_media('Frozen', test_user, date, type)
        response = self.client.get(reverse('shelves:list_media'))
        self.assertContains(response, 'books')

    def test_list_media_view_with_media_count(self):
        date = "2002-03-02"
        type = 'Book'
        test_user = create_user("bob", "bobpassword123", self)
        test_media_one = add_media('Book One', test_user, date, type)
        test_media_two = add_media('Book Two', test_user, date, type)
        test_media_three = add_media('Book Three', test_user, date, type)
        test_media_four = add_media('Book Four', test_user, date, type)

        add_book(test_media_one, 1234567890123)
        add_book(test_media_two, 1234567890123)
        add_book(test_media_three, 1234567890123)
        add_book(test_media_four, 1234567890123)

        response = self.client.get(reverse('shelves:list_media'))
        num_media = len([media for media in response.context['media_collection']['books'].values()])
        self.assertEqual(num_media, 4)

    def test_list_media_view_with_song_type_count(self):
        songType = 'Song'
        bookType = 'Book'
        date = "2002-03-02"
        test_user = create_user("bob", "bobpassword123", self)
        test_media_one = add_media('Book One', test_user, date, bookType)
        test_media_two = add_media('Book Two', test_user, date, bookType)
        add_book(test_media_one, 1234567890123)
        add_book(test_media_two, 1234567890123)

        test_media_three = add_media('Song One', test_user, date, songType)
        test_media_four = add_media('Song Two', test_user, date, songType)
        test_media_five = add_media('Song Three', test_user, date, songType)
        test_media_six = add_media('Song Four', test_user, date, songType)

        add_song(test_media_three,)
        add_song(test_media_four,)
        add_song(test_media_five,)
        add_song(test_media_six,)
        
        response = self.client.get(reverse('shelves:list_media'))
        num_songs = len(response.context['media_collection']['songs'])
        self.assertEqual(num_songs, 4)


def add_media(title, user, releaseDate, type):
    media = Media.objects.get_or_create(title=title, user=user, releaseDate=releaseDate)[0]
    media.type = type
    media.save()
    return media

def add_book(media, isbn):
    book = Book.objects.get_or_create(media=media)[0]
    book.isbn = isbn
    book.save()
    return book

def add_movie(media, duration):
    movie = Movie.objects.get_or_create(media=media)[0]
    movie.duration = duration
    movie.save()
    return movie

def add_show(media, seasons=0, episodes=0):
    show = Show.objects.get_or_create(media=media)[0]
    show.seasons = seasons
    show.episdoes = episodes
    show.save()
    return show

def add_song(media,):
    song = Song.objects.get_or_create(media=media)[0]
    song.save()
    return song

def add_post(media, user, title, likes):
    post = Post.objects.get_or_create(media=media, user=user)[0]
    post.title = title
    post.likes = likes
    return post

def create_user(username, password, self):
    my_user = User.objects.create_user(username=username, password=password)
    my_user.save()
    self.client.login(username=username, password=password)
    return my_user

def create_user_profile(username, password, self):
    user = create_user(username, password, self)
    user = UserProfile.objects.get_or_create(user=user)[0]
    user.save()
    return user

def add_friends(user_one, user_two):
    user_one.friends.add(user_two)
    user_two.friends.add(user_one)