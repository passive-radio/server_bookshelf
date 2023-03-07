from flask import *
from flask_cors import CORS

from logger import http_request_logging
import csv
import lab_bookshelft as lab_bookshelft

app = Flask(__name__)
CORS(app)

BOOKSHELF_PATH = "/home/yokubo/dev/quagga_host/server/log/bookshelf.csv"
bookshelf = lab_bookshelft.Bookshelf(BOOKSHELF_PATH)



@app.route("/book", methods=["POST"])
@http_request_logging
def book():
    id = request.get_json()["id"]
    print("id:", id)
    bookshelf.add_book("", int(id), "", "", "", "")
    
    return id



if __name__ == "__main__":
    
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
    