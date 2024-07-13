from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
from django.conf import settings
import requests
import json
import datetime
from django.contrib import messages


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order, 'form': self.form_class})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)


# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
# CallbackURL = 'http://127.0.0.1:8000/order/verify/'
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id
        }
        # data = {
        #     "MerchantID": settings.MERCHANT,
        #     "Amount": order.get_total_price(),
        #     "Description": description,
        #     "Phone": request.user.phone_number,
        #     "CallbackURL": CallbackURL,
        # }
        # data = json.dumps(data)
        # headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        # try:
        #     response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        #
        #     if response.status_code == 200:
        #         response = response.json()
        #         if response['Status'] == 100:
        #             return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
        #                     'authority': response['Authority']}
        #         else:
        #             return {'status': False, 'code': str(response['Status'])}
        #     return response
        #
        # except requests.exceptions.Timeout:
        #     return {'status': False, 'code': 'timeout'}
        # except requests.exceptions.ConnectionError:
        #     return {'status': False, 'code': 'connection error'}


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        # data = {
        #     "MerchantID": settings.MERCHANT,
        #     "Amount": order.get_total_price(),
        #     "Authority": request.GET['Authority'],
        # }
        # data = json.dumps(data)
        # # set content length by data
        # headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        # response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        #
        # if response.status_code == 200:
        #     response = response.json()
        #     if response['Status'] == 100:
        #         return {'status': True, 'RefID': response['RefID']}
        #     else:
        #         return {'status': False, 'code': str(response['Status'])}
        # return response


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'Coupon does not exist', 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('orders:order_detail', order.id)
