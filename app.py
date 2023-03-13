from flask import request, Response, jsonify
import json
from flask import Flask
import simple_search
app = Flask(__name__)

@app.route("/api/search", methods=['POST'])
def search():
    try:
        req_json = json.loads(request.data)
        print(req_json)
        result = simple_search.get_best_matches(
            data=req_json['data'],
            query=req_json['query'],
            case_sensitivity=req_json['case_sensitivity'],
            fuzzy_search=req_json['fuzzy_search'],
            nlp_search=req_json['nlp_search']
        )
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=False)
