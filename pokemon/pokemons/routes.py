from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_required
from pokemon.models import Pokemon, Type
from pokemon.extensions import db

pokemons_bp = Blueprint('pokemons', __name__, template_folder='templates')

@pokemons_bp.route('/')
@login_required
def index():
    query = db.select(Pokemon).where(Pokemon.user_id == current_user.id)
    pokemons = db.session.scalars(query).all()
    return render_template('pokemons/index.html',
                           title='Pokemons Page',
                           pokemons=pokemons)

@pokemons_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_pokemon():
    types = db.session.scalars(db.select(Type).order_by(Type.name)).all()

    if request.method == 'POST':
        name = request.form.get('name')
        height = request.form.get('height')
        weight = request.form.get('weight')
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        user_id = current_user.id
        pokemon_types = request.form.getlist('pokemon_types')

        pokemon = db.session.scalar(db.select(Pokemon).where(Pokemon.name == name))
        if pokemon:
            flash(f'Pokemon: {pokemon.name} is already exists!', 'warning')
            return redirect(url_for('pokemons.new_pokemon'))

        p_types = [db.session.get(Type, int(tid)) for tid in pokemon_types if tid]

        pokemon = Pokemon(
            name=name,
            height=height,
            weight=weight,
            description=description,
            img_url=img_url,
            user_id=user_id,
            types=p_types
        )
        db.session.add(pokemon)
        db.session.commit()
        flash('Add new pokemon successful', 'success')
        return redirect(url_for('pokemons.index'))

    return render_template('pokemons/new_pokemon.html',
                           title='New Pokemon Page',
                           types=types)