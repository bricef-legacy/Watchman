
import bottle
import tornado
import os
import sys


mypath = os.path.dirname(os.path.abspath(__file__))
STATICPATH = os.path.join(mypath, "static")


app = bottle.Bottle()

@app.route("/api/status")
def status():
  return {"status":"nominal"}



@app.route("/<filepath:path>")
def static(filepath):
  return bottle.static_file(filepath, STATICPATH) 
    
interface = app
    

