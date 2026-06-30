from django.urls import path
from .views import AssignAgentView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView, lead_list, lead_detail, lead_create, lead_update, lead_delete
from .views import (
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, 
    CategoryListView, CategoryDetailView, LeadCategoryUpdateView
)

app_name = "leads"

urlpatterns = [
    # path('', lead_list, name='lead-list'), # in case there is a name, in any href, you can use the name through the attribute href={% url 'namespace:name' %} as in href= {% url 'leads:lead-list' %}
    path('', LeadListView.as_view(), name='lead-list'), # in case there is a name, in any href, you can use the name through the attribute href={% url 'namespace:name' %} as in href= {% url 'leads:lead-list' %}
    
    # path('create/', lead_create, name='lead-create'), # this has to be above <pk>/ path if the datatype of pk is not specified
    path('create/', LeadCreateView.as_view(), name='lead-create'), # this has to be above <pk>/ path if the datatype of pk is not specified
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'), # this has to be above <pk>/ path if the datatype of pk is not specified
    # path('<pk>/', lead_detail)
    # path('<int:pk>/', lead_detail, name='lead-detail'), # this is to avoid any prblem with other paths | in case you want to use a parameter in the link and the name, use href = {% url 'namespace:name' lead.pk %}
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'), # this is to avoid any prblem with other paths | in case you want to use a parameter in the link and the name, use href = {% url 'namespace:name' lead.pk %}
    # path('<int:pk>/update', lead_update, name='lead-update'), # in case you want to use a parameter in the link and the name, use href = {% url 'namespace:name' lead.pk %}
    path('<int:pk>/update', LeadUpdateView.as_view(), name='lead-update'),
    # path('<int:pk>/delete', lead_delete, name='lead-delete')
    path('<int:pk>/delete', LeadDeleteView.as_view(), name='lead-delete'),
    path('category-create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),

]