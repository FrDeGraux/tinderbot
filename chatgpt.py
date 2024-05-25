API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
import os
from dotenv import load_dotenv
import dialog
env_path = '/home/frank/Documents/Tokens/.env'
load_dotenv(dotenv_path=env_path)

import requests
env_path = '/home/frank/Documents/Tokens/.env'

# System message
AI_SYSTEM_MESSAGE = "You are a helpful assistant"

# Initialize message history with system message
API_KEY =os.getenv('OPENAPI_KEY')
import time
class ChatGPTCustom :

    def __init__(self) :
        self.message_history = [{"role": "system", "content": AI_SYSTEM_MESSAGE}]

    def invoke_chatgpt_sleep(self,message_history):

        return self.invoke_chatgpt(message_history)
    def invokegpt_first(self):

          res = ["Je suis vraiment content que tu sois curieuse à propos de mon travail. C'est un domaine assez complexe et technique, mais j'aime beaucoup ce que je fais. C'est toujours intéressant de résoudre des problèmes et de trouver des solutions. Et toi, comment trouves-tu ton travail au SPF Ag Fisc ? Est-ce que c'est quelque chose que tu as toujours voulu faire ?Quant à mon histoire de célibataire, je dirais que je ne suis pas quelqu'un qui court après les relations. Je préfère prendre mon temps et laisser les choses se développer naturellement. Je crois que chaque relation est unique et qu'elle doit être nourrie avec soin et attention. Je suis sur Tinder depuis peu, j'essaie de voir si je peux faire de belles rencontres ici. Et toi, qu'est-ce qui t'a poussé à te joindre à l'application ? Et oui, tu as raison de dire que j'apprécie l'humour, l'intelligence et la communication chez une femme. J'ajouterais également l'honnêteté et la loyauté à cette liste. Je crois que ces valeurs sont essentielles pour construire une relation solide et durable. Et toi, quelles sont les qualités que tu apprécies chez un homme ?\n\nEnfin, je me demandais si tu avais déjà visité Bruxelles ? J'y ai vécu pendant un certain temps et je pense que c'est une ville magnifique avec beaucoup de choses à offrir. Si tu n'y es jamais allée, peut-être pourrions-nous y aller ensemble un jour ? Qu'en penses-tu ?",
            "D'autant plus, peut-être quelqu'un qui est aussi à l'aise avec l'idée de passer une soirée tranquille à la maison ou de sortir découvrir de nouvelles choses. J'imagine que tu n'es pas du genre à te contenter de la routine habituelle ? Ah, je suis curieux de savoir ce qui, selon toi, fait qu'une relation est réussie. Qu'est-ce qui, à ton avis, est le plus important pour maintenir une relation heureuse et saine ?",
            "Je suis vraiment ravi d'apprendre que tu es liégeoise d'origine. C'est une ville dynamique et j'adore déjà l'ambiance ici. Quant à mon histoire, je dirais qu'elle est assez typique pour un geek des maths comme moi. J'ai toujours été fasciné par les chiffres et la manière dont ils peuvent être utilisés pour résoudre des problèmes. Mon travail me donne l'occasion de faire ça tous les jours, donc oui, je l'aime beaucoup.\n\nJe suis célibataire depuis trois mois maintenant. Ma dernière relation n'a pas duré très longtemps mais elle m'a appris beaucoup sur moi-même et sur ce que je recherche chez un partenaire. J'aime les gens qui sont authentiques, ouverts d'esprit et qui ont un sens de l'humour. J'apprécie également les personnes qui sont ambitieuses et qui ont une passion pour ce qu'elles font.\n\nPour ce qui est de mon temps libre, j'aime faire du sport, surtout du taekwondo, lire des livres et passer du temps avec mes amis. J'aime aussi beaucoup voyager et découvrir de nouveaux endroits. Et toi, qu'est-ce que tu aimes faire pendant ton temps libre ? Quels sont tes hobbies favoris ?"]

          return res
    def invokegpt_second(self):

          res = ["Je suis vraiment content que tu sois curieuse à propos de mon travail. C'est un domaine assez complexe et technique, mais j'aime beaucoup ce que je fais. C'est toujours intéressant de résoudre des problèmes et de trouver des solutions. Et toi, comment trouves-tu ton travail au SPF Ag Fisc ? Est-ce que c'est quelque chose que tu as toujours voulu faire ?Quant à mon histoire de célibataire, je dirais que je ne suis pas quelqu'un qui court après les relations. Je préfère prendre mon temps et laisser les choses se développer naturellement. Je crois que chaque relation est unique et qu'elle doit être nourrie avec soin et attention. Je suis sur Tinder depuis peu, j'essaie de voir si je peux faire de belles rencontres ici. Et toi, qu'est-ce qui t'a poussé à te joindre à l'application ? Et oui, tu as raison de dire que j'apprécie l'humour, l'intelligence et la communication chez une femme. J'ajouterais également l'honnêteté et la loyauté à cette liste. Je crois que ces valeurs sont essentielles pour construire une relation solide et durable. Et toi, quelles sont les qualités que tu apprécies chez un homme ?\n\nEnfin, je me demandais si tu avais déjà visité Bruxelles ? J'y ai vécu pendant un certain temps et je pense que c'est une ville magnifique avec beaucoup de choses à offrir. Si tu n'y es jamais allée, peut-être pourrions-nous y aller ensemble un jour ? Qu'en penses-tu ?",
            "D'autant plus, peut-être quelqu'un qui est aussi à l'aise avec l'idée de passer une soirée tranquille à la maison ou de sortir découvrir de nouvelles choses. J'imagine que tu n'es pas du genre à te contenter de la routine habituelle ? Ah, je suis curieux de savoir ce qui, selon toi, fait qu'une relation est réussie. Qu'est-ce qui, à ton avis, est le plus important pour maintenir une relation heureuse et saine ?",
            "Je suis vraiment ravi d'apprendre que tu es liégeoise d'origine. C'est une ville dynamique et j'adore déjà l'ambiance ici. Quant à mon histoire, je dirais qu'elle est assez typique pour un geek des maths comme moi. J'ai toujours été fasciné par les chiffres et la manière dont ils peuvent être utilisés pour résoudre des problèmes. Mon travail me donne l'occasion de faire ça tous les jours, donc oui, je l'aime beaucoup.\n\nJe suis célibataire depuis trois mois maintenant. Ma dernière relation n'a pas duré très longtemps mais elle m'a appris beaucoup sur moi-même et sur ce que je recherche chez un partenaire. J'aime les gens qui sont authentiques, ouverts d'esprit et qui ont un sens de l'humour. J'apprécie également les personnes qui sont ambitieuses et qui ont une passion pour ce qu'elles font.\n\nPour ce qui est de mon temps libre, j'aime faire du sport, surtout du taekwondo, lire des livres et passer du temps avec mes amis. J'aime aussi beaucoup voyager et découvrir de nouveaux endroits. Et toi, qu'est-ce que tu aimes faire pendant ton temps libre ? Quels sont tes hobbies favoris ?"]

          return res

    [
        "Certainement, je pense que vous êtes quelqu'un qui est à l'aise que ce soit pour passer une soirée tranquille à la maison, ou pour sortir et découvrir de nouvelles choses. Je me permets de supposer que vous n'êtes pas du genre à vous contenter de la routine habituelle ? Je serais vraiment ravi d'entendre votre point de vue sur ce qui, selon vous, contribue à la réussite d'une relation. Qu'est-ce qui, à votre avis, est le plus important pour maintenir une relation heureuse et saine ?",
        "Pourrais-je suggérer, avec beaucoup de respect, que vous pourriez être quelqu'un qui est aussi à l'aise avec l'idée de passer une soirée tranquille à la maison que de sortir pour découvrir de nouvelles choses. Est-ce que je me trompe en pensant que vous n'êtes pas du genre à vous contenter de la routine habituelle ? Si vous me le permettez, j'aimerais beaucoup savoir ce qui, selon vous, fait qu'une relation est réussie. Pourriez-vous, si cela ne vous dérange pas, partager avec moi ce qui, à votre avis, est le plus important pour maintenir une relation heureuse et saine ?",
        'Bien sûr, je serais ravi de vous aider à reformuler votre message de façon plus polie :\n\n"De surcroît, je me demandais si, comme moi, vous appréciez autant une soirée tranquille à la maison que la découverte de nouvelles expériences. J\'ai l\'impression, et veuillez me corriger si je me trompe, que vous n\'êtes pas du genre à vous satisfaire de la routine habituelle. Si cela ne vous dérange pas, j\'aimerais connaître votre avis sur ce qui fait, d\'après vous, qu\'une relation est réussie. Quels éléments considérez-vous comme essentiels pour maintenir une relation heureuse et saine ?"']
    def invoke_chatgpt(self,message_history):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4",
            "messages": message_history,
            "max_tokens": 1000,
            "temperature": 0.7
        }

        response = requests.post(API_ENDPOINT, headers=headers, json=data)
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    def ask_to_gpt(self,question,n_alternatives = 1) :
        # Add new user prompt to² list of messages
        self.message_history.append({"role": "user", "content": question})

        # Query ChatGPT
       # ai_response = ["Option " + str(idx) for idx in range((n_alternatives))]

        ai_response = [self.invoke_chatgpt(self.message_history) for idx in range((n_alternatives))]
        # Output response to a file and open it with the default text editor

        # Add ChatGPT response to list of messages
        self.message_history.append({"role": "assistant", "content": ai_response[0]})
        return ai_response
    def enrich_by_gpt(self,current_message,msg_enhancement,n_alternatives = 1) :

        dict_question_gpt = {'role' : 'user', 'content' :  dialog.Dialog.PREFIX_ENHANCEMENT + " " + msg_enhancement  + " : " + current_message + " : "  }

        self.message_history = [self.message_history[0], dict_question_gpt]
        ai_response = [self.invoke_chatgpt(self.message_history) for idx in range((n_alternatives))]

        # Query ChatGPT
       # ai_response = ["Enhanced " + msg_enhancement + " : " + str(idx) for idx in range((n_alternatives))]

        # ai_response = [self.invoke_chatgpt(self.message_history) for idx in range((n_alternatives))]
        # Output response to a file and open it with the default text editor

        # Add ChatGPT response to list of messages
        self.message_history[-1] = ({"role": "assistant", "content": ai_response[0]})
        return ai_response


