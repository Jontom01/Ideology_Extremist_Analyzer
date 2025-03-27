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
      - buzzword_density
      - identity_fusion_score
      - emotional_intensity
      - conspiratorial_thinking_score
    Plus any other relevant keys you wish to include.
    """
    system_prompt = """You are a professional language analysis model trained in political psychology, ideological extremism, and behavioral linguistics. Your task is to analyze informal online communication (such as Reddit comments or posts) and score the presence of psychological traits that correlate with ideological extremity.
            You must return a valid Python dictionary with two keys:
            1. 'text' the original input message
            2. 'features' a dictionary of 7 float scores (0.0 to 1.0), each measuring a specific psychological/linguistic trait

            ---

            ### BACKGROUND CONTEXT (Research Summary)

            Research has consistently found the following psychological characteristics strongly associated with ideological extremity:

            - **Cognitive Rigidity**  
            Difficulty adapting beliefs; favors black-and-white thinking.  
            ↳ Related to: *cognitive_rigid_score*

            - **Group-Based Identity Fusion & In-group Bias**  
            Merging of self and group identity; views outsiders as threats.  
            ↳ Related to: *identity_fusion_score, external_blame_score*

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
            ↳ Related to: *social_hostility_score, identity_fusion_score*

            - **Ideological Buzzword Use (Signaling/Tribalism)**  
            Frequent use of politically charged terminology as a marker of ideological belonging.  
            ↳ Related to: *buzzword_density*

            ---

            ### FEATURE DEFINITIONS

            Return float values between 0.0 and 1.0 for each of these features:
            - **cognitive_rigid_score: Measures rigidity, absolutism, simplistic thinking, intolerance of ambiguity
            - **external_blame_score**: How much the speaker blames outside groups, systems, or others. Potentially has victim-mindset.
            - **buzzword_density**: Frequency of ideological or tribal buzzwords ("woke", "deep state", etc.).
            - **emotional_intensity**: High emotional charge (anger, outrage, disgust).
            - **identity_fusion_score**: Alignment between self and a group identity (“we,” “our movement”).
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
                'buzzword_density': 0.7,
                'emotional_intensity': 0.8,
                'identity_fusion_score': 0.3,
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

        # Safely parse the returned string as a Python dictionary
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

def eval_features(text_list: list[str]) -> dict:
    features_dict_list = []
    for msg in text_list:
        tmp = extract_features(msg)
        if tmp != {}: 
            tmp = label_classification(tmp)
            features_dict_list.append(tmp) #the if statement is because the dict_to_csv function will throw an error if it gets an unexpected dict format.
    return features_dict_list

# Example usage (for testing):
if __name__ == "__main__":
    test_text = "The system is rigged and anyone who disagrees is clearly brainwashed."
    test_text2 = "I really am not sure if i like honey or not. Stupid thing to ask but I really don't like the taste myself, despite other people thinking it is yummy."
    l = [test_text, test_text2]
    fin = eval_features(l)
    print(fin)
   # dict_to_csv(fin)
