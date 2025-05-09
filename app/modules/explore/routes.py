from flask import render_template, request, jsonify

from app.modules.explore import explore_bp
from app.modules.explore.forms import ExploreForm
from app.modules.explore.services import ExploreService
from app.modules.api.decorators import token_required


@explore_bp.route('/explore', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        query = request.args.get('query', '')
        form = ExploreForm()
        return render_template('explore/index.html', form=form, query=query)

    if request.method == 'POST':
        criteria = request.get_json()
        print(criteria)
        datasets = ExploreService().filter(**criteria)
        return jsonify([dataset.to_dict() for dataset in datasets])


# ==============================================================================
# Routes for the explore module to consume from discord bot

@explore_bp.route('/api/explore/<query>', methods=['GET'])
@token_required
def api_explore(query):
    datasets = ExploreService().filter(query=query)
    return jsonify([dataset.to_dict() for dataset in datasets])
