from eco_et.settings import BASE_URL, X_Api_Token
from django.shortcuts import render, redirect
from main.api_client import APIClient

api_client = APIClient(base_url=BASE_URL, token=X_Api_Token)


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('_id')
        title = request.POST.get('title')
        price = float(request.POST.get('sale_cost'))
        photo = request.POST.get('photo', '')
        category_id = request.POST.get('category_id')
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', [])

        existing = next((item for item in cart if item['_id'] == product_id), None)

        if existing:
            existing['quantity'] += quantity
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
        return redirect('index')
    else:
        return redirect('index')


def index_handler(request):
    categories = api_client.get_categories()

    products = api_client.get_products('cat:3')

    return render(
        request, 'index.html',
        {
            'categories': categories,
            'products': products,
        },
    )


def cart_handler(request):
    cart = request.session.get('cart', [])
    return render(request, 'corzina.html', {})


def details_handler(request):
    return render(request, 'details.html', {})


def that_meet_handler(request):
    return render(request, 'that_meet.html', {})


def custom_404(request):
    return render(request, '404.html', {}, status=404)

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
