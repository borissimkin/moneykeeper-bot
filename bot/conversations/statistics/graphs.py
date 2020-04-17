# -*- coding: utf-8 -*-
import os
import tempfile

import matplotlib.pyplot as plt
import numpy as np

from bot.conversations.statistics.type_transacation_graph import TypeTransaction
from bot.conversations.statistics.utils import remove_emoji


def make_pie_graph(data, labels, title, type_transactions: TypeTransaction):
    labels = [remove_emoji(label) for label in labels]
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



