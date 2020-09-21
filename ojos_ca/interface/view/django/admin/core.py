from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect


class BaseAdmin(admin.ModelAdmin):
    date_hierarchy    = 'created_at'
    ordering          = ('-created_at',)
    readonly_fields   = ('created_at', 'updated_at',)
    actions_on_top    = True
    # actions_on_bottom = True

    # def delete_queryset(self, request, queryset):
    #     queryset.delete()
    #     for obj in queryset:
    #         self.post_delete(request, obj)

    # def pre_save(self, request, obj, form, change):
    #     print('pre_save')

    # def post_save(self, request, obj, form, change):
    #     print('post_save')

    # # 個別編集・リストページの保存ボタン押下時に呼び出される
    # def save_model(self, request, obj, form, change):
    #     self.pre_save(request, obj, form, change)
    #     super(BaseAdmin, self).save_model(request, obj, form, change)
    #     self.post_save(request, obj, form, change)

    # def post_delete(self, request, obj):
    #     print('post_delete')

    # 個別編集ページの削除ボタン押下時に呼び出される
    # def delete_model(self, request, obj):
    #     super(BaseAdmin, self).delete_model(request, obj)
    #     self.post_delete(request, obj)

    def changelist_view(self, request, extra_context=None):
        selected = request.POST.getlist(admin.helpers.ACTION_CHECKBOX_NAME)
        try:
            action = self.get_actions(request)[request.POST['action']][0]
            allow_no_selection = action.allow_no_selection
        except (KeyError, AttributeError):
            allow_no_selection = False

        if allow_no_selection and not selected:
            action(self, request)
            return HttpResponseRedirect(request.get_full_path())
        return admin.ModelAdmin.changelist_view(self, request, extra_context)

