import random
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone

from .models import Category, Budget, Transaction, UserProfile
from .forms import CategoryForm, BudgetForm, TransactionForm, SignupForm, OTPForm, LoginForm, UserProfileUpdateForm

def profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.save()
            user_profile.age = form.cleaned_data['age']
            user_profile.city = form.cleaned_data['city']
            user_profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('q18_profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'age': user_profile.age,
            'city': user_profile.city,
        }
        form = UserProfileUpdateForm(initial=initial_data)
    return render(request, 'profile.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Store signup data in session
            request.session['signup_data'] = form.cleaned_data
            request.session['otp'] = otp
            
            # Send Email
            try:
                send_mail(
                    'Your Studio OTP Verification Code',
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )
                return redirect('q18_verify_otp')
            except Exception as e:
                messages.error(request, f"Failed to send email. Please check your SMTP settings. Error: {str(e)}")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def verify_otp_view(request):
    if 'signup_data' not in request.session or 'otp' not in request.session:
        return redirect('q18_signup')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == request.session['otp']:
                data = request.session['signup_data']
                
                # Check if user already exists
                if User.objects.filter(username=data['email']).exists() or User.objects.filter(email=data['email']).exists():
                    messages.error(request, "A user with this email already exists.")
                    return redirect('q18_signup')
                
                # Create user
                user = User.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name']
                )
                
                # Create UserProfile
                UserProfile.objects.create(
                    user=user,
                    age=data['age'],
                    city=data['city']
                )
                
                # Clear session data
                del request.session['signup_data']
                del request.session['otp']
                
                # Auto-login the user after successful registration
                login(request, user)
                return redirect('q18_dashboard')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate typically uses username, which we set as the email
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('q18_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('q18_login')

@login_required(login_url='q18_login')
def dashboard_view(request):
    # Get period from request or default to current month
    now = timezone.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))
    
    # Calculate previous and next month for navigation
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    # Selected Month Statistics
    transactions = Transaction.objects.filter(date__month=month, date__year=year).order_by('-date')
    recent_transactions = transactions[:5]
    
    selected_income = Transaction.objects.filter(type='Income', date__month=month, date__year=year).aggregate(Sum('amount'))['amount__sum'] or 0
    selected_expenses = Transaction.objects.filter(type='Expense', date__month=month, date__year=year).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # All-time Net Worth (Cumulative)
    all_income = Transaction.objects.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    all_expenses = Transaction.objects.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_balance = all_income - all_expenses
    
    # Category summary for the selected month
    categories = Category.objects.annotate(
        total_spent=Sum('transaction__amount', filter=Q(
            transaction__type='Expense', 
            transaction__date__month=month, 
            transaction__date__year=year
        ))
    ).filter(total_spent__gt=0)
    
    context = {
        'recent_transactions': recent_transactions,
        'selected_income': selected_income,
        'selected_expenses': selected_expenses,
        'total_balance': total_balance,
        'categories_summary': categories,
        'current_month_name': calendar.month_name[month],
        'current_month': month,
        'current_year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'is_current_period': (month == now.month and year == now.year)
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='q18_login')
def transaction_list_view(request):
    now = timezone.now()
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    # Filter by month/year if provided
    if month and year:
        transactions = Transaction.objects.filter(date__month=month, date__year=year).order_by('-date')
        period_name = f"{calendar.month_name[int(month)]} {year}"
    else:
        transactions = Transaction.objects.all().order_by('-date')
        period_name = "All Time"

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('q18_transactions')
    else:
        # Pre-fill type if provided in GET
        initial_type = request.GET.get('type', 'Expense')
        form = TransactionForm(initial={'type': initial_type})
    return render(request, 'transactions.html', {
        'transactions': transactions, 
        'form': form,
        'period_name': period_name
    })

@login_required(login_url='q18_login')
def category_list_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('q18_categories')
    else:
        form = CategoryForm()
    
    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'categories.html', context)

