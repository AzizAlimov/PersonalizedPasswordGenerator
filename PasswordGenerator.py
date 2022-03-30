import random
from MarkovModel import MarkovModel
from Password import Password

'''
Class for a password generator that uses the markov model, categories, numbers and emoticons to
generate passwords
'''
class PasswordGenerator:
    generatedPasswordHistory: dict = {}
    markovchain: MarkovModel
    numbers: list
    emoticons: list

    def __init__(self, categories, word_choices, numbers, emoticons):
        self.markovchain = MarkovModel(categories)
        self.markovchain.update_probabilities(word_choices)
        self.numbers = numbers
        self.emoticons = emoticons

    def generatePassword(self, word2vec) -> Password:
        while True:
            password = Password()
            categories = self.markovchain.sample(3)
            components = [(word2vec.getWordInCategory(0.8, category), category) for category in categories]

            num_index = random.randint(0, len(components))
            number = (self.numbers[random.randint(0, len(self.numbers) - 1)], "number")
            components.insert(num_index, number)

            emoticon_index = random.randint(0, len(components))
            emoticon = (self.emoticons[random.randint(0, len(self.emoticons) - 1)], "emoticon")
            components.insert(emoticon_index, emoticon)

            if emoticon_index <= num_index:
                num_index += 1

            for index, component in enumerate(components):
                if index == num_index:
                    password.addNumber(component[0])
                elif index == emoticon_index:
                    password.addEmoticon(component[0])
                else:
                    password.addWord(component[0], component[1])

            if password not in self.generatedPasswordHistory:
                self.generatedPasswordHistory[password.password] = password
                return password

    def chosen_password(self, password: str):
        password = self.generatedPasswordHistory[password]
        categories = [word[1] for word in password.words]
        self.markovchain.update_probabilities(categories)

    def unchosen_password(self, password: str):
        pass
