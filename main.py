import json
from datetime import datetime
import click


# Категории:
CATEGORIES = {
    "+": "Доход",
    "-": "Расход"
}


@click.group()
def my_commands():
    """Команды (список ниже)"""
    pass


@click.command()
def balance():
    """Ваш баланс"""                        # Команда для вывода баланса из файла data.json
    with open("data.json", "r") as f:       # Если файла нет или файл пустой, то выводит 0 рублей
        try:
            data = json.load(f)
            if not data["balance"]:
                click.echo("0 рублей")
            click.echo(f'{data["balance"]} рублей')
        except:
            click.echo("0 рублей")


@click.command()
@click.option("-c", "--category", prompt="Выберите категорию", type=click.Choice(CATEGORIES.keys()), help="Категория")
@click.option("-s", "--summ", prompt="Введите сумму", type=int, help="Сумма")
@click.option("-d", "--desc", prompt="Описание", help="Описание")
def add(summ, desc, category):
    """Добавить запись"""
    with open("data.json", "r") as f:
        data = json.load(f)
        if category == "+":                          # Команда для добавления записи в data.json
            data["balance"] += summ                  # Если категория "+", то баланс увеличивается
        elif category == "-":                        # Если категория "-", то баланс уменьшается
            data["balance"] -= summ                  # Если категория "-" и баланс меньше нуля, то выводится сообщение
            if data["balance"] < 0:
                click.echo("Недостаточно средств")
                return
        else:
            click.echo("Неизвестная категория")
            return
        new_id = len(data["list"]) + 1

        for nt in data["list"]:
            while new_id == nt["id"]:
                new_id += 1

        note = {                                            # Создаем словарь с данными для записи в data.
            "id": new_id,                                   # ID записи
            "date": datetime.now().strftime("%Y_%m_%d"),    # Дата
            "category": CATEGORIES[category],               # Категория (+ или -)
            "summ": summ,                                   # Сумма
            "description": desc                             # Описание
        }

        data["list"].append(note)

    with open("data.json", "w") as f:                       # Записываем изменения в data.json
        json.dump(data, f)

    note_ru = (f'"id": {note["id"]}, "Дата": "{note["date"]}", "Категория": {note["category"]}, '
               f'"Сумма": {note["summ"]}, "Описание": "{note["description"]}"')

    click.echo("Запись добавлена")
    click.echo(note_ru)                                     # Выводим добавленную запись на русском языке
    click.echo(f"Ваш баланс {data['balance']} рублей")


