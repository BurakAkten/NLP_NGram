from collections import *
from random import random
import pprint
import operator
import pickle


class NGram:

    def __init__(self, filePath , syllableOrChar):
        self.__type = syllableOrChar.lower()
        self.__model = []
        self.__data = ""
        self.__path = filePath
        self.__readData()
        self.__unk = {"UNK" : 0}
        self.__n = 0
        self.__probability = 1

    def __readData(self):
        print("Reading Data...")
        file = open(self.__path)

        self.__data =file.read()

        file.close()

    def __process_text(self , text):

        text = text.lower()
        text = text.replace(',', ' ')
        text = text.replace('/', ' ')
        text = text.replace('(', ' ')
        text = text.replace(')', ' ')
        text = text.replace('\'' , ' ')
        text = text.replace('\"' , '')
        text = text.replace('.' , ' ')
        text = text.replace(':' , ' ')



        # Convert text string to a list of words
        return text

    def __generate_ngrams_for_syllable(self, words_list, n):
        ngrams_list = list()
        print("Processing...")
        for num in range(0, len(words_list)):
            ngram = ' '.join(words_list[num:num + n])
            ngrams_list.append(ngram)
        return ngrams_list

    def __generate_ngrams_for_char(self , data, n):
        ngrams_list = list()
        print("Processing...")
        for i in range(len(data)):
            ngram = ''.join(data[i:i + n])
            ngrams_list.append(ngram)
        return ngrams_list

    def __create_word_all_grams_with_probabilies(self ,data,n, function):
        print("Model is creating...")
        #all_grams = list()

        #for i in range(1,n + 1): # for find the all n grams 1,2,3,...n gram into model
        n_grams = function(data,n)
        n_counts = Counter(n_grams)
        print("N-Grams created...")
        probs = {gram : (n_counts[gram] + 1)/(len(n_counts) + len(data)) for gram in n_counts.keys()} # n_1_counts[''.join(gram[:-1])]
        #probs = {gram : (n_counts[gram])/(len(n_counts)) for gram in n_counts.keys()} # n_1_counts[''.join(gram[:-1])]

        self.__model.append(probs)
        print("Model is created...")
        return self.__model #, sorted_grams

    def __syllable_perplexity(self , data):

        tokens = data.split()
        power = len(tokens)

        prob = self.__syllable_probability(data)
        result = (1 / prob) ** (1 / (1 + power - self.__n))
        return result

    def __char_perp(self , text):


        power = len(text)

        prob =self.__character_probability(text)

        return (1 / prob) ** (1 / (1 + power - self.__n))



    def __character_probability(self , text):
        self.__unk = {"UNK" : 0}
        result = 1.0
        power = len(text)
        for i in range(1 + power - self.__n):
            next_gram = ''.join(text[i:i + self.__n])
            if(self.__model[0].get(next_gram) == None):
                result *= (self.__unk.get("UNK") + 1) / len(self.__model[0])
                self.__unk["UNK"] = self.__unk.get("UNK") + 1
            else:
                result *= self.__model[0].get(next_gram)
        self.__probability = result
        return result


    def __syllable_probability(self , data):
        self.__unk = {"UNK" : 0}
        result = 1.0
        #print(data)
        tokens = data.split()
        power = len(tokens)
        next_gram = ""
        for i in range(1 + power - self.__n):
            next_gram = ' '.join(tokens[i:i + self.__n])
            if (self.__model[0].get(next_gram) == None):
                result *= (self.__unk.get("UNK") + 1) / len(self.__model[0])
                self.__unk["UNK"] = self.__unk.get("UNK") + 1
            else:
                result *= self.__model[0].get(next_gram)

        self.__probability = result
        return result


    def save_model(self, name ):
        print("{}-Gram model is saving...".format(self.__n))
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print("The model saved..")

    def load_model(name):
        print("N-Gram model is loading...")
        with open(name + '.pkl', 'rb') as f:
            print("The model is loaded...")
            return pickle.load(f)


    def create_NGram(self , n = 3):
        print("{} {}-Gram model is creating...".format(self.__type,n))
        self.__n = n

        if(self.__type == "character"):
            return self.__create_word_all_grams_with_probabilies(
                             self.__process_text(self.__data),
                             n,
                             function = self.__generate_ngrams_for_char)
        else:
            data = self.__process_text(self.__data)
            data = data.replace("-" , " ")
            data = data.split()
            return self.__create_word_all_grams_with_probabilies(
                            data,
                            n,
                            function = self.__generate_ngrams_for_syllable)

    def perplexity_of(self , text):
        text = text.lower()
        if(self.__type == "character"):
            return "The perplexity of the character type {}-gram for the given text : {}".format(self.__n,self.__char_perp(text))
        else:
            syllables = Syllable(text).get_all_syllables()
            syllables_text = ' '.join(syllables)
            return "The perplexity of the syllable type {}-gram for the given text : {}".format(self.__n,self.__syllable_perplexity(syllables_text.replace("-" , " ")))#for syllable

    def probability_of(self , text):
        text = text.lower()

        if(self.__type == "character"):
            return "The probability of the character type {}-gram for the given text : {}".format(self.__n,self.__character_probability(text))
        else:
            syllables = Syllable(text).get_all_syllables()
            syllables_text = ' '.join(syllables)
            return "The probability of the syllable type {}-gram for the given text : {}".format(self.__n,self.__syllable_probability(syllables_text.replace("-" , " ")))#for syllable

    def getModel_info(self):
        return self.__model

