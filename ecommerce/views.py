from django.shortcuts import render

# Create your views here # Assuming these models are in the "catalog" app

from django.shortcuts import render
from .models import Product,Brand , Category,Cart 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render




def product_list(request):
    # Retrieve all products from the database
   

    # Pass the products to the template context
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    # Pass the products to the template context
    context = {'products': products,'brands':brands,'categories':categories}
    # Render the template with the product data
    return render(request, 'ecommerce/home.html', context)


from django.shortcuts import render
from .forms import ContactForm

from django.shortcuts import render
from .forms import ContactForm, CheckoutForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # You can add a success message or redirect to a thank-you page
            products = Product.objects.all()
            brands = Brand.objects.all()
            categories = Category.objects.all()
    # Pass the products to the template context
            context = {'products': products,'brands':brands,'categories':categories}
    # Render the template with the product data
            return render(request, 'ecommerce/home.html', context)
  # Assuming you have a 'contact_success' URL pattern
    else:
        form = ContactForm()

    return render(request, 'ecommerce/contact.html', {'form': form})




from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Product

from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Cart, Product  # Import your Cart and Product models

def recommend_products(request):
    # Assuming you have a 'cart' model with a 'products' field representing the products in the cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Get the product descriptions for products in the cart
    cart_descriptions = [product.description for product in user_cart.products.all()]

    # Get all products (excluding those in the cart)
    all_products = Product.objects.exclude(id__in=[product.id for product in user_cart.products.all()])

    # Get all product descriptions
    all_descriptions = [product.description for product in all_products]

    # Combine cart and all product descriptions
    all_descriptions.extend(cart_descriptions)

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_descriptions)

    # Calculate cosine similarity
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Get indices of products in the cart
    cart_indices = [product.id for product in user_cart.products.all()]
    print("cosine_similarities shape:", cosine_similarities.shape)
    print("cart_indices:", cart_indices)

    # Make sure the indices are within bounds
    valid_cart_indices = [index for index in cart_indices if 0 <= index < cosine_similarities.shape[0]]

    # Get similarity scores for products not in the cart
    similar_scores = cosine_similarities[valid_cart_indices, :].sum(axis=0)

    # Get indices of top N similar products
    top_n_indices = similar_scores.argsort()[::-1][:5]

    # Get the top N recommended products
    top_n_products = [all_products[int(index)] for index in top_n_indices if 0 <= index < len(all_products)]

    # Pass the recommended products to the template context
    context = {'recommended_products': top_n_products}

    return context

@login_required
def cart(request):
    # Retrieve the user's cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    recommended_context = recommend_products(request)
    recommended_products = recommended_context.get('recommended_products', [])
    # Pass the cart items to the template context
    context = {'cart_items': user_cart.products.all(), 'recommended_products':recommended_products}
    
    return render(request, 'ecommerce/cart.html', context)




# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product, Cart

def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        product.availability -= 1
        product.save()
        return JsonResponse({'message': 'Product added to cart successfully.'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found.'})
    


from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def delete_from_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)
        product.availability += 1  # Increase availability as item is removed from the cart
        product.save()
        user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Pass the cart items to the template context
        context = {'cart_items': user_cart.products.all()}

        return render(request, 'ecommerce/cart.html', context)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found.'})

from django.shortcuts import render, redirect

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            checkout_instance = form.save(commit=False)
            checkout_instance.user = request.user
            checkout_instance.save()
            return redirect('ecommerce:base')  # Redirect to a success page
    else:
        form = CheckoutForm()

    return render(request, 'ecommerce/recommendation.html', {'form': form})



