from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Vendor, Purchase, StockMovement
from django.contrib import messages
from decimal import Decimal
from .decorators import role_required
from django.contrib.auth import login
from .forms import RegisterForm, PurchaseForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# Registration Page


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the user   
            return redirect("login")  # Redirect to the login page after successful registration
    else:
        form = RegisterForm()
    
    return render(request, "main/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on group
            if user.groups.filter(name="General manager").exists():
                return redirect('general_manager_dashboard')  # Replace with the actual view name
            elif user.groups.filter(name="Inventory Manager").exists():
                return redirect('inventory_dashboard')  # Replace with the actual view name
            elif user.groups.filter(name="Supervisor").exists():
                return redirect('supervisor_dashboard')  # Replace with the actual view name
            else:
                messages.error(request, "User does not belong to a recognized group.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'main/login.html')  # Replace 'login.html' with your login template

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

# End Of Registration and  Login Page



# This is the Inventory managers view
@login_required
@role_required('Inventory Manager')
def inventory_dashboard(request):
    categories = Category.objects.prefetch_related('product_set').all()
    vendors = Vendor.objects.all()
    purchases = Purchase.objects.select_related('product', 'vendor').all()
    movements = StockMovement.objects.select_related('product').all()

    context = {
        'categories': categories,
        'vendors': vendors,
        'purchases': purchases,
        'movements': movements,
    }
    return render(request, 'inventory_manager/dashboard.html', context)

@login_required
@role_required('Inventory Manager')
def product_purchases(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    purchases = Purchase.objects.filter(product=product).select_related('vendor')

    stock_movements = StockMovement.objects.filter(product=product)
    
    if request.method == "POST":
        purchase_id = request.POST.get('purchase_id')
        purchase = get_object_or_404(Purchase, id=purchase_id)

        # Approve the purchase
        purchase.is_approved = True
        purchase.approved_by = request.user
        purchase.save()

        messages.success(request, "Purchase approved successfully!")
        return redirect('product_purchases', product_id=product_id)

    context = {
        'product' : product,
        'purchases' : purchases,
        'stock_movements' : stock_movements,
    }

    return render(request, 'inventory_manager/product_purchases.html', context)

@login_required
@role_required('Inventory Manager')
def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category_id')
        unit_price = Decimal(request.POST['unit_price'])  # Convert to Decimal
        stock_balance = int(request.POST['stock_balance'])
        image = request.FILES.get('image')

        # Check if all required fields are filled
        if not product_name or not category_id or not unit_price:
            messages.error(request, 'All fields are required.')
            return redirect('add_product')

        try:
            # Convert unit_price to Decimal
            unit_price = Decimal(unit_price)
            
            # Get the selected category from Category model
            category = Category.objects.get(id=category_id)

            # Save the new Product
            Product.objects.create(
                name=product_name,
                category=category,
                unit_price=unit_price,
                stock_balance=stock_balance,
                image=image,
            )

            messages.success(request, 'Product added successfully.')
            return redirect('success')

        except Category.DoesNotExist:
            messages.error(request, 'Selected category does not exist.')
            return redirect('add_product')
        except ValueError:
            messages.error(request, 'Unit price must be a valid number.')
            return redirect('add_product')

    # Get all categories to display on the frontend
    categories = Category.objects.all()
    return render(request, 'inventory_manager/add_product.html', {'categories': categories})


@login_required
@role_required('Inventory Manager')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        unit_price = request.POST.get('unit_price', product.unit_price)
        stock_increment = request.POST.get('stock_increment', 0)

        try:
            # Ensure correct data types
            unit_price = Decimal(unit_price)  # Convert to Decimal
            stock_increment = int(stock_increment)  # Convert to int

            # Update the product's unit price and stock balance
            product.unit_price = unit_price
            product.stock_balance += stock_increment  # Add to the stock balance
            product.save()

            messages.success(request, "Product updated successfully!")
            return redirect('inventory_dashboard')  # Redirect to your dashboard or product list

        except (ValueError, TypeError) as e:
            messages.error(request, "Invalid input for price or stock increment.")
            return redirect('edit_product', product_id=product.id)

    return render(request, 'inventory_manager/edit_product.html', {'product': product})


@login_required
@role_required('Inventory Manager')
def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')

        # Ensure category name is provided
        if not category_name:
            messages.error(request, 'Category name is required.')
            return redirect('add_category')

        # Save the new Category
        Category.objects.create(name=category_name)
        messages.success(request, 'Category added successfully.')
        return redirect('success')
    
    return render(request, 'inventory_manager/add_category.html')


@login_required
@role_required('Inventory Manager')
def success(request):
    return render(request, 'inventory_manager/success.html')


@login_required
@role_required('Inventory Manager')
def add_stock_movement(request):
    if request.method == "POST":
        product_id = request.POST['product']
        quantity_issued = int(request.POST.get('quantity_issued', 0))
        quantity_returned = int(request.POST.get('quantity_returned', 0))
        location_received = request.POST['location_received']

        # Fetch the product instance
        product = Product.objects.get(id=product_id)

        # Create the stock movement record
        StockMovement.objects.create(
            product=product,
            quantity_issued=quantity_issued,
            quantity_returned=quantity_returned,
            location_received=location_received
        )

        messages.success(request, "Stock movement added successfully!")
        return redirect('add_stock_movement')
    
    product_id = request.GET.get('product', None)
    products = Product.objects.all()
    selected_product = Product.objects.get(id=product_id) if product_id else None

    products = Product.objects.all()
    return render(request, 'inventory_manager/add_stock_movement.html', {'products': products, 'selected_product': selected_product,})
# End of Inventory Managers View

# Supervisor  View

@login_required
@role_required('Supervisor')
def supervisor_dashboard(request):
    # Fetch all products
    categories = Category.objects.prefetch_related('product_set').all()

    # Filter purchases by approval status and supervisor
    pending_requests = Purchase.objects.filter(supervisor=request.user, is_approved=False)
    approved_requests = Purchase.objects.filter(supervisor=request.user, is_approved=True)


    


    context = {
        'categories': categories,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        }


    return render(request, 'supervisor/dashboard.html', context)


def request_purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product by ID
    vendors = Vendor.objects.all()  # Get all vendors
    
    if request.method == "POST":
        # Create a purchase request from the form data
        quantity_received = int(request.POST.get('quantity_received'))
        vendor_id = request.POST.get('vendor')

        # Create the Purchase object
        purchase = Purchase(
            product=product,  # Associate the product with the purchase
            supervisor=request.user,  # Associate the logged-in supervisor
            vendor_id=vendor_id,  # Get the selected vendor
            quantity_received=quantity_received,  # Set the received quantity
            is_approved=False  # Set approval status to false by default
        )
        
        purchase.save()  # Save the purchase request
        messages.success(request, "Purchase request submitted successfully!")
        return redirect('supervisor_dashboard')  # Redirect to the supervisor page or desired page

    # For GET request, create an empty form context
    form = PurchaseForm()  # Initialize an empty form

    context = {
        'form': form,
        'product': product,
        'vendors': vendors,  # Pass the list of vendors to the context
    }
    return render(request, 'supervisor/request_purchase.html', context)



# End of Supervisor Views



def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')





def manager_dashboard(request):
    return render(request, 'dashboard/manager_dashboard.html')