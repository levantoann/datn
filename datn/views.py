from django.shortcuts import render
from store.models import Product, ReviewRating, ProductViewByUser, recommendation_by_user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    print("login id user: ", request.user.id)
    list_products = []
    list_p = recommendation_by_user.objects.filter(user_id=request.user.id).exists()
    print("check: ", list_p)

    if request.user.id is None or list_p is False:
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')

        # Phân trang
        paginator = Paginator(products, 12)  # Chia mỗi trang thành 8 sản phẩm
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

        context = {
            'products': products,
            'reviews': reviews,
        }
    else:
        tmp_recomendation_user = recommendation_by_user.objects.get(user_id=request.user.id)
        array_list_product_id = tmp_recomendation_user.product_id_list.split(" ")

        for item in array_list_product_id:
            one_product = Product.objects.get(id=item)
            list_products.append(one_product)

        # Phân trang
        paginator = Paginator(list_products, 12)  # Chia mỗi trang thành 8 sản phẩm
        page = request.GET.get('page')

        try:
            list_products = paginator.page(page)
        except PageNotAnInteger:
            list_products = paginator.page(1)
        except EmptyPage:
            list_products = paginator.page(paginator.num_pages)

        for product in list_products:
            reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

        context = {
            'products': list_products,
            'reviews': reviews,
        }

    return render(request, 'home.html', context)