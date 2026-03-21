from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from paytmchecksum import PaytmChecksum
from .models import Order

def payment_form(request):
    return render(request, 'Q16/payment_form.html')

def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')

        # Generate unique order ID
        order_id = str(uuid.uuid4())[:20]

        # Create order in database
        order = Order.objects.create(
            order_id=order_id,
            amount=amount,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone
        )

        # Paytm parameters
        paytm_params = {
            "MID": settings.PAYTM_MERCHANT_ID,
            "ORDER_ID": order_id,
            "CUST_ID": customer_email,
            "TXN_AMOUNT": amount,
            "CHANNEL_ID": settings.PAYTM_CHANNEL_ID,
            "INDUSTRY_TYPE_ID": settings.PAYTM_INDUSTRY_TYPE_ID,
            "WEBSITE": settings.PAYTM_WEBSITE,
            "CALLBACK_URL": request.build_absolute_uri('/q16/callback/'),
        }

        # Generate checksum
        checksum = PaytmChecksum.generateSignature(paytm_params, settings.PAYTM_MERCHANT_KEY)

        paytm_params["CHECKSUMHASH"] = checksum

        return render(request, 'Q16/paytm_form.html', {'paytm_params': paytm_params})

    return redirect('payment_form')

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        paytm_params = {}
        checksum = None
        for key, value in request.POST.items():
            if key == 'CHECKSUMHASH':
                checksum = value
            else:
                paytm_params[key] = value

        if checksum is None:
            return render(request, 'Q16/payment_status.html', {'error': 'Checksum not found in response'})

        # Verify checksum
        is_valid_checksum = PaytmChecksum.verifySignature(paytm_params, settings.PAYTM_MERCHANT_KEY, checksum)

        if is_valid_checksum:
            order_id = paytm_params.get('ORDERID')
            txn_id = paytm_params.get('TXNID')
            status = paytm_params.get('STATUS')

            try:
                order = Order.objects.get(order_id=order_id)
                order.txn_id = txn_id
                if status == 'TXN_SUCCESS':
                    order.status = 'SUCCESS'
                else:
                    order.status = 'FAILED'
                order.save()
            except Order.DoesNotExist:
                pass

            return render(request, 'Q16/payment_status.html', {
                'order': order,
                'status': status,
                'txn_id': txn_id
            })
        else:
            return render(request, 'Q16/payment_status.html', {'error': 'Checksum verification failed'})

    return redirect('payment_form')
