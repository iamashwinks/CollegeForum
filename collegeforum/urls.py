from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from forum.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', signin),
    path('signup/', signup),
    path('', post_question),
    path('logout/', signout),
    path('question/<int:qid>/', question_page),
    path('upvote/<int:aid>/', upvote),
    path('comment/<int:aid>/', comment),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)