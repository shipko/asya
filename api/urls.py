from django.conf.urls import include, url

from .methods import (
    auth as auth,
    timer as timer,
    user as user,
    quest as quest
)
from . import views

# from methods import
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^token$', auth.auth),

    url(r'^method/', include([
        url(r'^auth.signup$', auth.signup),
        url(r'^timer.get', timer.get),

        url(r'^user.list', user.list),
        url(r'^user.get', user.get),
        url(r'^user.delete', user.delete),

        url(r'^quest.list', quest.list),
        url(r'^quest.take', quest.take)

    ]))
]
