import re


def message_has_delete_consumption(command_text: str):
    result = re.match('/del_c', command_text)
    return True if result else False


def get_id_transaction(command_text: str):
    id_transaction = re.findall(r"\d{1,}", command_text)[0]
    return int(id_transaction)

