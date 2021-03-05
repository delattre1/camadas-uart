from flask import Flask, render_template, request
import os
import sys
from werkzeug.utils import secure_filename

app = Flask(__name__)

# caminho_boleto = os.path.join(
#    app.config['UPLOAD_FOLDER'], filename)
# f.save(caminho_boleto)


@app.route('/', methods=['GET', 'POST'])
def show_contas():
    if request.method == 'POST':
        save_path = '/imgs/'
        # app.config['UPLOAD_FOLDER'] = save_path
        f = request.files['file']
        filename = (secure_filename(f.filename))
        print(f'file: {filename}\n{save_path+filename}', file=sys.stderr)
        return (render_template('home.html'))
    else:
        return render_template('home.html')  # , boletos=boletos)
