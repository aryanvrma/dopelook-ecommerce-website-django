from django import forms
from .models import Order , refund_requested


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']

class RefundForm(forms.ModelForm):
    class Meta:
        model = refund_requested
        fields = ['order_number' , 'email' , 'image' , 'reason' , 'Account_Number']