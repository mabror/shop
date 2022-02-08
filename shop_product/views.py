from django.shortcuts import render, redirect
from django.views.generic import ListView, View, UpdateView, DetailView, TemplateView, CreateView
from .models import Category, Product, Brand, CartProduct, Cart, Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import OrderForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class LandingPage(TemplateView):
    template_name = "landing.html"


class ProductView(ListView):
    model = Product
    template_name = "shop_product/product.html"
    context_object_name = 'products'
    paginate_by = 4




class ProductDetailView(LoginRequiredMixin, TemplateView):
    template_name = "shop_product/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        prod = Product.objects.get(slug=url_slug)
        prod.view_count += 1
        prod.save()
        context['product'] = prod
        return context


def categories_all(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        "products": products,
    }
    return render(request, 'shop_product/categories.html', context)


def category_by_id(request, pk):
    category_f = Product.objects.filter(category_id=pk)
    brand_all = Brand.objects.filter(category=pk)
    context = {
        'category_f': category_f,
        'brand_all': brand_all,
    }
    return render(request, 'shop_product/category.html', context)




class AddToCartView(LoginRequiredMixin,View):
    def get(self, request, pro_id):
        product_id = pro_id
        # mahsulotni olish

        product_obj = Product.objects.get(id=product_id)
    #     # Maxsulot mavjudligini tekshirish
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.selling_price,
                                                         quantity=1, subtotal=product_obj.selling_price)

                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(user=self.request.user, total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,
                                                     rate=product_obj.selling_price, subtotal=product_obj.selling_price, quantity=1)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        # messages.info(request, "This item was added to your cart.")
        return redirect('shop_product:mycart')



class MyCartView(TemplateView):
    template_name = "shop_product/cart.html"
    def get_context_data(self, **kwargs):
        context = super(MyCartView, self).get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cartt = Cart.objects.get(id=cart_id)
        else:
            cartt = None
        context['cartt'] = cartt
        return context


class ManagerCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            # messages.info(request, "This item quantity was updated.")
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            # messages.info(request, "This item was removed from your cart.")
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
            # messages.info(request, "This item was deleted from your cart.")
        return redirect('shop_product:mycart')



class AllDeleteView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
            # messages.info(request, "This items was cleaned from your cart.")
        return redirect('shop_product:mycart')


class ProductEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = "shop_product/product_edit.html"
    success_url = "/"
    fields = '__all__'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.user == self.request.user


class ChekoutView(CreateView):
    template_name = 'shop_product/chekout.html'
    form_class = OrderForm
    success_url = reverse_lazy("shop_product:myorder")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            user = self.request.user
            form.instance.user = user
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Buyurtma qabul qilindi"
            del self.request.session['cart_id']
        else:
            return redirect('shop_product:myorder')
        return super().form_valid(form)


"""
<< Delete product >>
"""
def delete_product(request, id):
    products = Product.objects.get(pk=id)
    products.delete()
    # messages.info(request, "Product ochirildi.")
    return redirect('shop_product:home_page')



def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(name_en__icontains=searched)
        context = {
            'searched': searched,
            'products': products,
        }
        
        return render(request, "shop_product/search.html", context)
    else:
        return render(request, "shop_product/search.html")



def brand_by_id(request, pk):
    brand_f = Product.objects.filter(brand_id=pk)
    
    context = {
        'brand_f': brand_f,
        
    }
    return render(request, "shop_product/brand.html", context)





class UserOrderDetaile(DetailView):
    template_name = 'shop_product/order_detail.html'
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('account:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserOrderDetaile, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


def orderview(request):
    users = request.user
    orders = Order.objects.filter(user=users)
    context = {
        "orders": orders
    }
    return render(request, 'shop_product/order.html', context)