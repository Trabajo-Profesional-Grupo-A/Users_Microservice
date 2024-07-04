from .parsers import ParseJobDesc, ParseResume
from .ReadPdf import read_single_pdf



class JobDescriptionProcessor:
    def __init__(self, input_file_name):
        self.input_file_name = input_file_name

    def process(self) -> bool:
        try:
            jd_dict = self._read_job_desc()
            return jd_dict
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return {"error": str(e)}

    # def _read_resumes(self) -> dict:
    #     data = read_single_pdf(self.input_file_name)
    #     output = ParseResume(data).get_JSON()
    #     return output

    def _read_job_desc(self) -> dict:
        data = read_single_pdf(self.input_file_name)
        output = ParseJobDesc(data).get_JSON()
        return output

    # def _write_json_file(self, resume_dictionary: dict):
    #     file_name = str(
    #         "JobDescription-"
    #         + self.input_file
    #         + resume_dictionary["unique_id"]
    #         + ".json"
    #     )
    #     save_directory_name = pathlib.Path(PROCESSED_JOB_DESCRIPTIONS_PATH ) / file_name
    #     json_object = json.dumps(resume_dictionary, sort_keys=True, indent=14)
    #     with open(save_directory_name, "w+") as outfile:
    #         outfile.write(json_object)
