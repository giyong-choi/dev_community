from ..forms import *
from ..models import *
from ..serializers import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator


class PortfolioListView(View):
    def get(self, request, page_num=1):
        items_per_page = 9

        post_portfolio = PostPortfolio.objects.order_by('-id')
        portfolio_lists = []

        query = request.GET.get('search')
        search_type = request.GET.get('search_type')

        filtered_portfolios = post_portfolio
        if query:
            if search_type == "title_content":
                filtered_portfolios = post_portfolio.filter(
                    Q(post__title__icontains=query) | Q(post__content__icontains=query)
                )
            elif search_type == "writer":
                filtered_portfolios = post_portfolio.filter(
                    Q(post__author__username__icontains=query)
                )
        else:
            query = ''
            search_type = ''

        page = request.GET.get("page", page_num)
        paginator = Paginator(filtered_portfolios, items_per_page)
        page_obj = paginator.get_page(page)

        for portfolio in page_obj:
            post = Post.objects.get(id=portfolio.post_id)
            author = UserProfile.objects.get(id=post.author_id)
            post_portfolio = get_object_or_404(PostPortfolio, id=portfolio.id)
            tech_stacks = post_portfolio.tech_stack.strip("[]'").split(",")

            portfolio_lists.append({
                        'title': post.title,
                        'created_at': post.created_at,
                        'author_id': post.author_id,
                        'post_portfolio': portfolio.id,
                        'author': author.username,
                        'tech_stacks': tech_stacks,
                    })

        context = {
            "post_lists": portfolio_lists,
            "board_name": "프로젝트",
            "is_portfolio": True,
            "page_obj": page_obj,
            "query": query,
            "search_type": search_type,
        }

        return render(request, 'portfolio_list.html', context)


class PortfolioView(View):
    def get(self, request, post_portfolio_id=None):
        if post_portfolio_id:
            post_portfolio = get_object_or_404(PostPortfolio, id=post_portfolio_id)
            post = get_object_or_404(Post, id=post_portfolio.post_id)
            author = get_object_or_404(UserProfile, id=post.author_id)
            tech_stacks = post_portfolio.tech_stack.strip("[]'").split(",")

            context = {
                'title': post.title,
                'author': author.username,
                'author_id': author.id,
                'created_at': post.created_at,
                'start_date': post_portfolio.start_date,
                'end_date': post_portfolio.end_date,
                'members': post_portfolio.members,
                'tech_stacks': tech_stacks,
                'ext_link': post_portfolio.ext_link,
                'content': post.content,
                'post_portfolio_id' : post_portfolio_id,
                'post_id': post.id,
            }
            return render(request, 'portfolio.html', context)
        else:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('hanwooplz_app:portfolio_list')


class WritePortfolioView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, post_portfolio_id=None):
        if post_portfolio_id:
            post_portfolio = get_object_or_404(PostPortfolio, id=post_portfolio_id)
            post = get_object_or_404(Post, id=post_portfolio.post_id)
        else:
            post_portfolio = PostPortfolio()
            post = Post()
        
        if post_portfolio_id and request.user.id != post.author_id:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('hanwooplz_app:portfolio_list')

        start_date = ''
        end_date = ''
        tech_stack = ''
        if post_portfolio_id:
            start_date = str(post_portfolio.start_date).replace('년 ','-').replace('월 ','-').replace('일','')
            end_date = str(post_portfolio.end_date).replace('년 ','-').replace('월 ','-').replace('일','')
            tech_stack = ' '.join(post_portfolio.tech_stack)

        context = {
            'post_portfolio_id': post_portfolio_id,
            'title': post.title if post_portfolio_id else '',
            'start_date': start_date,
            'end_date': end_date,
            'members': post_portfolio.members if post_portfolio_id else '',
            'tech_stack': tech_stack,
            'ext_link': post_portfolio.ext_link if post_portfolio_id else '',
            'content': post.content if post_portfolio_id else '',
            'post_author_id': post.author_id if post_portfolio_id else '',
        }
        return render(request, 'write_portfolio.html', context)

    @method_decorator(login_required(login_url='login'))
    def post(self, request, post_portfolio_id=None):
        if post_portfolio_id:
            post_portfolio = get_object_or_404(PostPortfolio, id=post_portfolio_id)
            post = get_object_or_404(Post, id=post_portfolio.post_id)
        else:
            post_portfolio = PostPortfolio()
            post = Post()
        
        if post_portfolio_id and request.user.id != post.author_id:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('hanwooplz_app:portfolio_list')

        if 'delete-button' in request.POST:
            post.delete()
            return redirect('hanwooplz_app:portfolio_list')
        
        request.POST._mutable = True
        request.POST['tech_stack'] = request.POST.get('tech_stack').split()
        post_form = PostForm(request.POST, request.FILES, instance=post)
        post_portfolio_form = PostPortfolioForm(request.POST, request.FILES, instance=post_portfolio)

        if post_form.is_valid() and post_portfolio_form.is_valid():
            post = post_form.save(commit=False)
            post_portfolio = post_portfolio_form.save(commit=False)
            if not post_portfolio_id:
                post.author_id = request.user.id
                post.save()
                post_portfolio.post_id = post.id
                post_portfolio.save()
                post_portfolio_id = post_portfolio.id
            else:
                post.save()
                post_portfolio.save()

            return redirect('hanwooplz_app:portfolio', post_portfolio_id)
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'members': request.POST.get('members'),
                'tech_stack': request.POST.get('tech_stack'),
                'ext_link': request.POST.get('ext_link'),
                'content': request.POST.get('content'),
            }
            return render(request, 'write_portfolio.html', context)
