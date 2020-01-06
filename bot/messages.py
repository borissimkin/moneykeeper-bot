import pymorphy2


def text_confirm_add_transaction(amount_money, category):
    morph = pymorphy2.MorphAnalyzer()
    money_morph = morph.parse('рубль')[0]
    return 'Записать <b>{} {}</b> на категорию <b>{}</b>?'.format(amount_money,
                                                                  money_morph.make_agree_with_number(int(
                                                                      amount_money)).word,
                                                                  category)