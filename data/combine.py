import json

data_points = [
  { 'name': 'Geçici Barınma Alanları', 'path': 'combined/barinma.json' },
  { 'name': 'Güvenli Toplanma Alanları', 'path': 'combined/toplanma.json' },
  { 'name': 'Para Bağışı İmkanları', 'path': 'combined/bagis.json' },
  { 'name': 'Eşya Bağışı İmkanları', 'path': 'combined/yardim_toplama_merkezleri.json' },
  { 'name': 'Kızılay Kan Bağış Noktaları', 'path': 'combined/blood.json' },
  { 'name': 'Önemli Telefon Numaraları', 'path': 'combined/telefon.json' },
  { 'name': 'Önemli Web Siteleri', 'path': 'faydali_linkler.json' },
  { 'name': 'Faydalı Yazılar', 'path': 'yazilar.json' },
  { 'name': 'Faydalı Yazılar', 'path': 'yazilar.json' },
  { 'name': 'Kök Hücre Bağış Noktaları', 'path': 'kokhucre.json' },
]

result = {
    'type': 'question',
    'text': 'Lütfen bilgi almak istediğiniz konuyu seçiniz.',
    'options': []
}

for data_point in data_points:
    with open(f"{data_point['path']}", "r", encoding="utf-8") as f:
        text = f.read().encode("utf-8")

        data = json.loads(text)

        result['options'].append({
            'name': data_point['name'],
            'value': data,
        })

print(json.dumps(result, ensure_ascii=False))

