from flask import Flask
from flask_restplus import Resource,Api,fields
#from flask_cors import CORS, cross_origin
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0',title='ToDo Restful',description="A simple ToDo restful application.")

ns = api.namespace('todos',description='ToDo Operations')

todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='Task details')
})

class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []
    
    def get(self,id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404,"Todo {} does n't exist".format(id))

    def create(self,data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self,id):
        todo = self.get(id)
        self.todos.remove(todo)

DAO = TodoDAO()
DAO.create({'task':'Build an API'})
DAO.create({'task':'????'})
DAO.create({'task':'profit!'})

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all Todos and lets you to add Todos'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo,code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload),201

    @ns.route('/<int:id>')
    @ns.response(404,'Todo not found')
    @ns.param('id','The task identifier')
    class Todo(Resource):
        '''Show a single todo item'''
        @ns.doc('get_todo')
        @ns.marshal_with(todo)
        def get(self,id):
            '''Fetch a given resource'''
            return DAO.get(id)

        @ns.doc('delete_todo')
        @ns.response(204, 'Todo deleted')
        def delete(self, id):
            '''Delete a task given its identifier'''
            DAO.delete(id)
            return '',204

        @ns.expect(todo)
        @ns.marshal_with(todo)
        def put(self, id):
            '''Update a task given its identifier'''
            return DAO.update(id, api.payload)

if __name__ == '__main__':
    app.run(debug = True)