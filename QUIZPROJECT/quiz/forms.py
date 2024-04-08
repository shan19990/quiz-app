from django import forms
from .models import *

class QuizForm(forms.ModelForm):

    title = forms.CharField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=264)
    duration_minutes = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Minutes'}))
    quiz_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'YYYY-MM-DD HH:MM:SS - 24hrs format'}), required=True)

    class Meta:
        model = Quiz
        fields = "__all__"

class AddQuestionForm(forms.Form):

    CHOICES = [('Option 1', 'Option 1'), ('Option 2', 'Option 2'), ('Option 3', 'Option 3'), ('Option 4', 'Option 4')]

    question_text = forms.CharField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control'}), label='Question',required=True)
    option_text_1 = forms.CharField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control'}), label='Option 1',required=True)
    option_text_2 = forms.CharField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control'}), label='Option 2',required=True)
    option_text_3 = forms.CharField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control'}), label='Option 3',required=True)
    option_text_4 = forms.CharField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control'}), label='Option 4',required=True)
    answer_text = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label='Correct Answer', required=True)

    def save(self, quiz_model):
        Question_instance = Question.objects.create(quiz=quiz_model,text=self.cleaned_data['question_text'])
        
        Option_instance_1 = Option.objects.create(question=Question_instance,text=self.cleaned_data['option_text_1'])
        Option_instance_2 = Option.objects.create(question=Question_instance,text=self.cleaned_data['option_text_2'])
        Option_instance_3 = Option.objects.create(question=Question_instance,text=self.cleaned_data['option_text_3'])
        Option_instance_4 = Option.objects.create(question=Question_instance,text=self.cleaned_data['option_text_4'])

        answer_text = self.cleaned_data['answer_text']
        if answer_text == 'Option 1':
            answer = self.cleaned_data['option_text_1']
        elif answer_text == 'Option 2':
            answer = self.cleaned_data['option_text_2']
        elif answer_text == 'Option 3':
            answer = self.cleaned_data['option_text_3']
        elif answer_text == 'Option 4':
            answer = self.cleaned_data['option_text_4']

        Answer_instance = Answer.objects.create(question=Question_instance,text=answer)

class ExamAttendForm(forms.Form):
    def __init__(self, *args, quiz_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if quiz_id is not None:
            questions = Question.objects.filter(quiz_id=quiz_id)
            for question in questions:
                options = question.option_set.all()
                options_list = [(option.id, option.text) for option in options]
                self.fields[str(question.id)] = forms.ChoiceField(
                    choices=options_list,
                    widget=forms.RadioSelect,
                    label=question.text
                )