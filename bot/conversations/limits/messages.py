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

