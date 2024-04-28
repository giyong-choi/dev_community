from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from ..forms import UserProfileForm
from ..models import UserProfile, Post, PostPortfolio, PostProject, PostQuestion


class MyInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'myinfo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('user_id')
        userinfo = UserProfile.objects.get(id=user_id)
        user_posts = Post.objects.filter(author=userinfo)
        tech_stacks = userinfo.tech_stack.strip("[]'").split(",")
        selected_category = self.request.GET.get('category', 'postportfolio')
        posts = []
        for post in user_posts:
            if selected_category == 'postportfolio':
                category = 'portfolio'
                postcategory = PostPortfolio.objects.filter(post=post).first()
            elif selected_category == 'postproject':
                category = 'project'
                postcategory = PostProject.objects.filter(post=post).first()
            elif selected_category == 'postquestion':
                category = 'question'
                postcategory = PostQuestion.objects.filter(post=post).first()
            if postcategory and selected_category == 'postquestion':
                posts.append({
                    'title': post.title,
                    'content': post.content,
                    'created_at': post.created_at,
                    'post_id': postcategory.id,
                    "category": category,
                })
            elif postcategory and selected_category != 'postquestion':
                tech_stack_str = postcategory.tech_stack.strip("[]'").split(",")
                posts.append({
                    'title': post.title,
                    'content': post.content,
                    'created_at': post.created_at,
                    'post_id': postcategory.id,
                    "category": category,
                    "post_tech_stack": tech_stack_str,
                })
        context.update({
            "user_id": userinfo.id,
            "username": userinfo.username,
            "full_name": userinfo.full_name,
            "job": userinfo.job,
            "tech_stack": tech_stacks,
            "career": userinfo.career,
            "career_detail": userinfo.career_detail,
            "introduction": userinfo.introduction,
            "posts": posts,
            "github_link": userinfo.github_link,
            "linkedin_link": userinfo.linkedin_link,
            "selected_category": selected_category,
            "user": userinfo,
        })
        return context
