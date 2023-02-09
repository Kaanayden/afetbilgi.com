import pandas as pd
import json

city_map = {
    'tr': ['Adana', 'Gaziantep', 'Malatya', 'Diyarbakır', 'Şanlıurfa', 'Kahramanmaraş', 'Osmaniye', 'Adıyaman', 'Kilis', 'Mardin', 'Hatay', 'Amasya', 'Ankara', 'Antalya', 'Balıkesir', 'Bayburt', 'Bitlis', 'Bursa', 'Denizli', 'Erzurum', 'Eskişehir', 'Kayseri', 'Kırklareli', 'Konya', 'Kütahya', 'Mersin', 'Muğla', 'Muş', 'Nevşehir', 'Rize', 'Sakarya', 'Sivas', 'Şırnak', 'Trabzon', 'Uşak', 'Van'],
    'en': ['Adana', 'Gaziantep', 'Malatya', 'Diyarbakır', 'Şanlıurfa', 'Kahramanmaraş', 'Osmaniye', 'Adıyaman', 'Kilis', 'Mardin', 'Hatay', 'Amasya', 'Ankara', 'Antalya', 'Balıkesir', 'Bayburt', 'Bitlis', 'Bursa', 'Denizli', 'Erzurum', 'Eskişehir', 'Kayseri', 'Kırklareli', 'Konya', 'Kütahya', 'Mersin', 'Muğla', 'Muş', 'Nevşehir', 'Rize', 'Sakarya', 'Sivas', 'Şırnak', 'Trabzon', 'Uşak', 'Van'],
    'ku': ['Adana- Edene', 'Gaziantep- Dîlok', 'Malatya- Meletî', 'Diyarbakır- Amed', 'Şanlıurfa- Riha', 'Kahramanmaraş- Gurgum', 'Osmaniye', 'Adıyaman- Semsûr', 'Kilis- Kilîs', 'Mardin- Mêrdîn', 'Hatay- Xetay', 'Amasya', 'Ankara- Enqere', 'Antalya', 'Balıkesir', 'Bayburt', 'Bitlis- Bedlîs', 'Bursa', 'Denizli', 'Erzurum- Erzêrom', 'Eskişehir', 'Kayseri- Qeyserî', 'Kırklareli', 'Konya- Qonye', 'Kütahya', 'Mersin- Mêrsîn', 'Muğla', 'Muş- Mûş', 'Nevşehir', 'Rize', 'Sakarya', 'Sivas- Sêwas', 'Şırnak-Şirnex', 'Trabzon', 'Uşak', 'Van- Wan']
}

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj




if __name__ == "__main__":
    sheet_id = "1La7CSZYBkpO_jvIe6Xs252VQPp_tVx1ioOWYvzyRK_k"
    sheet_name = "Veterinerler"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    json_name = "../datasets/veteriner.json"
    df = pd.read_csv(url, encoding="utf-8")

    print(df)
    df = df.rename(columns={
        "Şehir": "city",
        "İsim": "name",
        "Telefon": "phone_number",
        "Konum": "address",
        "Konum Linki": "maps_link",
    })

    cities = df['city'].unique()

    json_obj = {
        "type": "question",
        "text": "Hangi şehirde veteriner arıyorsunuz?",
        "options": [
            {
                "name": city,
                "value": None,
            } for city in cities
        ]
    }


    for city in cities:
        city_df = df[df['city'] == city]
        city_df = city_df.drop(columns=['city'])
        city_dict = city_df.to_dict(orient='records')
        city_dict = todict(city_dict)

        for option in json_obj['options']:
            if option['name'] == city:
                city_name = city.strip()

                option['name_tr'] = city_map['tr'][city_map['tr'].index(city_name)]
                option['name_en'] = city_map['en'][city_map['tr'].index(city_name)]
                option['name_ku'] = city_map['ku'][city_map['tr'].index(city_name)]

                option['value'] = {
                    "type": "data",
                    "data": {
                        "dataType": "data-vet",
                        "city": city,
                        "vets": city_dict
                    }
                }
                continue

    for option in json_obj['options']:
        del option['name']

    with open(json_name, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=4)
