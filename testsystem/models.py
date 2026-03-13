from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

# ===================== Выбор предмета =====================
SUBJECT_CHOICES = [
    ('algebra', 'Алгебра'),
    ('geometry', 'Геометрия'),
    ('physics', 'Физика'),
]

# ===================== Тесты =====================
class Test(models.Model):
    title = models.CharField("Название теста", max_length=255)
    description = models.TextField("Описание теста", blank=True)
    published_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    time_limit = models.IntegerField(default=10, help_text="Время на тест в минутах")

    # Новое поле — предмет
    subject = models.CharField(
        "Предмет",
        max_length=20,
        choices=SUBJECT_CHOICES,
        default='algebra',
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField("Текст вопроса")
    image = models.ImageField("Изображение вопроса", upload_to='questions/', blank=True, null=True)
    allow_text_answer = models.BooleanField("Разрешить текстовый ответ", default=False)

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField("Текст ответа", max_length=255)
    is_correct = models.BooleanField("Правильный ответ", default=False)

    def __str__(self):
        return self.text


class Result(models.Model):
    student_name = models.CharField("Имя ученика", max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField("Баллы")
    grade = models.IntegerField("Оценка", blank=True, null=True)
    date_taken = models.DateTimeField("Дата прохождения", auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.test.title} - {self.score} баллов"


class StudentAnswer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField("Правильно", default=False)

    def __str__(self):
        return f"{self.question.text[:40]} - {self.is_correct}"


# ===================== CMS и меню =====================
class MainMenuItem(models.Model):
    title = models.CharField("Название пункта", max_length=100)
    url = models.CharField("Ссылка", max_length=200)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Пункт основного меню"
        verbose_name_plural = "Основное меню"

    def __str__(self):
        return self.title


class SideMenuItem(models.Model):
    title = models.CharField("Название пункта", max_length=100)
    url = models.CharField("Ссылка", max_length=200)
    icon = models.CharField("Иконка", max_length=50, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Пункт бокового меню"
        verbose_name_plural = "Боковое меню"

    def __str__(self):
        return self.title


class SidebarLink(models.Model):
    title = models.CharField("Текст ссылки", max_length=200)
    url = models.CharField("Ссылка", max_length=200)
    description = models.TextField("Описание", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Ссылка в боковой панели"
        verbose_name_plural = "Ссылки в боковой панели"

    def __str__(self):
        return self.title


class SitePage(models.Model):
    title = models.CharField("Заголовок страницы", max_length=200)
    slug = models.SlugField("URL (slug)", max_length=200, unique=True, blank=True)
    lead = models.TextField("Вступительная часть", blank=True)
    body = RichTextUploadingField("Основной текст", blank=True)
    image = models.ImageField("Изображение", upload_to='page_images/', blank=True, null=True)
    image_caption = models.CharField("Подпись к изображению", max_length=300, blank=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    # Новое поле — выбор предмета
    subject = models.CharField(
        "Раздел предмета",
        max_length=20,
        choices=SUBJECT_CHOICES,
        default='algebra',
    )

    class Meta:
        verbose_name = "Страница сайта"
        verbose_name_plural = "Страницы сайта"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автогенерация slug из title, если не заполнен
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class MathFormula(models.Model):
    name = models.CharField("Название формулы", max_length=100)
    latex_code = models.TextField("LaTeX код")
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Математическая формула"
        verbose_name_plural = "Математические формулы"

    def __str__(self):
        return self.name