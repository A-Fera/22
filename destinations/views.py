from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from .models import Destination, Photo
from .forms import DestinationForm, PhotoForm
from reviews.models import DestinationReview

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Destination.objects.all().order_by('-created_at')
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(state__icontains=search) |
                Q(description__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Destination.CATEGORY_CHOICES
        context['search'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    photos = destination.photos.all()
    accommodations = destination.accommodations.filter(is_available=True)[:6]
    reviews = DestinationReview.objects.filter(
        destination=destination, 
        is_approved=True
    ).order_by('-created_at')[:5]
    
    # Check if user has already reviewed this destination
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = DestinationReview.objects.filter(
            destination=destination, 
            user=request.user
        ).exists()
    
    context = {
        'destination': destination,
        'photos': photos,
        'accommodations': accommodations,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'destinations/destination_detail.html', context)

@login_required
def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.created_by = request.user
            destination.save()
            messages.success(request, 'Destination created successfully!')
            return redirect('destinations:destination_detail', pk=destination.pk)
    else:
        form = DestinationForm()
    
    return render(request, 'destinations/destination_form.html', {'form': form, 'title': 'Add New Destination'})

@login_required
def destination_update(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    
    if request.user != destination.created_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this destination.')
        return redirect('destinations:destination_detail', pk=pk)
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination updated successfully!')
            return redirect('destinations:destination_detail', pk=destination.pk)
    else:
        form = DestinationForm(instance=destination)
    
    return render(request, 'destinations/destination_form.html', {'form': form, 'title': 'Update Destination'})

@login_required
def photo_upload(request, destination_pk):
    destination = get_object_or_404(Destination, pk=destination_pk)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.destination = destination
            photo.uploaded_by = request.user
            photo.save()
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('destinations:destination_detail', pk=destination.pk)
    else:
        form = PhotoForm()
    
    return render(request, 'destinations/photo_upload.html', {'form': form, 'destination': destination})