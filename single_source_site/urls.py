from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('music_videos', views.display_music_videos),
    path('narrative', views.display_narrative),
    path('commercial', views.display_commercial),
    path('3_ton_list', views.display_3_ton_list),
    path('1_ton_list', views.display_1_ton_list),
    path('electric_list', views.display_electric_list),
    path('about', views.display_about),
    path('contact', views.display_contact),
    path('dolly_list', views.display_dolly_list),
    path('quote_page', views.build_quote),
    path('add_accessories/<int:product_id>', views.get_accessories),
    path('add_to_cart', views.display_cart),
    path('get_order/<int:order_id>', views.get_order),
    path('delete_order_item/<int:order_id>/<str:item_id>', views.delete_order_item),
    path('send_quote/<int:order_id>', views.send_quote),
]