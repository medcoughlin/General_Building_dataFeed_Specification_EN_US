#Flask: 是一个基于Python的Web框架，用于构建Web应用程序。

#jsonify: 是Flask提供的一个函数，用于将Python对象转换为JSON格式的响应。

#render_template: 是Flask提供的一个函数，用于渲染HTML模板并返回给客户端。

#redirect: 是Flask提供的一个函数，用于进行URL重定向。

#request: 是Flask提供的一个全局对象，用于访问客户端发送的请求数据。

#url_for: 是Flask提供的一个函数，用于生成URL路径。

#flash: 是Flask提供的一个用于向用户显示闪现消息的功能。

#send_from_directory: 是Flask提供的一个函数，用于从指定目录中发送文件给客户端。

#os: 是Python标准库中的模块，提供了与操作系统相关的功能，如文件路径操作和目录操作等。

#random: 是Python标准库中的模块，提供了生成随机数的功能。

#datetime: 是Python标准库中的模块，提供了日期和时间相关的功能。

#werkzeug.utils: 是Werkzeug库中的一个模块，提供了一些常用的实用函数，如安全的文件名处理函数secure_filename。

#math: 是Python标准库中的模块，提供了数学运算相关的函数和常量。

#json: 是Python标准库中的模块，提供了JSON数据的编码和解码功能
from flask import Flask,jsonify,render_template,redirect, request, url_for, flash, send_from_directory
import os,random,datetime
from werkzeug.utils import secure_filename
basedir = os.path.abspath(os.path.dirname(__file__))                 # 获取当前文件所在目录
UPLOAD_FOLDER = basedir+'/static/files'                           # 计算图片文件存放目录
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}     # 设置可上传图片后缀
import math,json
from concurrent.futures import ProcessPoolExecutor
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['SECRET_KEY']='&*89^77568%095656'
import plotly
import plotly.express as px
import pandas as pd

from draw import draw_data

@app.route('/',methods=['GET','POST'],endpoint='index')
def index():
    files=os.listdir(UPLOAD_FOLDER)
    # fig=create_plotly_figure()
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html')
#这行代码使用os.listdir()函数获取指定文件夹UPLOAD_FOLDER中的所有文件和文件夹的列表，并将结果赋值给变量files。这里假设UPLOAD_FOLDER是一个包含上传的图片文件的文件夹路径。
#fig=create_plotly_figure(): 这行代码调用了一个名为create_plotly_figure()的函数，并将返回的结果赋值给变量fig。这个函数应该是在另一个文件中定义的，根据代码中的引用可以推断出它与Plotly库有关，用于创建一个图形对象。
#graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder): 这行代码使用json.dumps()函数将图形对象fig转换为JSON格式的字符串，并将结果赋值给变量graphJSON。这里使用了plotly.utils.PlotlyJSONEncoder类来处理特定的编码要求，将Plotly图形对象转换为JSON。
#return render_template('index.html',pics=files,graphJSON=graphJSON): 这行代码使用render_template()函数渲染名为index.html的HTML模板，并将files和graphJSON作为参数传递给模板。这样，模板中可以使用这些参数来显示文件列表和图形数据。

def allowed_file(filename):                                          # 检查上传图片是否在可上传图片允许列表
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            # return jsonify({'code': 400, 'msg': '没有选择文件'})
            return redirect(url_for('index'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            # return jsonify({'code': 400, 'msg': '文件没有名字无法获取'})
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            # 获取安全的文件名 正常文件名
            filename = secure_filename(file.filename)
            # 生成随机数
            random_num = random.randint(0, 100)
            # f.filename.rsplit('.', 1)[1] 获取文件的后缀
            # filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(random_num) + "." + filename.rsplit('.', 1)[1]
            filename=f"原始文件.{filename.rsplit('.', 1)[1]}"
            file_path = app.config['UPLOAD_FOLDER']  # basedir 代表获取当前位置的绝对路径
            # 如果文件夹不存在，就创建文件夹
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            """
            file.save(os.path.join(file_path, filename))这个步骤就是你进行数据
            处理的步骤，我这边是一个保存操作，你可以对这个文件进行读取操作,首先上传文
            件然后保存文件最后对保存的文件进行读取处理
            """
            file.save(os.path.join(file_path, filename))
            """
            stats=os.stat(os.path.join(file_path, filename))
            print(f'文件大小{stats.st_size}')
            这就是对我们刚才保存的文件进行一个大小的获取，同样你可以用你的代码进行你的逻辑
            处理
            """
            stats=os.stat(os.path.join(file_path, filename))
            print(f'文件大小{stats.st_size}')
            flash('文件保存成功')
            # map_data,city_data=draw_data()
            # print(city_data)
            # return render_template('index.html',map_data=map_data,cities=city_data)
            fig = draw_data(os.path.join(file_path, filename))
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('index.html', graphJSON=graphJSON)
        else:
            flash('不是csv或xlsx或xls文件')
            return redirect(url_for('index'))


if __name__=='__main__':

    app.run(debug=True)