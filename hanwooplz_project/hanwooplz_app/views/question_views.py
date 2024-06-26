from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from ..forms import PostForm, PostQuestionForm
from ..models import Post, PostQuestion, PostAnswer, UserProfile, AnswerLike


class QuestionListView(View):
    def get(self, request, page_num=1):
        items_per_page = 10

        post_question = PostQuestion.objects.order_by('-id')
        question_lists = []

        query = request.GET.get('search')
        search_type = request.GET.get('search_type')

        filtered_questions = post_question
        if query:
            if search_type == "title_content":
                filtered_questions = post_question.filter(
                    Q(post__title__icontains=query) | Q(post__content__icontains=query)
                )
            elif search_type == "writer":
                filtered_questions = post_question.filter(
                    Q(post__author__username__icontains=query)
                )
        else:
            query = ''
            search_type = ''

        page = request.GET.get("page", page_num)
        paginator = Paginator(filtered_questions, items_per_page)
        page_obj = paginator.get_page(page)

        for question in page_obj:
            post = Post.objects.get(id=question.post_id)
            author = UserProfile.objects.get(id=post.author_id)
            post_question = get_object_or_404(PostQuestion, id=question.id)
            keywords = post_question.keyword.strip("[]'").split(",")

            question_lists.append({
                'title': post.title,
                'created_at': post.created_at,
                'author_id': post.author_id,
                'post_question': question.id,
                'author': author.username,
                'keywords': keywords,
            })

        context = {
            "post_lists": question_lists,
            "board_name": "질의응답",
            "is_portfolio": True,
            "page_obj": page_obj,
            "query": query,
            "search_type": search_type,
        }

        return render(request, 'question_list.html', context)


class QuestionView(View):
    def get(self, request, post_question_id=None):
        if post_question_id:
            post_question = get_object_or_404(PostQuestion, id=post_question_id)
            post = get_object_or_404(Post, id=post_question.post_id)
            author = get_object_or_404(UserProfile, id=post.author_id)
            keywords = post_question.keyword.strip("[]'").split(",")

            post_answer = PostAnswer.objects.filter(question_id=post_question_id)
            if post_answer:
                post_ = Post.objects.filter(id__in=post_answer.values_list('post_id', flat=True))
                author_ = UserProfile.objects.filter(id__in=post_.values_list('author_id', flat=True))
                post_answer, post_ , author_ = post_answer.values(), post_.values(), author_.values()
                for p_ in post_:
                    p_['answer_id'] = p_['id']
                    p_.pop('id')
                for a_ in author_:
                    a_.pop('id')
                answers = []
                answer_post_id_list = []
                for i in range(len(post_answer)):
                    likes = AnswerLike.objects.filter(answer=post_answer[i]["id"]).count()
                    answers.append({**post_answer[i],**post_[i],**author_[i],"likes": likes})
                    answer_post_id_list.append(post_answer[i]["post_id"])
                answered = True if request.user.id in post_.values_list('author_id', flat=True) else False
            else:
                answers = []
                answered = False
                answer_post_id_list = []

            context = {
                'title': post.title,
                'content': post.content,
                'author': author.username,
                'author_id': author.id,
                'created_at': post.created_at,
                'like': post_question.likes.count(),
                'keywords': keywords,
                'post_question_id' : post_question_id,
                'post_id': post.id,
                'answers': answers,
                'answer_post_id_list': answer_post_id_list,
                'answered': answered,
            }
            return render(request, 'question.html', context)
        else:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('hanwooplz_app:question_list')


class WriteQuestionView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, post_question_id=None):
        if post_question_id:
            post_question = get_object_or_404(PostQuestion, id=post_question_id)
            post = get_object_or_404(Post, id=post_question.post_id)
        else:
            post_question = PostQuestion()
            post = Post()

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

    def post(self, request, post_question_id=None):
        if post_question_id:
            post_question = get_object_or_404(PostQuestion, id=post_question_id)
            post = get_object_or_404(Post, id=post_question.post_id)
        else:
            post_question = PostQuestion()
            post = Post()

        # 작성 시
        if request.method == 'POST':
            if 'delete-button' in request.POST:
                post.delete()
                return redirect('hanwooplz_app:question_list')

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
                context = {
                    'title': request.POST.get('title'),
                    'content': request.POST.get('content'),
                    'keyword': request.POST.get('keyword'),
                }
                return render(request, 'write_question.html', context)


