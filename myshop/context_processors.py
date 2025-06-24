from .models import CartItem, Category

def cart_item_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_item_count': count}

def category_nav(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    return {'parent_categories': parent_categories}


# from django.db.models import Sum

# def cart_item_count(request):
#     if request.user.is_authenticated:
#         count = CartItem.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum'] or 0
#     else:
#         count = 0
#     return {'cart_item_count': count}
