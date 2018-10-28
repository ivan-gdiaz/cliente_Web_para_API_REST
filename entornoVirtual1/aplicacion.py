from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request


app = Flask(__name__, static_url_path = "")

usuarios = [
	{'id':1,
	'nombreUsuario': u'David Gilmour',
	'email': u'gilmour@pinkfloyd.com',
	'activo': True
	},
	{'id':2,
	'nombreUsuario': u'Richard Wright',
	'email': u'wright@pinkfloyd.com',
	'activo': False
	},
	{'id':3,
	'nombreUsuario': u'Roger Waters',
	'email': u'waters@pinkfloyd.com',
	'activo': True
	}
]

@app.route('/')
def root():
	return app.send_static_file('index.html')

@app.route('/v1/usuarios/', methods=['GET'])
def getUsuarios():
	return jsonify({'usuarios': usuarios})

@app.route('/v1/usuarios/<int:id>/', methods=['GET'])
def getUsuario(id):
        for usuario in usuarios:
                if usuario.get('id') == id:
                        return jsonify({'usuarios':usuario})
        abort(404)

#Definimos la respuesta para el codigo de error 404
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'No encontrado'}),404)

@app.route('/v1/usuarios/', methods=['POST'])
def crearUsuario():
        if not request.json or not 'email' in request.json:
                abort(404)
        id = usuarios[-1].get('id') + 1
        nombreUsuario = request.json.get('nombreUsuario')
        email = request.json.get('email')
        activo = False
        usuario = {'id': id, 'nombreUsuario': nombreUsuario, 'email': email, 'activo': activo}
        usuarios.append(usuario)
        return jsonify({'usuario':usuario}),201

@app.route('/v1/usuarios/<int:id>/', methods=['PUT'])
def actualizarUsuario(id):
	usuario = [usuario for usuario in usuarios if usuario['id'] == id]
	usuario[0]['nombreUsuario'] = request.json.get('nombreUsuario', usuario[0]['nombreUsuario'])
	usuario[0]['email'] = request.json.get('email', usuario[0]['email'])
	usuario[0]['activo'] = request.json.get('activo', usuario[0]['activo'])
	return jsonify({'usuarios':usuario[0]})

@app.route('/v1/usuarios/<int:id>/', methods=['DELETE'])
def borrarUsuario(id):
	usuario = [usuario for usuario in usuarios if usuario['id'] == id]
	usuarios.remove(usuario[0])
	return jsonify({}), 204 # No content

if __name__ == '__main__':
        app.run(debug=True)


