from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Avatar, AvatarHashtag, UserProfile, UserReading, ContinueReading, Notification
from book.models import Chapter
from .forms import UserCreationForm, UserChangeForm
from django_dynamic_admin_forms.admin import DynamicModelAdminMixin

# Register your models here.
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ('name', 'email', 'date_joined', 'is_active',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )

    filter_horizontal = ("groups", "user_permissions")
    list_filter = ()
    fieldsets = ()
    ordering = ('-date_joined',)

class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'hashtag', 'image_tag')
    list_filter = ['hashtag__name']

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'avatar')

class UserReadingAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'book')

@admin.register(ContinueReading)
class ContinueReadingAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    #raw_id_fields = ('user', 'book')
    autocomplete_fields = ['user', 'book']
    dynamic_fields = ("chapter",)

    def get_dynamic_chapter_field(self, data):
        book = data.get("book")
        if not book:
            queryset = Chapter.objects.all()
            value = data.get("chapter")
        else:
            queryset = Chapter.objects.filter(book=book)
            value = queryset.first()
            hidden = not queryset.exists()
        return queryset, value, hidden

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "book":
    #         print('\n******************88asdfasf******************88\n')

    #     if db_field.name == "chapter":
    #         continue_reading_id = request.resolver_match.kwargs.get('object_id')
    #         continue_reading = ContinueReading.objects.get(id=continue_reading_id)
    #         book = continue_reading.book
    #         kwargs["queryset"] = Chapter.objects.filter(book=book)
        
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(User, UserAdmin)
admin.site.register(AvatarHashtag)
admin.site.register(Avatar, AvatarAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserReading, UserReadingAdmin)
admin.site.register(Notification)