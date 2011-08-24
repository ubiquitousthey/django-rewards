from django.conf.urls.defaults import patterns
from satchmo_store.shop.satchmo_settings import get_satchmo_setting
import payment.views
import views
ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = patterns('',
    (r'^$', views.one_step, {'SSL': ssl}, 'REWARD_POINTS_satchmo_checkout-step2'),
    (r'^success/$', views.success, {'SSL': ssl, 'template':'shop/checkout/rewards_points/success.html'}, 'REWARD_POINTS_satchmo_checkout-success'),
    (r'^failure/$', views.failure, {'SSL': ssl, 'template':'shop/checkout/rewards_points/failure.html'}, 'REWARD_POINTS_satchmo_checkout-success'),
)