# -*- coding: utf-8 -*-
import datetime
import os
import tempfile

import matplotlib.pyplot as plt
import numpy as np
import sqlalchemy
from matplotlib import rc

from bot.conversations.statistics.type_transacation_graph import TypeTransaction
from bot.conversations.statistics.utils import divide_into_money_and_categories_consumption, get_current_month, \
    get_consumptions_for_graph_user
from bot.models import CategoryConsumption, Consumption


def make_pie_graph(data, labels, title, type_transactions: TypeTransaction):
    explode = [0.01 for _ in labels]
    data = [int(x) for x in data]
    sum_data = sum(data)
    patches, texts, _ = plt.pie(data, labels=labels, startangle=90, pctdistance=0.85, explode=explode,
                                autopct=lambda x: '{}р.'.format(int(sum_data / 100 * x)))
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    make_center_text(type_transactions, sum_data)
    fig = plt.gcf()
    plt.title(title, fontsize=20)

    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    plt.tight_layout()
    path_to_graph = os.path.join(tempfile.mkdtemp(), 'figure.jpg')
    plt.savefig(path_to_graph)
    plt.close()
    return path_to_graph


def make_center_text(type_transactions, amount_money):
    if type_transactions == type_transactions.CONSUMPTION:
        text = 'Расходы\n{} р.'.format(amount_money)
        color = 'red'
    elif type_transactions == type_transactions.EARNING:
        text = 'Доходы\n{} р.'.format(amount_money)
        color = 'green'
    else:
        text = 'Неопределено'
        color = 'black'
    plt.annotate(text, xy=(0, 0), fontsize=18, ha="center", color=color)


def make_stack_histogram_average(session, user):
    """
        Стэковая гистограмма средних значений расходов.
        Все время, месяц, неделя, день
    """
    n_bins = 4
    # y-axis in bold
    rc('font', weight='bold')

    category_consumption = session.query(CategoryConsumption).filter(
        CategoryConsumption.user_id == user.id
    ).all()
    colors_category = generate_colors(category_consumption)
    # средние значения за все время
    averages_all_time = session.query(sqlalchemy.func.avg(Consumption.amount_money), Consumption.category_id).filter(
            Consumption.user_id == user.id,
        ).group_by(Consumption.category_id).all()
    get_averages_by_month(session, user_id=user.id)
    # averages_by_month = session.query(sqlalchemy.func.avg(Consumption.amount_money), Consumption.category_id).filter(
    #     Consumption.user_id == user.id,
    # ).group_by(sqlalchemy.func.strftime("%Y-%m-%d", Consumption.time_creation)).all()
    # averages_by_month = session.query(sqlalchemy.func.avg(Consumption.amount_money), Consumption.category_id).filter(
    #     Consumption.user_id == user.id,
    # ).group_by(sqlalchemy.func.strftime("%m-%d", Consumption.time_creation)).all()
    averages_all_time = sorted(averages_all_time, key=lambda x: x[1])
    averages, labels = preprocess_averages(session, averages_all_time)
    # fill_empty_category
    for key in colors_category.keys():
        category = session.query(CategoryConsumption).get(key)
        if category.category not in labels:
            averages.append(0)
            labels.append(category.category)


    # av = [averages, [100, 50, 30, 0, 0, 0, 0], [50, 50, 50, 0, 0, 0, 0], [15, 10, 5, 4, 0, 0, 0, 0]]
    names = ['Все время', 'Месяц', 'Неделя', 'День']
    bar_width = 1
    plt.hist(av, n_bins, histtype='bar', stacked=True)
    plt.legend(loc="upper right")
    plt.title('Stacked-histogram ')
    path_to_graph = os.path.join(tempfile.mkdtemp(), 'figure.jpg')
    plt.savefig(path_to_graph)
    plt.close()
    return path_to_graph


def get_averages_by_month(session, user_id):
    try:
        averages = session.query(Consumption).filter(
            Consumption.user_id == user_id
        ).order_by(Consumption.time_creation.asc()).all()
    except Exception as e:
        print(e)
    print(averages)


def generate_colors(categories_consumption):
    colors = {}
    cmap = get_cmap(len(categories_consumption))
    for index, category in enumerate(categories_consumption):
        colors[category.id] = cmap(index)
    return colors


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def preprocess_averages(session, averages):
    average_all_time, labels_all_time = divide_into_money_and_categories_consumption(session, averages)
    averages_all_time = [int(x) for x in average_all_time]
    return averages_all_time, labels_all_time



