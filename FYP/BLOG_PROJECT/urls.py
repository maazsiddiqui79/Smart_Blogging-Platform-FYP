from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler400 = "blog.views.custom_404_view"
handler404 = "blog.views.custom_404_view"
handler401 = "blog.views.custom_404_view"
handler403 = "blog.views.custom_404_view"
handler408 = "blog.views.custom_404_view"
handler409 = "blog.views.custom_404_view"
handler429 = "blog.views.custom_404_view"
handler500 = "blog.views.custom_404_view"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
| Code    | Name               | Meaning              |
| ------- | ------------------ | -------------------- |
| **400** | Bad Request        | Invalid request data |
| **401** | Unauthorized       | Not logged in        |
| **403** | Forbidden          | No permission        |
| **404** | Not Found          | URL doesn’t exist    |
| **405** | Method Not Allowed | GET/POST mismatch    |
| **408** | Request Timeout    | Client too slow      |
| **409** | Conflict           | Resource conflict    |
| **429** | Too Many Requests  | Rate limit exceeded  |

'''