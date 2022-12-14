from django.contrib import admin
from django.urls import path, include,re_path
from rest_framework.routers import SimpleRouter
from product.views import ProductViewSet
from django.conf.urls.static import static
from django.conf import settings
from category.views import CategoryViewSet
from cart.views import CartApiView



from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)




router=SimpleRouter()
router.register('products',ProductViewSet)
router.register('categories', CategoryViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include(router.urls)),
    path('api/v1/', include('product.urls')),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/cart/', CartApiView.as_view()),
    path('api/v1/orders/',include('order.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

