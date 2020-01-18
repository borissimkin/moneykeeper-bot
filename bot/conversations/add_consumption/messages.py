from bot.utils import ruble_declension


def text_to_choose_category(amount_money):
    return 'Выберите категорию, куда вы потратили <b>{} {}.</b>'.format(amount_money,
                                                                        ruble_declension(int(amount_money)))


def text_error_enter_amount_money():
    return 'Извините, вы ошиблись при вводе количества расходов. Попробуйте снова.'


def text_to_write_money():
    return 'Введите количество денег, которое вы потратили.'


def text_success_add_consumption():
    return 'Расход успешно записан!'


def text_exit_point():
    return 'Вы вышли из диалога <b>добавления расходов.</b>'


def text_timeout():
    return 'Вы вышли из диалога <b>добавления расходов</b> из-за бездействия.'
