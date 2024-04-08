"""
URL configuration for QUIZPROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import QuizListView, QuizEditView,QuizDeleteView,QuizAddView,QuizQuestionListView,QuizQuestionDeleteView,ExamAttendeView,ExamAttendListView,ExamAnswerSheetView
from .views import QuizQuestionAddView

urlpatterns = [
    path('',QuizListView,name="quiz-list"),
    path('add/',QuizAddView,name="quiz-add"),
    path('edit/<int:id>',QuizEditView,name="quiz-edit"),
    path('delete/<int:id>',QuizDeleteView,name="quiz-delete"),
    path('question_list/<int:id>',QuizQuestionListView,name="quiz-question-list"),
    path('question_delete/<int:id_question>/<int:id_quiz>/',QuizQuestionDeleteView,name="quiz-question-delete"),
    path('question_add/<int:id_quiz>/',QuizQuestionAddView,name="quiz-question-add"),
    path('attend_exam/<int:id_quiz>/',ExamAttendeView,name="attend-exam"),
    path('attend_exam_list/<int:quiz_id>',ExamAttendListView,name="attend-exam-list"),
    path('exam_answer_sheet/<int:quiz_attempt>',ExamAnswerSheetView,name="exam-answer-sheet"),
]
