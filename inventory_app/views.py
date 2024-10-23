from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage

from .forms import LocationForm, ProductForm, TaskForm
from .models import Product, Rack, Location, Room, Task


class IndexView(View):
    """
    Zobrazuje statistiky produktů, regálů, lokací a počet neuložených, aktivních a neaktivních produktů na hlavní stránce.
    """

    def get(self, request):
        products = Product.objects.all().count()
        racks = Rack.objects.all().count()
        locations = Location.objects.all().count()
        unordered_products = Product.objects.filter(location__isnull=True).count()

        is_active_true = Product.objects.filter(is_active=True).count()
        is_active_false = Product.objects.filter(is_active=False).count()
        return render(request, "inventory_app/index.html", {
            "products": products,
            "racks": racks,
            "locations": locations,
            "unordered_products": unordered_products,
            "is_active_true": is_active_true,
            "is_active_false": is_active_false
        })


class SearchView(View):
    """View slouží k vyhledávání produktů pomocí filtrů a poté je možné je ukládat do session a spravovat."""

    def get_saved_products(self, request):
        """Získá uložené produkty v session saved_products a vrátí je"""

        saved_products_session = request.session.get("saved_products", [])
        # __in= timto muzu filtrovat vsechny zaznamy najednou (mnozina, pole [1, 2, 4])
        saved_products = Product.objects.filter(
            id__in=saved_products_session).prefetch_related("location").order_by("product_id")

        for product in saved_products:
            product.location_arr = ", ".join([str(location) for location in product.location.all()])

        return saved_products

    def get_search_filters(self, request):
        """Získá vyhledávání a filtry z GET nebo session last_search"""

        # smazani filtru
        if "clear_filters" in request.GET:
            if "last_search" in request.session:
                del request.session['last_search']
                request.session.modified = True
            return "", "", None

        search = request.GET.get("search", "")
        brand_filter = request.GET.get("brand", "")
        rack_filter = request.GET.get("rack", "")

        if rack_filter:
            try:
                rack_filter = int(rack_filter)
            except ValueError:
                rack_filter = None
        else:
            rack_filter = None

        # pokud existuje session "last_search", nacti do promennych hodnoty
        if not search and not brand_filter and not rack_filter:
            last_search = request.session.get("last_search", {})
            search = last_search.get("search", "")
            brand_filter = last_search.get("brand", "")
            rack_filter = last_search.get("rack", "")

        # ulozeni aktualniho vyhledavani do session "last_search"
        request.session["last_search"] = {
            "brand": brand_filter,
            "rack": rack_filter,
            "search": search
        }
        request.session.modified = True

        return search, brand_filter, rack_filter

    def get_searched_products(self, search, brand_filter, rack_filter):
        """
        Filtruje produkty podle zadanych parametru
        :param search:
        :param brand_filter:
        :param rack_filter:
        :return:
        """

        search_products = Product.objects.all().prefetch_related("location").order_by("product_id")

        if search:
            search_products = search_products.filter(Q(
                product_id__icontains=search) | Q(name__icontains=search))

        if brand_filter:
            search_products = search_products.filter(brand=brand_filter)

        if rack_filter:
            search_products = search_products.filter(location__rack__id=rack_filter).distinct().order_by("location")

        for product in search_products:
            product.location_arr = ", ".join([str(location) for location in product.location.all()])

        return search_products

    def get(self, request):
        rooms = Room.objects.all().order_by("name")
        racks = Rack.objects.all()
        brands = Product.objects.values("brand").distinct().order_by("brand")

        saved_products_session = request.session.get("saved_products", [])

        # smazani vsech produktu ze session "saved_products"
        if "delete_saved_products" in request.GET:
            if "saved_products" in request.session:
                del request.session["saved_products"]
                request.session.modified = True
            saved_products_session = []

        # ulozeni produktu do session "saved_products"
        product_to_save = request.GET.get("save_product")
        if product_to_save and product_to_save not in saved_products_session:
            saved_products_session.append(product_to_save)
            request.session["saved_products"] = saved_products_session
            request.session.modified = True

        # smazani produktu ze session "saved_products"
        product_to_delete = request.GET.get("delete_product")
        if product_to_delete and product_to_delete in saved_products_session:
            saved_products_session.remove(product_to_delete)
            request.session["saved_products"] = saved_products_session
            request.session.modified = True

        saved_products = self.get_saved_products(request)

        search, brand_filter, rack_filter = self.get_search_filters(request)

        if search or brand_filter or rack_filter:
            search_products = self.get_searched_products(search, brand_filter, rack_filter)
        else:
            search_products = Product.objects.all().prefetch_related("location").order_by("product_id")

        items_per_page = int(request.GET.get("items_per_page", 10))
        paginator = Paginator(search_products, items_per_page)
        page_number = request.GET.get("page", 1)

        # osetreni aby se uzivatel nedostal na neexistujici stranku
        try:
            search_products_paginator = paginator.page(page_number)
        except EmptyPage:
            search_products_paginator = paginator.page(paginator.num_pages)

        total_products = search_products.count()

        return render(request, "inventory_app/search.html", {
            "rooms": rooms,
            "racks": racks,
            "brands": brands,
            "saved_products": saved_products,
            "search_products": search_products_paginator,
            "total_products": total_products,
            "page_number": page_number,
            "items_per_page": items_per_page,
            "search": search,
            "brand_filter": brand_filter,
            "rack_filter": rack_filter,
        })


