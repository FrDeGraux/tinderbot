
class Dialog:
    PREFIX_TYPICAL = """
        You are now playing the role of [Sender] and your task is to respond to [Receiver] in the Tinder conversation below. Your response should be about 2000 words and end with a question. Please respond in the language used by [Sender].
    """
    PREFIX_INITIALIZE = """
        Make a Tinder opener in maximum three sentences in the language based on this bio : 
    """
    PREFIX_PICKUP = """
        You are now playing the role of [Sender] and your task is to respond to [Receiver] in the Tinder conversation below. Your response should not exceed 50 words and end with a question. Please respond in the language used by [Sender].
    """

    PREFIX_FINAL = """ Respond the the Tinder conversation below: Suggest the idea of  Knowing all this, I have already a good idea where I might take you out"""

    PREFIX_FINAL_SECOND = " Respond the the Tinder conversation below: . Suggest also the bar : Cafe Brazil to take her out. Tell her it is very good for intimacy so we can know each better"
    PREFIX_FINA_THIRD = " Answer to this conversation by suggesting moving out to some messenger ; give my phone number : 0468276470 "
    def generate_typic_input(self, from_user_id, to_user_id, dialog):
        dialog = dialog[-20:]

        context = '\n'.join([str(d).replace(from_user_id, '[Sender]').replace(to_user_id, '[Receiver]') for d in dialog])
        return f'{self.PREFIX_TYPICAL} \n\n{context}\n[Sender]:'
    def generate_initialize_input(self, from_user_id, to_user_id, in_sMatch):
        return self.PREFIX_INITIALIZE + in_sMatch.bio + " in the language " + in_sMatch.language
    def generate_close_input_first(self,in_sMatch):
        return self.PREFIX_FINAL
    def generate_close_input_second(self,in_sMatch):
        return self.PREFIX_FINAL_SECOND
    def generate_close_input_third(self,in_sMatch):
        return self.PREFIX_FINA_THIRD
    def generate_pick_up_input(self, from_user_id, to_user_id, dialog):
        context = '\n'.join([str(d).replace(from_user_id, '[Sender]').replace(to_user_id, '[Receiver]') for d in dialog])
        return f'{self.PREFIX_PICKUP} \n\n{context}\n[Sender]:'