@click.command()
@click.option("-id", type=int, prompt="Введите id записи", help="ID записи")
@click.option("-c", "--category", prompt="Выберите категорию", type=click.Choice(CATEGORIES.keys()), help="Категория")
@click.option("-s", "--summ", prompt="Введите сумму", type=int, help="Сумма")
@click.option("-d", "--desc", prompt="Описание", help="Описание")
def update(id, summ, desc, category):               # Команда для изменения записи в data.json
    """Изменить запись"""
    with open("data.json", "r") as f:               # Открываем data.json
        data = json.load(f)

        if not data["list"]:                        # Если список пуст, то выводится сообщение
            click.echo("Список пуст")
            return

        for item in data["list"]:
            if item["id"] == id:
                note = item
            else:                                   # Если запись не найдена, то выводится сообщение
                click.echo("Нет такой записи")
                return
        if note["category"] == CATEGORIES['+']:     # Если категория "+", то сумма старой записи вычитается из баланса
            data["balance"] -= note["summ"]
        elif note["category"] == CATEGORIES['-']:   # Если категория "-", то сумма старой записи добавляется в баланс
            data["balance"] += note["summ"]

        date = note["date"]

        data["list"].pop(id - 1)                    # Удаляем старую запись

        if category == "+":                         # Если категория "+", то сумма новой записи добавляется в баланс
            data["balance"] += summ
        elif category == "-":                       # Если категория "-", то сумма новой записи вычитается из баланса
            data["balance"] -= summ
            if data["balance"] < 0:                 # Если баланс меньше нуля, то выводится сообщение
                click.echo("Недостаточно средств")
                return
        else:                                       # Если категория не известна, то выводится сообщение
            click.echo("Неизвестная категория")
            return

        new_note = {                                # Создаем словарь с данными для записи в data.json
            "id": id,
            "date": date,
            "category": CATEGORIES[category],
            "summ": summ,
            "description": desc
        }

        data["list"].append(new_note)               # Записываем изменения в data.json

    with open("data.json", "w") as f:
        json.dump(data, f)

    note_ru = (f'"id": {note["id"]}, "Дата": "{note["date"]}", "Категория": {note["category"]}, '
               f'"Сумма": {note["summ"]}, "Описание": "{note["description"]}"')
    new_note_ru = (f'"id": {new_note["id"]}, "Дата": "{new_note["date"]}", "Категория": {new_note["category"]}, '
                   f'"Сумма": {new_note["summ"]}, "Описание": "{new_note["description"]}"')

    click.echo("Запись обновлена")                      # Выводим обновленную запись на русском языке
    click.echo(note_ru)                                 # Выводим старую запись на русском языке
    click.echo("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    click.echo(new_note_ru)                             # Выводим обновленную запись на русском языке
    click.echo(f"Ваш баланс {data['balance']} рублей")  # Выводим баланс на русском языке


@click.command()
@click.option("-id", type=int, prompt="Введите id записи", help="ID записи", default=0)
@click.option("-c", "--category", prompt="Выберите категорию (+, -)", help="Категория", default="")
@click.option("-s", "--summ", prompt="Введите сумму", type=int, help="Сумма", default=0)
@click.option("-d", "--date", prompt="Введите дату", help="Дата", default="-")
def list(id, category, date, summ):             # Команда выводит список записей соответствующих условиям
    """Список записей"""
    with open("data.json", "r") as f:           # Открываем data.json
        data = json.load(f)
        if not data["list"]:                    # Если список пуст, то выводится сообщение
            click.echo("Список пуст")
            return
        if id == 0:                             # Если id равен 0, то выводится список всех записей
            if category == "":                  # Если категория равна "", то выводится список всех записей
                if summ == 0:                   # Если сумма равна 0, то выводится список всех записей
                    if date == "-":             # Если дата равна "-", то выводится список всех записей
                        data["list"].sort(key=lambda x: x["id"])
                        for note in data["list"]:
                            note_ru = (f'"id": {note["id"]}, "Дата": "{note["date"]}", "Категория": {note["category"]}, '
                                       f'"Сумма": {note["summ"]}, "Описание": "{note["description"]}"')

                            click.echo(note_ru)

                    else:                       # Если дата не равна "-", то выводится список записей с заданной датой
                        for item in data["list"]:
                            if item["date"] == date:    # Если дата совпадает с заданной, то выводится запись
                                note_ru = (
                                    f'"id": {item["id"]}, "Дата": "{item["date"]}", "Категория": {item["category"]}, '
                                    f'"Сумма": {item["summ"]}, "Описание": "{item["description"]}"')
                                click.echo(note_ru)

                            else:                       # Если дата не совпадает с заданной
                                continue

                else:                            # Если сумма не равна 0, то выводится список записей с заданной суммой
                    for item in data["list"]:
                        if item["summ"] == summ:  # Если сумма совпадает с заданной, то выводит запись
                            note_ru = (f'"id": {item["id"]}, "Дата": "{item["date"]}", "Категория": {item["category"]},'
                                       f' "Сумма": {item["summ"]}, "Описание": "{item["description"]}"')
                            click.echo(note_ru)
                        else:                   # Если сумма не совпадает
                            continue

            elif category == "+":               # Если категория Доход, выводятся соответствующие записи
                for item in data["list"]:
                    if item["category"] == "Доход":
                        note_ru = (f'"id": {item["id"]}, "Дата": "{item["date"]}", "Категория": {item["category"]}, '
                                   f'"Сумма": {item["summ"]}, "Описание": "{item["description"]}"')
                        if summ == 0:           # Если сумма равна 0, то выводятся соответствующие записи с любой суммой
                            click.echo(note_ru)
                        else:               # Если сумма не равна 0, то выводятся соответствующие записи с равной суммой
                            if item["summ"] == summ:
                                click.echo(note_ru)
                            else:           # Если заданной суммы нет
                                continue
                    else:
                        continue
            elif category == "-":           # Если категория Расход, выводятся соответствующие записи
                for item in data["list"]:
                    if item["category"] == "Расход":
                        note_ru = (f'"id": {item["id"]}, "Дата": "{item["date"]}", "Категория": {item["category"]}, '
                                   f'"Сумма": {item["summ"]}, "Описание": "{item["description"]}"')
                        if summ == 0:       # Если сумма равна 0, то выводятся соответствующие записи с любой суммой
                            click.echo(note_ru)
                        else:               # Если сумма не равна 0, то выводятся соответствующие записи с равной суммой
                            if item["summ"] == summ:
                                click.echo(note_ru)
                            else:           # Если заданной суммы нет
                                continue
                    else:
                        continue
            else:       # Если категория не соответствует условиям
                click.echo("Неизвестная категория")
                return

        else:           # Если id не раен 0, то выводится запись с заданным id
            for item in data["list"]:
                if item["id"] == id:
                    note = item
                else:     # Если записи с заданный id нет
                    continue
            note_ru = (f'"id": {note["id"]}, "Дата": "{note["date"]}", "Категория": {note["category"]}, '
                       f'"Сумма": {note["summ"]}, "Описание": "{note["description"]}"')
            click.echo(note_ru)

        click.echo(f"Ваш баланс {data['balance']} рублей")      # Выводим баланс на русском языке
        return


@click.command()
@click.option("-id", type=int, prompt="Введите id записи", help="ID записи")
def delete(id):                                                 # Команда удаляет запись с заданным id
    """Удалить запись"""
    with open("data.json", "r") as f:                           # Открываем data.json
        data = json.load(f)

        if not data["list"]:                                    # Если список пуст, то выводится сообщение
            click.echo("Список пуст")
            return

        for item in data["list"]:
            if item["id"] == id:                                # Если id совпадает с заданным, то удаляется запись
                note = item
            else:                                               # Если id не совпадает с заданным
                click.echo("Нет такой записи")
                return
        if note["category"] == CATEGORIES['+']:                 # Если категория Доход, то сумма вычитается из баланса
            data["balance"] -= note["summ"]
        elif note["category"] == CATEGORIES['-']:               # Если категория Расход, то сумма прибавляется к балансу
            data["balance"] += note["summ"]

        data["list"].pop(id - 1)
        with open("data.json", "w") as f:                       # Записываем изменения в data.json
            json.dump(data, f)
        note_ru = (f'"id": {note["id"]}, "Дата": "{note["date"]}", "Категория": {note["category"]}, '
                   f'"Сумма": {note["summ"]}, "Описание": "{note["description"]}"')

        click.echo(note_ru)                                     # Выводим удаленную запись на русском языке
        click.echo(f"Запись удалена")
        click.echo(f"Ваш баланс {data['balance']} рублей")      # Выводим баланс на русском языке


my_commands.add_command(balance)
my_commands.add_command(add)
my_commands.add_command(update)                                 # Добавляем команды в my_commands
my_commands.add_command(list)
my_commands.add_command(delete)

if __name__ == "__main__":                                      # Если запускается как главный файл
    my_commands()