class WriteAnswerView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, post_question_id, post_answer_id=None):
        if post_question_id:
            post_question = get_object_or_404(PostQuestion, id=post_question_id)
            post_ = get_object_or_404(Post, id=post_question.post_id)
            author_ = get_object_or_404(UserProfile, id=post_.author_id)
            keywords = post_question.keyword.strip("[]'").split(",")
            if post_answer_id:
                post_answer = get_object_or_404(PostAnswer, id=post_answer_id)
                post = get_object_or_404(Post, id=post_answer.post_id)
            else:
                post_answer = PostAnswer()
                post = Post()
        else:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('hanwooplz_app:question_list')

        if post_answer_id:
            if request.user.id == post.author_id:
                context = {
                    'title_question': post_.title,
                    'keywords_question': keywords,
                    'content_question': post_.content,
                    'author_question': author_.username,
                    'author_id_question': author_.id,
                    'created_at_question': post_.created_at,
                    'post_question_id': post_question_id,
                    'post_answer_id': post_answer_id,
                    'content': post.content,
                    'post_author_id': post.author_id,
                }
                return render(request, 'write_answer.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('hanwooplz_app:question', post_question_id)
        else:
            context = {
                    'title_question': post_.title,
                    'keywords_question': keywords,
                    'content_question': post_.content,
                    'author_question': author_.username,
                    'author_id_question': author_.id,
                    'created_at_question': post_.created_at,
                    'post_question_id': post_question_id,
            }
            return render(request, 'write_answer.html', context)

    def post(self, request, post_question_id, post_answer_id=None):
        if post_question_id:
            post_question = get_object_or_404(PostQuestion, id=post_question_id)
            post_ = get_object_or_404(Post, id=post_question.post_id)
            author_ = get_object_or_404(UserProfile, id=post_.author_id)
            keywords = post_question.keyword.strip("[]'").split(",")
            if post_answer_id:
                post_answer = get_object_or_404(PostAnswer, id=post_answer_id)
                post = get_object_or_404(Post, id=post_answer.post_id)
            else:
                post_answer = PostAnswer()
                post = Post()
        else:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('hanwooplz_app:question_list')

        # 작성 시
        if request.method == 'POST':
            if 'delete-button' in request.POST:
                post.delete()
                return redirect('hanwooplz_app:question', post_question_id)

            request.POST._mutable = True
            request.POST['title'] = '제목없음'
            post_form = PostForm(request.POST, request.FILES, instance=post)

            if post_form.is_valid():
                post = post_form.save(commit=False)
                if not post_answer_id:
                    post.author_id = request.user.id
                    post.save()
                    post_answer.post_id = post.id
                    post_answer.question_id = post_question_id
                    post_answer.save()
                else:
                    post.save()
                    post_answer.save()

                return redirect('hanwooplz_app:question', post_question_id)
            else:
                messages.info(request, '답변을 등록하는데 실패했습니다. 다시 시도해주세요.')
                context={
                    'title_question': post_.title,
                    'keywords_question': keywords,
                    'content_question': post_.content,
                    'author_question': author_.username,
                    'author_id_question': author_.id,
                    'created_at_question': post_.created_at,
                    'post_question_id': post_question_id,
                    'content': request.POST.get('content'),
                }
                return render(request, 'write_answer.html', context)

@login_required
def like(request, post_question_id, answer_id=None):
    if request.user.is_authenticated:
        if not answer_id:
            post = get_object_or_404(PostQuestion, pk=post_question_id)
        else:
            post = get_object_or_404(PostAnswer, pk=answer_id)
        user = get_object_or_404(UserProfile, pk=request.user.id)

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        post.save()
        return redirect('hanwooplz_app:question', post_question_id)
    return redirect('hanwooplz_app:question', post_question_id)
