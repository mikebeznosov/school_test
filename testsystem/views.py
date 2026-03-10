from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Test, Question, Answer, Result
from .models import MainMenuItem, SideMenuItem, SidebarLink, SitePage, MathFormula


# ===================== Главная страница =====================
def home_page(request):
    """
    Главная страница сайта с управляемым контентом
    """
    page_content = SitePage.objects.filter(is_published=True).first()

    context = {
        'main_menu': MainMenuItem.objects.filter(is_active=True).order_by('order'),
        'side_menu': SideMenuItem.objects.filter(is_active=True).order_by('order'),
        'sidebar_links': SidebarLink.objects.filter(is_active=True).order_by('order'),
        'page': page_content,
        'formulas': MathFormula.objects.all()[:5],  # последние 5 формул для примера
    }
    return render(request, 'home_page.html', context)


def page_view(request):
    """Просмотр отдельной страницы сайта"""
    context = {
        'main_menu': MainMenuItem.objects.filter(is_active=True),
        'side_menu': SideMenuItem.objects.filter(is_active=True),
        'sidebar_links': SidebarLink.objects.filter(is_active=True),
        'page': SitePage.objects.filter(is_published=True).first(),
        'formulas': MathFormula.objects.all()[:5],  # последние 5 формул
    }
    return render(request, 'page_detail.html', context)


# ===================== Список тестов =====================
def index(request):
    tests = Test.objects.all().order_by('-id')  # новые сверху
    return render(request, 'testsystem/index.html', {'tests': tests})


# ===================== Прохождение теста =====================
def test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.prefetch_related('answers')  # оптимизация: сразу подтягиваем ответы

    if request.method == 'POST':
        name = request.POST.get('name', 'Аноним')
        score = 0

        for q in questions:
            if q.allow_text_answer:
                answer_text = request.POST.get(f'text_{q.id}', '').strip()
                correct_answers = [a.text.strip() for a in q.answers.filter(is_correct=True)]
                if answer_text in correct_answers:
                    score += 1
            else:
                selected = request.POST.get(str(q.id))
                if selected:
                    try:
                        answer = Answer.objects.get(id=selected)
                        if answer.is_correct:
                            score += 1
                    except Answer.DoesNotExist:
                        pass

        total_questions = questions.count()
        percent = score / total_questions * 100 if total_questions > 0 else 0

        if percent >= 90:
            grade = 5
        elif percent >= 75:
            grade = 4
        elif percent >= 50:
            grade = 3
        else:
            grade = 2

        # Сохраняем результат
        Result.objects.create(
            student_name=name,
            test=test,
            score=score,
            grade=grade,
            date_taken=timezone.now()
        )

        # Перенаправляем на страницу с результатами этого пользователя
        return redirect('result_list', student_name=name)

    return render(request, 'testsystem/test.html', {'test': test, 'questions': questions})


# ===================== Просмотр результатов =====================
def result_list(request, student_name):
    results = Result.objects.filter(student_name=student_name).order_by('-date_taken')
    return render(request, 'testsystem/results_list.html', {'results': results, 'student_name': student_name})


def results_list_all(request):
    results = Result.objects.select_related('test').order_by('-date_taken')
    return render(request, 'testsystem/results.html', {'results': results})