class WarehouseView(View):
    """Toto view zajišťuje zobrazení a vytváření nových lokací."""

    def get(self, request):
        all_locations = Location.objects.all()
        form = LocationForm()
        return render(request, "inventory_app/warehouse.html", {
            "form": form,
            "all_locations": all_locations
        })

    def post(self, request):
        all_locations = Location.objects.all()
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            form = LocationForm()
            return render(request, "inventory_app/warehouse.html", {
                "form": form,
                "success": True,
                "all_locations": all_locations
            })

        return render(request, "inventory_app/warehouse.html", {
            "form": form,
            "all_locations": all_locations
        })


class ProductsView(View):
    """
    View zajišťuje zobrazení všech produktů z databáze. Umožnuje vyhledávání a filtraci produktů.
    Hlavní funkcí je přidávání lokací k jednotlivým produktům.
    """

    def get(self, request):
        brands = Product.objects.values("brand").distinct().order_by("brand")
        products = Product.objects.all().prefetch_related("location").order_by("product_id")

        brand_filter = request.GET.get("brand", "")
        search = request.GET.get("search", "")

        if brand_filter:
            products = products.filter(brand=brand_filter)

        if search:
            products = products.filter(
                Q(product_id__icontains=search) | Q(name__icontains=search))

        items_per_page = int(request.GET.get("items_per_page", 20))
        paginator = Paginator(products, items_per_page)
        page_number = request.GET.get("page")
        products_paginator = paginator.get_page(page_number)

        total_products = products.count()

        for product in products_paginator:
            product.location_arr = ", ".join([str(location) for location in product.location.all()])

        return render(request, "inventory_app/products.html", {
            "products_paginator": products_paginator,
            "total_products": total_products,
            "page_number": page_number,
            "items_per_page": items_per_page,
            "brands": brands,
            "brand_filter": brand_filter,
            "search": search,

        })


class NewProductView(View):
    """Toto view slouží k přidávání nových produktů."""

    def get(self, request):
        form = ProductForm()
        return render(request, "inventory_app/add_product.html", {
            "form": form
        })

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")

        return render(request, "inventory_app/add_product.html", {
            "form": form
        })


class EditProductView(View):
    """
    Toto view umožňuje editaci pouze pole 'location' daného produktu.
    Ostatní pole je readonly, protože data jsou automaticky stahována z XML feedu.
    """

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = ProductForm(instance=product)

        # zablokovani upravy danych poli
        form.fields["name"].widget.attrs["readonly"] = True
        form.fields["brand"].widget.attrs["readonly"] = True
        form.fields["product_id"].widget.attrs["readonly"] = True
        form.fields["url"].widget.attrs["readonly"] = True

        return render(request, "inventory_app/edit_product.html", {
            "form": form,
            "product": product
        })

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("products")

        return render(request, "inventory_app/edit_product.html", {
            "form": form,
        })


class TasksView(View):
    """View zobrazuje seznam všech úkolů"""

    def get(self, request):
        tasks = Task.objects.all().order_by("id")
        return render(request, "inventory_app/tasks.html", {
            "tasks": tasks
        })

    def post(self, request):
        tasks = Task.objects.all().order_by("id")
        task_id = request.POST.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        task.is_done = True
        task.save()

        return render(request, "inventory_app/tasks.html", {
            "tasks": tasks
        })


class NewTaskView(View):
    """Umožňuje přidání nového úkolu prostřednictvím formuláře."""

    def get(self, request):
        form = TaskForm()
        return render(request, "inventory_app/add_task.html", {
            "form": form
        })

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks")

        return render(request, "inventory_app/add_task.html", {
            "form": form
        })
