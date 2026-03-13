from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import (
    Test, Question, Answer, Result, StudentAnswer,
    MainMenuItem, SideMenuItem, SidebarLink, SitePage, MathFormula
)

# ===============================
# Главная страница / CMS
# ===============================
SUBJECT_CHOICES = [
    ('algebra', 'Алгебра'),
    ('geometry', 'Геометрия'),
    ('physics', 'Физика'),
]

def tests_by_subject(request, subject):
    # Получаем человекочитаемое название предмета
    subject_name = dict(SUBJECT_CHOICES).get(subject, subject.title())

    # Фильтруем тесты по предмету
    tests = Test.objects.filter(subject=subject)  # если связь Test ↔ SitePage есть
    # ИЛИ, если ты будешь хранить subject прямо в Test, тогда:
    # tests = Test.objects.filter(subject=subject)

    context = {
        'tests': tests,
        'subject_name': subject_name
    }
    return render(request, 'testsystem/tests_by_subject.html', context)


# ===============================
# Тесты по предмету
# ===============================

# ===============================
# Поиск тестов
# ===============================
def tests_search(request):
    query = request.GET.get('q', '').strip()
    tests = Test.objects.all()
    if query:
        # фильтруем именно по названию теста
        tests = tests.filter(title__icontains=query)
    context = {
        'tests': tests,
        'query': query,
    }
    return render(request, 'testsystem/tests_search.html', context)


# ===============================
# Прохождение теста
# ===============================
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
                correct_answers = [a.text.strip() for a in q.answers.filter(is_correct=True)]
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
        percent = (score / total_questions * 100) if total_questions else 0
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
        'questions': questions,
        'time_limit': test_obj.time_limit
    })


# ===============================
# Детальный разбор теста
# ===============================
def result_detail(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    answers = StudentAnswer.objects.filter(result=result).select_related("question", "selected_answer")
    total_questions = result.test.questions.count()
    percent = (result.score / total_questions * 100) if total_questions else 0

    return render(request, 'testsystem/result_detail.html', {
        'result': result,
        'answers': answers,
        'total_questions': total_questions,
        'percent': round(percent, 1)
    })


# ===============================
# Результаты ученика
# ===============================
def result_list(request, student_name):
    results = Result.objects.filter(student_name=student_name).order_by('-date_taken')
    results_with_percent = []
    for r in results:
        total_questions = r.test.questions.count()
        percent = (r.score / total_questions * 100) if total_questions else 0
        results_with_percent.append({
            'id': r.id,
            'student_name': r.student_name,
            'test_title': r.test.title,
            'score': r.score,
            'total_questions': total_questions,
            'percent': round(percent, 1),
            'grade': r.grade
        })
    return render(request, 'testsystem/results_list.html', {
        'results': results_with_percent,
        'student_name': student_name
    })


# ===============================
# Все результаты
# ===============================
def results_list_all(request):
    results = Result.objects.select_related('test').order_by('-date_taken')
    return render(request, 'testsystem/results_list.html', {
        'results': results
    })


# ===============================
# CMS страницы
# ===============================
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
def home_page(request):
    return redirect('tests_by_subject', subject='algebra')  # редирект на алгебру по умолчанию