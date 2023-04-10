from django.contrib import admin
from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "joined_at", "last_action_at")
    

class QuestionInline(admin.StackedInline):
    model = models.Question
    exclude = ("index",)
    extra = 0
    
    
@admin.register(models.FlowProcess)
class FlowProcessAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name")
    inlines = [QuestionInline]
    

@admin.register(models.Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
