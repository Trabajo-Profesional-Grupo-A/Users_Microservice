import re
import urllib.request
import pandas as pd

import spacy
import csv
from resume_parsing.constants import DEGREE_PATTERNS, EDUCATION, RESUME_SECTIONS
from resume_parsing.scripts.TextCleaner import TextCleaner
from transformers import BartTokenizer, BartForConditionalGeneration



class DataExtractor:
    """
    A class for extracting various types of data from text.
    """

    def __init__(self, raw_text: str, nlp_sm, nlp_md, path_skills, path_universities, path_titles):
        """
        Initialize the DataExtractor object.

        Args:
            raw_text (str): The raw input text.
        """
        self.path_skills = path_skills
        self.path_universities = path_universities
        self.path_titles = path_titles

        self.nlp = nlp_sm
        self.matcher = spacy.matcher.Matcher(self.nlp.vocab)
        self.designitionmatcher = spacy.matcher.PhraseMatcher(self.nlp.vocab)

        # Load the tokenizer and model
        self.tokenizer = BartTokenizer.from_pretrained('ilsilfverskiold/tech-keywords-extractor')
        self.model = BartForConditionalGeneration.from_pretrained('ilsilfverskiold/tech-keywords-extractor')

        self.text = raw_text
        self.clean_text = TextCleaner(self.text).clean_text()
        self.doc = self.nlp(self.text)
        self.doc_clean = self.nlp(self.clean_text)

    def extract_links(self):
        """
        Find links of any type in a given string.

        Args:
            text (str): The string to search for links.

        Returns:
            list: A list containing all the found links.
        """
        link_pattern = r"\b(?:https?://|www\.)\S+\b"
        links = re.findall(link_pattern, self.text)
        return links

    def extract_links_extended(self):
        """
        Extract links of all kinds (HTTP, HTTPS, FTP, email, www.linkedin.com,
          and github.com/user_name) from a webpage.

        Args:
            url (str): The URL of the webpage.

        Returns:
            list: A list containing all the extracted links.
        """
        links = []
        try:
            response = urllib.request.urlopen(self.text)
            html_content = response.read().decode("utf-8")
            pattern = r'href=[\'"]?([^\'" >]+)'
            raw_links = re.findall(pattern, html_content)
            for link in raw_links:
                if link.startswith(
                    (
                        "http://",
                        "https://",
                        "ftp://",
                        "mailto:",
                        "www.linkedin.com",
                        "github.com/",
                        "twitter.com",
                    )
                ):
                    links.append(link)
        except Exception as e:
            print(f"Error extracting links: {str(e)}")
        return links

    def extract_names(self):
        """Extracts and returns a list of names from the given
        text using spaCy's named entity recognition.

        Args:
            text (str): The text to extract names from.

        Returns:
            list: A list of strings representing the names extracted from the text.
        """
        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        
        self.matcher.add('NAME', [pattern])
        matches = self.matcher(self.doc)
        
        # Extract names using Matcher
        matcher_names = [self.doc[start:end].text for match_id, start, end in matches]

        
        # Extract names using NER
        ner_names = [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]

        
        # Combine results and remove duplicates
        all_names = list(set(matcher_names + ner_names))
        
        return all_names
    

    def extract_emails(self):
        """
        Extract email addresses from a given string.

        Args:
            text (str): The string from which to extract email addresses.

        Returns:
            list: A list containing all the extracted email addresses.
        """
        # First method using spaCy matcher
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        email_pattern = [{'LIKE_EMAIL': True}]
        matcher.add('EMAIL', [email_pattern])
        
        matches = matcher(self.doc)
        spacy_emails = set()  # Use a set to store unique emails from spaCy
        for match_id, start, end in matches:
            if match_id == self.nlp.vocab.strings['EMAIL']:
                spacy_emails.add(self.doc[start:end].text)

        # Second method using regular expression
        email_pattern_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        regex_emails = set(re.findall(email_pattern_regex, self.text))  # Use a set to store unique emails from regex

        # Combine both sets of emails
        unique_emails = spacy_emails.union(regex_emails)

        # Return the list of unique emails
        return list(unique_emails)

    def extract_phone_numbers(self):
        """
        Extract phone numbers from a given string.

        Args:
            text (str): The string from which to extract phone numbers.

        Returns:
            list: A list containing all the extracted phone numbers.
        """
        phone_number_patterns = [
        r"^(\+\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$",  # General format
        r"\(\d{3}\) \d{3}-\d{4}",  # Alternate format: (123) 456-7890
        r"(?:\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"  # Other common formats
    ]

        # Try each pattern and return the first match found
        for pattern in phone_number_patterns:
            match = re.search(pattern, self.text)
            if match:
                return match.group(0)

        return None  # Return None if no phone number is found

    def extract_experience(self):
        """
        Extract experience from a given string. It does so by using the Spacy module.

        Args:
            text (str): The string from which to extract experience.

        Returns:
            str: A string containing all the extracted experience.
        """
        experience_section = []
        in_experience_section = False

        for token in self.doc_clean:
            if token.text.lower() in RESUME_SECTIONS:
                if token.text.lower() == "experience":
                    in_experience_section = True
                else:
                    if in_experience_section:
                        break  # Stop adding tokens when a new section is encountered
                    in_experience_section = False

            if in_experience_section:
                experience_section.append(token.text)

        return " ".join(experience_section)
    
    def extract_education(self):
        """
        Extract education from a given string. It does so by using the Spacy module.

        Args:
            text (str): The string from which to extract education.

        Returns:
            str: A string containing all the extracted education.
        """
        education_section = []
        in_education_section = False

        for token in self.doc_clean:
            if token.text.lower() in RESUME_SECTIONS:
                if token.text.lower() == "education":
                    in_education_section = True
                else:
                    if in_education_section:
                        break
                    in_education_section = False

            if in_education_section:
                education_section.append(token.text)

        education_text = " ".join(education_section)

        return education_text
    
    def extract_education_title(self):
        """
        Extract education title from a given string. It does so by using the Spacy module.

        Args:
            text (str): The string from which to extract education title.

        Returns:
            list: A list containing the extracted education titles.
        """
        # Sentence Tokenizer
        nlp_text = [sent.text.strip() for sent in self.doc.sents]

        education_titles = []

        # Extract education degree
        for text in nlp_text:
            for word in text.split():
                # Replace all special symbols
                word_clean = re.sub(r'[?|$|.|!|,]', r'', word)
                if word_clean.upper() in EDUCATION or word_clean.upper() in DEGREE_PATTERNS.keys():
                    # Append the entire sentence if the word is found in EDUCATION
                    education_titles.append(text)
                    break  # Stop after finding the first match in the sentence

        

        # Post-process to extract only the relevant part of the sentence
        processed_titles = []
        for title in education_titles:
            match = re.search(r'(' + '|'.join(EDUCATION) + r')\s*.*?,\s*.*?(?=,|$)', title, re.IGNORECASE)
            if match:
                processed_titles.append(match.group(0).strip())
            for _, patterns in DEGREE_PATTERNS.items():
                pattern = '|'.join(patterns)
                match_qual = re.search(pattern, title, re.IGNORECASE)
                if match_qual:
                    processed_titles.append(match_qual.group(0).strip())

        return processed_titles 
    
    def extract_qualifications(self):
        """
        Extract qualifications from a given string. It does so by using the Spacy module.

        Args:
            text (str): The string from which to extract qualifications.

        Returns:
            str: A string containing all the extracted qualifications.
        """
    
        # Sentence Tokenizer
        nlp_text = [sent.text.strip() for sent in self.doc.sents]

        qualifications = []
        

        # Extract education degree
        for text in nlp_text:
            for word in text.split():
                # Replace all special symbols
                word_clean = re.sub(r'[?|$|.|!|,]', r'', word)
                if  word_clean.upper() in DEGREE_PATTERNS.keys():
                    # Append the entire sentence if the word is found in EDUCATION
                    qualifications.append(text)
                    break  # Stop after finding the first match in the sentence

        # Post-process to extract only the relevant part of the sentence
        processed_titles = []
        for title in qualifications:
            for _, patterns in DEGREE_PATTERNS.items():
                pattern = '|'.join(patterns)
                match_qual = re.search(pattern, title, re.IGNORECASE)
                if match_qual:
                    processed_titles.append(match_qual.group(0).strip())

        return processed_titles 
    
    def extract_universities(self):
        """
        Extract university from a given string. It does so by using the Spacy module.

        Args:
            text (str): The string from which to extract university.

        Returns:
            str: A string containing all the extracted university.
        """
    
        # Method 1: Using spaCy NER
        universities_spacy = set()  # Use a set to avoid duplicates
        for entity in self.doc.ents:
            if entity.label_ == "ORG" and ("university" in entity.text.lower() or "college" in entity.text.lower() or "institute" in entity.text.lower()):
                universities_spacy.add(entity.text)

        # Method 2: Using a list of known universities from a CSV file
        df = pd.read_csv(self.path_universities, header=None)
        known_universities = [i.lower() for i in df[1]]
        universities_csv = set()  # Use a set to avoid duplicates

        for uni in known_universities:
            if re.search(r'\b' + re.escape(uni) + r'\b', self.clean_text):
                universities_csv.add(uni)

        # Combine results from both methods and convert to list
        all_universities = list(universities_spacy.union(universities_csv))

        return all_universities
    
    def _extract_skills_from_BERT(self):
        # Tokenize the input text
        inputs = self.tokenizer(self.clean_text, return_tensors='pt')

        # Generate keywords
        outputs = self.model.generate(**inputs, max_new_tokens=40)

        # Decode the generated keywords
        keywords = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return keywords.split(", ")
    
    def _load_keywords(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            return set(row[0] for row in reader)
        
    def _csv_skills(self):
        skills_keywords = self._load_keywords(self.path_skills)
        skills = set()

        for keyword in skills_keywords:
            if keyword.lower() in self.doc.text.lower():
                skills.add(keyword)

        return skills

    def extract_skills(self):
        skills_csv = self._csv_skills()
        skills_BERT = self._extract_skills_from_BERT()
         
        combined_skills = skills_csv.union(skills_BERT)  # Combine filtered skills without duplicates
        
        return list(combined_skills)  # Return combined filtered skills as a list


    def extract_particular_words(self):
        """
        Extract nouns and proper nouns from the given text.

        Args:
            text (str): The input text to extract nouns from.

        Returns:
            list: A list of extracted nouns.
        """
        pos_tags = ["NOUN", "PROPN"]
        nouns = [token.text for token in self.doc if token.pos_ in pos_tags]
        return nouns

    def extract_entities(self):
        """
        Extract named entities of types 'GPE' (geopolitical entity) and 'ORG' (organization) from the given text.

        Args:
            text (str): The input text to extract entities from.

        Returns:
            list: A list of extracted entities.
        """
        entity_labels = ["GPE", "ORG"]
        entities = [
            token.text for token in self.doc.ents if token.label_ in entity_labels
        ]
        return list(set(entities))
    

    def extract_designition(self):
        """
        Extract designition from a given string.

        Args:
            text (str): The string from which to extract designition.

        Returns:
            str: A string containing the extracted designition.
        """

        with open(self.path_titles, "r", encoding='utf-8') as f:
            designation = [line.strip().lower() for line in f]
        
        patterns = [self.nlp.make_doc(text) for text in designation if len(self.nlp.make_doc(text)) < 10]
        self.designitionmatcher.add("Job title", None, *patterns)
        
        job_titles = set()
        matches = self.designitionmatcher(self.doc_clean)
        
        for match_id, start, end in matches:
            span = self.doc_clean[start:end]
            job_titles.add(span.text)
        
        return list(job_titles)
