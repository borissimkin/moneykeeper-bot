import pymorphy2


def text_to_write_money():
    return 'Введите количество денег, которое вы получили.'


def text_timeout():
    return 'Вы вышли из диалога <b>добавления доходов</b> из-за бездействия.'


def text_exit_point():
    return 'Вы вышли из диалога <b>добавления доходов.</b>'


def text_error_enter_amount_money():
    return 'Извините, вы ошиблись при вводе количества доходов. Попробуйте снова.'


def text_to_choose_category(amount_money):
    morph = pymorphy2.MorphAnalyzer()
    money_morph = morph.parse('рубль')[0]
    return 'Выберите категорию, откуда вы получили <b>{} {}.</b>'.format(amount_money,
                                                                         money_morph.
                                                                         make_agree_with_number(int(amount_money)).word)


def text_confirm_add_earning(amount_money, category):
    morph = pymorphy2.MorphAnalyzer()
    money_morph = morph.parse('рубль')[0]
    return 'Записать <b>{} {}</b> на категорию <b>{}</b>?'.format(amount_money,
                                                                  money_morph.make_agree_with_number(int(
                                                                      amount_money)).word,
                                                                  category)


def text_success_add_earning():
    return 'Доход успешно записан!'
