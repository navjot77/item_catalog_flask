from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()





class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                results = session.query(Restaurant).all()
                print results
                output=''
                output += "<html><body><h1><a href='/restaurants/new'>Make A new Restaurant</a><br></h1><ul>"
                for result in results:
                    output += "<li>%s</li>"%result.name
                    output += "<a href='/restaurants/%s/edit'  name='id'>  EDIT </a><br>"% result.id
                    output += "<a href='/restaurants/%s/delete'>  Delete  </a>"%result.id
                output += "</ul></html></body>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                item_id=self.path.split("/")[2]

                results = session.query(Restaurant).filter_by(id=item_id).one()
                print results
                output = ''
                output += "<html><body><h1><a href='/restaurants/new'>Are you sure to delete ?</a><br></h1><ul>"
                output += "<li>%s</li>" % results.name
                output += "</ul></html></body>"
                output += '''<form method='POST' enctype='multipart/form-data'
                    action='http://127.0.0.1:8080/restaurants/%s/delete'>
                     <input type="submit" value="DELETE">
                     </form>'''%item_id
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ''
                output += "<html><body><h1>Create A New Restaurant<br></h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='http://127.0.0.1:8080/restaurants/new'>
                <input name="message" type="text" >
                <input type="submit" value="CREATE">
                 </form>'''
                output += "</html></body>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/edit'):
                restaurant_id=self.path.split('/')[2]
                query=session.query(Restaurant).filter_by(id = restaurant_id).one()
                if query != []:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = ''
                    output += "<html><body><h1>Edit an Item  %s <br></h1>"%query.name
                    output += '''<form method='POST' enctype='multipart/form-data'
                        action='http://127.0.0.1:8080/restaurants/%s/edit'>
                        <input name="message" type="text" >
                        <input type="submit" value="Rename">
                         </form>'''%restaurant_id
                    output += "</html></body>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('content_type', 'text/html')
                self.end_headers()

                output = ''
                output += "<html><body>&#161Hola ! <a href='/hello'>Back to Hello</a>"

                output += '''<form method='POST' enctype='multipart/form-data'
                action='http://127.0.0.1:8080/hello'>
                <h2>What would you like me to say?</h2>
                <input name="message" type="text" >
                <input type="submit" value="Submit">
                 </form>'''

                output += "</html></body>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404,'FIle not found %s!' %self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/edit'):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageData = fields.get('message')
                item_id=self.path.split('/')[2]
                print messageData

                myquery=session.query(Restaurant).filter_by(id=item_id).one()
                myquery.name=messageData[0]
                session.add(myquery)
                session.commit()

                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('location', '/restaurants')
                self.end_headers()

            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageData = fields.get('message')
                item_id = self.path.split('/')[2]
                print messageData

                myquery = session.query(Restaurant).filter_by(id=item_id).one()
                session.delete(myquery)
                session.commit()

                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('location', '/restaurants')
                self.end_headers()

            if self.path.endswith('/restaurants/new'):

                ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messageData=fields.get('message')

                print messageData

                restaurant=Restaurant(name=messageData[0])
                session.add(restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('content-type','text/html')
                self.send_header('location','/restaurants')
                self.end_headers()


        except:
            self.send_error(404, 'FIle not found %s!' % self.path)



def main():
    try:
        port=8080
        server=HTTPServer(('',port),webserverHandler)
        print "Web server running on 8080"
        server.serve_forever()

    except KeyboardInterrupt:
        server.server_close()

if __name__ == '__main__':
    main()