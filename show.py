import cgi, os

print('content-type:text/html\r\n\r\n')

form = cgi.FieldStorage()
pn = str(form.getvalue("pname"))
des = str(form.getvalue("des"))
fle = form['filename']

fn = os.path.basename(fle.filename)
open("C:/Users/Justin/Documents/GitHub/HiddenPathSolver/temp" + fn, "wb").write(fle.file.read())

print('<html>')
print('<body><center>')
print('<h1>Product Name\n(%s)</h1>'%pn)
print('<img src=temp/%s>'%fn)
print('<h2>%s</h2>'%des)
print('</center></body></html>')
