from aiogram.utils.callback_data import CallbackData

faq_callback = CallbackData("set", "command_name", "start", "end")
get_question_callback = CallbackData("set", "command_name", "pk", "start", "end")
catalog_callback = CallbackData("set", "command_name", "start", "end")
sub_category_callback = CallbackData("set", "command_name", "pk", "start", "end")
show_product_callback = CallbackData("set", "command_name", "pk_products", "pk_sub_categories", "number")
buy_product_callback = CallbackData("set", "command_name", "pk", "quantity", "pk_sub_categories", "number")
my_order_callback = CallbackData("set", "command_name", "start", "end")
show_orders_callback = CallbackData("set", "command_name", "pk_orders")
check_payment_callback = CallbackData("set", "command_name", "coin", "price", "pk", "quantity",
                                      "pk_sub_categories")
choice_payment_callback = CallbackData("set", "command_name", "coin", "pk", "quantity", "pk_sub_categories", "number")
characteristic_callback = CallbackData("set", "command", "pk", "start", "end", "keys", "value")
