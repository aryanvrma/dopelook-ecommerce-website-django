from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm, RefundForm
import datetime
from .models import Order, OrderProduct, refund_requested
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    grand_total = total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.payment = "Cash on delivery"
            data.is_ordered = True
            data.save()

            # Move the cart items to Order Product table
            cart_items = CartItem.objects.filter(user=request.user)

            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = data.id
                orderproduct.payment = True
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variation)
                orderproduct.save()
                # Reduce the quantity of the sold products
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

                # Clear cart
            CartItem.objects.filter(user=request.user).delete()
            # Send order recieved email to customer
            mail_subject = 'Thank you for your order!'
            message = render_to_string('orders/order_recieved_email.html', {
                'user': request.user,
                'order': data,
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # Send order number and transaction id back to sendData method via JsonResponse
            data = {
                'order_number': data.order_number,
            }

            order = Order.objects.get(
                user=current_user, is_ordered=True, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'order_number': order_number,
                'total': total,
                'grand_total': grand_total,
            }
            return render(request, 'orders/order_complete.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'payment': order.payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Order.DoesNotExist):
        return redirect('home')


def refund(request):
    form = RefundForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            
            order_number = form.cleaned_data.get('order_number')
            reason = form.cleaned_data.get('reason')
            email = form.cleaned_data.get('email')
            Account_Number = form.cleaned_data.get('Account_Number')
            image = form.cleaned_data.get('image')
            try:
                order = Order.objects.get(order_number=order_number)
                order.refund_request = True
                order.save()

                refund = refund_requested()
                refund.user = request.user
                refund.order_number = order_number
                refund.order = order
                refund.reason = reason
                refund.email = email
                refund.Account_Number = Account_Number
                refund.image = image
                refund.save()
                mail_subject = 'Thank you for your Return Request!'

                message = render_to_string('orders/returns_email.html', {
                    'user': request.user,
                    'order': refund,
                })
                to_email = request.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, "Return request submitted succesfully")
                return redirect('home')

            except ObjectDoesNotExist:
                messages.warning(request, "Order does not exists")
                return redirect('home')

    return render(request, 'orders/refund.html', {'form': form})
