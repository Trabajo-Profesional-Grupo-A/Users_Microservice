
from resume_parsing.scripts.Extractor import DataExtractor
from resume_parsing.scripts.KeytermsExtraction import KeytermExtractor
from resume_parsing.scripts.TextCleaner import CountFrequency, TextCleaner
from resume_parsing.scripts.utils.Utils import generate_unique_id

class ParseResume:

    def __init__(self, resume: str, resume_dict_OCR: dict):
        self.resume_data = resume
        print("1")
        self.clean_data = TextCleaner(self.resume_data).clean_text()
        print("2")
        self.entities = DataExtractor(self.resume_data).extract_entities()
        print("1")
        self.name = DataExtractor(self.resume_data[:30]).extract_names()
        print("1")
        self.experience = DataExtractor("", resume_dict_OCR).extract_experience()
        print("1")
        self.education = DataExtractor("", resume_dict_OCR).extract_education()
        print("1")
        self.education_title = DataExtractor(self.resume_data).extract_education_title()
        print("1")
        self.universities = DataExtractor(self.resume_data).extract_universities()
        print("1")
        self.skills = DataExtractor(self.resume_data, resume_dict_OCR).extract_skills()
        print("1")
        self.emails = DataExtractor(self.resume_data).extract_emails()
        print("1")
        self.phones = DataExtractor(self.resume_data).extract_phone_numbers()
        print("1")
        self.key_words = DataExtractor(self.resume_data).extract_particular_words()
        print("1")
        self.job_title = DataExtractor(self.clean_data).extract_designition()
        print("1")
        self.pos_frequencies = CountFrequency(self.clean_data).count_frequency()
        print("1")
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()
        print("1")
        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        print("1")
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()
        print("1")
        self.personal_info = DataExtractor("",resume_dict_OCR).extract_personal_info()
        print("1")
        self.extra = DataExtractor("",resume_dict_OCR).extract_extra_info()

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
            "personal_info": self.personal_info,
            "extra": self.extra
        }

        return resume_dictionary
