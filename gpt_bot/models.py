import datetime

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.template.loader import render_to_string
from weasyprint import HTML


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_action_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user_id)

    class Meta:
        db_table = "tg_user"
        ordering = ["-joined_at"]


class Gender(models.TextChoices):
    famale = "famale", "Famale"
    male = "male", "Male"


class Specialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class FlowProcess(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=8, choices=Gender.choices)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    specialization = models.ManyToManyField(Specialization)
    cv = models.URLField(null=True, blank=True)

    iq_test_score = models.IntegerField(null=True, blank=True)

    soft_skill_main_result = models.TextField(null=True, blank=True)
    soft_skill_recommendation = models.TextField(null=True, blank=True)

    professional_test_main_result = models.TextField(null=True, blank=True)
    professional_test_recommendation = models.TextField(null=True, blank=True)

    generated_resume = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.full_name} - {self.id}"

    def get_age(self):
        return (datetime.date.today() - self.birth_date).days // 365

    def generate_resume(self):
        self.iq_test_score = self.iq_test_score or 0
        if self.iq_test_score > 150:
            iq_score_range = "1"
        elif self.iq_test_score > 140:
            iq_score_range = "2"
        elif self.iq_test_score > 124:
            iq_score_range = "3"
        elif self.iq_test_score > 115:
            iq_score_range = "4"
        elif self.iq_test_score > 110:
            iq_score_range = "5"
        elif self.iq_test_score > 90:
            iq_score_range = "6"
        elif self.iq_test_score > 80:
            iq_score_range = "7"
        elif self.iq_test_score > 70:
            iq_score_range = "8"
        else:
            iq_score_range = "9"

        context = {
            "full_name": self.full_name,
            "age": self.get_age(),
            "specialty": ", ".join(map(str, self.specialization.all())),
            "soft_skill_result": self.soft_skill_main_result,
            "soft_skill_recommendation": self.soft_skill_recommendation,
            "professional_test_main_result": self.professional_test_main_result,
            "professional_test_recommendation": self.professional_test_recommendation,
            "iq_score": self.iq_test_score,
            "iq_score_range": iq_score_range
        }
        html_string = render_to_string("resume.html", context)
        html_file = HTML(string=html_string).write_pdf()
        self.generated_resume.save(f"media/generated_resume/{self.pk}.pdf", ContentFile(html_file))
        self.save()


class QuestionType(models.TextChoices):
    iq_test = "iq_test", "IQ Test"
    soft_skill = "soft_skill", "Soft Skill"
    professional_test = "professional_test", "Professional Test"


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    process = models.ForeignKey(FlowProcess, on_delete=models.CASCADE, null=True, blank=True)
    index = models.IntegerField(default=1)
    question_type = models.CharField(max_length=32, choices=QuestionType.choices)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self) -> str:
        return f"{self.question_type} - {self.index}"


class UserLimit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=255)
    limit = models.IntegerField(default=0)
    used = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.phone_number
