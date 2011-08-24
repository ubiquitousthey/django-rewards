from django.utils.translation import ugettext as _
from l10n.utils import moneyfmt
from payment.modules.base import BasePaymentProcessor, ProcessorResult
from rewards.models import Account, Activity

class PaymentProcessor(BasePaymentProcessor):

    def __init__(self, settings):
        super(PaymentProcessor, self).__init__('rewards_points', settings)

    def capture_payment(self, testing=False, order=None, amount=None):
        """
        Process the transaction and return a ProcessorResponse
        """
        if not order:
            order = self.order

        payment = None
        success = False
        response_text = _("General Failure.")

        if self.order.paid_in_full:
            success = True
            reason_code = "0"
            response_text = _("No balance to pay")
            self.record_payment()

        else:
            account = None
            try:
                account = Account.objects.get(user=order.contact.user)
            except Account.DoesNotExist:
                success = False
                reason_code="1"
                response_text = _("User does not have a rewards account.")

            if account:
                if account.balance < order.balance:
                    success = False
                    reason_code="2"
                    response_text = _("Rewards balance does not cover order balance.")

                else:
                    reason_code = "0"
                    response_text = _("Success")
                    success = True
                    payment = self.record_payment(order.balance,order=order)
                    Activity.create_from_ref(order.contact.user, payment)

                    if not self.order.paid_in_full:
                        response_text = _("%s balance remains after gift certificate was applied") % moneyfmt(self.order.balance)

        return ProcessorResult(self.key, success, response_text, payment=payment)
