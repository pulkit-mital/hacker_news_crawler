from Article import Article
from flask import Flask
from flask import jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'hackernews'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hackernews'
mongo = PyMongo(app)


@app.route('/articles', methods=['GET'])
def get_all_articles():
    articles = mongo.db.articles
    output = []
    error = ''
    status = ''
    if articles.count() > 0:
        for article in articles.find():
            status = 'success'
            post_article = Article(article['title'], article['description'], article['image_url'], article['url'],
                                   article['category_name'], article['category_slug'], article['created_at'])
            output.append(post_article.__dict__)

    else:
        status: "error"
        error = "No Articles found"
        return jsonify({'status': status, 'error': error}), 404

    return jsonify({'status': status, 'articles': output})


if __name__ == '__main__':
    app.run(debug=True)
