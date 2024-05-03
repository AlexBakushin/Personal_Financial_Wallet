import json


def full_data():
    data_json = {
        "balance": 530,
        "list": [
            {
                "id": 1,
                "date": "2024_05_03",
                "category": "\u0414\u043e\u0445\u043e\u0434",
                "summ": 1000,
                "description": "\u0417\u0430\u0440\u043f\u043b\u0430\u0442\u0430"
            },
            {
                "id": 2,
                "date": "2024_05_03",
                "category": "\u0420\u0430\u0441\u0445\u043e\u0434",
                "summ": 20,
                "description": "\u041f\u0440\u043e\u0435\u0437\u0434 \u043c\u0435\u0442\u0440\u043e"
            },
            {
                "id": 3,
                "date": "2024_05_03",
                "category": "\u0420\u0430\u0441\u0445\u043e\u0434",
                "summ": 300,
                "description": "\u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b"
            },
            {
                "id": 4,
                "date": "2024_05_03",
                "category": "\u0420\u0430\u0441\u0445\u043e\u0434",
                "summ": 200,
                "description": "\u0412\u0435\u0440\u043d\u0443\u043b \u0434\u043e\u043b\u0433"
            },
            {
                "id": 5,
                "date": "2024_05_03",
                "category": "\u0414\u043e\u0445\u043e\u0434",
                "summ": 500,
                "description": "\u041d\u0430\u0448\u0435\u043b \u0437\u0430\u043d\u0430\u0447\u043a\u0443"
            },
            {
                "id": 6,
                "date": "2024_05_03",
                "category": "\u0420\u0430\u0441\u0445\u043e\u0434",
                "summ": 450,
                "description": "\u041a\u0432\u0430\u0440\u0442\u043f\u043b\u0430\u0442\u0430"
            }
        ]
    }
    with open("data.json", "w") as f:  # Записываем изменения в data.json
        json.dump(data_json, f)


if __name__ == "__main__":
    full_data()
