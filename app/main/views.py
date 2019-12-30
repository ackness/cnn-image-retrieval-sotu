import os

from flask import (current_app, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

from utils import download

from .. import get_image_search
from . import main
from .forms import ImgForm, URLForm

# 不同数据集有不同的路径
dataset_path_dict = {
    'holiday': 'holiday/jpg/',
    'ukbench': 'ukbench/full/',
}


@main.route('/', methods=['GET', 'POST'])
def index():
    imgform = ImgForm()
    urlform = URLForm()

    if imgform.validate_on_submit():
        file = imgform.fileimg.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_DIR'], filename)
        if not os.path.exists(filepath):
            file.save(filepath)
        return redirect(url_for('.result', filename=filename))
    elif urlform.validate_on_submit():
        url = urlform.txturl.data
        filename = secure_filename(url.split('/')[-1])
        filepath = os.path.join(current_app.config['UPLOAD_DIR'], filename)
        download(url, current_app.config['UPLOAD_DIR'], filename)
        if not os.path.exists(filepath):
            flash('无法取回指定URL的图片')
            return redirect(url_for('.index'))
        else:
            return redirect(url_for('.result', filename=filename))
    return render_template('index.html')


@main.route('/result', methods=['GET'])
def result():
    filename = request.args.get('filename')
    uri = os.path.join(current_app.config['UPLOAD_DIR'], filename)
    img_d, images, scores = get_image_search(uri)
    dataset = 'holiday'
    images = [os.path.join(dataset_path_dict[dataset], i) for i in images]
    print(images)

    return render_template('result.html', filename=filename, images=images)


@main.route('/images/<path:uri>')
def download_file(uri):
    return send_from_directory(current_app.config['DATABASE_DIR'],
                               uri, as_attachment=True)
