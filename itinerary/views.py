from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from .models import Itinerary, ItineraryItem
from .forms import ItineraryForm, ItineraryItemForm, QuickDestinationForm


@login_required
def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user).annotate(
        total_items=Count('itinerary_items'),
        total_cost=Sum('itinerary_items__estimated_cost')
    )

    context = {
        'itineraries': itineraries
    }
    return render(request, 'itinerary/itinerary_list.html', context)


@login_required
def itinerary_detail(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    items = itinerary.itinerary_items.all().select_related('destination', 'accommodation')

    # Group items by date
    items_by_date = {}
    for item in items:
        date_key = item.start_date
        if date_key not in items_by_date:
            items_by_date[date_key] = []
        items_by_date[date_key].append(item)

    # Calculate summary statistics
    total_cost = items.aggregate(total=Sum('estimated_cost'))['total'] or 0
    destinations_count = items.filter(item_type='destination').count()
    accommodations_count = items.filter(item_type='accommodation').count()

    context = {
        'itinerary': itinerary,
        'items': items,
        'items_by_date': dict(sorted(items_by_date.items())),
        'total_cost': total_cost,
        'destinations_count': destinations_count,
        'accommodations_count': accommodations_count,
    }
    return render(request, 'itinerary/itinerary_detail.html', context)


@login_required
def itinerary_create(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.user = request.user
            itinerary.save()
            messages.success(request, 'Itinerary created successfully!')
            return redirect('itinerary:itinerary_detail', pk=itinerary.pk)
    else:
        form = ItineraryForm()

    return render(request, 'itinerary/itinerary_form.html', {
        'form': form,
        'title': 'Create New Itinerary'
    })


@login_required
def itinerary_update(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ItineraryForm(request.POST, instance=itinerary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Itinerary updated successfully!')
            return redirect('itinerary:itinerary_detail', pk=itinerary.pk)
    else:
        form = ItineraryForm(instance=itinerary)

    return render(request, 'itinerary/itinerary_form.html', {
        'form': form,
        'title': f'Update {itinerary.title}',
        'itinerary': itinerary
    })


@login_required
def itinerary_delete(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)

    if request.method == 'POST':
        itinerary_title = itinerary.title
        itinerary.delete()
        messages.success(request, f'Itinerary "{itinerary_title}" deleted successfully!')
        return redirect('itinerary:itinerary_list')

    return render(request, 'itinerary/itinerary_confirm_delete.html', {'itinerary': itinerary})


@login_required
def item_create(request, itinerary_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)

    if request.method == 'POST':
        form = ItineraryItemForm(request.POST, itinerary=itinerary)
        if form.is_valid():
            item = form.save(commit=False)
            item.itinerary = itinerary
            item.save()
            messages.success(request, 'Item added to itinerary!')
            return redirect('itinerary:itinerary_detail', pk=itinerary.pk)
    else:
        form = ItineraryItemForm(itinerary=itinerary)

    return render(request, 'itinerary/item_form.html', {
        'form': form,
        'itinerary': itinerary,
        'title': 'Add Item to Itinerary'
    })


@login_required
def item_update(request, itinerary_pk, item_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)
    item = get_object_or_404(ItineraryItem, pk=item_pk, itinerary=itinerary)

    if request.method == 'POST':
        form = ItineraryItemForm(request.POST, instance=item, itinerary=itinerary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('itinerary:itinerary_detail', pk=itinerary.pk)
    else:
        form = ItineraryItemForm(instance=item, itinerary=itinerary)

    return render(request, 'itinerary/item_form.html', {
        'form': form,
        'itinerary': itinerary,
        'item': item,
        'title': 'Update Itinerary Item'
    })


@login_required
def item_delete(request, itinerary_pk, item_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)
    item = get_object_or_404(ItineraryItem, pk=item_pk, itinerary=itinerary)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item removed from itinerary!')
        return redirect('itinerary:itinerary_detail', pk=itinerary.pk)

    return render(request, 'itinerary/item_confirm_delete.html', {
        'itinerary': itinerary,
        'item': item
    })


@login_required
def quick_add_destination(request, itinerary_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk, user=request.user)

    if request.method == 'POST':
        form = QuickDestinationForm(request.POST, itinerary=itinerary)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            ItineraryItem.objects.create(
                itinerary=itinerary,
                item_type='destination',
                destination=destination,
                title=f"Visit {destination.name}",
                description=destination.description[:200] + "..." if len(
                    destination.description) > 200 else destination.description,
                location=f"{destination.location}, {destination.state}",
                start_date=start_date,
                end_date=end_date,
                estimated_cost=destination.entry_fee if destination.entry_fee > 0 else None
            )

            messages.success(request, f'{destination.name} added to your itinerary!')
            return redirect('itinerary:itinerary_detail', pk=itinerary.pk)

    return JsonResponse({'error': 'Invalid request'}, status=400)


class PublicItineraryListView(ListView):
    model = Itinerary
    template_name = 'itinerary/public_itinerary_list.html'
    context_object_name = 'itineraries'
    paginate_by = 12

    def get_queryset(self):
        return Itinerary.objects.filter(is_public=True).annotate(
            total_items=Count('itinerary_items'),
            total_cost=Sum('itinerary_items__estimated_cost')
        ).order_by('-created_at')


def public_itinerary_detail(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, is_public=True)
    items = itinerary.itinerary_items.all().select_related('destination', 'accommodation')

    # Group items by date
    items_by_date = {}
    for item in items:
        date_key = item.start_date
        if date_key not in items_by_date:
            items_by_date[date_key] = []
        items_by_date[date_key].append(item)

    context = {
        'itinerary': itinerary,
        'items': items,
        'items_by_date': dict(sorted(items_by_date.items())),
        'is_public_view': True,
    }
    return render(request, 'itinerary/public_itinerary_detail.html', context)