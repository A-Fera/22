from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q, Avg
from datetime import datetime, timedelta
from .models import Accommodation, Booking
from .forms import AccommodationForm, BookingForm
from reviews.models import AccommodationReview

class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'bookings/accommodation_list.html'
    context_object_name = 'accommodations'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Accommodation.objects.filter(is_available=True).order_by('-created_at')
        search = self.request.GET.get('search')
        accommodation_type = self.request.GET.get('type')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(destination__name__icontains=search) |
                Q(address__icontains=search)
            )
        
        if accommodation_type:
            queryset = queryset.filter(accommodation_type=accommodation_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accommodation_types'] = Accommodation.ACCOMMODATION_TYPES
        return context

def accommodation_detail(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    reviews = AccommodationReview.objects.filter(
        accommodation=accommodation,
        is_approved=True
    ).order_by('-created_at')[:10]
    
    # Check if user has booked this accommodation and can review
    user_can_review = False
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_booked = Booking.objects.filter(
            accommodation=accommodation,
            user=request.user,
            booking_status='confirmed'
        ).exists()
        
        user_has_reviewed = AccommodationReview.objects.filter(
            accommodation=accommodation,
            user=request.user
        ).exists()
        
        user_can_review = user_has_booked and not user_has_reviewed
    
    context = {
        'accommodation': accommodation,
        'reviews': reviews,
        'user_can_review': user_can_review,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'bookings/accommodation_detail.html', context)

@login_required
def accommodation_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to add accommodations.')
        return redirect('bookings:accommodation_list')
    
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES)
        if form.is_valid():
            accommodation = form.save(commit=False)
            accommodation.created_by = request.user
            accommodation.save()
            messages.success(request, 'Accommodation created successfully!')
            return redirect('bookings:accommodation_detail', pk=accommodation.pk)
    else:
        form = AccommodationForm()
    
    return render(request, 'bookings/accommodation_form.html', {'form': form, 'title': 'Add New Accommodation'})

@login_required
def book_accommodation(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.accommodation = accommodation
            
            # Calculate total amount
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            nights = (check_out - check_in).days
            booking.total_amount = nights * accommodation.price_per_night
            
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        form = BookingForm()
    
    return render(request, 'bookings/booking_form.html', {'form': form, 'accommodation': accommodation})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})