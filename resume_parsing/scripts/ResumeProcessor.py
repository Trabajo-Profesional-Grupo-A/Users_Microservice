from resume_parsing.OCRParsing import OCRParsing
from .parsers import ParseJobDesc, ParseResume
from .ReadPdf import read_single_pdf


class ResumeProcessor:
    def __init__(self, input_file_name):
        self.input_file_name = input_file_name
        print(f"Input file name: {self.input_file_name}")

    def process(self):
        try:
            resume_dict = self._read_resumes()
            return resume_dict
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def _read_resumes(self) -> dict:
        data = read_single_pdf(self.input_file_name)

        resume_dict_OCR = self._read_resumes_OCR(self.input_file_name)
        print("resume dict ocr", resume_dict_OCR)
        output = ParseResume(data, resume_dict_OCR).get_JSON()
        print("output parse resume", resume_dict_OCR)
        return output
 
 
    def _read_resumes_OCR(self, file_name) -> dict:
            # Create an instance of the OCRParsing class
            ocr_parser = OCRParsing()
            print("a")
            # Convert PDF to images
            images = ocr_parser.convertPdfToImage(file_name)
            print("a")
            # Apply OCR to images
            bounds = ocr_parser.applyOCR(images)
            print("a")
            # Create bounding boxes for relevant categories
            box = ocr_parser.createBoxes(bounds)
            print("a")
            columns = ocr_parser.checkColumns(box)
            print("a")
            # Create new bounds based on column or normal layout
            if columns:
                new_bounds = ocr_parser.createColumnBounds(box)
            else:
                new_bounds = ocr_parser.createNormalBounds(box)

            new_bounds = list(map(lambda x: ([x[0][3], x[0][2], x[0][1], x[0][0]], x[1]) if x[0][3] != [0, 0] else x, new_bounds))
            print("a")
            # Assign proper names to the bounding boxes
            proper_names = ocr_parser.giveProperNames(new_bounds)
            print("a")
            # Draw bounding boxes on images
            ocr_parser.drawBoxes(images[0], proper_names)
            print("a")
            # Extract text from images
            extracted_text = ocr_parser.extractText(images[0], proper_names)
            print("extracted text", extracted_text)
            return extracted_text 
