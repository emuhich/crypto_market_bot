async def get_button_next_back(number_position, end, start):
    if number_position <= 8:
        next, back = False, False
    elif end < number_position and start > 0:
        next, back = True, True
    elif start == 0:
        next, back = True, False
    elif end >= number_position:
        next, back = False, True
    else:
        print("Возникло исключение в кнопках вперед/назад")

    return next, back
