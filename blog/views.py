from django.core import paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm 
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect

from .forms import (
    PostForm
)


def post_share(request, post_id):  #it retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():   #if all fields contain valid data then it returnd true else returns false
            cd = form.cleaned_data   #if form is valid then it retrieve validated data 
            post_url = request.build_absolute_uri(post.get_absolute_url())
 
            subject = '{} ({}) recommends your reading  " {} "'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:
            form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form':form, 'sent':sent})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tag__in=[tag])

    paginator = Paginator(object_list, 3)  #it have 3 posts in each page
    page = request.GET.get('page')  #it indicates the current page number
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/post/list.html', { 'page': page, 'posts': posts, 'tag' : tag})
    

    

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
     
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    #List of similar posts

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]



    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new _comment' : new_comment, 'comment_form' : comment_form ,  'similar_posts': similar_posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    pagination_by = 3
    template_name = 'blog/post/list.html'

    

#create new post
def create_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
    context = {
    'form': form
    }

    return render(request, "blog/post/post_form.html", context)




    

 

# Create your views here.
