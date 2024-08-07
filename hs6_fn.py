import os

from openai import OpenAI
# import openai
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# remember the model choices between completions and chat/completions
# /v1/chat/completions: gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
# /v1/completions:    text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001
# remember about the different endpoints!!!

protected_characteristics = [
    'race', 'religion', 'ethnic origin', 'national origin', 'sex', 'disability', 'sexual orientation', 'gender identity', 'neurotype', 'body size'
]



HS_definition = '"Hate speech" is speech that attacks a person or group on the basis of attributes such as: ' + ', '.join(protected_characteristics) +'.'


# for the example
hs_examples_dict = [
    {'example input':'You lost! Succer!',
     'example output':['not hate speech','', 1]},
    {'example input':'you hateful sack of flesh',
     'example output':['not hate speech','', 1]},
    {'example input':'“Pick one, kidd,” one nudged. Then, “Choose FA GO TT.”',
     'example output':['hate speech','sexual orientation', 1]},
    # {'example input':'Aspie my ass. too slow to remember, so dont waste our time playing',
    #  'example output':['hate speech','neurotype', 1]},
    {'example input':'“Kept being called a "Jew" for no reason.”; "A player on the other team was named Hitler.” “[One player] threatened to get antisemitic if I didnt talk. [They] talked about Jew tunnels.”',
     'example output':['hate speech','race', 1]},
    {'example input':'if money was grown on trees women would be dating monkeys oh wait never mind',
     'example output':['hate speech','sex', 1]},
    {'example input':'well my dear lgbtq brothers and sisters i do not want to die at the hands of a muslim terrorist and as you are putting my life in danger with your politics i would like to suggest that you all go fuck yourselves',
     'example output':['hate speech',['gender identity', 'sexual orientation', 'religion'], 1]}
]


hs_examples_str = '\n'
for ind in range(len(hs_examples_dict)):
  hs_examples_str += "\n" + str(hs_examples_dict[ind])[1:-1]


test_texts = [
    # "You f**king evil pieces of s**t @china",
    # "You're kind of a dick, aren't you?",
    # "If you have a d then you can't be a woman!",
    # "Fuck that! So now we have to explain to you, remember for you? Should we also play for you?",
    # "a woman shall not wear man's clothing, nor shall a man put on a woman's clothing; for whoever does these things is an abomination to the LORD your God.",
    # "Seriously, Blake? Brace yourself for the beta uprising, femoid.",
    # "You mean who the real bitches are? Haha!",
    # "Haha, right on! Let's fuck them up!",
    "Fluke my ass, you're just a klutz!",
    "You'd be cute if you lost some weight."
]



def classify_hs(message:str, protected_characteristics_str:str, HS_definition:str, examples:str, verbose=False):
    

    prompt = f"""
    DEFINITIONS:
    Consider the following definition: '{HS_definition}'. 

    INSTRUCTION: 
    Using the provided definition of hate speech, classify the following fragment from a chat as either hate speech with respect to one or more of protected characteristics from the following list: '{protected_characteristics_str}', or not hate speech with respect to the protected characteristics from the following list: '{protected_characteristics_str}'.
    
    OUTPUT:
    The output should only contain 3 elements: 
    1) "hate speech" or "not hate speech", 
    2) one or more protected characteristic labels from the list: '{protected_characteristics_str}', 
    3) the probability with two decimal points.

    OUTPUT FORMAT:
    ['hate speech', 'sexual orientation', 0.98]

    EXAMPLES:
    Consider the following examples:'{examples}'.
    
    MESSAGE:
    '{message}'. 
    """
    ### part that if added suddenly doesn't recognise transphobia and misogyny:

    # OUTPUT FORMAT EXAMPLE:
    # 'hate speech', 'religion', 0.98


    if verbose:
       print(message)

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature = 0.0,
    messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# response = completion["choices"][0]["text"].strip()

# for text in test_texts:
#     print("=============================")
#     print(classify_hs(
#             message = text, 
#             protected_characteristics_str = ", ".join(protected_characteristics), 
#             HS_definition=HS_definition, 
#             examples=hs_examples_str))