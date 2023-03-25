import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, int_list_validator


class Media(models.Model):
    # FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Choice types
    TYPE_CHOICES = (
       ('Book','Book'),
       ('Movie','Movie'),
       ('Show','Show'),
       ('Song','Song'),
    )

    # Max-length values
    TITLE_MAX_LENGTH = 50
    WRITER_MAX_LENGTH = 50
    LANG_MAX_LENGTH = 50
    TYPE_MAX_LENGTH = 50

    # Fields
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    type = models.CharField(max_length=TYPE_MAX_LENGTH, choices=TYPE_CHOICES)
    coverImage = models.ImageField(blank=True)
    writer = models.CharField(max_length=WRITER_MAX_LENGTH)
    language = models.CharField(max_length=LANG_MAX_LENGTH)
    releaseDate = models.DateField(blank=True, validators=[MaxValueValidator(limit_value=datetime.date.today())])
    avgScore = models.FloatField(default=0)
    
    # Keep track of avg. rating for media
    def updateAvgScore(self, media):
        posts = media.post_set.all()
        numberOfPosts = len(posts)

        if (numberOfPosts != 0):
            scoreSum = 0

            for post in posts:
                scoreSum += post.rating
            
            self.avgScore = scoreSum/numberOfPosts
            self.save()

    # To string
    def __str__(self):
        return self.title
    
    # Slug
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.type = self.type.lower()
        self.slug = slugify(self.title)
        super(Media, self).save(*args, **kwargs)
    

class Book(models.Model):
    # FK
    media = models.OneToOneField(Media, on_delete=models.CASCADE)

    # Max-length values
    ISBN_MAX_LENGTH = 13

    # Fields
    isbn = models.CharField(max_length=ISBN_MAX_LENGTH, validators=[MinLengthValidator(13), int_list_validator(sep='')])
    
    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)


class Movie(models.Model):
    # FK
    media = models.OneToOneField(Media, on_delete=models.CASCADE)

    # Fields
    duration = models.DurationField(default=datetime.timedelta())
    
    def save(self, *args, **kwargs):
        super(Movie, self).save(*args, **kwargs)


class Show(models.Model):
    # FK
    media = models.OneToOneField(Media, on_delete=models.CASCADE)

    # Fields
    episodes = models.IntegerField(default=0)
    seasons = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        super(Show, self).save(*args, **kwargs)


class Song(models.Model):
    # FK
    media = models.OneToOneField(Media, on_delete=models.CASCADE)

    # Fields
    duration = models.DurationField(default=datetime.timedelta())
    
    def save(self, *args, **kwargs):
        super(Song, self).save(*args, **kwargs)


class Post(models.Model):
    # FK
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Max-length values
    TITLE_MAX_LENGTH = 50
    COMM_MAX_LENGTH = 1000

    # Fields
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=False)
    rating = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(max_length=COMM_MAX_LENGTH, blank=True)
    publishDate = models.DateField(default=datetime.date.today)
    likes = models.IntegerField(default=0)

    # Links user and media so that a user cannot have more than 1 post per media
    class Meta:
        unique_together = ('media','user')
    
    # To string
    def __str__(self):
        return self.title
    
    # Slug
    # slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        self.media.updateAvgScore(media=self.media)
    

class UserProfile(models.Model):
    # FK
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Fields
    picture = models.ImageField(blank=True)
    # age = models.IntegerField(validators=[MinValueValidator(13)])
    joinDate = models.DateField(default=datetime.date.today)

    # To string
    def __str__(self):
        return self.user.username
