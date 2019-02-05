from flask import Flask, request, jsonify, render_template
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

    def __init__(self, document='', status=200, e_msg=None):

        self.e_msg = e_msg
        self.status = status

        self.document = document
        self.sentences = []

        if status == 200:
            self.clear_args()
            self.set_data()

    def clear_args(self):
        if self.document:
            self.document = self.document.strip()

    def set_data(self):
        if not self.document:
            return
        doc = nlp(self.document)
        tokens = []
        text_ = []
        for token in doc.conll_file.conll_as_string().split('\n'):
            token_ = token.split('\t')
            if len(token_) == 1:
                if tokens:
                    self.sentences.append({
                        'tokens': tokens,
                        'text': ' '.join(text_),
                    })

                tokens = []
                text_ = []
            else:
                token_d = {
                    'id': token_[0],
                    'form': token_[1],
                    'lemma': token_[2],
                    'upos': token_[3],
                    'xpos': token_[4],
                    'feats': token_[5],
                    'head': token_[6],
                    'deprel': token_[7],
                    'deps': token_[8],
                    'misc': token_[9],
                }
                tokens.append(token_d)
                text_.append(token_[1])

    def get_data_as_dict(self):
        return {
            'document': self.document,
            'sentences': self.sentences
        }

    def return_content(self):
        if self.status != 200:
            return self.e_msg, self.status
        return jsonify(self.get_data_as_dict()), self.status


@app.route('/api', methods=['GET'])
def return_tmp_data():
    obj = DocumentView.create_with_param(request.args)
    return obj.return_content()


@app.route('/', methods=['GET'])
def parse():
    obj = DocumentView.create_with_param(request.args)
    data = obj.get_data_as_dict()
    return render_template('parse.html', data=data)


if __name__ == '__main__':
    app.run(port=default_port, host=default_host)
