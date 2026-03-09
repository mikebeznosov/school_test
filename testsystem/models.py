from django.db import models

class Test(models.Model):
    title = models.CharField("Название теста", max_length=255)
    description = models.TextField("Описание теста", blank=True)
    published_date = models.DateTimeField("Дата публикации", auto_now_add=True)  # дата публикации

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField("Текст вопроса")
    image = models.ImageField("Изображение вопроса", upload_to='questions/', blank=True, null=True)
    allow_text_answer = models.BooleanField("Разрешить текстовый ответ", default=False)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField("Текст ответа", max_length=255)
    is_correct = models.BooleanField("Правильный ответ", default=False)

    def __str__(self):
        return self.text


class Result(models.Model):
    student_name = models.CharField("Имя ученика", max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField("Баллы")
    date_taken = models.DateTimeField("Дата прохождения", auto_now_add=True)
    grade = models.IntegerField("Оценка", blank=True, null=True)  # поле для оценки 2–5

    def __str__(self):
        return f"{self.student_name} - {self.test.title} - {self.score} баллов"