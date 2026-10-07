from datetime import datetime, timezone, date
from urllib.parse import urlsplit

from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    abort,
    session,
    jsonify
)

import sqlalchemy as sa
import random
import requests

from app import app, db


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title='Home')

@app.route('/bio')
def bio():
    return render_template('bio.html', title='Bio')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Posts', posts=posts)

@app.route('/post')
def post():
    return render_template('posts/healthcare.html', title='Posts', posts=posts)

@app.route('/data')
def data():
    return render_template('posts/datasecurity.html', title='Posts', posts=posts)

@app.route('/project')
def project():
    return render_template('projects/tamagotchi.html', title='Project')

@app.route('/projects')
def projects():
    return render_template('projects.html', title='Projects')

@app.route('/mandible')
def mandible():
    return render_template('projects/mandible.html', title='Mandible')

@app.route('/garden')
def garden():
    return render_template('posts/garden_of_earthly_delights.html', title='Garden')

@app.route('/trial')
def trial():
    return render_template('posts/the_trial.html', title='The Trial')

@app.route("/independent-study")
def independent_study():
    return render_template("projects/independent_study.html")


@app.route("/dad-life")
def dad_life():
    return render_template("projects/dad_life_project.html")

@app.route("/pokemon_game_project")
def pokemon_game_project():
    return render_template("projects/pokemon_game_project.html")

@app.route('/pokemon-game', methods=['GET', 'POST'])
def pokemon_game():
    # Initialize or reset game state
    if 'game_state' not in session or request.method == 'POST':
        session['game_state'] = {
            'score': 0,
            'current_pokemon': None,
            'options': [],
            'correct_guesses': 0,
            'total_guesses': 0,
            'cute_list': session.get('game_state', {}).get('cute_list', [])
        }
        session.modified = True

    game_state = session['game_state']

    # Get a random Pokémon if none is set
    if not game_state['current_pokemon']:
        random_pokemon_id = random.randint(1, 1000)
        pokemon_data = get_pokemon_data(random_pokemon_id)

        if pokemon_data:
            game_state['current_pokemon'] = pokemon_data
            options = generate_options(pokemon_data['name'])
            game_state['options'] = options
            session.modified = True

    return render_template('pokemon_game.html', game_state=game_state)

@app.route('/pokemon-guess/<guess>')
def pokemon_guess(guess):
    game_state = session.get('game_state', {})
    correct = False

    if game_state and game_state['current_pokemon']:
        correct_pokemon = game_state['current_pokemon']['name']
        correct = guess.lower() == correct_pokemon.lower()

        game_state['total_guesses'] += 1

        if correct:
            game_state['correct_guesses'] += 1
            game_state['score'] += 10

        game_state['current_pokemon'] = None
        session.modified = True

    return jsonify({
        'correct': correct,
        'correct_pokemon': correct_pokemon if game_state else None,
        'score': game_state.get('score', 0),
        'accuracy': calculate_accuracy(game_state) if game_state else 0
    })


@app.route('/add-cute/<pokemon_name>')
def add_cute(pokemon_name):
    game_state = session.get('game_state', {})

    if game_state:
        if 'cute_list' not in game_state:
            game_state['cute_list'] = []

        pokemon_data = None

        if (game_state['current_pokemon'] and
                game_state['current_pokemon']['name'] == pokemon_name):

            pokemon_data = game_state['current_pokemon']

        else:
            response = requests.get(
                f"{POKEAPI_BASE_URL}pokemon/{pokemon_name.lower()}"
            )

            if response.status_code == 200:
                data = response.json()

                pokemon_data = {
                    'id': data['id'],
                    'name': data['name'],
                    'sprite': data['sprites']['front_default']
                }

        if pokemon_data and pokemon_data not in game_state['cute_list']:
            game_state['cute_list'].append(pokemon_data)
            session.modified = True

            return jsonify({
                'success': True,
                'message': f'{pokemon_name.title()} added to cute list!'
            })

    return jsonify({
        'success': False,
        'message': 'Failed to add to cute list'
    })


@app.route('/view-cute-list')
def view_cute_list():
    game_state = session.get('game_state', {})
    cute_list = game_state.get('cute_list', [])

    return render_template(
        'cute_list.html',
        cute_list=cute_list
    )

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"


def get_pokemon_data(pokemon_id):
    try:
        response = requests.get(
            f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}"
        )

        if response.status_code == 200:
            data = response.json()

            return {
                'id': data['id'],
                'name': data['name'],
                'sprite': data['sprites']['front_default'],
                'silhouette': data['sprites']['front_default']
            }

    except Exception as e:
        print(f"Error fetching Pokémon data: {e}")

    return None


def generate_options(correct_name):
    # Start with the correct answer
    options = [correct_name]

    # Add three incorrect Pokémon
    while len(options) < 4:

        random_id = random.randint(1, 1000)

        pokemon = get_pokemon_data(random_id)

        if pokemon and pokemon['name'] not in options:
            options.append(pokemon['name'])

    # Randomize the answer positions
    random.shuffle(options)

    return options


def calculate_accuracy(game_state):
    if game_state['total_guesses'] == 0:
        return 0

    return (
        game_state['correct_guesses']
        / game_state['total_guesses']
    ) * 100


@app.route('/potoo')
def potoo():
   return render_template('projects/potoo.html', title='Potoo') 




