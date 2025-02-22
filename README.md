✅ /orders/ → HTML-страница со списком заказов
✅ /api/orders/ → JSON-список заказов
✅ /api/orders/{id}/ → JSON-детали заказа
✅ /api/orders/create/ → Создание заказа (POST)
✅ /api/orders/{id}/update/ → Обновление заказа (PUT/PATCH)
✅ /api/orders/{id}/delete/ → Удаление заказа (DELETE)
✅ /api/orders/total/ → Общая сумма оплаченных заказов
✅ /api/dish/ → JSON-список блюд
✅ /api/dish/ → post Создание блюда (POST)


$ python manage.py show_urls
/       cafe_em.views.web_views.OrderListView   cafe_em:order_list
/<int:pk>/order_delete  cafe_em.views.web_views.OrderDeleteView cafe_em:order_delete
/<int:pk>/order_update  cafe_em.views.web_views.OrderUpdateView cafe_em:order_update_form
/api/dish/      cafe_em.views.api_views.DishViewSet     cafe_em:dish-list
/api/dish/<pk>/ cafe_em.views.api_views.DishViewSet     cafe_em:dish-detail
/api/dish/<pk>\.<format>/       cafe_em.views.api_views.DishViewSet     cafe_em:dish-detail
/api/dish\.<format>/    cafe_em.views.api_views.DishViewSet     cafe_em:dish-list
/api/orders/    cafe_em.views.api_views.OrderViewSet    cafe_em:order-list
/api/orders/<pk>/       cafe_em.views.api_views.OrderViewSet    cafe_em:order-detail
/api/orders/<pk>/delete/        cafe_em.views.api_views.OrderViewSet    cafe_em:order-delete-order
/api/orders/<pk>/delete\.<format>/      cafe_em.views.api_views.OrderViewSet    cafe_em:order-delete-order
/api/orders/<pk>/update/        cafe_em.views.api_views.OrderViewSet    cafe_em:order-partial-update-order
/api/orders/<pk>/update\.<format>/      cafe_em.views.api_views.OrderViewSet    cafe_em:order-partial-update-order 
/api/orders/<pk>\.<format>/     cafe_em.views.api_views.OrderViewSet    cafe_em:order-detail
/api/orders/create/     cafe_em.views.api_views.OrderViewSet    cafe_em:order-create-order
/api/orders/create\.<format>/   cafe_em.views.api_views.OrderViewSet    cafe_em:order-create-order
/api/orders/status/<status>/    cafe_em.views.api_views.OrderViewSet    cafe_em:order-filter-by-status
/api/orders/status/<status>\.<format>/  cafe_em.views.api_views.OrderViewSet    cafe_em:order-filter-by-status     
/api/orders/total/      cafe_em.views.api_views.OrderViewSet    cafe_em:order-total-sum
/api/orders/total\.<format>/    cafe_em.views.api_views.OrderViewSet    cafe_em:order-total-sum
/api/orders\.<format>/  cafe_em.views.api_views.OrderViewSet    cafe_em:order-list
/dish/<int:pk>/ cafe_em.views.web_views.DishDetailView  cafe_em:dish_detail
/dishs/ cafe_em.views.web_views.DishListView    cafe_em:dish_list
/new_dish       cafe_em.views.web_views.DishCreateView  cafe_em:dish_form
/new_order      cafe_em.views.web_views.OrderCreateView cafe_em:order_form
/order/<int:pk>/        cafe_em.views.web_views.OrderDetailView cafe_em:order_detail
/redoc/ drf_yasg.views.SchemaView       cafe_em:schema-redoc
/total_sum      cafe_em.views.web_views.OrderTotalSumView       cafe_em:total_sum