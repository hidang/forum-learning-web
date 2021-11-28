from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Question
from django.contrib.auth.decorators import login_required
from . import forms
from django.core.paginator import Paginator

# Create your views here.


def question_list(request, tag_name=""):
    q = request.GET.get('q')

    questions = Question.objects.all().order_by(
        'date').reverse()  # lấy tất cả các câu hỏi trong database

    question_top_10 = sorted(
        questions, key=lambda x: x.comments.count(), reverse=True)[:10]  # lấy 10 câu hỏi có nhiều comment nhất

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
        'tag_name': tag_name,
        'question_top_10': question_top_10
    }
    return render(request, 'questions/question_list.html', context)


def question_detail(request, question_id):
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


def question_edit(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = forms.CreateQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('accounts:accounts_profile_me')
    else:
        form = forms.CreateQuestionForm(instance=question)
    return render(request, 'questions/question_edit.html', {'form': form, 'question': question})


@login_required(login_url='/accounts/login/')
def question_delete(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.user == question.author:
        question.delete()
        question.save()
    return HttpResponseRedirect('/accounts/profile/me')


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
