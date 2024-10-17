def post(self, request):
    rooms = Room.objects.all().order_by("name")
    racks = Rack.objects.all()
    brands = Product.objects.values("brand").distinct().order_by("brand")

    # ulozeni produktu do session "saved_products"
    product_to_save = request.POST.get("save_product")
    if product_to_save:
        saved_products_session = request.session.get("saved_products", [])
        saved_products_session.append(product_to_save)
        request.session["saved_products"] = saved_products_session
        request.session.modified = True  # -> session byla zmenema, uloz ji

    # smazani produktu ze session "saved_products"
    product_to_delete = request.POST.get("delete_product")
    if product_to_delete:
        saved_products_session = request.session.get("saved_products", [])
        if product_to_delete in saved_products_session:
            saved_products_session.remove(product_to_delete)
            request.session["saved_products"] = saved_products_session
            request.session.modified = True

    # nacteni produktu ze session "saved_products"
    saved_products_session = request.session.get("saved_products", [])
    saved_products = Product.objects.filter(id__in=saved_products_session)

    # _________________________________________
    # vyprazdnit session - pridat tlacitko do tabulky
    # request.session.flush()
    # _________________________________________

    search = request.POST.get("search")
    brand_filter = request.POST.get("brand")
    rack_filter = request.POST.get("rack")
    search_products = None

    if "last_search" in request.session:
        last_search = request.session["last_search"]
        search = last_search.get("search")
        brand_filter = last_search.get("brand_filter")
        rack_filter = last_search.get("rack_filter")

    if search or brand_filter or rack_filter:
        search_products = Product.objects.all()

        if search:
            search_products = Product.objects.filter(
                product_id__icontains=search) | Product.objects.filter(name__icontains=search)

        if brand_filter:
            search_products = search_products.filter(brand=brand_filter)

        if rack_filter:
            search_products = search_products.filter(location__rack__id=rack_filter)

    request.session["last_search"] = {
        "search": search,
        "brand_filter": brand_filter,
        "rack_filter": rack_filter
    }
    request.session.modified = True

    return render(request, "inventory_app/search.html", {
        "rooms": rooms,
        "racks": racks,
        "brands": brands,
        "search": search,
        "search_products": search_products,
        "saved_products": saved_products
    })


# origin view

