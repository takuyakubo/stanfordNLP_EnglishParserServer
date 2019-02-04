from flask import Flask, request
import stanfordnlp

from download_model import DEFAULT_MODEL_DIR

app = Flask(__name__)
default_port = 5020
default_host = "0.0.0.0"

nlp = stanfordnlp.Pipeline(models_dir=DEFAULT_MODEL_DIR)


class DocumentView:
    @classmethod
    def create_with_param(cls, args):

        val = args.get('document', None)
        if not val:
            return cls(status=400, e_msg='Parameter "document" is required.')

        return cls(document=val)

    def __init__(self, document=None, status=200, e_msg=None):

        self.document = document
        self.e_msg = e_msg
        self.status = status

    def get_sentence_conll(self):
        doc = nlp(self.document)
        return doc.conll_file.conll_as_string()

    def return_content(self):
        if self.status != 200:
            return self.e_msg, self.status
        return self.get_sentence_conll(), self.status


def data_(form):
    obj = form.create_with_param(request.args)
    return obj.return_content()


@app.route('/', methods=['GET'])
def return_tmp_data():
    return data_(DocumentView)


if __name__ == '__main__':
    app.run(port=default_port, host=default_host)
