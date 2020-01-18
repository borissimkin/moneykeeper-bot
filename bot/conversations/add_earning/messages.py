from bot.utils import ruble_declension


def text_to_write_money():
    return 'Введите количество денег, которое вы получили.'


def text_timeout():
    return 'Вы вышли из диалога <b>добавления доходов</b> из-за бездействия.'


def text_exit_point():
    return 'Вы вышли из диалога <b>добавления доходов.</b>'


def text_error_enter_amount_money():
    return 'Извините, вы ошиблись при вводе количества доходов. Попробуйте снова.'


def text_to_choose_category(amount_money):
    return 'Выберите категорию, откуда вы получили <b>{} {}.</b>'.format(amount_money,
                                                                         ruble_declension(int(amount_money)))


def text_success_add_earning():
    return 'Доход успешно записан!'
