
from resume_parsing.scripts.Extractor import DataExtractor
from resume_parsing.scripts.KeytermsExtraction import KeytermExtractor
from resume_parsing.scripts.TextCleaner import CountFrequency, TextCleaner
from resume_parsing.scripts.utils.Utils import generate_unique_id

class ParseResume:

    def __init__(self, resume: str, nlp_sm, nlp_md, path_skills, path_universities, path_titles):
        self.resume_data = resume
        self.clean_data = TextCleaner(self.resume_data).clean_text()
        self.entities = DataExtractor(self.resume_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_entities()
        self.name = DataExtractor(self.resume_data[:30], nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_names()
        self.experience = DataExtractor(self.clean_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_experience()
        self.education = DataExtractor(self.clean_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_education()
        self.education_title = DataExtractor(self.resume_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_education_title()
        self.universities = DataExtractor(self.resume_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_universities()
        self.skills = DataExtractor(self.resume_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_skills()
        self.emails = DataExtractor(self.resume_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_emails()
        self.phones = DataExtractor(self.resume_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_phone_numbers()
        self.key_words = DataExtractor(self.resume_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_particular_words()
        self.job_title = DataExtractor(self.clean_data, nlp_sm,nlp_md, path_skills, path_universities, path_titles).extract_designition()
        self.pos_frequencies = CountFrequency(self.clean_data, nlp_md).count_frequency()
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()
        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()

    def get_JSON(self) -> dict:
        """
        Returns a dictionary of resume data.
        """
        resume_dictionary = {
            "unique_id": generate_unique_id(),
            "resume_data": self.resume_data,
            "clean_data": self.clean_data,
            "entities": self.entities,
            "extracted_keywords": self.key_words,
            "keyterms": self.keyterms,
            "name": self.name,
            "experience": self.experience,
            "education": self.education,
            "education_title": self.education_title,
            "universities": self.universities,
            "job_title": self.job_title,
            "skills": self.skills,
            "emails": self.emails,
            "phones": self.phones,
            "bi_grams": str(self.bi_grams),
            "tri_grams": str(self.tri_grams),
            "pos_frequencies": self.pos_frequencies,
        }

        return resume_dictionary
