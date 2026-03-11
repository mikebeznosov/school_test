from django.contrib import admin
from django.utils.html import format_html
from .models import Test, Question, Answer, Result
from .models import MainMenuItem, SideMenuItem, SidebarLink, SitePage, MathFormula

# ============= НАСТРОЙКА ВНЕШНЕГО ВИДА АДМИНКИ =============
admin.site.site_header = "Управление школьными тестами"
admin.site.site_title = "Админка тестов"
admin.site.index_title = "Добро пожаловать в панель управления"


# ============= МОДЕЛИ ДЛЯ ТЕСТОВ (ВАШИ СТАРЫЕ) =============
class QuestionAdmin(admin.ModelAdmin):
    fields = ['test', 'text', 'image', 'allow_text_answer']
    list_display = ['short_text', 'test', 'allow_text_answer']
    list_filter = ['test', 'allow_text_answer']
    search_fields = ['text']

    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    short_text.short_description = "Текст вопроса"


admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)


# ============= МЕНЮ САЙТА (НОВЫЕ МОДЕЛИ) =============
@admin.register(MainMenuItem)
class MainMenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'url']


@admin.register(SideMenuItem)
class SideMenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'url']


@admin.register(SidebarLink)
class SidebarLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']


# ============= УПРАВЛЕНИЕ КОНТЕНТОМ СТРАНИЦЫ (УЛУЧШЕННАЯ ВЕРСИЯ) =============
@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'is_published', 'updated_at')
    list_filter = ('subject', 'is_published')
    search_fields = ('title', 'body')

    # Указываем поля формы явно
    fields = ('title', 'slug', 'subject', 'lead', 'body', 'image', 'image_caption', 'is_published')

    prepopulated_fields = {'slug': ('title',)}



    def preview_lead(self, obj):
        if obj.lead:
            return obj.lead[:100] + "..." if len(obj.lead) > 100 else obj.lead
        return "—"

    preview_lead.short_description = "Вступление"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Превью"


# ============= МАТЕМАТИЧЕСКИЕ ФОРМУЛЫ =============
@admin.register(MathFormula)
class MathFormulaAdmin(admin.ModelAdmin):
    list_display = ['name', 'preview_formula', 'description']
    search_fields = ['name', 'latex_code', 'description']

    def preview_formula(self, obj):
        return f"${obj.latex_code}$"

    preview_formula.short_description = "Формула (LaTeX)"