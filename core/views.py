from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Link
from .forms import AddLinkForm

from django.views.generic import DeleteView

def home(request):
    no_discounted = 0
    error = None

    form = AddLinkForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "ERROR - Name or price"
        except:
            error = "ERROR - Something went wrong"
    
    form = AddLinkForm()

    qs = Link.objects.all()
    items_no = qs.count()

    if items_no > 0:
        discounted_list = []
        for item in qs:
            if item.old_price > item.current_price:
                discounted_list.append(item)
            no_discounted = len(discounted_list)

    context = {
        'qs': qs,
        'items_no': items_no,
        'no_discounted': no_discounted,
        'form': form,
        'error': error,
    }

    return render(request, 'core/main.html', context)


class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'core/confirm_del.html'
    success_url = reverse_lazy('home')


def update_prices(reques):
    qs = Link.objects.all()
    for link in qs:
        link.save()
    return redirect('home')