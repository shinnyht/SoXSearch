import sys

from soxsearch import app

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
