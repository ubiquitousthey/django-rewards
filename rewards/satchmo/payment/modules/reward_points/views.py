from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache
from livesettings import config_get_group
from payment.utils import pay_ship_save, get_processor_by_key
from payment.views import confirm, payship
import logging
from satchmo_store.contact.models import Contact
from satchmo_store.shop.models import Cart, Order
from satchmo_utils.dynamic import lookup_url, lookup_template
from rewards.models import Account
from satchmo_utils.views import bad_or_missing


log = logging.getLogger("rewards_points.views")

payment_config = config_get_group('PAYMENT_REWARD_POINTS')

def one_step(request):
    #First verify that the customer exists
    try:
        contact = Contact.objects.from_request(request, create=False)
    except Contact.DoesNotExist:
        url = lookup_url(payment_config, 'satchmo_checkout-step1')
        return HttpResponseRedirect(url)
    #Verify we still have items in the cart
    tempCart = Cart.objects.from_request(request)
    if tempCart.numItems == 0:
        template = lookup_template(payment_config, 'shop/checkout/empty_cart.html')
        return render_to_response(template,
                                  context_instance=RequestContext(request))

    # Create a new order
    newOrder = Order(contact=contact)
    pay_ship_save(newOrder, tempCart, contact,
        shipping="", discount="", notes="")

    request.session['orderID'] = newOrder.id

    processor = get_processor_by_key('PAYMENT_REWARD_POINTS')
    processor.prepare_data(newOrder)
    processor_result = processor.process(newOrder)

    if processor_result.success:
        tempCart.empty()
        return success(request)
    else:
        return failure(request)
one_step = never_cache(one_step)

def success(request):
    """
    The order has been succesfully processed.  This can be used to generate a receipt or some other confirmation
    """
    try:
        order = Order.objects.from_request(request)
        account = Account.objects.get(user=order.contact.user)
    except Order.DoesNotExist:
        return bad_or_missing(request, _('Your order has already been processed.'))

    del request.session['orderID']
    return render_to_response('shop/checkout/reward_points/success.html',
                              {'order': order, 'account' : account},
                              context_instance=RequestContext(request))
success = never_cache(success)

def failure(request):
    try:
        order = Order.objects.from_request(request)
        account = Account.objects.get(user=order.contact.user)
    except Order.DoesNotExist:
        return bad_or_missing(request, _('Your order has already been processed.'))


    return render_to_response(
        'shop/checkout/reward_points/failure.html',
        {'order': order, 'account' : account},
        context_instance=RequestContext(request)
    )