class SearchView(View):
    def get(self, request):
        rooms = Room.objects.all().order_by("name")
        racks = Rack.objects.all()
        brands = Product.objects.values("brand").distinct().order_by("brand")

        saved_products_session = request.session.get("saved_products", [])
        # __in= timto muzu filtrovat vsechny zaznamy najednou (mnozina, pole [1, 2, 4])
        saved_products = Product.objects.filter(id__in=saved_products_session).prefetch_related("location")

        for product in saved_products:
            product.location_arr = ", ".join([str(location) for location in product.location.all()])

        # -------

        search = request.GET.get("search", "")
        brand_filter = request.GET.get("brand", "")
        rack_filter = request.GET.get("rack", "")

        if not search and not brand_filter and not rack_filter:
            last_search = request.session.get("last_search", {})
            search = last_search.get("search", "")
            brand_filter = last_search.get("brand_filter", "")
            rack_filter = last_search.get("rack_filter", "")

        # Uložení aktuálního vyhledávání do session "last_search"
        request.session["last_search"] = {
            "search": search,
            "brand_filter": brand_filter,
            "rack_filter": rack_filter
        }
        request.session.modified = True

        search_products = None

        if search or brand_filter or rack_filter:
            search_products = Product.objects.all()

            if search:
                search_products = search_products.filter(Q(
                    product_id__icontains=search) | Q(name__icontains=search))

            if brand_filter:
                search_products = search_products.filter(brand=brand_filter)

            if rack_filter:
                search_products = search_products.filter(location__rack__id=rack_filter).distinct()

            for product in search_products:
                product.location_arr = ", ".join([str(location) for location in product.location.all()])

        # ------

        return render(request, "inventory_app/search.html", {
            "rooms": rooms,
            "racks": racks,
            "brands": brands,
            "saved_products": saved_products,
            "search_products": search_products
        })

    def post(self, request):
        rooms = Room.objects.all().order_by("name")
        racks = Rack.objects.all()
        brands = Product.objects.values("brand").distinct().order_by("brand")

        # smazani produktu ze session "saved_products"
        if "delete_saved_products" in request.POST:
            if "saved_products" in request.session:
                del request.session['saved_products']
                request.session.modified = True

        # ulozeni produktu do session "saved_products"
        product_to_save = request.POST.get("save_product")
        if product_to_save:
            saved_products_session = request.session.get("saved_products", [])
            if product_to_save not in saved_products_session:
                saved_products_session.append(product_to_save)
                request.session["saved_products"] = saved_products_session
                request.session.modified = True

        # smazani produktu ze session "saved_products"
        product_to_delete = request.POST.get("delete_product")
        if product_to_delete:
            saved_products_session = request.session.get("saved_products", [])
            if product_to_delete in saved_products_session:
                saved_products_session.remove(product_to_delete)
                request.session["saved_products"] = saved_products_session
                request.session.modified = True

        # nacteni produktu ze session "saved_products"
        saved_products_session = request.session.get("saved_products", [])
        saved_products = Product.objects.filter(id__in=saved_products_session).prefetch_related("location")

        for product in saved_products:
            product.location_arr = ", ".join([str(location) for location in product.location.all()])

        search = request.POST.get("search", "")
        brand_filter = request.POST.get("brand", "")
        rack_filter = request.POST.get("rack", "")
        search_products = None

        # pokud existuje session "last_search", nacti do promennych hodnoty
        if not search and not brand_filter and not rack_filter:
            last_search = request.session.get("last_search", {})
            search = last_search.get("search", "")
            brand_filter = last_search.get("brand_filter", "")
            rack_filter = last_search.get("rack_filter", "")

        # ulozeni aktualniho vyhledavani do session "last_search"
        request.session["last_search"] = {
            "search": search,
            "brand_filter": brand_filter,
            "rack_filter": rack_filter
        }
        request.session.modified = True

        if search or brand_filter or rack_filter:
            search_products = Product.objects.all()

            if search:
                search_products = search_products.filter(Q(
                    product_id__icontains=search) | Q(name__icontains=search))

            if brand_filter:
                search_products = search_products.filter(brand=brand_filter)

            if rack_filter:
                search_products = search_products.filter(location__rack__id=rack_filter).distinct()

            for product in search_products:
                product.location_arr = ", ".join([str(location) for location in product.location.all()])

        return render(request, "inventory_app/search.html", {
            "rooms": rooms,
            "racks": racks,
            "brands": brands,
            "search": search,
            "search_products": search_products,
            "saved_products": saved_products
        })


# puvodni Search view s GET a POST

