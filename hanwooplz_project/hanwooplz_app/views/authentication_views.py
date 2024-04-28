from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from ..forms import LoginForm, CustomUserCreationForm, UserProfileForm


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hanwooplz_app:login')
        return render(request, 'registration/register.html', {'form': form})


class EditProfileView(View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        form.fields['username'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True
        return render(request, 'edit_profile.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user_profile = form.save(commit=False)
            if 'user_img' in request.FILES:
                user_img = request.FILES['user_img']
                filename = f'user_img_{user_profile.id}_{user_img.name}'
                user_profile.user_img.save(filename, user_img)
            user_profile.save()
            user_id = request.user.id
            return redirect(reverse('hanwooplz_app:myinfo', args=[user_id]))
        return render(request, 'edit_profile.html', {'form': form})


class ChangePasswordView(View):
    def get(self, request):
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'password_change_form': password_change_form})

    def post(self, request):
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, request.user)
            return redirect(reverse("hanwooplz_app:login"))
        return render(request, 'change_password.html', {'password_change_form': password_change_form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "registration/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error(None, "로그인에 실패했습니다. 올바른 아이디와 비밀번호를 입력하세요.")
        return render(request, "registration/login.html", {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("hanwooplz_app:login"))
