# features/feature_extraction.py
from openai import OpenAI
import ast
from config import OPENAI_API_KEY
import pandas as pd
from csv_processing import dict_to_csv
from classify import label_classification

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_features(text: str) -> dict:
    """
    Extracts feature scores from the input text using the ChatGPT API.
    Returns a Python dictionary with the following keys (floats in 0.0–1.0 range):
      - cognitive_rigid_score
      - external_blame_score
      - social_hostility_score
      - emotional_intensity
      - conspiratorial_thinking_score
    Plus any other relevant keys you wish to include.
    """
    system_prompt = """You are a professional language analysis model trained in political psychology, ideological extremism, and behavioral linguistics. Your task is to analyze informal online communication (such as Reddit comments or posts) and score the presence of psychological traits that correlate with ideological extremity.
            You must return a valid Python dictionary with two keys:
            1. 'text' the original input message
            2. 'features' a dictionary of 5 float scores (0.0 to 1.0), each measuring a specific psychological/linguistic trait

            ---

            ### BACKGROUND CONTEXT (Research Summary)

            Research has consistently found the following psychological characteristics strongly associated with ideological extremity:

            - **Cognitive Rigidity**  
            Difficulty adapting beliefs; favors black-and-white thinking.  
            ↳ Related to: *cognitive_rigid_score*

            - **Group-Based Identity Fusion & In-group Bias**  
            Merging of self and group identity; views outsiders as threats.  
            ↳ Related to: *external_blame_score*

            - **Conspiratorial Mindset**  
            Distrust of mainstream sources; belief in hidden agendas.  
            ↳ Related to: *conspiratorial_thinking_score*

            - **Authoritarian Personality**  
            Preference for order and obedience; aggression toward out-groups.  
            ↳ Related to: *social_hostility_score, external_blame_score, cognitive_rigid_score*

            - **Need for Closure / Intolerance of Ambiguity**  
            Discomfort with uncertainty; prefers definitive answers.  
            ↳ Related to: *cognitive_rigid_score*

            - **Moral Outrage and Emotional Intensity**  
            High emotional charge; anger and disgust drive polarization.  
            ↳ Related to: *emotional_intensity, cognitive_rigid_score*

            - **Perceived Threat & Victimhood Narrative**  
            Belief that one's group is unjustly persecuted.  
            ↳ Related to: *external_blame_score, conspiratorial_thinking_score*

            - **Dogmatism**  
            Blind adherence to ideology without nuance or evidence.  
            ↳ Related to: *cognitive_rigid_score*

            - **Social Dominance Orientation (SDO)**  
            Desire for dominance of one's group over others.  
            ↳ Related to: *social_hostility_score*


            ---

            ### FEATURE DEFINITIONS

            Return float values between 0.0 and 1.0 for each of these features:
            - **cognitive_rigid_score: Measures rigidity, absolutism, simplistic thinking, intolerance of ambiguity
            - **external_blame_score**: How much the speaker blames outside groups, systems, or others. Potentially has victim-mindset.
            - **emotional_intensity**: High emotional charge (anger, outrage, disgust).
            - **conspiratorial_thinking_score**: Suspicion of hidden agendas or manipulation.
            - **social_hostility_score**: Hostility, aggression, condescension, dismissiveness, mockery, superiority, towards opponents.

            ---

            ### OUTPUT FORMAT

            Return only a valid **Python dictionary** with this exact format (no commentary or explanation):

            {
            'text': "The original Reddit message or comment here.",
            'features': {
                'cognitive_rigid_score': 0.8,
                'external_blame_score': 0.6,
                'social_hostility_score': 0.6,
                'emotional_intensity': 0.8,
                'conspiratorial_thinking_score': 0.6
            }
            }
            """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=300
        )
        reply_text = response.choices[0].message.content.strip() #"  {'text': 'blah'}\n\n".strip()  # → "{'text': 'blah'}"

        #Safely parse the returned string as a Python dictionary
        try:
            features = ast.literal_eval(reply_text) 
            """
            eval in general attempts to evaluate a string. For examples:
                eval("2 + 2")              # → 4
                eval("'hello'.upper()")    # → 'HELLO'
                eval("{'a': 1}")            # → {'a': 1}
                eval("__import__('os').system('rm -rf /')")  # This is DANGEROUS!
            Eval lets you evaluate any string, thus we use ast.literal_eval which 
            is a safer option and wont evaluate possibly malicious text. 
            """
        except Exception as parse_err:
            print("Error parsing output as Python dict:", parse_err)
            features = {}
        return features

    except Exception as e:
        print("Error during feature extraction:", e)
        return {}

def eval_features(text_list: list[dict]) -> dict:
    features_dict_list = []
    for msg_dict in text_list:
        tmp = extract_features(msg_dict['comment'])
        if tmp != {}: 
            tmp = label_classification(tmp)
            tmp['subreddit'] = msg_dict['subreddit']
            tmp['utc_time'] = msg_dict['utc_time']
            features_dict_list.append(tmp) #the if statement is because the dict_to_csv function will throw an error if it gets an unexpected dict format.
    return features_dict_list


if __name__ == "__main__":
    test_text = {'comment': 'I am a little bit guilty of posting a not so personal things but I think at this point, you guys are doing the right thing.', 'subreddit': 'TrueOffMyChest', 'utc_time': 1615763367.0}
    test_text2 = {'comment': 'how soon before you mods are gonna burn out?', 'subreddit': 'TrueOffMyChest', 'utc_time': 1615763367.0}
    l = [test_text, test_text2]
    fin = eval_features(l)
    for item in fin:
        print(item)
        print('\n')
   # dict_to_csv(fin)
