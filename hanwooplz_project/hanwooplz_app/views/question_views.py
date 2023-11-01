from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import *
from ..models import *
from ..serializers import *

def question_list(request, page_num=1):
    items_per_page = 10  # 페이지 당 항목 수

    # 페이지 번호를 이용해 해당 페이지의 포트폴리오 검색
    start_index = (page_num - 1) * items_per_page
    end_index = page_num * items_per_page

    post_question = PostQuestion.objects.order_by('-id')[start_index:end_index]
    question_lists = []

    query = request.GET.get('search')
    search_type = request.GET.get('search_type')  # 검색 옵션을 가져옵니다

    for question in post_question:
        post = Post.objects.get(id=question.post_id)
        author = UserProfile.objects.get(id=post.author_id)

        if query:
            # 검색 쿼리와 검색 옵션에 따라 검색 결과 필터링
            if search_type == "title_content" and ((query in post.title) or (query in post.content)):
                question_lists.append({
                    'title': post.title,
                    'created_at': post.created_at,
                    'author_id': post.author_id,
                    'post_question': question.id,
                    'author': author.username,
                })
            elif search_type == "writer" and (query in author.username):
                question_lists.append({
                    'title': post.title,
                    'created_at': post.created_at,
                    'author_id': post.author_id,
                    'post_question': question.id,
                    'author': author.username,
                })
        else:
            # 검색 쿼리가 없는 경우, 모든 포트폴리오 추가
            question_lists.append({
                'title': post.title,
                'created_at': post.created_at,
                'author_id': post.author_id,
                'post_question': question.id,
                'author': author.username,
            })

    context = {
        "question_lists": question_lists,
    }

    return render(request, 'question_list.html', context)


def question(request, post_question_id=None):
    if post_question_id:
        post_question = get_object_or_404(PostQuestion, id=post_question_id)
        post = get_object_or_404(Post, id=post_question.post_id)
        author = get_object_or_404(UserProfile, id=post.author_id)
        context = {
            'title': post.title,
            'content': post.content,
            'author': author.username,
            'author_id': author.id,
            'created_at': post.created_at,
            'like': post_question.like,
            'keywords': post_question.keyword,
            'post_question_id' : post_question_id,
            'post_id': post.id,
        }
        return render(request, 'question.html', context)
    else:
        messages.info('올바르지 않은 접근입니다.')
        return redirect('hanwooplz_app:question_list')

@login_required(login_url='login')
def write_question(request, post_question_id=None):
    if post_question_id:
        post_question = get_object_or_404(PostQuestion, id=post_question_id)
        post = get_object_or_404(Post, id=post_question.post_id)
    else:
        post_question = PostQuestion()
        post = Post()
    
    if request.method == 'POST':
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('hanwooplz_app:question_list')
        if 'temp-save-button' in request.POST:
            messages.info(request, '임시저장은 현재 지원되지 않는 기능입니다.')
            context={
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'keyword': request.POST.get('keyword'),
            }
            return render(request, 'write_question.html', context)
        
        request.POST._mutable = True
        request.POST['keyword'] = request.POST.get('keyword').split()
        post_form = PostForm(request.POST, request.FILES, instance=post)
        post_question_form = PostQuestionForm(request.POST, request.FILES, instance=post_question)

        if post_form.is_valid() and post_question_form.is_valid():
            post = post_form.save(commit=False)
            post_question = post_question_form.save(commit=False)
            if not post_question_id:
                post.author_id = request.user.id
                post.save()
                post_question.post_id = post.id
                post_question.save()
                post_question_id = post_question.id
            else:
                post.save()
                post_question.save()

            return redirect('hanwooplz_app:question', post_question_id)
        else:
            messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
            context={
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'keyword': request.POST.get('keyword'),
            }
            return render(request, 'write_question.html', context)
    else:
        if post_question_id:
            if request.user.id == post.author_id:
                context = {
                    'post_question_id': post_question_id,
                    'title': post.title,
                    'content': post.content,
                    'keyword': ' '.join(post_question.keyword),
                    'post_author_id': post.author_id,
                }
                return render(request, 'write_question.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('hanwooplz_app:question', post_question_id)
        else:
            return render(request, 'write_question.html')
