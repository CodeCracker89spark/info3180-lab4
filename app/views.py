"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from flask_wtf import FlaskForm
import os
from wtforms import StringField
from wtforms.validators import DataRequired, Length,InputRequired, Email
from wtforms import StringField, TextField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
import os
from app.forms import UploadForm
from app.__init__ import UPLOAD_FOLDER
from app import app
from app import forms
from flask import render_template, request, redirect, url_for, flash, session, abort, Flask,Markup
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    mlist = get_uploaded_images()
    #string = "<ul>\n"
    string =  Markup( "<img src = '{{url_for('static',filename='uploads/crabrawler.jpg' )}}' alt ='crab guy' /> ")
    output =Markup (str(mlist[1][65:]))
   # hope=Markup("<img  src =  '{{url_for('uploads'filename='crabrawler.jpg' )}}'/>")
    hope= Markup("<img src ="+str(mlist[1][65:])+" />")
    #string +="</ul>"
    """string = "<ul>\n"
    for s in mlist:
        string += "<li>" +"<img src = "+str({{url_for('static',filename=str(s) )}})+ "> </li>\n"
    string += "</ul>"
    return string"""
    #return render_template('files.html',st=string)

    """Render the website's about page."""
    return render_template('about.html', name="Tyler Thomas", st = hope,k=output)


@app.route('/files')
def files():
    mlist = get_uploaded_images()

    """
    string = "<ul>\n"
    for s in mlist:
        string += "<li> <img src ="+str(s)+" alt = /> </li>\n"
    string += "</ul>"
    string = Markup(string)"""
    
    return render_template('files.html',images=mlist)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    
    filefolder = UPLOAD_FOLDER

    form = UploadForm()
    
    if not session.get('logged_in'):
        abort(401)

    # Instantiate your form class

    # Validate file upload on submit
    if request.method == 'POST':
        # Get file data and save to your uploads folder
        if form.validate_on_submit():
            file = request.files.get('file')
            
            filename = secure_filename(form.upload.data.filename)
            form.upload.data.save(os.path.join(filefolder, filename))
            flash('File Saved', 'success')
            return redirect(url_for('home'))

    if request.method == 'GET':
        
         return render_template('upload.html',form=form)

    return render_template('upload.html', form=form)
    
def get_uploaded_images():
    rootdir = os.getcwd()
    image_list=[]
    print (rootdir)
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
        for file in files:
            # print (os.path.join(subdir, file))
            print(file)
            image_list.append( file)
            
    return image_list
@app.route('/login', methods=['POST', 'GET'])
def login():
    get_uploaded_images()
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in', 'success')
            return redirect(url_for('upload'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
