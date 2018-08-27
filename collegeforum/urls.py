from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from forum.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', signin),
    path('signup/', signup),
    path('home/', post_question),
    path('logout/', signout),
    path('question/<int:qid>/', question_page),
    path('upvote/<int:aid>/', upvote),
]

