import sys
from flask import request, redirect, render_template, flash
import cgi
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
#import cartopy.feature as cfeature
from clean import clean
from models import get_hits

#%matplotlib inline

from app import app, db, engine, update_database

#from clean import

@app.route('/update')
def update():
    return render_template('update.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    hurricane_data_from_sql = pd.read_sql_table(
        'hurricane',
        con=engine
    )

    if (hurricane_data_from_sql.empty and request.args.get('data_url')== None):
        return redirect('/update')
    elif hurricane_data_from_sql.empty:
        hurricane_data_url = request.args.get('data_url')
        hurricane_data = clean(hurricane_data_url)
        update_database(hurricane_data)
        return "<h1>Data loaded</h1>"
    elif request.method == 'POST' :        
        my_location = [float(request.form['latitude']), float(request.form['longitude'])]
        radius = float(request.form['radius'])
        total_hits = get_hits(hurricane_data_from_sql, my_location, radius)
        return render_template('/analysis.html', total_hits = len(total_hits[0]), total_storms = total_hits[1])
    else:
        return render_template('/index.html')
if __name__ == '__main__':
    app.run()