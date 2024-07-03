from .parsers import ParseJobDesc, ParseResume
from .ReadPdf import read_single_pdf


class ResumeProcessor:
    def __init__(self, input_file_name, nlp_sm, nlp_md, path_skills, path_universities, path_titles):
        self.nlp_sm = nlp_sm
        self.nlp_md = nlp_md
        self.path_skills = path_skills
        self.path_universities = path_universities
        self.path_titles = path_titles

        self.input_file_name = input_file_name
        print(f"Input file name: {self.input_file_name}")

    def process(self):
        try:
            resume_dict = self._read_resumes()
            print("return del read_resumes", resume_dict)
            return resume_dict
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def _read_resumes(self) -> dict:
        data = read_single_pdf(self.input_file_name)
        output = ParseResume(data, self.nlp_sm,self.nlp_md, self.path_skills, self.path_universities, self.path_titles).get_JSON()
        print("return del parse resume  .json", output)
        return output

    # def _read_job_desc(self) -> dict:
    #     data = read_single_pdf(self.input_file_name)
    #     output = ParseJobDesc(data).get_JSON()
    #     return output

    # def _write_json_file(self, resume_dictionary: dict):
    #     file_name = str(
    #         "Resume-" + self.input_file + resume_dictionary["unique_id"] + ".json"
    #     )
    #     save_directory_name = pathlib.Path(PROCESSED_RESUMES_PATH) / file_name
    #     json_object = json.dumps(resume_dictionary, sort_keys=True, indent=14)
    #     with open(save_directory_name, "w+") as outfile:
    #         outfile.write(json_object)
