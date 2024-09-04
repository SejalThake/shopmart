from django.shortcuts import render,redirect
from seller.models import Category
from django.contrib.auth.models import User
from seller.models import Product

# Create your views here.
def dashboard(request):
    if(request.user.is_authenticated):
        return render(request,'seller/dashboard.html')
    else:
        return redirect("/")
    
def add_category(request):
    data={}
    categories = Category.objects.filter(seller_id=request.user.id)
    data['categories'] = categories
    if(request.method == 'POST'):
        category = request.POST.get('category')
        if(category==""):
            data["error_msg"]="Please give category name"
        elif(Category.objects.filter(name=category).exists()):
            data["error_msg"]=category+" is already exists"
        else:
            seller=User.objects.get(id=request.user.id)
            c=Category.objects.create(name=category,seller_id=seller)
            c.save()
            return redirect('/seller/categories/')
    return render(request,'seller/add_category.html',context=data)

def delete_category (request,category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    return redirect("/seller/categories/")


def add_product(request,category_id):
    data = {}
    category = Category.objects.get(id=category_id)
    data['category_name'] = category.name
    if(request.method == 'POST'):
        pname = request.POST.get("name")
        pprice = request.POST.get("price")
        pdiscription = request.POST.get("description")
        pquantity = request.POST.get("quantity")
        pimage = request.FILES.get("image")
        pis_available ="is_available" in request.POST
        # print(pname,pprice,pdiscription,pquantity,pimage,pis_available)
        seller = User.objects.get(id=request.user.id)

        product = Product.objects.create(name=pname,price=pprice,description=pdiscription,quantity=pquantity,is_active=pis_available,image=pimage,seller_id=seller,category_id=category)
        product.save()
        return redirect("/")
    
    return render (request,'seller/add_product.html',context=data)

def view_products(request):
    data={}
    products=Product.objects.filter(seller_id=request.user.id)
    # for product in products:
    #     print(product.name)
    #     return redirect("/")
    data['products']=products
    data['total_products'] = products.count()
    return render(request,'seller/products.html',context=data)

def delete_product (request,product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect("/seller/products/")

def update_product(request,product_id):
   data={}
   products=Product.objects.filter(id=product_id)
   data['product']=products[0]
   if(request.method=="POST"):
      pname=request.POST.get("name")
      pprice=request.POST.get("price")
      pdescription=request.POST.get("description")
      pquantity=request.POST.get("quantity")
      pimage=request.FILES.get("image")
      pis_available="is_available" in request.POST
     
      products.update(name=pname,price=pprice,description=pdescription,quantity=pquantity,is_active=pis_available)
     
      product=Product.objects.get(id=product_id)
      from seller.forms import ImageForm
      import os
      form=ImageForm(request.POST, request.FILES,instance=product)
      if form.is_valid():
         image_path=product.image.path
         if(os.path.exists(image_path)):
            os.remove(image_path)
         form.save()

      return redirect("/seller/products")
   return render(request,'seller/update_product.html',context=data)
