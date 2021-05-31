from PyPDF2 import PdfFileReader
from pdfminer import high_level
import os.path
import docx
from spacy import displacy
import en_core_web_sm


class DocumentReader:
    '''
    A class that reads the input document, gathers metadata & text,
    removes images, phone numbers, email-addresses
    '''

    def __init__(self, filename):
        extension = os.path.splitext(filename)[1]
        if extension == '.doc' or extension == '.docx':
            self.is_pdf = False
            self.ext_text = {"Metadata": [], "Text": []}
            self.doc_docx_reader(filename)
            self.spacy_entity_extractor()
        elif extension == '.pdf':
            self.is_pdf = True
            self.ext_text = {"Metadata": [], "Text": []}
            self.pdf_reader(filename)
            self.spacy_entity_extractor()
        else:
            pass

    def doc_docx_reader(self, filename):
        # https://automatetheboringstuff.com/chapter13/
        doc = docx.Document(filename)
        self.ext_text["Metadata"].append(self.getMetaData(doc))
        for paragr in doc.paragraphs:
            self.ext_text["Text"].append(paragr.text)

    def pdf_reader(self, filename):
        pdf = PdfFileReader(str(filename))
        self.ext_text["Metadata"].append(pdf.documentInfo)

        for page in range(pdf.getNumPages()):
            tmp = pdf.getPage(page)

            if tmp.extractText() == '':  # means PyPDF2 cannot extract text
                print(f'Page: {page} - PyPDF2 cannot extract text.'
                      f'Switching to fallback (pdfminer.six)')
                self.ext_text["Text"].append(
                    self.fallback_pdf_reader(filename))
                # raise Exception('PyPDF2 cannot extract text.')
            else:
                self.ext_text["Text"].append(tmp.extractText())

    @staticmethod
    def fallback_pdf_reader(filename):
        extracted_text = high_level.extract_text(filename)
        return repr(extracted_text)

    def getMetaData(self, doc):
        metadata = {}
        prop = doc.core_properties
        metadata["author"] = prop.author
        metadata["category"] = prop.category
        metadata["content_status"] = prop.content_status
        metadata["created"] = prop.created
        metadata["identifier"] = prop.identifier
        metadata["keywords"] = prop.keywords
        metadata["language"] = prop.language
        metadata["subject"] = prop.subject
        metadata["title"] = prop.title
        metadata["version"] = prop.version
        return metadata

    def spacy_entity_extractor(self):
        # python3 -m spacy download en_core_web_trf (~500 mbs)
        nlp = en_core_web_sm.load()

        pdf_text = self.ext_text['Text']

        # convert list to string
        pdf_text = ''.join(pdf_text)

        # strip all bad symbols (even when inside the word)
        pdf_text = pdf_text.replace('\n', '').replace('\n \n\n \n', '')\
                           .replace('\n \n\n \n  \n \n', '')\
                           .replace(',', '').replace('.', '').replace(':', '')\
                           .replace('/', '').replace('-', '')\
                           .replace('(', '').replace(')', '')\
                           .rstrip()

        tokenized_pdf = nlp(pdf_text)

        # removing stop words and including only alpha and numeric
        pdf_text_stopwords_stripped = [
            token for token in tokenized_pdf
            if not token.is_stop
            and (str(token).isalpha() or str(token).isnumeric())
            ]

        # converting back to string, to create tokens for displacy
        tokenized_pdf = [str(token) for token in pdf_text_stopwords_stripped]
        tokenized_pdf = ' '.join(tokenized_pdf)
        self.tokenized_pdf = nlp(tokenized_pdf)

    @staticmethod
    def displacy_entity_html(tokenized_text):
        nlp = en_core_web_sm.load()
        tokenized_text_html = nlp(tokenized_text)
        return displacy.render(tokenized_text_html, style='ent', minify=True)

    def __repr__(self):
        return(f'Extracted text from document: {self.ext_text["Text"]}. '
               f'PDF? {self.is_pdf}. '
               f'Tokenized document: {self.tokenized_pdf}')
