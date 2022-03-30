import os

from fastapi import FastAPI
from pydantic import BaseModel
from PasswordManager import PasswordManager
import random
import uvicorn

app = FastAPI()
manager = PasswordManager()
colors = ["A8E6CE", "DCEDC2", "FFD3B5", "FFAAA6", "FF8C94"]

class WordcloudChoices(BaseModel):
    choices: list

class PasswordChoice(BaseModel):
    selected_password: str
    unselected_passwords: list

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/getWords/")
async def get_words(number: int = 10):
    words = manager.getWordsInCategory(number, 0.8)
    return_words = []
    id = 1
    categories = list(words.keys())
    random.shuffle(categories)
    for i, key in enumerate(categories):
        for word in words[key]:
            return_words.append({'name': word, 'id': id, 'size': 150, 'fillColor': colors[i]})
            id += 1

    return return_words



@app.post("/buildModel/")
async def build_model(choices: WordcloudChoices, client_id: int = 1):
    manager.add_client(choices.choices, client_id)

@app.get("/generatePassword/")
async def generate_passwords(client_id: int = 1, n: int = 1):
    return manager.generate_passwords(client_id, n)


@app.put("/selected/")
async def selected_password(choice: PasswordChoice, client_id: int = 1):
    manager.selected_password(choice.selected_password, client_id)
    for unselected in choice.unselected_passwords:
        manager.unselected_password(unselected, client_id)


port = int(os.environ.get("PORT", 8000))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
