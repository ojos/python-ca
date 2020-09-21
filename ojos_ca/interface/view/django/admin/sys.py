from django.contrib import admin

from ojos_ca.interface.repo.rds.django.model import SeqModel, SysVarModel
from .core import BaseAdmin


@admin.register(SysVarModel)
class SysVarAdmin(BaseAdmin):
    fieldsets = (
        ('', {
            'fields': (
                'created_at', 'updated_at',
                'key', 'raw_data', 'module', 'note',
            )
        }),
    )
    readonly_fields    = (
        'created_at', 'updated_at',
    )
    # actions            = BaseAdmin.actions + [
    #     delete_selected_cache, delete_all_cache,
    # ]
    list_display       = ('updated_at', 'key', 'raw_data', 'module', 'note',)
    # list_editable      = ('raw_data',)
    search_fields      = ('key',)
    list_display_links = ('key',)
    list_filter        = ('module',)

    # def __init__(self, model, admin_site):
    #     super(SystemVariableAdmin, self).__init__(model, admin_site)

    # def post_save(self, request, obj, form, change):
    #     entity = SystemVariableSerializer.model_to_entity(obj)
    #     self.repo.cache_repo.update_or_create(entity)

    # def post_delete(self, request, obj):
    #     self.repo.cache_repo.delete(obj.pk)

@admin.register(SeqModel)
class SeqAdmin(BaseAdmin):
    fieldsets = (
        ('', {
            'fields': (
                'created_at', 'updated_at',
                'seq_id', 'count'
            )
        }),
    )
    readonly_fields    = (
        'created_at', 'updated_at',
    )
    list_display       = ('updated_at', 'seq_id', 'count',)
    # list_editable      = ()
    search_fields      = ('seq_id',)
    list_display_links = ('seq_id',)
    # list_filter        = ()

