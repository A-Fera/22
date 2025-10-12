from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.http import JsonResponse
from destinations.models import Destination
from bookings.models import Accommodation, Booking
from .models import DestinationReview, AccommodationReview, ReviewPhoto
from .forms import DestinationReviewForm, AccommodationReviewForm, ReviewPhotoFormSet

@login_required
def destination_review_create(request, destination_pk):
    destination = get_object_or_404(Destination, pk=destination_pk)
    
    # Check if user already reviewed this destination
    if DestinationReview.objects.filter(destination=destination, user=request.user).exists():
        messages.error(request, 'You have already reviewed this destination.')
        return redirect('destinations:destination_detail', pk=destination.pk)
    
    if request.method == 'POST':
        form = DestinationReviewForm(request.POST)
        photo_formset = ReviewPhotoFormSet(request.POST, request.FILES)
        
        if form.is_valid() and photo_formset.is_valid():
            review = form.save(commit=False)
            review.destination = destination
            review.user = request.user
            review.save()
            
            # Save photos
            for photo_form in photo_formset:
                if photo_form.cleaned_data and not photo_form.cleaned_data.get('DELETE', False):
                    if photo_form.cleaned_data.get('image'):
                        photo = photo_form.save(commit=False)
                        photo.destination_review = review
                        photo.save()
            
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('destinations:destination_detail', pk=destination.pk)
    else:
        form = DestinationReviewForm()
        photo_formset = ReviewPhotoFormSet(queryset=ReviewPhoto.objects.none())
    
    context = {
        'form': form,
        'photo_formset': photo_formset,
        'destination': destination,
        'title': f'Review {destination.name}'
    }
    return render(request, 'reviews/destination_review_form.html', context)

@login_required
def accommodation_review_create(request, accommodation_pk):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_pk)
    
    # Check if user has booked this accommodation
    has_booking = Booking.objects.filter(
        accommodation=accommodation,
        user=request.user,
        booking_status='confirmed'
    ).exists()
    
    if not has_booking:
        messages.error(request, 'You can only review accommodations you have booked.')
        return redirect('bookings:accommodation_detail', pk=accommodation.pk)
    
    # Check if user already reviewed this accommodation
    if AccommodationReview.objects.filter(accommodation=accommodation, user=request.user).exists():
        messages.error(request, 'You have already reviewed this accommodation.')
        return redirect('bookings:accommodation_detail', pk=accommodation.pk)
    
    if request.method == 'POST':
        form = AccommodationReviewForm(request.POST)
        photo_formset = ReviewPhotoFormSet(request.POST, request.FILES)
        
        if form.is_valid() and photo_formset.is_valid():
            review = form.save(commit=False)
            review.accommodation = accommodation
            review.user = request.user
            review.save()
            
            # Save photos
            for photo_form in photo_formset:
                if photo_form.cleaned_data and not photo_form.cleaned_data.get('DELETE', False):
                    if photo_form.cleaned_data.get('image'):
                        photo = photo_form.save(commit=False)
                        photo.accommodation_review = review
                        photo.save()
            
            # Update accommodation rating
            avg_rating = AccommodationReview.objects.filter(
                accommodation=accommodation
            ).aggregate(Avg('rating'))['rating__avg']
            accommodation.rating = round(avg_rating, 1) if avg_rating else 0
            accommodation.save()
            
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('bookings:accommodation_detail', pk=accommodation.pk)
    else:
        form = AccommodationReviewForm()
        photo_formset = ReviewPhotoFormSet(queryset=ReviewPhoto.objects.none())
    
    context = {
        'form': form,
        'photo_formset': photo_formset,
        'accommodation': accommodation,
        'title': f'Review {accommodation.name}'
    }
    return render(request, 'reviews/accommodation_review_form.html', context)

def review_detail(request, review_type, review_pk):
    if review_type == 'destination':
        review = get_object_or_404(DestinationReview, pk=review_pk)
        template = 'reviews/destination_review_detail.html'
    else:
        review = get_object_or_404(AccommodationReview, pk=review_pk)
        template = 'reviews/accommodation_review_detail.html'
    
    context = {'review': review}
    return render(request, template, context)