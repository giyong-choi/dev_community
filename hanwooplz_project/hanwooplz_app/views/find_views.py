from django.shortcuts import render
from django.views import View

class FindIdView(View):
    def get(self, request):
        return render(request, 'find_userinfo/find_id.html')

class FindPasswordView(View):
    def get(self, request):
        return render(request, 'find_userinfo/find_pw.html')

class FoundPasswordView(View):
    def get(self, request):
        return render(request, 'find_userinfo/found_pw.html')
