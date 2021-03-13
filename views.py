from flask import request, jsonify
from flask.views import MethodView
from app import app
from errors import NotFound
from models import Ads


class AdsView(MethodView):

    def get(self, user_id):
        user = Ads.by_id(user_id)
        return jsonify(user.to_dict())

    def post(self):
        ads = Ads(**request.json)
        ads.set_date()
        ads.add()
        return jsonify(ads.to_dict())

    def put(self, user_id):
        ads = Ads(**request.json)
        ads_one = Ads.query.filter_by(id=user_id).first()
        ads_one.title = ads.title
        ads_one.description = ads.description
        ads_one.creator = ads.creator
        ads_one.add()
        return jsonify(ads_one.to_dict())

    def delete(self, user_id):
        ads_id = Ads.by_id(user_id)
        if Ads.del_id(ads_id):
            return jsonify({"message": "Delet ads"})
        else:
            return NotFound


@ app.route('/health/', methods=['GET', ])
def health():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})
    return {'status': 'OK'}


app.add_url_rule(
    '/ads/<int:user_id>', view_func=AdsView.as_view('ads_get'), methods=['GET'])

app.add_url_rule(
    '/ads/', view_func=AdsView.as_view('ads_create'), methods=['POST', ])

app.add_url_rule(
    '/ads/<int:user_id>', view_func=AdsView.as_view('ads_delete'), methods=['DELETE', 'PUT'])
