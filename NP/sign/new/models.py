from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from new.texts import text1, text2, text3
from django.urls import reverse
from django.core.validators import MinValueValidator

article = 'AL'
news = 'NW'

TYPE = [
    (article, 'статья'),
    (news, 'новость'),
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        set_rating_comment_self = Comment.objects.filter(user__username=self.user.username).values("rating")
        sum_rating_comment_self = 0
        for i in set_rating_comment_self:
            sum_rating_comment_self = sum_rating_comment_self + list(i.values())[0]
        set_rating_post = Post.objects.filter(author__user=self.user).values("rating")
        sum_rating_post = 0
        rating_post = ''
        for i in set_rating_post:
            sum_rating_post = sum_rating_post + list(i.values())[0]
            rating_post = sum_rating_post * 3
        set_self_post = Post.objects.filter(author__user=self.user).values("id")
        post_id = []
        sum_comm_self_post = 0
        for i in set_self_post:
            c = list(i.values())[0]
            post_id.append(c)
        for i in post_id:
            c = Comment.objects.filter(post__id=i).values("rating")
            for x in c:
                rating_comm_post = list(x.values())[0]
                sum_comm_self_post = sum_comm_self_post + rating_comm_post
        all_rating = rating_post + sum_rating_comment_self + sum_comm_self_post
        self.rating = all_rating
        self.save()
        return print(f'суммарный рейтинг каждой статьи автора:{rating_post}'
                     f' суммарный рейтинг всех комментариев автора:{sum_rating_comment_self}'
                     f' суммарный рейтинг всех комментариев к статьям автора:{sum_comm_self_post}'
                     f' суммарный рейтинг автора:{all_rating}')


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):

    article = 'AL'
    news = 'NW'

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2,
                                choices=TYPE,)
    time_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=10000)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        text_post = self.text
        len_text = len(text_post)
        if len_text >= 124:
            return f'{text_post[0:124]}...'
        else:
            return text_post[0:len_text]

    def __str__(self):
        return f'{self.title.title()}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    time_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()