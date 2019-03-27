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
    path('oauth/', include('social_django.urls', namespace='social')), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = ''

