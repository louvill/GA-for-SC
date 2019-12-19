import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World')

app = webapp2.WSGIApplication([('pivotal-spark-262218', MainPage),],debug=True)