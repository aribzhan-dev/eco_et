from django.http import JsonResponse

from eco_et.settings import BASE_URL, X_Api_Token
from django.shortcuts import render, redirect
from main.api_client import APIClient
from django.views.decorators.csrf import csrf_exempt
from main.models import Services


api_client = APIClient(base_url=BASE_URL, token=X_Api_Token)


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('_id')
        title = request.POST.get('title', '')
        price = float(request.POST.get('sale_cost') or 0)
        photo = request.POST.get('photo', '')
        category_id = request.POST.get('category_id', '')
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', [])
        existing = next((item for item in cart if item['_id'] == product_id), None)

        if existing:
            existing['quantity'] = quantity
        else:
            cart.append({
                '_id': product_id,
                'title': title,
                'sale_cost': price,
                'photo': photo,
                'category_id': category_id,
                'quantity': quantity
            })

        request.session['cart'] = cart
        return JsonResponse({'status': 'ok'})


def index_handler(request):
    categories = api_client.get_categories()
    for cat in categories:
        cat['id'] = int(cat['_id'])

    search_query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category_id', '').strip()
    category_id = int(category_id) if category_id else None

    if search_query:
        products = api_client.get_products(search_query)
    elif category_id:
        products = api_client.get_products(f'cat:{category_id}')
    else:
        products = api_client.get_products()

    for pro in products:
        pro['id'] = int(pro['_id'])
        pro['category_id'] = int(pro['category_id']) if pro.get('category_id') is not None else 0

    category_map = {cat['id']: cat['title'] for cat in categories}
    for pr in products:
        pr['category_title'] = category_map.get(pr['category_id'], '')

    products_count = len(products)

    return render(
        request, 'index.html',
        {
            'categories': [{'id': cat['id'], 'title': cat['title']} for cat in categories],
            'products': products,
            'products_count': products_count,
            'search_query': search_query,
            'category_id': category_id,
        },
    )







def cart_handler(request):
    services = Services.objects.filter(status=0)
    cart = request.session.get('cart', [])
    total_price = sum(item['sale_cost'] * item['quantity'] for item in cart)
    summ = 0

    for item in cart:
        item['sum'] = round(item['sale_cost'] * item['quantity'], 2)
        summ += item['sum']
        item['id'] = item['_id']

    return render(request, 'corzina.html',
                  {
                      'cart': cart,
                      'total_price': total_price,
                      'summ': summ,
                      'services': services,
                  }
    )




def that_meet_handler(request, category_id, blog_id):
    products = api_client.get_products(f'cat:{category_id}')
    product = next((p for p in products if str(p.get('_id')) == str(blog_id)), None)

    if not product:
        return custom_404(request)

    product['id'] = product['_id']
    categories = api_client.get_categories()
    category_map = {str(cat['_id']): cat['title'] for cat in categories}
    product['category_title'] = category_map.get(str(product['category_id']), '')

    return render(request, 'that_meet.html', {'product': product})





def custom_404(request):
    return render(request, '404.html', {}, status=404)







@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('_id')
        action = request.POST.get('action')
        cart = request.session.get('cart', [])
        updated_cart = []

        for item in cart:
            if item['_id'] == product_id:
                if action == 'increase':
                    item['quantity'] += 1
                elif action == 'decrease':
                    item['quantity'] -= 1
                    if item['quantity'] <= 0:
                        continue
                else:
                    try:
                        new_quantity = int(request.POST.get('quantity', 1))
                        item['quantity'] = max(1, new_quantity)
                    except:
                        pass
            updated_cart.append(item)

        request.session['cart'] = updated_cart
    return redirect('cart_handler')

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('_id')
        cart = request.session.get('cart', [])
        cart = [item for item in cart if item['_id'] != product_id]
        request.session['cart'] = cart
    return redirect('cart_handler')







# {% for product in products %}
#   <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
#     <h3>{{ product.title }}</h3>
#     <p>Price: {{ product.sale_cost }} KZT</p>
#
#     <form action="{% url 'add_to_cart' %}" method="POST">
#       {% csrf_token %}
#       <input type="hidden" name="_id" value="{{ product._id }}">
#       <input type="hidden" name="title" value="{{ product.title }}">
#       <input type="hidden" name="sale_cost" value="{{ product.sale_cost }}">
#       <input type="hidden" name="photo" value="{{ product.photo }}">
#       <input type="hidden" name="category_id" value="{{ product.category_id }}">
#
#        <button type="button" onclick="changeQuantity(this, -1)">-</button>
#       <input type="number" name="quantity" value="1" min="1" style="width: 50px; text-align: center;">
#       <button type="button" onclick="changeQuantity(this, 1)">+</button>
#
#       <button type="submit">Add to Cart</button>
#     </form>
#   </div>
# {% endfor %}
#
# <script>
# function changeQuantity(button, delta) {
#     const input = button.parentElement.querySelector('input[name="quantity"]');
#     let current = parseInt(input.value) || 1;
#     current += delta;
#     if (current < 1) current = 1;
#     input.value = current;
# }
# </script>
