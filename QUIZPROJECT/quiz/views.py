from django.shortcuts import render, redirect
from .models import Quiz,Question,Option,Answer,QuizAttempt,QuestionAttempt
from .forms import QuizForm,AddQuestionForm,ExamAttendForm
from datetime import datetime, timedelta,timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.forms import formset_factory
from datetime import datetime
import pytz
from django.contrib import messages

# Create your views here.
def QuizListView(request):
    quiz_model = Quiz.objects.order_by('quiz_date')
    current_time = datetime.now(timezone.utc)

    current_time_utc = datetime.now(timezone.utc)

    # Add 5 hours and 30 minutes to the current time
    current_time_ist = current_time_utc + timedelta(hours=5, minutes=30)

    ongoing_quizzes_dict = {}
    upcomming_quizzes = []
    ended_quizzes = []

    for quiz in quiz_model:
        try:
            quiz_attempt_model = QuizAttempt.objects.get(user=request.user, quiz=quiz)
            quiz_attempt_check = True
        except QuizAttempt.DoesNotExist:
            quiz_attempt_model = None
            quiz_attempt_check = False

        end_time = quiz.quiz_date + timedelta(minutes=quiz.duration_minutes)
        if quiz.quiz_date < current_time_ist < end_time:
            ongoing_quizzes_dict[quiz] = quiz_attempt_check
        elif current_time_ist > end_time:
            ended_quizzes.append(quiz)
        else:
            upcomming_quizzes.append(quiz)
        reversed_list = reversed(ended_quizzes)
    return render(request, "quiz/quiz-list.html", {"ongoing_quizzes_dict": ongoing_quizzes_dict, "upcomming_quizzes": upcomming_quizzes, "ended_quizzes": reversed_list})


def QuizEditView(request,id):
    instance = Quiz.objects.get(id=id)
    if request.method == "POST":
        form_quiz = QuizForm(request.POST,instance=instance)
        if form_quiz.is_valid():
            request.session['form_submitted'] = True
            print(form_quiz.data)
            form_quiz.save()
            return redirect('quiz-list')
    else:
        form_quiz = QuizForm(instance=instance)
    return render(request, "quiz/quiz-add-edit.html",{"form_quiz":form_quiz})

def QuizDeleteView(request, id):
    Quiz.objects.get(id=id).delete()
    return redirect('quiz-list')

def QuizAddView(request):
    if request.method == "POST":
        form_quiz = QuizForm(request.POST)
        if form_quiz.is_valid():
            request.session['form_submitted'] = True
            print(form_quiz.data)
            form_quiz.save()
            return redirect('quiz-list')
    else:
        form_quiz = QuizForm()
    return render(request,"quiz/quiz-add-edit.html",{"form_quiz":form_quiz})

def QuizQuestionListView(request,id):

    question_model = []

    quiz_list = get_object_or_404(Quiz, id=id)
    question_list = Question.objects.filter(quiz=quiz_list)
    for question in question_list:
        option_model = Option.objects.filter(question=question)
        answer_model = Answer.objects.filter(question=question)
        question_dict = {"question":question,"option_model":option_model,"answer_model":answer_model}
        question_model.append(question_dict)
    return render(request,"quiz/quiz-question-list.html",{"quiz":quiz_list,"question_model":question_model})

def QuizQuestionDeleteView(request, id_question,id_quiz):
    delete_question = Question.objects.get(id=id_question).delete()
    url = reverse('quiz-question-list', args=[id_quiz])
    return redirect(url)

def QuizQuestionAddView(request, id_quiz,extra=1):
    quiz_model = Quiz.objects.get(id=id_quiz)
    quiz_formset = formset_factory(AddQuestionForm , extra=extra)
    if request.method == "POST":
        formset = quiz_formset(request.POST)
        if formset.is_valid():
            request.session['form_submitted'] = False
            #print(request.session['form_submitted'])
            for form in formset:
                form.save(quiz_model)
                url = reverse('quiz-question-list', args=[id_quiz])
                return redirect(url)
    else:
        formset = quiz_formset()
    return render(request, "quiz/quiz-question-add.html", {"formset":formset})

def ExamAttendeView(request, id_quiz):
    quiz = Quiz.objects.get(id=id_quiz)
    start_time = quiz.quiz_date
    quiz_duration = quiz.duration_minutes * 60

    total_score = 0

    current_time_utc = datetime.now(timezone.utc)
    current_time_ist = current_time_utc + timedelta(hours=5, minutes=30)

    start_time = datetime.strptime(str(start_time), "%Y-%m-%d %H:%M:%S%z")
    current_time_ist = datetime.strptime(str(current_time_ist), "%Y-%m-%d %H:%M:%S.%f%z")
    remaining_time = int((current_time_ist - start_time).total_seconds())
    remaining_time_dif = quiz_duration - remaining_time

    
    # Calculate the remaining time based on the time elapsed since the quiz started
    
    if remaining_time_dif < 0:
        remaining_time_dif = 0  # Ensure remaining time is not negative

    timer_duration = round(remaining_time_dif)  # Initial value for the timer


    if request.user.is_authenticated:
        form_submitted = request.session.get(f'form_submitted_{request.user.id}', False)

    if form_submitted:
        # Form has already been submitted, redirect to another page or show a message
        messages.info(request, 'You have already submitted the form.')
        return redirect('quiz-list')  # Replace 'another_page' with the name of another page URL pattern

    if request.method == 'POST':
        form = ExamAttendForm(request.POST)
        if form.is_valid():
            request.session[f'form_submitted_{request.user.id}'] = True
            end_time = datetime.now(timezone.utc)
            quiz_attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz, start_time=start_time, end_time=end_time)
            for question_id, choice_id in form.data.items():
                if question_id != 'csrfmiddlewaretoken':
                    print(f"Question {question_id}: Choice {choice_id}")
                    question = Question.objects.get(id=question_id)
                    selected_option = Option.objects.get(id=choice_id)
                    correct_answer = Answer.objects.get(question=question)
                    print("Selected Option:" , selected_option.text, ", Correct: ",correct_answer.text)
                    if selected_option.text == correct_answer.text:
                        marks_obtained = 1
                        total_score += 1
                    else:
                        marks_obtained = 0
                    QuestionAttempt.objects.create(quiz_attempt=quiz_attempt, question = question, selected_option=selected_option,marks_obtained=marks_obtained)
            quiz_attempt.score = total_score
            quiz_attempt.save()
            return redirect('quiz-list')
    else:
        form = ExamAttendForm(quiz_id=id_quiz)

    return render(request, 'quiz/exam-attend.html', {'quiz': quiz, 'form': form, 'timer_duration': timer_duration,'form_submitted': form_submitted})


def ExamAttendListView(request, quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)
    if request.user.is_staff:
        quiz_attempts = QuizAttempt.objects.filter(quiz=quiz)
    else:
        quiz_attempts = QuizAttempt.objects.filter(quiz=quiz, user=request.user)
    quiz_scores = {attempt: attempt.score for attempt in quiz_attempts}
    total_questions = Question.objects.filter(quiz=quiz)
    question_count = len(total_questions)
    return render(request,'quiz/exam-attempt-list.html',{"quiz_scores":quiz_scores,"question_count":question_count})

def ExamAnswerSheetView(request,quiz_attempt):
    quiz_attempts = QuizAttempt.objects.get(id=quiz_attempt)
    question_attempt = QuestionAttempt.objects.filter(quiz_attempt=quiz_attempts)
    for question in question_attempt:
        print(question.question.answer_set.all())
    return render(request,"quiz/exam-answer-sheet.html",{"question_attempt":question_attempt})


