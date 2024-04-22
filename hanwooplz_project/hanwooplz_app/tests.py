from django.test import TestCase
from .models import UserProfile
from .forms import CustomUserCreationForm, LoginForm

class UserTest(TestCase):
    def test_register(self):
        form_data = {
            'username': 'test_user_id',
            'email': 'test@test.com',
            'password1': 'test_password',
            'password2': 'test_password',
            'full_name': 'test_user_name',
            'job': 'test_backend',
            'tech_stack': 'test_python',
            'career': 1,
            'career_detail': '테스트 주니어',
            'introduction': '테스트중입니다.',
            'github_link': '',
            'linkedin_link': ''
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(UserProfile.objects.filter(username='test_user_id').exists())

    def test_login(self):
        # 회원가입을 먼저 해야합니다.
        self.test_register()

        form_data = {
            'username': 'test_user_id',
            'password': 'test_password',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

        # 로그인 시도
        response = self.client.post('/login/', data=form_data)

        # 로그인이 성공적으로 이루어졌는지 확인
        self.assertEqual(response.status_code, 302)  # 리디렉션 확인
        self.assertIn('/', response.url)  # 로그인 성공 후 리디렉션된 URL 확인
