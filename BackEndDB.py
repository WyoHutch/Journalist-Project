from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import sqlite3


import os

app = Flask(__name__)
heroku = Heroku(app)


basedir = os.path.abspath(os.path.dirname(__file__))
dbFile = "sqlite:///" + os.path.join(basedir, "Journalist.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = dbFile
conn = sqlite3.connect('./Journalist.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://nftkskfcppdfmm:dd0940e817dc6997ce88498edf55455202daedc994e8193beecbc06f70c94b6e@ec2-54-235-163-246.compute-1.amazonaws.com:5432/dbci322q72m264"

CORS(app)

class Journalist(db.Model):
    __tablename__ = "Journalist"
    ID = db.Column(db.Integer, primary_key = True)
    FName = db.Column(db.String(12), unique = False)
    LName = db.Column(db.String(20), unique = False)
    Description = db.Column(db.Text(128), unique = False)
    # Picture = db.Column(db.Blob, unique = True)

    def __init__(self, FName, LName, Description):
        self.FName = FName
        self.LName = LName
        self.Description = Description
        # self.Picture = Picture

class Articles(db.Model):
    __tablename__ = "Articles"
    ArtID = db.Column(db.Integer, primary_key = True)
    Writer = db.Column(db.Integer, unique = False)
    Heading = db.Column(db.Text(80), unique = False)
    Subheading = db.Column(db.Text(128), unique = False)
    Body = db.Column(db.Text(2000), unique = True)

    def __init__(self, Writer, Heading, Subheading, Body):
        self.Writer = Writer
        self.Heading = Heading
        self.Subheading = Subheading
        self.Body = Body

class Pictures(db.Model):
    __tablename__ = "Pictures"
    PicID = db.Column(db.Integer, primary_key = True)
    ArticleID = db.Column(db.Integer, unique = False)
    TagLine = db.Column(db.Text(128), unique = False)
    # Picture = db.Column(db.Blob, unique = False)

    def __init__(self, ArticleID, TagLine):
        self.ArticleID = ArticleID
        self.TagLine = TagLine
        # self.Picture = Picture

class JournalSchema(ma.Schema):
    class Meta:
        fields = ("ID", "FName", "LName", "Description")

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ("ArtID", "Writer", "Heading", "Subheading", "Body")

class PictureSchema(ma.Schema):
    class Meta:
        fields = ("PicID", "ArticleID", "TagLine")

single_jschema = JournalSchema()
plural_jschema = JournalSchema(many = True)

single_aschema = ArticleSchema()
plural_aschema = ArticleSchema(many = True)

single_pschema = PictureSchema()
plural_pschema = PictureSchema(many = True)

@app.route('/journalist', methods=['POST'])
def add_journal():
    FName = request.json["FName"]
    LName = request.json["LName"]
    Description = request.json["Description"]
    # Picture = request.json["Picture"]

    new_journal = Journalist(FName, LName, Description)

    db.session.add(new_journal)
    db.session.commit()

    return single_jschema.jsonify(Journalist.query.get(new_journal.ID))

# Journalist Endpoints Defined Here

@app.route('/journalists', methods=['GET'])
def get_journalists():
    all_journalists = Journalist.query.all()
    return jsonify(plural_jschema.dump(all_journalists))

@app.route('/getJournal/<id>', methods=['GET'])
def return_journal(id):
    journal = Journalist.query.get(id)
    return jsonify(single_jschema.dump(journal))

@app.route('/journalist/<id>', methods=['PUT'])
def update_journalist(id):
    journal = Journalist.query.get(id)

    journal.FName = request.json('FName')
    journal.LName = request.json('LName')
    journal.Description = request.json('Description')
    # journal.Pictures = request.json('Pictures')

    db.session.commit()
    return single_jschema.jsonify(journal)

@app.route('/delJournal/<id>', methods=['DELETE'])
def delete_journal(id):
    journal = Journalist.query.get(id)
    db.session.delete(journal)
    db.session.commit()

    return "Journalist Record Deleted"

# Article Endpoints Defined Here

@app.route('/article', methods=['POST'])
def add_article():
    Writer = request.json["Writer"]
    Heading = request.json["Heading"]
    Subheading = request.json["Subheading"]
    Body = request.json["Body"]

    new_journal = Articles(Writer, Heading, Subheading, Body)

    db.session.add(new_article)
    db.session.commit()

    return single_aschema.jsonify(Articles.query.get(new_article.ID))

@app.route('/articles', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    return jsonify(plural_aschema.dump(all_articles))

@app.route('/getArticle/<id>', methods=['GET'])
def return_article(id):
    article = Articles.query.get(id)
    return jsonify(single_aschema.dump(article))

@app.route('/article/<id>', methods=['PUT'])
def update_article(id):
    article = Articles.query.get(id)

    article.Writer = request.json('Writer')
    article.Heading = request.json('Heading')
    article.Subheading = request.json('Subheading')
    article.Body = request.json('Body')

    db.session.commit()
    return single_aschema.jsonify(article)

@app.route('/delArticle/<id>', methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return "Article Record Deleted"

# Picture Endpoints Defined Here

@app.route('/picture', methods=['POST'])
def add_picture():
    ArticleID = request.json["ArticleID"]
    TagLine = request.json["TagLine"]


    new_article = Journalist(ArticleID, TagLine)

    db.session.add(new_picture)
    db.session.commit()

    return single_aschema.jsonify(Journalist.query.get(new_picture.ID))

@app.route('/pictures', methods=['GET'])
def get_pictures():
    all_pictures = Pictures.query.all()
    return jsonify(plural_jschema.dump(all_pictures))

@app.route('/getPicture/<id>', methods=['GET'])
def return_picture(id):
    picture = Pictures.query.get(id)
    return jsonify(single_jschema.dump(picture))

@app.route('/picture/<id>', methods=['PUT'])
def update_picture(id):
    picture = Pictures.query.get(id)

    picture.ArticleID = request.json('ArticleID')
    picture.TagLine = request.json('TagLine')


    db.session.commit()
    return single_jschema.jsonify(picture)

@app.route('/delPicture/<id>', methods=['DELETE'])
def delete_picture(id):
    picture = Picture.query.get(id)
    db.session.delete(picture)
    db.session.commit()

    return "Picture Record Deleted"

if __name__ == '__main__':
    app.run(debug = True)
