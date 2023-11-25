from django.contrib import admin

from cafe.models import Cafe
from tables.models import Table
from asgiref.sync import sync_to_async


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafe', 'quantity')

    @sync_to_async
    def get_form(self, request, obj=None, **kwargs):
        """
        При создании нового объекта другие экземпляры моделей
        будут связаны с кафе администратора
        """
        form = super(TableAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        form.base_fields['cafe'].queryset = Cafe.objects.filter(
            cafe=request.user.cafe.id)
        return form

    @sync_to_async
    def get_queryset(self, request):
        """
        Персонал получит информацию о столах в его кафе,
        суперпользователя это не касается
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(cafe=request.user.cafe.id)
