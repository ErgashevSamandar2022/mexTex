from django.urls import path
from .views import (JournalPagesViews,
                    JournalCreateViews,
                    JournalEditViews,
                    JournalDeleteViews,
                    ArxivPagesViews,
                    tastiqMaqolalar_royxati
                    )

urlpatterns = [
	path('journals/',JournalPagesViews.as_view(),name='journals'),
 path('journals/create/',JournalCreateViews.as_view(),name='journal_create'),
	path('journals/<int:pk>/edit/',JournalEditViews.as_view(),name='journal_edit'),
	path('journals/<int:pk>/delete/',JournalDeleteViews.as_view(),name='journal_delete'),
 path('arxiv/', ArxivPagesViews.as_view(), name='arxiv'),
 path('tastiqMaqolalar/', tastiqMaqolalar_royxati, name='tastiqMaqolalar_royxati')
 
]
