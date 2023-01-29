from django.shortcuts import render
from app.forms import CommentForm, SubscribeForm
from app.models import Post, Comments, Profile, Tag, WebsiteMeta
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    posts = Post.objects.all()
    subscribe_form = SubscribeForm()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    subscribe_successful = None
    featured_blog = Post.objects.filter(is_featured=True)
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]


    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful = 'Subscribed Successfully'
            subscribe_form = SubscribeForm()

    recent_post = Post.objects.all().order_by('-last_updated')[0:3]
    context = {
        'posts': posts,
        'top_posts' : top_posts,
        'recent_posts' : recent_post,
        'subscribe_form' : subscribe_form,
        'subscribe_successful' : subscribe_successful,
        'featured_blog' : featured_blog,
        'website_info' : website_info,
    }
    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm()
    comments = Comments.objects.filter(post=post, parent=None)

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            parent_obj = None
            if request.POST.get('parent'):
                # save reply
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))    
            else:
                # save comment
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id=postid)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    } 
    return render(request, 'app/post.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:2]
    tags = Tag.objects.all()
    context = {
        'tag' : tag,
        'top_posts' : top_posts,
        'recent_posts' : recent_posts,
        'tags' : tags,
    }
    return render(request, 'app/tag.html', context)


def author_page(request, slug):
    author = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author__in=[author.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author__in=[author.id]).order_by('-last_updated')[0:3]
    other_authors = Profile.objects.all()[0:3]
    context = {
        'author' : author,
        'top_posts' : top_posts,
        'recent_posts' : recent_posts,
        'other_authors' : other_authors,
    }
    return render(request, 'app/author.html', context)


def search_posts(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    context = {
        'posts' : posts,
        'search_query' : search_query,
    }
    return render(request, 'app/search.html', context)


def about(request):
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {
        'website_info' : website_info,
    }
    return render(request, 'app/about.html', context)