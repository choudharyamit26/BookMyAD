from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views

app_name = 'src'
urlpatterns = [
    path('', views.SearchAdView.as_view(), name='ad'),
    path('package-detail/<int:pk>/', views.PackageDetails.as_view(), name='package-detail'),
    path('add-to-cart/<int:pk>/', views.AddToCart.as_view(), name='add-to-cart'),
    path('ajax/load_publications/', views.load_publications, name='ajax_load_publications'),
    path('ajax/load_adtype/', views.load_adtype, name='ajax_load_adtype')
    # path('', views.SearchAdView.as_view(), name='person_changelist'),
    # path('add/', views.PersonCreateView.as_view(), name='person_add'),
    # path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),
    #  # <-- this one here
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)