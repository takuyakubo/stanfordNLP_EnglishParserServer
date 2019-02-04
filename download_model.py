import stanfordnlp

DEFAULT_MODEL_DIR = './stanford_resource'

if __name__ == '__main__':
    stanfordnlp.download('en_ewt', resource_dir=DEFAULT_MODEL_DIR)
