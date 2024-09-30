import calendar
import csv

from django.shortcuts import render, redirect,get_list_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import logout,authenticate,login
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import User

from admin_soft.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm

from .forms import (PhoneNumberForm,
                    FullReviewForm,SimpleReviewForm ,ManualForm,
                    PurposeForm, DepartmentForm,
                    )
from .models import *
from datetime import timedelta,date,datetime


def index(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
        
            return HttpResponseRedirect('') 
    else:
        form = PhoneNumberForm()

    return render(request, 'pages/index.html',{
        'form': form,  # Pass the form to the template
        'segment': 'billing',
    })

def see_qr(request):

    return render(request, 'pages/qr.html', )

def submit_review(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', None)

        if not phone_number:
            # If phone number is not provided, render the phone number form
            form = PhoneNumberForm()
            return render(request, 'pages/phone_number.html', {'form': form})

        # Check if the phone number already exists
        existing_reviews = Review.objects.filter(phone_number=phone_number)

        if existing_reviews.exists():
            # Redirect to the simple review form for updating/adding a new review
            return redirect('simple-review', phone_number=phone_number)
        else:

            # Collect full info if no review exists
            form = FullReviewForm(request.POST)
            if form.is_valid():
                # Save new user and review
                Review.objects.create(
                    name=form.cleaned_data['name'],
                    phone_number=form.cleaned_data['phone_number'],
                    email=form.cleaned_data['email'],
                    organization_name=form.cleaned_data.get('organization_name'),  # New organization name field
                    department=form.cleaned_data['department'],  
                    purpose=form.cleaned_data['purpose'], 
                    review=form.cleaned_data['purpose_of_visit'],
                    created_at=timezone.now()
                )
                return redirect('thankyou')
            else:
                # Render the full review formssss with errors
                return render(request, 'pages/submit-review.html', {'form': form, 'phone_number': phone_number})
    else:
        # Display phone number entry form
        form = PhoneNumberForm()
        return render(request, 'pages/phone_number.html', {'form': form})

def simple_review(request, phone_number):
    # Fetch the existing reviews with the given phone number
    existing_reviews = get_list_or_404(Review, phone_number=phone_number)
    
    if request.method == 'POST':
        form = SimpleReviewForm(request.POST)
        if form.is_valid():
            try:
                # Create a new review instance with the same phone number
                new_review = form.save(commit=False)
                new_review.phone_number = phone_number  # Keep the same phone number
                new_review.pk = None  # Ensure a new instance is created
                # If created_at is not set, assign the current time
                if not new_review.created_at:
                    new_review.created_at = timezone.now()
                new_review.save()
                return redirect('thankyou')
            except IntegrityError:
                form.add_error(None, "A review with this phone number already exists.")
    else:
        # Initialize the form with existing review data (use data from the first review)
        first_review = existing_reviews[0]
        form = SimpleReviewForm(initial={
            'name': first_review.name,
            'phone_number': first_review.phone_number,
            'email': first_review.email,
            'organization_name': first_review.organization_name,  # Include organization name
            'department': first_review.department,
            'purpose': first_review.purpose,
            'other_purpose': first_review.other_purpose,
            'review': first_review.review,

        })
    
    return render(request, 'pages/simple_review.html', {'form': form, 'existing_reviews': existing_reviews})
@login_required
def manual_entry(request):
    if request.method == 'POST':
        form = ManualForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')  
    else:
        form = ManualForm()
    
    return render(request, 'pages/manual_entry.html', {'form': form})

@login_required
def dashboard(request):
    today = date.today()
    
    # Calculate total visitors
    total_visitors_all_time = Review.objects.count()
    total_visitors_today = Review.objects.filter(created_at__date=today).count()
    total_visitors_this_month = Review.objects.filter(created_at__year=today.year, created_at__month=today.month).count()
    total_visitors_this_year = Review.objects.filter(created_at__year=today.year).count()
    
    # Calculate visitors for this month and last month
    current_month = today.month
    current_year = today.year
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1
    
    visitors_this_month = Review.objects.filter(created_at__year=current_year, created_at__month=current_month).count()
    visitors_last_month = Review.objects.filter(created_at__year=last_month_year, created_at__month=last_month).count()
    
    # Prepare data for charts
    departments = Department.objects.all()
    department_counts = Review.objects.values('department__name').annotate(count=Count('id')).order_by('department__name')
    
    purposes = Purpose.objects.all()
    purpose_counts = Review.objects.values('purpose__name').annotate(count=Count('id')).order_by('purpose__name')
    
    # Prepare data for charts
    month_data = {
        'labels': ['This Month', 'Last Month'],
        'data': [visitors_this_month, visitors_last_month]
    }
    
    context = {
        'total_visitors_all_time': total_visitors_all_time,
        'total_visitors_today': total_visitors_today,
        'total_visitors_this_month': total_visitors_this_month,
        'total_visitors_this_year': total_visitors_this_year,
        'department_counts': department_counts,
        'purpose_counts': purpose_counts,
        'month_data': month_data,
    }
    
    return render(request, 'pages/dashboard.html', context)


def thank_you_view(request):
    return render(request, 'pages/thankyou.html')
def thanks(request):
    return render(request, 'pages/thanks.html')
@login_required
def visitor_statistics(request):
    # Fetching query parameters
    filter_type = request.GET.get('filter', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page_number = request.GET.get('page_filtered', 1)
    
    # Filter reviews based on date range
    reviews = Review.objects.all()

    # Date filtering logic
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            reviews = reviews.filter(created_at__date__gte=start_date)
        except ValueError:
            start_date = None

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            reviews = reviews.filter(created_at__date__lte=end_date)
        except ValueError:
            end_date = None

    # Apply predefined filters for today, this month, this year
    if filter_type == 'today':
        today = date.today()
        reviews = reviews.filter(created_at__date=today)
    elif filter_type == 'this_month':
        today = date.today()
        reviews = reviews.filter(created_at__year=today.year, created_at__month=today.month)
    elif filter_type == 'this_year':
        today = date.today()
        reviews = reviews.filter(created_at__year=today.year)

    # Pagination
    paginator = Paginator(reviews, 10)  # Show 10 reviews per page
    reviews_filtered = paginator.get_page(page_number)

    # Total visitors for today, all time, this month, and this year
    total_visitors_today = Review.objects.filter(created_at__date=date.today()).count()
    total_visitors_all_time = Review.objects.count()

    # Calculate total visitors this month and this year
    today = date.today()
    total_visitors_this_month = Review.objects.filter(created_at__year=today.year, created_at__month=today.month).count()
    total_visitors_this_year = Review.objects.filter(created_at__year=today.year).count()

    context = {
        'reviews_filtered': reviews_filtered,
        'total_visitors_today': total_visitors_today,
        'total_visitors_all_time': total_visitors_all_time,
        'total_visitors_this_month': total_visitors_this_month,
        'total_visitors_this_year': total_visitors_this_year,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'pages/visitor_statistics.html', context)



@login_required
def export_visitor_statistics_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitor_statistics.csv"'

    writer = csv.writer(response)
    # Updated CSV header to include 'Organization Name'
    writer.writerow(['Name', 'Email', 'Phone Number', 'Organization', 'Department', 'Purpose', 'Review', 'Created At'])

    reviews = Review.objects.all()
    for review in reviews:
        writer.writerow([
            review.name,
            review.email,
            review.phone_number,
            review.organization_name if review.organization_name else 'N/A',  # Get organization name
            review.department.name if review.department else 'N/A',  # Get department name
            review.purpose.name if review.purpose else 'N/A',  # Get purpose name
            review.review,
            review.created_at.strftime('%Y-%m-%d %H:%M:%S') if review.created_at else 'N/A',  # Handle null created_at
        ])

    return response
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitor_statistics.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone Number', 'Department', 'Purpose', 'Review', 'Created At'])

    reviews = Review.objects.all()
    for review in reviews:
        writer.writerow([
            review.name,
            review.email,
            review.phone_number,
            review.organization_name if review.organization_name else 'N/A',  # Get organization name
            review.department.name if review.department else 'N/A',  # Get department name
            review.purpose.name if review.purpose else 'N/A',  # Get purpose name
            review.review,
            review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    return response

# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm
  def get_success_url(self):
        return reverse_lazy('dashboard') 
  

@login_required
def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            try:
                user = User.objects.create_user(username=username, password=password)
                messages.success(request, 'User created successfully.')
                return redirect('add_user')  
            except IntegrityError:
                messages.error(request, 'User with this username already exists.')
            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')
        else:
            messages.error(request, 'Username and password are required.')
    users = User.objects.all()  # Fetch the list of users to display
    return render(request, 'pages/add_user.html', {'users': users})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('add_user')  # Redirect to the page where users are listed


# def register(request):
#   if request.method == 'POST':
#     form = RegistrationForm(request.POST)
#     if form.is_valid():
#       form.save()
#       print('Account created successfully!')
#       return redirect('/accounts/login/')
#     else:
#       print("Register failed!")
#   else:
#     form = RegistrationForm()

#   context = { 'form': form }
#   return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm


@login_required
def add_department (request):
    if request.method == 'POST':
        department_name = request.POST.get('name')
        if department_name:
            Department.objects.create(name=department_name)
            return redirect('add_department')
    departments = Department.objects.all()
    return render(request, 'pages/add_department.html', { 'departments': departments })

@login_required
def edit_department(request, id):
    department = get_object_or_404(Department, id=id)

    if request.method == 'POST':
        department_name = request.POST.get('name')
        if department_name:
            department.name = department_name
            department.save()
        return redirect('add_department')  # Redirect back to the department list after saving

    return render(request, 'pages/edit_department.html', {'department': department})


@login_required
def delete_department(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == 'POST':  # Handle form submission for delete
        department.delete()
        return redirect('add_department')
    
    # After deleting, ensure we always render the updated list
    departments = Department.objects.all()
    return render(request, 'pages/add_department.html', {'departments': departments})

@login_required
def add_purpose(request):
    if request.method == 'POST':
        purpose_name = request.POST.get('name')
        if purpose_name:
            Purpose.objects.create(name=purpose_name)  # Use Purpose, not Department
            return redirect('add_purpose')
    
    purposes = Purpose.objects.all()  # Retrieve all purposes
    return render(request, 'pages/add_purpose.html', { 'purposes': purposes })  # Correct template

@login_required
def edit_purpose(request, id):
    purpose = get_object_or_404(Purpose, id=id)  # Fetch the specific Purpose object

    if request.method == 'POST':
        purpose_name = request.POST.get('name')
        if purpose_name:
            purpose.name = purpose_name
            purpose.save()
        return redirect('add_purpose')  # Redirect back to the list of purposes

    return render(request, 'pages/edit_purpose.html', {'purpose': purpose})

@login_required
def delete_purpose(request, id):
    purpose = get_object_or_404(Purpose, id=id)
    if request.method == 'POST':  # Handle form submission for delete
        purpose.delete()
        return redirect('add_purpose')
    
    # After deleting, ensure we always render the updated list
    purposes = Purpose.objects.all()
    return render(request, 'pages/add_purpose.html', {'purposes': purposes})