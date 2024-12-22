import requests
import json

with open("Acil.json", "r", encoding="utf-8") as fp:
    acil_json = json.load(fp)

book_id = 1
transformed_list = [
    {
        "nth_sentence": str(index + 1),
        "book_id": str(book_id),
        "sentence": sentence,
        "transcript": ",".join(files),
    }
    for index, (sentence, files) in enumerate(acil_json.items())
]

print("transformde", transformed_list)
for data in transformed_list:
    print("data içerde")
    deneme = requests.post(
        "http://127.0.0.1:2020/v1.0/book_contents/add_sentence", json=data)

    print("deneme", deneme)
