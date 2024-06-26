from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from ..forms import PostForm, PostProjectForm
from ..models import Post, PostProject, ProjectMembers, UserProfile


class ProjectListView(View):
    def get(self, request, page_num=1):
        items_per_page = 9

        post_project = PostProject.objects.order_by('-id')
        project_lists = []

        query = request.GET.get('search')
        search_type = request.GET.get('search_type')

        filtered_projects = post_project
        if query:
            if search_type == "title_content":
                filtered_projects = post_project.filter(
                    Q(post__title__icontains=query) | Q(post__content__icontains=query)
                )
            elif search_type == "writer":
                filtered_projects = post_project.filter(
                    Q(post__author__username__icontains=query)
                )
        else:
            query = ''
            search_type = ''

        filter_option = request.GET.get('filter_option')
        if filter_option == 'recruiting':
            filtered_projects = filtered_projects.filter(status=1)

        # 페이지네이션
        page = request.GET.get("page", page_num)
        paginator = Paginator(filtered_projects, items_per_page)
        page_obj = paginator.get_page(page)

        for project in page_obj:
            post = Post.objects.get(id=project.post_id)
            author = UserProfile.objects.get(id=post.author_id)
            post_project = get_object_or_404(PostProject, id=project.id)
            tech_stacks = post_project.tech_stack.strip("[]'").split(",")
            is_recruiting = "모집중" if project.status == 1 else False
            project_status = "모집 완료" if project.status == 2 else "모집 중단"

            project_lists.append({
                'title': post.title,
                'created_at': post.created_at,
                'author_id': post.author_id,
                'post_project': project.id,
                'author': author.username,
                'tech_stacks': tech_stacks,
                'isRecruiting': is_recruiting,
                "project_status": project_status,
            })

        context = {
            "post_lists": project_lists,
            "board_name": "팀원 모집",
            "is_portfolio": False,
            "page_obj": page_obj,
            "query": query,
            "search_type": search_type,
        }

        return render(request, 'project_list.html', context)


class ProjectView(View):
    def get(self, request, post_project_id=None):
        if post_project_id:
            post_project = get_object_or_404(PostProject, id=post_project_id)
            post = get_object_or_404(Post, id=post_project.post_id)
            author = get_object_or_404(UserProfile, id=post.author_id)
            tech_stacks = post_project.tech_stack.strip("[]'").split(",")
            members = ProjectMembers.objects.filter(project=post_project_id).count()
            context = {
                'title': post.title,
                'author': author.username,
                'author_id': author.id,
                'created_at': post.created_at,
                'start_date': post_project.start_date,
                'end_date': post_project.end_date,
                'members': members,
                'target_members': post_project.target_members,
                'tech_stacks': tech_stacks,
                'ext_link': post_project.ext_link,
                'content': post.content,
                'post_project_id': post_project_id,
                'post_id': post.id,
                'project_status': post_project.status,
            }
            return render(request, 'project.html', context)
        else:
            messages.info('올바르지 않은 접근입니다.')
            return redirect('hanwooplz_app:project_list')


class WriteProjectView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, post_project_id=None):
        if post_project_id:
            post_project = get_object_or_404(PostProject, id=post_project_id)
            post = get_object_or_404(Post, id=post_project.post_id)
        else:
            post_project = PostProject()
            post = Post()

        if post_project_id:
            if request.user.id == post.author_id:
                start_date = str(post_project.start_date).replace('년 ', '-').replace('월 ', '-').replace('일', '')
                end_date = str(post_project.end_date).replace('년 ', '-').replace('월 ', '-').replace('일', '')
                context = {
                    'post_project_id': post_project_id,
                    'title': post.title,
                    'start_date': start_date,
                    'end_date': end_date,
                    'target_members': post_project.target_members,
                    'tech_stack': ' '.join(post_project.tech_stack),
                    'ext_link': post_project.ext_link,
                    'content': post.content,
                    'post_author_id': post.author_id,
                }
                return render(request, 'write_project.html', context)
            else:
                messages.info('올바르지 않은 접근입니다.')
                return redirect('hanwooplz_app:project', post_project_id)
        else:
            return render(request, 'write_project.html')

    def post(self, request, post_project_id=None):
        if post_project_id:
            post_project = get_object_or_404(PostProject, id=post_project_id)
            post = get_object_or_404(Post, id=post_project.post_id)
        else:
            post_project = PostProject()
            post = Post()

        if request.method == 'POST':
            if 'delete-button' in request.POST:
                post.delete()
                return redirect('hanwooplz_app:project_list')

            request.POST._mutable = True

            tech_stack = request.POST.get('tech_stack')
            if tech_stack:
                tech_stack_lower = ' '.join(tech_stack.split()).lower()
                request.POST['tech_stack'] = tech_stack_lower

            post_form = PostForm(request.POST, request.FILES, instance=post)
            post_project_form = PostProjectForm(request.POST, request.FILES, instance=post_project)

            if post_form.is_valid() and post_project_form.is_valid():
                post = post_form.save(commit=False)
                post_project = post_project_form.save(commit=False)
                if not post_project_id:
                    post.author_id = request.user.id
                    post.save()
                    post_project.post_id = post.id
                    post_project.save()
                    post_project_id = post_project.id
                    user = get_object_or_404(UserProfile, pk=request.user.id)
                    project = get_object_or_404(PostProject, pk=post_project_id)
                    ProjectMembers.objects.create(project=project, member=user)
                else:
                    post.save()
                    post_project.save()

                return redirect('hanwooplz_app:project', post_project_id)
            else:
                messages.info(request, '질문을 등록하는데 실패했습니다. 다시 시도해주세요.')
                context = {
                    'title': request.POST.get('title'),
                    'start_date': request.POST.get('start_date'),
                    'end_date': request.POST.get('end_date'),
                    'members': request.POST.get('members'),
                    'tech_stack': request.POST.get('tech_stack'),
                    'ext_link': request.POST.get('ext_link'),
                    'content': request.POST.get('content'),
                }
                return render(request, 'write_project.html', context)

def update_views(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        status = request.POST.get("status")
        project = get_object_or_404(PostProject, pk=project_id)
        project.status = status
        project.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
