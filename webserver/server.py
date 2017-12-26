#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://aja2173:6944@35.196.90.148/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)
#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible. """
  try: 
    print "done!!!"
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass




@app.route('/')
def index():

  
  print type(g.conn)
  return render_template("index.html")




@app.route('/first')
def first():
  command = "select * from album where album.year>2014 order by album.year ;"
  
  c = g.conn.execute(command)
  a = []
  for row in c : 
	local = []
	local.append(str(row['artist_id']))
	local.append(row['year'])
	local.append(str(row['album_id']))
	a.append(local)
  
  c.close()
  context = dict(data = a)


  return render_template("another.html", **context)


@app.route('/second')
def second():
  command = "SELECT   A1.artist_id   Artist,   COUNT(A2.award_id)   The_number_of_winning_the_album_of_year FROM   album   A1,   awarded_album   A2 WHERE   A1.album_id=A2.album_id GROUP   BY   A1.artist_id ORDER   BY   the_number_of_winning_the_album_of_year   DESC;"

  c = g.conn.execute(command)
  a = []
  for row in c :
        local = []
        local.append(str(row['artist']))
        local.append(str(row['the_number_of_winning_the_album_of_year']))
        a.append(local)

  c.close()
  context = dict(data = a)


  return render_template("second.html", **context)


@app.route('/third')
def third():
  command = "SELECT   C1.artist_id   artist,   C1.country   Country,   COUNT(C2.album_id)   total_album FROM   artist   C1,   album   C2 WHERE   C1.artist_id   =   C2.artist_id GROUP   BY   C1.artist_id ORDER   BY   total_album   DESC;"
  c = g.conn.execute(command)
  a = []
  for row in c :
        local = []
        local.append(str(row['artist']))
        local.append(str(row['country']))
        local.append(str(row['total_album']))
        a.append(local)

  c.close()
  context = dict(data = a)


  return render_template("third.html", **context)


@app.route('/fourth')
def fourth():
  command = "SELECT   B1.artist_id1   Origin,   B2.artist_id   AS   Similar,   B2.album_id   AS   Similar_album,   B2.rating   AS   Rating FROM   similar_artists   B1 INNER   JOIN   album   B2 ON   B1.artist_id2   =   B2.artist_id ORDER   BY   Rating   ASC   LIMIT   1;"

  c = g.conn.execute(command)
  a = []
  tmp = ['origin', 'similar', 'album', 'rating']
  a.append(tmp)
  for row in c :
        local = []
        local.append(str(row['origin']))
        local.append(str(row['similar']))
        local.append(str(row['similar_album']))
        local.append(str(row['rating']))
        a.append(local)

  c.close()
  context = dict(data = a)


  return render_template("fourth.html", **context)

@app.route('/sixth')
def sixth():
  command = "select artist_id artist, album_id album, name song from song where artist_id = 'Swift'and album_id = 'Fearless';"

  c = g.conn.execute(command)
  a = []
  tmp = ['artist', 'album', 'song']
  a.append(tmp)
  for row in c :
        local = []
        local.append(str(row['artist']))
        local.append(str(row['album']))
        local.append(str(row['song']))
        a.append(local)

  c.close()
  context = dict(data = a)


  return render_template("sixth.html", **context)


@app.route('/seventh')
def seventh():
  command = "select country, genre_id Genre, artist_id artist from artist where country = 'USA' and genre_id='country' group by artist_id;"

  c = g.conn.execute(command)
  a = []
  tmp = ['country', 'genre', 'artist']
  a.append(tmp)
  for row in c :
        local = []
        local.append(str(row['country']))
        local.append(str(row['genre']))
        local.append(str(row['artist']))
        a.append(local)

  c.close()
  context = dict(data = a)


  return render_template("seventh.html", **context)



@app.route('/fifth')
def fifth():
  a = []
  context = dict(data = a)
  return render_template("fifth.html", **context)


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


@app.route('/do_select', methods=['POST'])
def do_select():
  
  year = request.form['year']
  if RepresentsInt(year)==False:
	a = ['Invalid Input']
	context = dict(data = a)
  	return render_template("fifth.html", **context)	
  
  if int(year)>2017 or int(year)<2010:
        a = ['No avaiable year']
        context = dict(data = a)
        return render_template("fifth.html", **context)
 

  command = "select * from album where year = "+year  

  c = g.conn.execute(command)
  tmp = ['Artist', 'album', 'year', 'rating']
  a = []
  a.append(tmp)
  for row in c :
        local = []
        local.append(str(row['artist_id']))
        local.append(str(row['album_id']))
        local.append(str(row['year']))
        local.append(str(row['rating']))
        a.append(local)
  c.close()
  context = dict(data = a)
  return render_template("fifth.html", **context)



# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  print 'Hi'
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=true, threaded=threaded)
  run()
