from django.shortcuts import render
from .models import Service, Car, Order
from django.views import generic
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    context = {
        'num_cars': Car.objects.count(),
        'num_services': Service.objects.count(),
        'num_orders_done': Order.objects.filter(status='i').count(),
    }
    return render(request, template_name="index.html", context=context)

def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, per_page=2)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        'cars': paged_cars,
    }
    return render(request, template_name='cars.html', context=context)


def car(request, pk):
    context = {
        'car': Car.objects.get(pk=pk)
    }
    return render(request, template_name="car.html", context=context)


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 2


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"