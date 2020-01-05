
def make_buttons_for_choose_category(count_buttons_per_row, categories):
    buttons = []
    row = []
    for index, category in enumerate(categories):
        row.append(category.category)
        if (index+1) % count_buttons_per_row == 0 and index > 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return buttons
