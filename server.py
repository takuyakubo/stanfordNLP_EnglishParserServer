from flask import Flask, request, render_template
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


@app.route('/parse', methods=['GET'])
def parse():
    text = request.args.get('text', '')
    data = dict(text=text)
    if text:
        data['sentences'] = []
        doc = nlp(text)
        tokens = []
        text_ = []
        for token in doc.conll_file.conll_as_string().split('\n')[:-1]:
            token_ = token.split('\t')
            if len(token_) == 1:
                data['sentences'].append({
                    'tokens': tokens,
                    'text': ' '.join(text_),
                })

                tokens = []
                text_ = []
            else:
                tokens.append(token_)
                text_.append(token_[1])
        else:
            if tokens:
                data['sentences'].append({
                    'tokens': tokens,
                    'text': ' '.join(text_),
                })
    return render_template('parse.html', data=data)


if __name__ == '__main__':
    app.run(port=default_port, host=default_host)
