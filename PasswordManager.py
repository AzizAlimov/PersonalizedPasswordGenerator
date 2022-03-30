from word2vec import word2vec
from PasswordGenerator import PasswordGenerator

class PasswordManager:
    categories: list = ["animals", "clothes", "sports", "games", "food"]
    word_similarity = word2vec()
    client_models: dict = {}

    def getWordsInCategory(self, number, cutoff):
        return self.word_similarity.getWordsInCategory(number, cutoff, self.categories)

    def get_client(self, client_id: int = 1):
        return client_models[client_id]

    def add_client(self, choices: list, client_id: int = 1):
        word_choices = choices[:10]
        emoticons = choices[10:12]
        numbers = choices[12:14]
        self.client_models[client_id] = PasswordGenerator(self.categories, word_choices, numbers, emoticons)

    def generate_passwords(self, client_id: int = 1, number_passwords: int = 1):
        model = self.client_models[client_id]
        passwords = []
        for _ in range(number_passwords):
            passwords.append(model.generatePassword(self.word_similarity).password)
        return passwords

    def selected_password(self, password, client_id):
        generator = self.client_models[client_id]
        generator.chosen_password(password)

    def unselected_password(self, password, client_id):
        generator = self.client_models[client_id]
        generator.unchosen_password(password)
