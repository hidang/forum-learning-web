import django
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Question
from django.contrib.auth.decorators import login_required
from . import forms
from django.core.paginator import Paginator

# Create your views here.


def question_list(request, tag_name=""):
    q = request.GET.get('q')

    questions = Question.objects.all().order_by(
        'date')  # lấy tất cả các câu hỏi trong database

    if tag_name:
        questions = questions.filter(tag__contains=tag_name)

    if q:
        questions = questions.filter(
            title__contains=q)

    question_paginator = Paginator(questions, 6)  # Show 6 questions per page

    page_number = request.GET.get('page')
    page = question_paginator.get_page(page_number)

    context = {
        'page': page,
        'page_range': question_paginator.page_range,
        'tag_name': tag_name
    }
    return render(request, 'questions/question_list.html', context)


def question_detail(request, question_id):
    # truy vấn vào database lấy câu hỏi có id =question_id
    question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        form = forms.CreateCommentForm(request.POST)
        if form.is_valid():
            # save comment to database
            instance = form.save(commit=False)
            instance.author = request.user
            instance.question = question
            instance.save()
            return HttpResponseRedirect(request.path)
    else:
        form = forms.CreateCommentForm(request.POST)

    return render(request, 'questions/question_detail.html', {'question': question, 'form': form})


@login_required(login_url='/accounts/login/')
def question_create(request):
    if request.method == 'POST':
        form = forms.CreateQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            # save question to database
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return question_list(request)
    else:
        form = forms.CreateQuestionForm(request.POST)
    return render(request, 'questions/question_create.html', {'form': form})
