import os
import json, yaml

from flask import Flask, after_this_request, send_file, safe_join, abort
from flask_restx import Resource, Api, fields
from flask_restx.api import Swagger

app = Flask(__name__)
api = Api(
    app=app,
    doc='/docs',
    version='1.0.0',
    title='TEST APP API',
    description='TEST APP API'
    )

response_fields = api.model('Resource', {
    'value': fields.String(required=True, min_length=1, max_length=200, description='example text')
})


# This class will handle POST
@api.route('/demo/', endpoint='demo')
@api.doc(responses={403: 'Not Authorized'})
class DemoList(Resource):
    @api.expect(response_fields, validate=True)
    @api.marshal_with(response_fields, code=200)
    def post(self):
        api.payload["value"] = 'Im the response ur waiting for'
        return api.payload


@api.route('/swagger')
class HelloSwagger(Resource):
    def get(self):
        data = json.loads(json.dumps(api.__schema__))
        with open('yamldoc.yml', 'w') as yamlf:
            yaml.dump(data, yamlf, allow_unicode=True, default_flow_style=False)
            file = os.path.abspath(os.getcwd())
            try:
                @after_this_request
                def remove_file(resp):
                    try:
                        os.remove(safe_join(file, 'yamldoc.yml'))
                    except Exception as error:
                        print("Error removing or closing downloaded file handle", error)
                    return resp

                return send_file(safe_join(file, 'yamldoc.yml'), as_attachment=True, attachment_filename='yamldoc.yml', mimetype='application/x-yaml')
            except FileExistsError:
                abort(404)


# main driver function
if __name__ == '__main__':
    app.run(port=5003, debug=True)
