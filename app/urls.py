from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    # presentation pages
    path('', index, name="index"),
    path('pricing', pricing, name="pricing"),
    path('complete', complete, name="complete"),
    path('setting', setting, name="setting"),

    # Home system
    path('home', home, name="home"),

    # system admin
    path('invoice', invoice, name="invoice"),
    path('remission', remission, name="remission"),
    path('service', service, name="service"),
    path('cotization', cotization, name="cotization"),

    # api client
    path('client', client, name="client"),
    path('client-view', client_view, name="client-view"),
    path('create-client', create_client, name="create-client"),
    path('delete-client', delete_client, name="delete-client"),
    path('update-client', update_client, name="update-client"),

    # api provider
    path('provider', provider, name="provider"),
    path('provider-view', provider_view, name="provider-view"),
    path('create-provider', create_provider, name="create-provider"),
    path('delete-provider', delete_provider, name="delete-provider"),
    path('update-provider', update_provider, name="update-provider"),

    path('product', product, name="product"),
    path('create-product', create_product, name="create-product"),
    path('delete-product', delete_product, name="delete-product"),
    path('update-product', update_product, name="update-product"),

    # auth
    path('sign-in', sign_in, name="sign-in"),
    path('sign-up', sign_up, name="sign-up"),
    path('log-out', log_out, name="log-out"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)