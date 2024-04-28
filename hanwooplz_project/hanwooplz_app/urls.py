from django.urls import path
from .views.authentication_views import LoginView, LogoutView, RegisterView, ChangePasswordView, EditProfileView
from .views.profile_views import MyInfoView
from .views.notification_views import SendApplicationView, MarkNotificationsAsReadView, GetNotificationsView, AcceptRejectNotificationView
from .views.portfolio_views import PortfolioListView, PortfolioView, WritePortfolioView
from .views.project_views import ProjectListView, ProjectView, WriteProjectView, update_views
from .views.question_views import QuestionListView, QuestionView, WriteQuestionView, WriteAnswerView, like
from .views.chat_views import CurrentChatView, ChatMessageView
from .views.main_views import MainView, IndexView
from .views.profile_views import MyInfoView
from .views.find_views import FindIdView, FindPasswordView, FoundPasswordView


app_name = 'hanwooplz_app'

urlpatterns = [
    # main_views.py
    path('', MainView.as_view(), name='main'),
    path('index/', IndexView.as_view(), name='index'),

    # authentication_views.py
    path('login/', LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),

    # find_views.py
    path('find_id/', FindIdView.as_view(), name='find_id'),
    path('find_pw/', FindPasswordView.as_view(), name='find_pw'),
    path('found_pw/', FoundPasswordView.as_view(), name='found_pw'),
    
    # profile_views.py
    path("myinfo/<int:user_id>", MyInfoView.as_view(), name="myinfo"),

    # notification_views.py
    path('send_application/', SendApplicationView.as_view(), name='send_application'),
    path('get_notifications/', GetNotificationsView.as_view(), name='get_notifications'),
    path('accept_reject_notification/', AcceptRejectNotificationView.as_view(), name='accept_reject_notification'),
    path('mark_notifications_as_read/', MarkNotificationsAsReadView.as_view(), name='mark_notifications_as_read'),
    
    # portfolio_views.py
    path('portfolio-list/', PortfolioListView.as_view(), name="portfolio_list"),
    path('portfolio/<int:post_portfolio_id>/', PortfolioView.as_view(), name="portfolio"),
    path('write-portfolio/', WritePortfolioView.as_view(), name="write_portfolio"),
    path('write-portfolio/<int:post_portfolio_id>/', WritePortfolioView.as_view(), name="write_portfolio"),

    # project_views.py
    path("project-list/", ProjectListView.as_view(), name="project_list"),
    path("project/<int:post_project_id>/", ProjectView.as_view(), name="project"),
    path("write-project/", WriteProjectView.as_view(), name="write_project"),
    path("write-project/<int:post_project_id>/", WriteProjectView.as_view(), name="write_project"),
    path("update-status/", update_views, name="update_status"),

    # question_views.py
    path("question-list/", QuestionListView.as_view(), name="question_list"),
    path("question/<int:post_question_id>", QuestionView.as_view(), name="question"),
    path("write-question/", WriteQuestionView.as_view(), name="write_question"),
    path("write-question/<int:post_question_id>", WriteQuestionView.as_view(), name="write_question"),
    path("write-answer/<int:post_question_id>", WriteAnswerView.as_view(), name="write_answer"),
    path("write-answer/<int:post_question_id>/<int:post_answer_id>", WriteAnswerView.as_view(), name="write_answer"),
    path("question-like/<int:post_question_id>", like, name="question_like"),
    path("question-like/<int:post_question_id>/<int:answer_id>", like, name="question_like"),

    # chat_views.py
    path('chat/<int:room_number>/<int:receiver_id>/', CurrentChatView.as_view(), name='chat'),
    path('chat-msg/<int:room_number>/', ChatMessageView.as_view(), name='chat_msg'),
]
