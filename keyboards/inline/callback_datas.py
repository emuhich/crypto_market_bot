from aiogram.utils.callback_data import CallbackData

faq_callback = CallbackData("set", "command_name", "start", "end")
get_question_callback = CallbackData("set", "command_name", "pk", "start", "end")
catalog_callback = CallbackData("set", "command_name", "start", "end")
sub_category_callback = CallbackData("set", "command_name", "pk", "start", "end")
show_product_callback = CallbackData("set", "command_name", "pk_products", "pk_sub_categories")
buy_product_callback = CallbackData("set", "command_name", "pk", "quantity", "pk_sub_categories")
my_order_callback = CallbackData("set", "command_name", "start", "end")
show_orders_callback = CallbackData("set", "command_name", "pk_orders")
