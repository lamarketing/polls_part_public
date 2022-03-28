from datetime import date

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

from polls.models import Polls, Answers, Questions, PollsResults, PollsStatistics, PollsMailing

from django.conf import settings


class QuestionsInline(admin.TabularInline):
    model = Questions


@admin.register(Polls)
class PollsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_start', 'date_end', 'status')
    inlines = (QuestionsInline, )
    list_display_links = ('name', )

    def status(self, object: Polls):
        today = date.today()
        html = 'прошло'
        if object.date_start <= today <= object.date_end:
            html = '<span style="color:green">действует</span>'
        elif object.date_start > today:
            html = '<span style="color:blue">ожидает</span>'

        return mark_safe(html)

    status.short_description = "Статус"


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'poll')
    fields = ('id', 'name', 'poll', 'answers')
    list_select_related = ('poll', )


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(PollsResults)
class PollsResultsAdmin(admin.ModelAdmin):
    list_display = ('id', 'consultant', 'poll', 'isFile', 'created')
    list_display_links = ('consultant', 'poll')
    list_select_related = ('consultant', 'poll')
    autocomplete_fields = ('consultant', )
    list_filter = ('poll', )
    actions = ['make_result_word']

    def make_result_word(self, request, queryset: QuerySet[PollsResults]):
        for result in queryset:
            try:
                a = result.create_word
            except Exception as exp:
                a = None
                self.message_user(request, f'Ошибка: {exp}', messages.ERROR)
        self.message_user(request, f'Файлы успешно созданы: {len(queryset)} шт.', messages.SUCCESS)

    make_result_word.short_description = 'создать для выбранных результатов word файлы'

    def isFile(self, object: PollsResults):
        if object.file:
            return mark_safe(f'<img src="/static/admin/img/icon-yes.svg" alt="True"><a href="{settings.MEDIA_URL[:-1]}{object.file}" '
                             f'target="_blank"> файл.docx</a>')
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')

    isFile.short_description = 'Есть Word'


@admin.register(PollsStatistics)
class PollsStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll', 'isFull', 'zipFile', 'wordBigFile', 'created')
    list_display_links = ('poll', )
    list_select_related = ('poll', )
    readonly_fields = ('statistics', 'isFull', 'zipFile', 'wordBigFile', 'created')


@admin.register(PollsMailing)
class PollsMailingAdmin(admin.ModelAdmin):
    list_display = ('slug', 'created')
    raw_id_fields = ('consultants_add', 'consultants_error')

