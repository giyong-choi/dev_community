from django.contrib.auth.models import AbstractUser
from django.db import models
from tinymce.models import HTMLField

class UserProfile(AbstractUser):
    # Custom columns
    full_name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    tech_stack = models.CharField(max_length=200)
    career = models.IntegerField(default=0)
    career_detail = models.TextField()
    introduction = models.TextField()
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    user_img = models.ImageField(upload_to="user_img", default=None, null=True)

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='Untitled')
    content = HTMLField()

class PostPnP(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    tech_stack = models.CharField(max_length=200)
    ext_link = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True

class PostPortfolio(PostPnP):
    members = models.IntegerField(default=1)

class PostProject(PostPnP):
    RECRUIT_STATUS_CHOICES = (
        (0, 'Recruitment Closed'),
        (1, 'Recruitment Open'),
        (2, 'Recruitment Completed'),
    )
    status = models.IntegerField(choices=RECRUIT_STATUS_CHOICES, default=1)
    members = models.ManyToManyField(UserProfile, through='ProjectMembers')
    target_members = models.IntegerField(default=1)

class ProjectMembers(models.Model):
    project = models.ForeignKey(PostProject, on_delete=models.CASCADE)
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class PostQnA(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class PostQuestion(PostQnA):
    keyword = models.CharField(max_length=200)
    likes = models.ManyToManyField(UserProfile, related_name='liked_questions', through='QuestionLike')

class PostAnswer(PostQnA):
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    likes = models.ManyToManyField(UserProfile, related_name='liked_answers', through='AnswerLike')

class QuestionLike(models.Model):
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class AnswerLike(models.Model):
    answer = models.ForeignKey(PostAnswer, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class ChatRoom(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):  
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='received_messages')
    message = models.CharField(max_length=500)
    read_or_not = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    chat_uuid = models.UUIDField(editable=False, unique=True, null=True)

class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='notifications')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,related_name='notification_sender')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accept_or_not = models.BooleanField(null=True)
    read_or_not = models.BooleanField(default=False)
