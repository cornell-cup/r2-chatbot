# from haystack import Finder
from haystack.pipeline import ExtractiveQAPipeline
from haystack.preprocessor.preprocessor import PreProcessor
from haystack.reader.farm import FARMReader
from haystack.utils import print_answers
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.retriever.sparse import ElasticsearchRetriever
import os
from subprocess import Popen, PIPE, STDOUT
from haystack.file_converter.txt import TextConverter
import time

os.system(
    'docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.6.2')

document_store = ElasticsearchDocumentStore(
    host='localhost', username="", password="", index="document")

converter = PDFToTextConverter(
    remove_numeric_tables=True, valid_languages=["en"])
converter2 = TextConverter(remove_numeric_tables=True, valid_languages=['en'])

context_dir = "data/"

processor = PreProcessor(clean_empty_lines=True,
                         clean_whitespace=True,
                         clean_header_footer=True,
                         split_by="word",
                         split_length=200,
                         split_respect_sentence_boundary=True)

document_store.delete_all_documents('document')
for filename in os.listdir(context_dir):
    if filename.endswith('.pdf'):
        path = context_dir + filename
        pdf_file = converter.convert(file_path=path)
        pdf_file = processor.process(pdf_file)
        document_store.write_documents(pdf_file)
    elif filename.endswith('.txt'):
        path = context_dir + filename
        txt_file = converter2.convert(file_path=path)
        txt_file = processor.process(txt_file)
        document_store.write_documents(txt_file)

retriever = ElasticsearchRetriever(document_store=document_store)

reader = FARMReader(
    model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

finder = ExtractiveQAPipeline(reader, retriever)


def get_answer(question):
    before = time.time()
    prediction = finder.run(query=question, top_k_retriever=10, top_k_reader=5)
    after = time.time()
    print(after - before)
    return prediction