class Syllable:
    def __init__(self , text):
        self.__words = text.split()

    #Reference for this method : https://gist.github.com/miratcan/9196ae2591b1f34ab645520a767ced17
    def __get_syllables_word(self , word):
        syllables = []

        """
        Aşağıdaki satır gelen kelimenin ünlü harfler 1, ünsüzler 0 olacak
        şekilde desenini çıkarır.
        Örneğin: arabacı -> 1010101, türkiye -> 010010
        """

        bits = ''.join(['1' if l in 'aeıioöuü' else '0' for l in word])

        """
        Aşağıdaki seperators listesi, yakalanacak desenleri ve desen yakalandığında
        kelimenin hangi pozisyondan kesileceğini tanımlıyor.
        Türkçede kelime içinde iki ünlü arasındaki ünsüz, kendinden sonraki
        ünlüyle hece kurar., yani 101 desenini yakaladığımızda kelimeyi
        bulunduğumuz yerden 1 ileri pozisyondan kesmeliyiz. ('101', 1)
        Kelime içinde yan yana gelen iki ünsüzden ilki kendinden önceki ünlüyle,
        ikincisi kendinden sonraki ünlüyle hece kurar. Bu da demek oluyor ki
        1001 desenini yakaladığımızda kelimeyi bulunduğumuz noktadan 2 ileriden
        kesmeliyiz. ('1001', 2),
        Kelime içinde yan yana gelen üç ünsüz harften ilk ikisi kendinden önceki
        ünlüyle, üçüncüsü kendinden sonraki ünlüyle hece kurar. Yani 10001 desenini
        gördüğümüzde kelimeyi bulunduğumuz yerden 3 ileri pozisyondan kesmemiz
        gerek. ('10001', 3)
        """

        seperators = (
            ('101', 1),
            ('1001', 2),
            ('10001', 3)
        )

        index, cut_start_pos = 0, 0

        # index değerini elimizdeki bitler üzerinde yürütmeye başlıyoruz.
        while index < len(bits):

            """
            Elimizdeki her ayırıcıyı (seperator), bits'in index'inci karakterinden
            itibarent tek tek deneyerek yakalamaya çalışıyoruz.
            """

            for seperator_pattern, seperator_cut_pos in seperators:
                if bits[index:].startswith(seperator_pattern):

                    """
                    Yakaladığımızda, en son cut_start posizyonundan, bulunduğumuz
                    pozisyonun serpator_cut_pos kadar ilerisine kadar bölümü alıp
                    syllables sepetine atıyoruz.
                    """

                    syllables.append(word[cut_start_pos:index + seperator_cut_pos])

                    """
                    Index'imiz seperator_cut_pos kadar ilerliyor, ve
                    cut_start_pos'u index'le aynı yapıyoruz.
                    """

                    index += seperator_cut_pos
                    cut_start_pos = index
                    break

            """
            Index ilerliyor, cut_start_pos'da değişiklik yok.
            """

            index += 1

        # Son kalan heceyi elle sepete atıyoruz.
        syllables.append(word[cut_start_pos:])
        return '-'.join(syllables)
    def get_all_syllables(self):
        return [self.__get_syllables_word(word) for word in self.__words]
