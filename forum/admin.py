from django.contrib import admin
from forum.models import Question, Solutions, Comment
from django_summernote.admin import SummernoteModelAdmin
from .models import SomeModel, Post

class QuestionAdmin(admin.ModelAdmin):
	list_display = ['question', 'author', 'datetime']
	search_fields = ['question', 'author']
	list_filter = ['datetime', 'author']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Solutions)
admin.site.register(Comment)


# Apply summernote to all TextField in model.
class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(SomeModel, SomeModelAdmin)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)