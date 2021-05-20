<<<<<<< HEAD
from flaskblog import create_app

app = create_app()
=======
from event import app # type: ignore
>>>>>>> c068f17ae7f5b605325383aa4998fc22e5b8afcd

if __name__ == '__main__':
    app.run(debug=True)
