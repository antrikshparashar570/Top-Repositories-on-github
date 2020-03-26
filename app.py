from flask import Flask, render_template
from flask_restful import Resource, Api
from top_repositories import OpenWebsite
from top_commitees import OpenRepository

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
    return render_template('input.html')

api.add_resource(OpenWebsite,'/openWebsite')
#api.add_resource(OpenRepository,'/openRepository')

if __name__ == '__main__':
    app.run()
