from django import forms
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, int_list_validator


class MediaForm(forms.ModelForm):
    title = forms.CharField(max_length=Media.TITLE_MAX_LENGTH,
                                help_text="Please enter the media title")
    
    type = forms.CharField(help_text="Please select the type of media",
                            widget=forms.Select(choices=Media.TYPE_CHOICES))

    writer = forms.CharField(max_length=Media.WRITER_MAX_LENGTH,
                                help_text="Please enter the media author")

    language = forms.CharField(max_length=Media.LANG_MAX_LENGTH,
                                help_text="Please enter the media language")
    
    releaseDate = forms.DateField(help_text="Please the enter release date")

    class Meta:
        model = Media
        fields = ('title', 'writer', 'language', 'releaseDate', 'type', )


class BookForm(forms.ModelForm):
        isbn = forms.CharField(max_length=Book.ISBN_MAX_LENGTH, 
                               help_text="The ISBN number must be 13 digits long")
        
        class Meta:
            model = Book
            fields = ('isbn', )


class MovieForm(forms.ModelForm):
        duration = forms.DurationField(help_text="Please enter the duration of the movie")
        
        class Meta:
            model = Movie
            fields = ('duration', )


class ShowForm(forms.ModelForm):
        episodes = forms.IntegerField(help_text="Please enter the number of episodes")
        seasons = forms.IntegerField(help_text="Please enter the number of seasons")
        
        class Meta:
            model = Show
            fields = ('episodes', 'seasons' )


class SongForm(forms.ModelForm):
        duration = forms.DurationField(help_text="Please enter the duration of the song")
        
        class Meta:
            model = Song
            fields = ('duration', )


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=Post.TITLE_MAX_LENGTH,
                                    help_text="Enter the title of your post")
    
    rating = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                    help_text="Provide a score between 0 and 10")
    
    comment = forms.CharField(widget=forms.Textarea, max_length=Post.COMM_MAX_LENGTH,
                                    help_text="Enter your comment")
    
    class Meta:
        model = Post
        fields = ['title', 'rating', 'comment',]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)