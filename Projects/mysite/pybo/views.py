from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
''', Answer'''
from .forms import QuestionForm, AnswerForm

def index(request):
    """
    pybo 목록 출력
    """

    question_list = Question.objects.order_by('-create_date')
    context = {'question_list' : question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    '''
    pybo 내용 출력
    '''

    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    '''
    pybo 답변 등록
    '''

    question = get_object_or_404(Question,pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False) # 임시저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

    ''' 또 다른 방법. 가장 제일 위에 Answer 꼭 넣어야 함 
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer(question=question, content=request.POST.get('content), create_date = timezone.now())
    answer.save()
    return redirect('pybo:detail', question_id=question.id)
    '''

def question_create(request):
    '''
    pybo 질문 등록
    '''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # 임시저장
            question.create_date = timezone.now()
            question.save() # 완전히 저장
            return redirect('pybo:index') # 저장 후 다시 원래 화면으로 돌아감
    else: # GET일 때
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)