from django.urls import path
from .views import (HomePagesViews,
                    AboutPagesViews,
                    MessagePagesViews,
                    # NewMessagePagesViews,
                    FoydalanuvchiPagesViews,
                    JournalMessagePagesViews,
                    # edit_article,
                    delete_article,
                    send_message,
                    my_articles_view
                    )

urlpatterns = [
	path('',HomePagesViews.as_view(),name='home'),
    path('about/',AboutPagesViews.as_view(),name='about'),
    path('message/',MessagePagesViews.as_view(),name='message'),
    # path('newmessage/',NewMessagePagesViews.as_view(),name='newMessage'),
    # path('journalMessage/',JournalMessagePagesViews.as_view(),name='journalMessage'),
    path('foydalanuvchilar/',FoydalanuvchiPagesViews.as_view(),name='foydalanuvchilar'),
    
    # path('edit_article/<int:pk>/', edit_article, name='edit_article'),
    path('delete_article/<int:pk>/', delete_article, name='delete_article'),
    path('send_message/<int:pk>/', send_message, name='send_message'),
    path('my-articles/', my_articles_view, name='my_articles'),
    
]