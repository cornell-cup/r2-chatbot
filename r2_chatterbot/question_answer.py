from haystack import Finder
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
print('Starting docker')
os.system('sudo docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.6.2')
print('Started docker')
document_store = ElasticsearchDocumentStore(host='localhost', username="", password="", index="document")

converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
converter2 = TextConverter(remove_numeric_tables=True, valid_languages=['en'])

context_dir = "/home/ec2-user/c1c0_aws_flask/r2-chatbot/r2_chatterbot_server/data/chatbot_contexts/"
print(f'Context_dir set to {context_dir}')
#if not os.path.isfile(context_dir):
#   import boto3
#   BUCKET_NAME, OBJECT_NAME, OUTPUT_FILE = 'chatbot-stuff', 'chatbot_contexts/', './data/chatbot_contexts/'
#   s3 = boto3.resource('s3')
#   bucket = s3.Bucket(BUCKET_NAME)
#   for obj in bucket.objects.filter(Prefix=OBJECT_NAME):
#       target = obj.key
#       # if not os.path.isdir(target):
#       #    bucket.download_file(obj.key, target)
#       if not os.path.exists(os.path.dirname(target)):
#           os.makedirs(os.path.dirname(target))
#       if obj.key[-1] == '/':
#           continue
#       bucket.download_file(obj.key, target)
#   # s3.download_file(BUCKET_NAME, OBJECT_NAME, OUTPUT_FILE)

processor = PreProcessor(clean_empty_lines=True,
                         clean_whitespace=True,
                         clean_header_footer=True,
                         split_by="word",
                         split_length=200,
                         split_respect_sentence_boundary=True)

document_store.delete_all_documents('document')
for filename in os.listdir(context_dir):
    if filename.endswith('.pdf'):
        print(f'Adding {filename}')
        path = context_dir + filename
        pdf_file = converter.convert(file_path=path)
        pdf_file = processor.process(pdf_file)
        document_store.write_documents(pdf_file)
    elif filename.endswith('.txt'):
        print(f'Adding {filename}')
        path = context_dir + filename
        txt_file = converter2.convert(file_path=path)
        txt_file = processor.process(txt_file)
        document_store.write_documents(txt_file)

retriever = ElasticsearchRetriever(document_store=document_store)

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

finder = ExtractiveQAPipeline(reader, retriever)


def get_answer(question):
    before = time.time()
    # prediction = finder.get_answers(question=question, top_k_reader=5) # will return top 5 answers, so hopefully we'll have some variety here in case we get it wrong the first time
    prediction = finder.run(query=question, top_k_retriever=10, top_k_reader=5)
    print_answers(prediction, details='minimal')
    after = time.time()
    print(after - before)
    return prediction
