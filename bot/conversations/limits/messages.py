from bot import config
from bot.conversations.limits.utils import current_amount_money_daily_limit_user, \
    current_amount_money_weekly_limit_user, current_amount_money_monthly_limit_user, get_emoji_for_limit
from bot.models import CategoryConsumption, TypeLimit, Limit


def text_exit_point():
    return 'Вы вышли из диалога <b>управления лимитами</b>.'


def text_timeout():
    return 'Вы вышли из диалога <b>управления лимитами</b> из-за бездействия.'


def text_no_limits():
    return 'У вас нет лимитов. Вы можете их добавить, нажав кнопку <b>Добавить</b>.'


def text_choose_type_limit():
    return 'Выберите тип лимита.'


def text_choose_category():
    return 'Выберите категорию.'


def text_to_write_money():
    return 'Введите количство денег, которое вы хотите не превышать.'


def text_error_write_money():
    return 'Извинте, кажется, вы ошиблись, попробуйте еще раз.'


def text_success_add_limit():
    return 'Лимит успешно добавлен!'


def text_choose_limit_to_edit():
    return 'Выберите лимит для изменения'


def text_choose_limit_to_delete():
    return 'Выберите лимит для удаления'


def make_text_and_dict_limits(session, limits):
    ids_limits = {}
    text = ''
    for index, limit in enumerate(limits):
        text += '{} {}\n'.format(index + 1, text_limit(session, limit))
        ids_limits[index + 1] = limit.id
    return text, ids_limits


def text_confirm_delete_limit(session, limit):
    return 'Вы уверены что хотите удалить этот лимит?\n' \
           '{}'.format(text_limit(session, limit))


def text_delete_success():
    return 'Данный лимит успешно удален!'


def text_to_edit_limit(session, limit):
    return 'Что вы хотите изменить в этом лимите?\n' \
           '{}'.format(text_limit(session, limit))


def text_choose_edit_type():
    return 'На какой тип вы хотите изменить?'


def text_edit_type_success(old_type: str, new_type: str):
    return 'Тип данного лимита изменен с <b>{}</b> на <b>{}</b>.'.format(old_type.title(),
                                                                         new_type.title())


def text_choose_edit_category():
    return 'Выберите новую категорию лимита.'


def text_edit_category_success(old_category: str, new_category: str):
    return 'Категория данного лимита измененена с <b>{}</b> на <b>{}</b>.'.format(old_category,
                                                                                  new_category)


def text_edit_amount_money_success(old_amount_money: float, new_amount_money: float):
    return 'Количество денег на лимит изменено с <b>{}</b> на <b>{}</b>.'.format(round(old_amount_money, 2),
                                                                                 round(new_amount_money), 2)


def text_main_menu(session, limits, now):
    if not limits:
        return text_no_limits()
    text = '<b>Информаця по лимитам:</b>\n'
    limits_daily = [x for x in limits if x.type_limit == TypeLimit.DAILY.value]
    limits_weekly = [x for x in limits if x.type_limit == TypeLimit.WEEKLY.value]
    limits_monthly = [x for x in limits if x.type_limit == TypeLimit.MONTHLY.value]
    if limits_daily:
        text += f'\n<i>{TypeLimit.text_type(TypeLimit.DAILY.value).title()}:\n</i>'
        for limit in limits_daily:
            text += '{}\n'.format(text_limit_for_general_info(session, limit, now))
    if limits_weekly:
        text += f'\n<i>{TypeLimit.text_type(TypeLimit.WEEKLY.value).title()}:\n</i>'
        for limit in limits_weekly:
            text += '{}\n'.format(text_limit_for_general_info(session, limit, now))
    if limits_monthly:
        text += f'\n<i>{TypeLimit.text_type(TypeLimit.MONTHLY.value).title()}:\n</i>'
        for limit in limits_monthly:
            text += '{}\n'.format(text_limit_for_general_info(session, limit, now))
    return text


def text_limit(session, limit):
    category = get_text_limit_category(session, limit)
    return f'{TypeLimit.text_type(limit.type_limit).title()} {category} - {limit.amount_money} р.'


def get_text_limit_category(session, limit):
    if limit.category_id:
        category = session.query(CategoryConsumption.category).filter(
            CategoryConsumption.id == limit.category_id
        ).first()[0]
    else:
        category = 'Общий'
    return category


def text_limit_for_general_info(session, limit, now):
    category = get_text_limit_category(session, limit)
    type_limit = TypeLimit(limit.type_limit)
    if type_limit == TypeLimit.DAILY:
        current_amount_money = current_amount_money_daily_limit_user(session, limit, now)
    elif type_limit == TypeLimit.WEEKLY:
        current_amount_money = current_amount_money_weekly_limit_user(session, limit, now)
    else:
        current_amount_money = current_amount_money_monthly_limit_user(session, limit, now)
    return '{} {} - {} из {} р.'.format(get_emoji_for_limit(limit.amount_money, current_amount_money,
                                                            config['conversations']['limit']['percent_warning']),
                                        category,
                                        int(current_amount_money),
                                        int(limit.amount_money))
