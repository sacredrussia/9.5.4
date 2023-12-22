from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TYPE
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from .filters import PostFilter
from .forms import PostForm
from .models import Post
from .models import Category
from django.shortcuts import get_object_or_404, render


class PostsList(ListView):
    model = Post
    ordering = '-time_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('new.add_post',
                           'new.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('new.add_post',
                           'new.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AL'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('new.add_post',
                           'new.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    context_object_name = 'news_edit'
    success_url = reverse_lazy('post_list')


class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('new.add_post',
                           'new.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    context_object_name = 'article_edit'
    success_url = reverse_lazy('post_list')


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(PostsList):
    name = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        self.filterset = PostFilter(self.request.GET, queryset)
        queryset = Post.objects.filter(category=self.category).order_by('-time_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['filterset'] = self.filterset
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей в категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
