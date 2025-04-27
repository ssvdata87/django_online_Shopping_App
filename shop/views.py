from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .models import Category
from shop.form import CustomUserForm
from shop.form import ShippingAddressForm
from django.shortcuts import render, redirect
from .models import Cart, Order, OrderDetails
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})



def orders(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)

        if request.method == 'POST':
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                # Process the form data and associate it with the user's cart
                shipping_address = form.save(commit=False)
                shipping_address.user = request.user
                shipping_address.save()

                # Create an order
                order = Order.objects.create(
                    total_amount=0,  # You'll update this later
                    user=request.user
                )

                # Iterate through cart items and create OrderDetails
                total_amount = 0
                for cart_item in cart:
                    order_detail = OrderDetails.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.product_qty,
                        unit_price=cart_item.product.selling_price
                    )
                    total_amount += order_detail.subtotal  # Update total amount

                # Update total amount in the order
                order.total_amount = total_amount
                order.save()

                # Optionally, you may want to clear the user's cart after creating the order
                cart.delete()

                # Redirect to a success page or do something else
                return render(request, "shop/order_success.html", {"order": order})

        else:
            form = ShippingAddressForm()

        return render(request, "shop/orders.html", {"cart": cart, "form": form})
    else:
        return redirect("/")




    

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:    
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
              
                return redirect("/")
            else:
              
                return redirect("/login")

        return render(request,"shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged out Successfully')
    return redirect("/")
 
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Success You can Login Now..!')
            return redirect('/login')
    return render(request,"shop/register.html",{"form":form})

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category":category})

def collectionsview(request,name):
  if(Category.objects.filter(name=name,status=0)):
      products=Product.objects.filter(category__name=name)
      return render(request,"shop/products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html", {"cart":cart})
    else:
        return redirect("/")

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=(data['pid'])
            product_status=Product.objects.get(id=product_id)
            if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Favorite'}, status=200)
            else:
                Favourite.objects.create(user=request.user,product_id=product_id)
                return JsonResponse({'status':'Product Added to Favorite'}, status=200)
            
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)

    else:
        return JsonResponse({'status':'invalid-Access'}, status=200)

def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    user=request.user
    return render(request,"shop/fav.html",{"fav":fav,"user":user})
  else:
    return redirect("/")


def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
# ------------------------------update cart quantity----------------------------------------------
def update_cart_quantity(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        new_quantity = data.get('new_quantity')

        cart_item = get_object_or_404(Cart, id=item_id)
        cart_item.product_qty = new_quantity
        cart_item.save()

        # You can return additional data in the response if needed
        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=(data['product_qty'])
            product_id=(data['pid'])
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product=product_id):
                    return JsonResponse({'status':'Product Already in cart'}, status=200)
                else:
                    if product_status.quentity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to cart Successfully'}, status=200)
                    else:
                        return JsonResponse({'status':'Product Stock not Available'}, status=200)       
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)

    else:
        return JsonResponse({'status':'invalid-Access'}, status=200)

    

def ball(request):
    return render(request,"shop/ball.html")

def gallery(request):
    return render(request,"shop/g.html")

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            dproduct=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"dproduct":dproduct})
        
        else:
            messages.error(request,"No Such Product Found")
            return redirect('collections')


    else:
        messages.error(request,"No Such Category Found")
        return redirect('collections')

