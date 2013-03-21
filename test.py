from flask import Flask
from flask import request,url_for
from flask import render_template
from flask import redirect,Response
import sqlite3
import json

app = Flask(__name__)

@app.route("/")
@app.route('/<imagename>', methods=['POST', 'GET'])
def mainpage(imagename=None):
    if request.method == 'GET':
        
        if imagename:
            imgname=(imagename,)
            con = sqlite3.connect('Image.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM Image WHERE imgname=?", imgname)
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    imgname = row[0]
                    imgdata = row[1]
                return render_template('paint.html', saved=imgdata)
            else:
                resp = Response("""<html> <script> alert("Image not found");document.location.href="/" </script> </html>""")
                return resp
        else:
            return render_template('paint.html')
	
	
    if request.method == 'POST':
        imgname=request.form['imagename']
        imgdata=request.form['string']
	    
        data=(imgname, imgdata)

        con = sqlite3.connect("Image.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Image(imgname text, imgdata string)")
        cur.execute("INSERT INTO Image VALUES(?, ?)", data)
        con.commit()
        con.close()
        resp = Response("saved")
        return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
