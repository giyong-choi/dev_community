from .views import views, chat_views, question_views, project_views, portfolio_views

from django.urls import path, include


app_name = 'hanwooplz_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/',views.index, name='index'),
    path('login/', views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path('register/', views.register, name='register'),
    path('find_id/', views.find_id, name='find_id'),
    path('find_pw/', views.find_pw, name='find_pw'),
    path('found_pw/', views.found_pw, name='found_pw'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path("myinfo/<int:user_id>", views.myinfo, name="myinfo"),
    path('send_application/', views.send_application, name='send_application'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('accept_reject_notification/', views.accept_reject_notification, name='accept_reject_notification'),
    path('mark_notifications_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    
    # portfolio_views.py
    path("portfolio-list/", portfolio_views.portfolio_list, name="portfolio_list"),
    path("portfolio/<int:post_portfolio_id>", portfolio_views.portfolio, name="portfolio"),
    path("write-portfolio/", portfolio_views.write_portfolio, name="write_portfolio"),
    path("write-portfolio/<int:post_portfolio_id>", portfolio_views.write_portfolio, name="write_portfolio"),

    # project_views.py
    path("project-list/", project_views.project_list, name="project_list"),
    path("project/<int:post_project_id>", project_views.project, name="project"),
    path("write-project/", project_views.write_project, name="write_project"),
    path("write-project/<int:post_project_id>", project_views.write_project, name="write_project"),
    path("update-status/", project_views.update_views, name="update_status"),

    # question_views.py
    path("question-list/", question_views.question_list, name="question_list"),
    path("question/<int:post_question_id>", question_views.question, name="question"),
    path("write-question/", question_views.write_question, name="write_question"),
    path("write-question/<int:post_question_id>", question_views.write_question, name="write_question"),
    path("write-answer/<int:post_question_id>", question_views.write_answer, name="write_answer"),
    path("write-answer/<int:post_question_id>/<int:post_answer_id>", question_views.write_answer, name="write_answer"),
    path("question-like/<int:post_question_id>", question_views.like, name="question_like"),
    path("question-like/<int:post_question_id>/<int:answer_id>", question_views.like, name="question_like"),

    # chat_views.py
    path('chat/<int:room_number>/<int:receiver_id>', chat_views.current_chat, name='chat'),
    path('chat-msg/<int:room_number>', chat_views.chat_msg, name='chat_msg'),
]
