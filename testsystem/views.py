from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import (
    Test, Question, Answer, Result, StudentAnswer,
    MainMenuItem, SideMenuItem, SidebarLink, SitePage, MathFormula
)


SUBJECTS = [
    ('algebra', 'Алгебра'),
    ('geometry', 'Геометрия'),
    ('physics', 'Физика'),
]


# =====================================
# Главная страница
# =====================================
def home_page(request, subject=None):

    pages = SitePage.objects.filter(is_published=True)

    if subject:
        pages = pages.filter(subject=subject)

    context = {
        'main_menu': MainMenuItem.objects.filter(is_active=True).order_by('order'),
        'side_menu': SideMenuItem.objects.filter(is_active=True).order_by('order'),
        'sidebar_links': SidebarLink.objects.filter(is_active=True).order_by('order'),
        'pages': pages,
        'formulas': MathFormula.objects.all()[:5],
        'subjects': SUBJECTS,
        'current_subject': subject,
    }

    page = pages.first() if pages.exists() else None
    context['page'] = page

    return render(request, 'testsystem/home_page.html', context)


# =====================================
# CMS страницы
# =====================================
def page_view(request, slug):

    page = get_object_or_404(SitePage, slug=slug, is_published=True)

    context = {
        'page': page,
        'main_menu': MainMenuItem.objects.filter(is_active=True).order_by('order'),
        'side_menu': SideMenuItem.objects.filter(is_active=True).order_by('order'),
        'sidebar_links': SidebarLink.objects.filter(is_active=True).order_by('order'),
        'formulas': MathFormula.objects.all()[:5],
        'subjects': SUBJECTS,
        'current_subject': page.subject,
        'pages': SitePage.objects.filter(is_published=True),
    }

    return render(request, 'testsystem/home_page.html', context)


# =====================================
# Список тестов
# =====================================
def index(request):

    tests = Test.objects.all().order_by('-id')

    return render(request, 'testsystem/index.html', {
        'tests': tests
    })


# =====================================
# Прохождение теста
# =====================================
def test(request, test_id):

    test_obj = get_object_or_404(Test, id=test_id)
    questions = test_obj.questions.all()

    for q in questions:
        q.shuffled_answers = list(q.answers.all())

    if request.method == 'POST':

        name = request.POST.get('name', 'Аноним')
        score = 0

        result = Result.objects.create(
            student_name=name,
            test=test_obj,
            score=0,
            grade=0,
            date_taken=timezone.now()
        )

        for q in questions:

            if q.allow_text_answer:

                answer_text = request.POST.get(f'text_{q.id}', '').strip()

                correct_answers = [
                    a.text.strip() for a in q.answers.filter(is_correct=True)
                ]

                is_correct = answer_text in correct_answers

                if is_correct:
                    score += 1

                StudentAnswer.objects.create(
                    result=result,
                    question=q,
                    text_answer=answer_text,
                    is_correct=is_correct
                )

            else:

                selected = request.POST.get(str(q.id))

                if selected:

                    try:

                        answer = Answer.objects.get(id=selected)

                        is_correct = answer.is_correct

                        if is_correct:
                            score += 1

                        StudentAnswer.objects.create(
                            result=result,
                            question=q,
                            selected_answer=answer,
                            is_correct=is_correct
                        )

                    except Answer.DoesNotExist:
                        pass

        total_questions = questions.count()

        percent = score / total_questions * 100 if total_questions else 0

        if percent >= 90:
            grade = 5
        elif percent >= 75:
            grade = 4
        elif percent >= 50:
            grade = 3
        else:
            grade = 2

        result.score = score
        result.grade = grade
        result.save()

        return redirect('result_detail', result_id=result.id)

    return render(request, 'testsystem/test.html', {
        'test': test_obj,
        'questions': questions
    })


# =====================================
# Детальный результат теста
# =====================================
def result_detail(request, result_id):

    result = get_object_or_404(Result, id=result_id)

    answers = result.answers.select_related(
        "question",
        "selected_answer"
    )

    return render(request, 'testsystem/result_detail.html', {
        'result': result,
        'answers': answers
    })


# =====================================
# Результаты ученика
# =====================================
def result_list(request, student_name):

    results = Result.objects.filter(
        student_name=student_name
    ).order_by('-date_taken')

    return render(request, 'testsystem/results_list.html', {
        'results': results,
        'student_name': student_name
    })


# =====================================
# Все результаты (админ)
# =====================================
def results_list_all(request):

    results = Result.objects.select_related(
        'test'
    ).order_by('-date_taken')

    return render(request, 'testsystem/results_list.html', {
        'results': results
    })