class SearchView(View):
    def get_saved_products(self, request):
        """Získá uložené produkty v session saved_products a vrátí je"""
        # nacteni produktu ze session "saved_products"

        saved_products_session = request.session.get("saved_products", [])
        # __in= timto muzu filtrovat vsechny zaznamy najednou (mnozina, pole [1, 2, 4])
        saved_products = Product.objects.filter(id__in=saved_products_session).prefetch_related("location")

        for product in saved_products:
            product.location_arr = ", ".join([str(location) for location in product.location.all()])

        return saved_products

    def get_search_filters(self, request):
        """Získá vyhledávání a filtry z GET, POST nebo session last_search"""

        search = request.GET.get("search", "") if request.method == "GET" else request.POST.get("search", "")
        brand_filter = request.GET.get("brand", "") if request.method == "GET" else request.POST.get("brand", "")
        rack_filter = request.GET.get("rack", "") if request.method == "GET" else request.POST.get("rack", "")

        # pokud existuje session "last_search", nacti do promennych hodnoty
        if not search and not brand_filter and not rack_filter:
            last_search = request.session.get("last_search", {})
            search = last_search.get("search", "")
            brand_filter = last_search.get("brand", "")
            rack_filter = last_search.get("rack", "")

        # ulozeni aktualniho vyhledavani do session "last_search"
        request.session["last_search"] = {
            "search": search,
            "brand": brand_filter,
            "rack": rack_filter
        }
        request.session.modified = True

        return search, brand_filter, rack_filter

    def get_searched_products(self, search, brand_filter, rack_filter):
        """Filtruje produkty podle zadanych parametru"""
        search_products = Product.objects.all().order_by("product_id")

        if search:
            search_products = search_products.filter(Q(
                product_id__icontains=search) | Q(name__icontains=search))

        if brand_filter:
            search_products = search_products.filter(brand=brand_filter)

        if rack_filter:
            search_products = search_products.filter(location__rack__id=rack_filter).distinct()

        for product in search_products:
            product.location_arr = ", ".join([str(location) for location in product.location.all()])

        return search_products

    # def pagination(self, search_products, request):
    #     """Paginator pro stránkování produktů"""
    #     items_per_page = int(request.GET.get("items_per_page", 10))
    #     paginator = Paginator(search_products, items_per_page)
    #     page_number = request.GET.get("page", 1)
    #     search_products_paginator = paginator.page(page_number)
    #
    #     return search_products_paginator, paginator.num_pages, items_per_page, page_number

    def get(self, request):
        rooms = Room.objects.all().order_by("name")
        racks = Rack.objects.all()
        brands = Product.objects.values("brand").distinct().order_by("brand")

        saved_products = self.get_saved_products(request)
        search, brand_filter, rack_filter = self.get_search_filters(request)

        search_products = None
        if search or brand_filter or rack_filter:
            search_products = self.get_searched_products(search, brand_filter, rack_filter)

        items_per_page = int(request.GET.get("items_per_page", 10))
        paginator = Paginator(search_products, items_per_page)
        page_number = request.GET.get("page", 1)
        search_products_paginator = paginator.page(page_number)

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

    def post(self, request):
        rooms = Room.objects.all().order_by("name")
        racks = Rack.objects.all()
        brands = Product.objects.values("brand").distinct().order_by("brand")

        saved_products = self.get_saved_products(request)
        search, brand_filter, rack_filter = self.get_search_filters(request)

        # smazani produktu ze session "saved_products"
        if "delete_saved_products" in request.POST:
            if "saved_products" in request.session:
                del request.session['saved_products']
                request.session.modified = True

        # ulozeni produktu do session "saved_products"
        product_to_save = request.POST.get("save_product")
        if product_to_save:
            saved_products_session = request.session.get("saved_products", [])
            if product_to_save not in saved_products_session:
                saved_products_session.append(product_to_save)
                request.session["saved_products"] = saved_products_session
                request.session.modified = True

        # smazani produktu ze session "saved_products"
        product_to_delete = request.POST.get("delete_product")
        if product_to_delete:
            saved_products_session = request.session.get("saved_products", [])
            if product_to_delete in saved_products_session:
                saved_products_session.remove(product_to_delete)
                request.session["saved_products"] = saved_products_session
                request.session.modified = True

        search_products = None
        if search or brand_filter or rack_filter:
            search_products = self.get_searched_products(search, brand_filter, rack_filter)

        items_per_page = int(request.GET.get("items_per_page", 10))
        paginator = Paginator(search_products, items_per_page)
        page_number = request.GET.get("page", 1)
        search_products_paginator = paginator.page(page_number)

        total_products = search_products.count()

        return render(request, "inventory_app/search.html", {
            "rooms": rooms,
            "racks": racks,
            "brands": brands,
            "search_products": search_products_paginator,
            "saved_products": saved_products,
            "total_products": total_products,
            "page_number": page_number,
            "items_per_page": items_per_page,
            "search": search,
            "brand_filter": brand_filter,
            "rack_filter": rack_filter,
        })
