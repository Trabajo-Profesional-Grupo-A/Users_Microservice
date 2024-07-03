from typing import List
import nltk
from scripts.utils.Utils import read_json
from scripts.similarity.get_score import *



try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def create_annotated_text(
    input_string: str, word_list: List[str], annotation: str, color_code: str
):
    # Tokenize the input string
    tokens = nltk.word_tokenize(input_string)

    # Convert the list to a set for quick lookups
    word_set = set(word_list)

    # Initialize an empty list to hold the annotated text
    annotated_text = []

    for token in tokens:
        # Check if the token is in the set
        if token in word_set:
            # If it is, append a tuple with the token, annotation, and color code
            annotated_text.append((token, annotation, color_code))
        else:
            # If it's not, just append the token as a string
            annotated_text.append(token)

    return annotated_text


def process_files(resume, job_description):
    resume_dict = read_json(PROCESSED_RESUMES_PATH + resume)
    job_dict = read_json(PROCESSED_JOB_DESCRIPTIONS_PATH + job_description)
    resume_keywords = resume_dict["extracted_keywords"]
    job_description_keywords = job_dict["extracted_keywords"]

    resume_string = " ".join(resume_keywords)
    jd_string = " ".join(job_description_keywords)
    final_result = get_score(resume_string, jd_string)
    for r in final_result:
        print(r.score)
    print(f"Processing resume: {resume}")
    print(f"Processing job description: {job_description}")

    similarity_score = round(final_result[0].score * 100, 2)
    score_color = "green"
    if similarity_score < 60:
        score_color = "red"
    elif 60 <= similarity_score < 75:
        score_color = "orange"


