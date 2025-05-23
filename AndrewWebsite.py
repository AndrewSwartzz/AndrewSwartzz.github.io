import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db}

if __name__ == '__main__':
    app.run(debug=True)