@login_required(login_url='q18_login')
def budget_list_view(request):
    budgets = Budget.objects.all()
    budget_data = []
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    for budget in budgets:
        spent = Transaction.objects.filter(
            category=budget.category, 
            type='Expense',
            date__month=current_month,
            date__year=current_year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        percentage = min(int((spent / budget.amount_limit) * 100) if budget.amount_limit > 0 else 100, 100)
        budget_data.append({
            'budget': budget,
            'spent': spent,
            'percentage': percentage,
            'is_exceeded': percentage >= 100,
            'is_warning': percentage >= 85 and percentage < 100
        })
        
    if request.method == 'POST':
        category_id = request.POST.get('category')
        instance = Budget.objects.filter(category_id=category_id).first()
        form = BudgetForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Budget limit updated successfully.")
            return redirect('q18_budgets')
    else:
        form = BudgetForm()
        
    context = {
        'budget_data': budget_data,
        'form': form,
        'total_budget': sum(b.amount_limit for b in budgets),
        'total_spent': sum(d['spent'] for d in budget_data),
    }
    return render(request, 'budgets.html', context)

@login_required(login_url='q18_login')
def reports_view(request):
    now = timezone.now()
    current_month = int(request.GET.get('month', now.month))
    current_year = int(request.GET.get('year', now.year))

    # 1. Monthly Summary (For Selected Period)
    total_income = Transaction.objects.filter(
        type='Income', 
        date__month=current_month, 
        date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = Transaction.objects.filter(
        type='Expense', 
        date__month=current_month, 
        date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    savings = total_income - total_expenses
    savings_rate = (savings / total_income * 100) if total_income > 0 else 0

    # 2. Category Breakdown (Expenses)
    category_expenses = Category.objects.filter(type='Expense').annotate(
        amount=Sum('transaction__amount', filter=Q(
            transaction__type='Expense',
            transaction__date__month=current_month,
            transaction__date__year=current_year
        ))
    ).filter(amount__gt=0).order_by('-amount')

    categories_list = []
    for cat in category_expenses:
        percentage = (cat.amount / total_expenses * 100) if total_expenses > 0 else 0
        categories_list.append({
            'name': cat.name,
            'amount': cat.amount,
            'percentage': round(percentage, 1),
            'icon': cat.icon,
            'color': cat.color_class
        })

    # 3. Monthly Trends (Last 6 Months)
    trends = []
    for i in range(5, -1, -1):
        # Calculate date for each of the last 6 months
        # A simple way to get month/year for the last 6 months
        target_month = current_month - i
        target_year = current_year
        while target_month <= 0:
            target_month += 12
            target_year -= 1
        
        m_inc = Transaction.objects.filter(type='Income', date__month=target_month, date__year=target_year).aggregate(Sum('amount'))['amount__sum'] or 0
        m_exp = Transaction.objects.filter(type='Expense', date__month=target_month, date__year=target_year).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Max height for bars is 100px. Scaling factor based on a reasonable max (e.g., 5000)
        scale = 50
        trends.append({
            'month': calendar.month_name[target_month][:3],
            'income': m_inc,
            'expense': m_exp,
            'income_h': min(int(m_inc / scale), 100) if m_inc > 0 else 2,
            'expense_h': min(int(m_exp / scale), 100) if m_exp > 0 else 2
        })

    # Calculate previous and next month for navigation
    prev_month = current_month - 1 if current_month > 1 else 12
    prev_year = current_year if current_month > 1 else current_year - 1
    next_month = current_month + 1 if current_month < 12 else 1
    next_year = current_year if current_month < 12 else current_year + 1

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'savings_rate': round(savings_rate, 1),
        'category_expenses': categories_list,
        'trends': trends,
        'top_category': categories_list[0] if categories_list else None,
        'current_month_name': calendar.month_name[current_month],
        'current_month': current_month,
        'current_year': current_year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'is_current_period': (current_month == now.month and current_year == now.year)
    }
    return render(request, 'reports.html', context)

@login_required(login_url='q18_login')
def delete_transaction_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction deleted successfully.")
    return redirect('q18_transactions')

@login_required(login_url='q18_login')
def delete_category_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
    return redirect('q18_categories')

@login_required(login_url='q18_login')
def delete_budget_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        category_name = budget.category.name
        budget.delete()
        messages.success(request, f"Budget for {category_name} removed successfully.")
    return redirect('q18_budgets')
