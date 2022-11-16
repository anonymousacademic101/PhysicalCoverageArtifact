import os
import glob
import datetime

from flask import send_from_directory
from flask import render_template
from flask import request
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    """
    Computes the all statistics and returns the index template with all required statistics 
    """
    return render_template('index.html')     

@app.route('/paper')
def about():
    """
    Shows the about page
    """
    return render_template('paper.html')     

@app.route('/documentation')
def documentation():
    """
    Shows the documentation page
    """
    return render_template('documentation.html')     

@app.route('/paper_appendix')
def appendix():
    """
    Shows the appendix page
    """
    return render_template('appendix.html')     

@app.route('/generating_results')
def results():
    """
    Shows the results page
    """
    return render_template('results.html')     
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
