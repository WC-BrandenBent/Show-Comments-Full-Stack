from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlalchemy

app = Flask(__name__)

# Initialize the database connection
db = sqlalchemy.create_engine("mariadb+pymysql://root:@localhost:3306/simpledb", echo=True)

# Apply CORS to the entire app
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/comment", methods=["POST"])
def add_comment_route():
    data = request.get_json()
    print(data)
    
    username = data.get("username")
    comment = data.get("comment_text")
    
    add_comment(username, comment)
    
    return jsonify({"message": "Comment successfully added"}), 200

@app.route("/api/comments", methods=["GET"])
def get_comments_route():
    comments = get_comments()
    return jsonify(comments), 200

@app.route("/api/comment", methods=["PUT"])
def update_comment_route():
    data = request.get_json()
    
    comment_id = data.get("comment_id")
    comment_text = data.get("comment_text")
    
    update_comment(comment_id, comment_text)
    
    return jsonify({"message": "Comment successfully updated"}), 200

@app.route("/api/comment/", methods=["DELETE"])
def delete_comment_route():
    data = request.get_json()
    print(data)
    
    comment_id = data.get("comment_id")
    comment_text = data.get("comment_text")
    
    delete_comment(comment_id, comment_text)    
    
    return jsonify({"message": "Comment successfully deleted"}), 200

def get_comments():
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM comments"))
        comments = []
        for row in result:
            comments.append({
            'comment_id': row[0],
            'username': row[1],
            'comment_text': row[2]
            })
    return comments

def add_comment(username, comment_text):
    with db.connect() as conn:
        conn.execute(sqlalchemy.text("""INSERT INTO `comments` (`comment_id`, `username`, `comment_text`) VALUES (NULL, :username, :comment_text)"""), 
        {
            "username": username,
            "comment_text": comment_text
        })
    return get_comments()

def update_comment(comment_id, comment_text):
    with db.connect() as conn:
        conn.execute(sqlalchemy.text("""UPDATE `comments` SET `comment_text` = :comment_text WHERE `comments`.`comment_id` = :comment_id"""), 
        {
            "comment_id": comment_id,
            "comment_text": comment_text
        })
    return get_comments()

def delete_comment(comment_id, comment_text):
    with db.connect() as conn:
        conn.execute(sqlalchemy.text("""DELETE FROM `comments` WHERE `comments`.`comment_id` = :comment_id AND `comments`.`comment_text` = :comment_text"""), 
        {
            "comment_id": comment_id,
            "comment_text": comment_text
        })
    return get_comments()

if __name__ == '__main__':
    app.run(port=5001, debug=True)