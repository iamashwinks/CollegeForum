from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from forum.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', signin),
    path('signup/', signup),
    path('discussion/', post_question),
    path('logout/', signout),
    path('question/<int:qid>/', question_page),
    path('upvote/<int:aid>/', upvote),
    path('comment/<int:aid>/', comment),
    path('index/', index),
    path('', home),
    path('post/<int:post_id>', post_page),
    path('blogcomment/<int:post_id>/', blogcomment),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)