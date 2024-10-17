from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('new_product/', views.NewProductView.as_view(), name='new-product'),
    path('edit_product/<slug:slug>', views.EditProductView.as_view(), name='edit-product'),
    path('warehouse/', views.WarehouseView.as_view(), name='warehouse'),
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('new_task/', views.NewTaskView.as_view(), name='new-task'),
    path('login/', auth_views.LoginView.as_view(
        template_name='inventory_app/login.html',
        next_page='/',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
]
