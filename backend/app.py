from flask import Flask, render_template, request, jsonify
import numpy as np
import random
from math import gcd
from datetime import datetime

app = Flask(__name__)

MOD = 26
TOL = 1e-6
MAX_ITER = 1000000000000  # Límite de iteraciones para evitar bucles infinitos

# ------------------------- FUNCIONES AUXILIARES -------------------------

def modulo_matriz(matriz, mod):
    return np.mod(matriz.round().astype(int), mod)

def es_convergente(T):
    valores_propios = np.linalg.eigvals(T)
    return max(abs(valores_propios)) < 1

def es_inversa_valida(K, K_inv, mod=26):
    producto = np.dot(K, K_inv) % mod
    identidad = np.eye(3, dtype=int)
    return np.array_equal(producto, identidad)

# ------------------------- MÉTODOS ITERATIVOS -------------------------

def jacobi(A, b, x0=None, tol=TOL, max_iter=MAX_ITER):
    n = len(b)
    x = np.zeros_like(b, dtype=float) if x0 is None else x0.astype(float)
    D = np.diag(np.diag(A))
    LU = A - D
    T = -np.dot(np.linalg.inv(D), LU)
    C = np.dot(np.linalg.inv(D), b)
    
    if not es_convergente(T):
        return None, max_iter, "No converge (radio espectral ≥ 1)"
    
    it = 0
    error_history = []
    while it < max_iter:
        x_nuevo = np.dot(T, x) + C
        error = np.max(np.abs(x_nuevo - x))
        error_history.append(error)
        
        if error < tol:
            break
        x = x_nuevo
        it += 1
    
    if it >= max_iter:
        return None, it, f"No converge después de {max_iter} iteraciones (error final: {error:.2e})"
    
    return x, it, f"Convergió en {it} iteraciones (error final: {error:.2e})"

def gauss_seidel(A, b, x0=None, tol=TOL, max_iter=MAX_ITER):
    n = len(b)
    x = np.zeros_like(b, dtype=float) if x0 is None else x0.astype(float)
    L = np.tril(A)
    U = A - L
    T = -np.dot(np.linalg.inv(L), U)
    C = np.dot(np.linalg.inv(L), b)
    
    if not es_convergente(T):
        return None, max_iter, "No converge (radio espectral ≥ 1)"
    
    it = 0
    error_history = []
    while it < max_iter:
        x_nuevo = np.dot(T, x) + C
        error = np.max(np.abs(x_nuevo - x))
        error_history.append(error)
        
        if error < tol:
            break
        x = x_nuevo
        it += 1
    
    if it >= max_iter:
        return None, it, f"No converge después de {max_iter} iteraciones (error final: {error:.2e})"
    
    return x, it, f"Convergió en {it} iteraciones (error final: {error:.2e})"

# ------------------------- INVERSIÓN ITERATIVA -------------------------

def invertir_matriz_iterativa(A, metodo):
    n = A.shape[0]
    inversa = np.zeros_like(A, dtype=float)
    total_it = 0
    mensajes = []
    
    for i in range(n):
        b = np.eye(n)[:, i]
        if metodo == 'jacobi':
            x, it, msg = jacobi(A, b)
        elif metodo == 'gauss':
            x, it, msg = gauss_seidel(A, b)
        else:
            return None, 0, ["Método no reconocido"]
        
        mensajes.append(f"Columna {i+1}: {msg}")
        total_it += it
        
        if x is None:
            return None, total_it, mensajes
        
        inversa[:, i] = x
    
    return inversa, total_it, mensajes

# ------------------------- MATRIZ PREDEFINIDA -------------------------

def seleccionar_matriz_valida():
    matrices = [
        np.array([[19., 19., 6.], [16., 16., 5.], [7., 8., 14.]]),
        np.array([[19., 12., 3.], [6., 4., 1.], [4., 15., 4.]]),
        np.array([[10., 9., 17.], [4., 8., 13.], [9., 10., 18.]]),
        np.array([[15., 12., 5.], [19., 13., 7.], [15., 2., 8.]]),
        np.array([[2., 1., 13.], [8., 8., 19.], [11., 12., 18.]]),
    ]
    while True:
        K = random.choice(matrices)
        det = int(round(np.linalg.det(K))) % MOD
        if det == 0 or gcd(det, MOD) != 1:
            continue
        return K

# ------------------------- CIFRADO / DESCIFRADO -------------------------

def vector_a_texto(vec):
    return ''.join(chr(int(round(num % 26)) + ord('A')) for num in vec)

def cifrar_hill(texto, K):
    texto = texto.upper().replace(" ", "X")
    vec = [ord(char) - ord('A') for char in texto if char.isalpha()]
    longitud = len(vec)
    relleno = (3 - (longitud % 3)) % 3
    vec += [0] * relleno
    vec = np.array(vec).reshape(-1, 3).T
    cifrado = np.dot(K, vec) % MOD
    return vector_a_texto(cifrado.T.flatten()), longitud

def descifrar_hill(texto, K_inv, longitud):
    vec = [ord(c.upper()) - ord('A') for c in texto if c.isalpha()]
    vec = np.array(vec).reshape(-1, 3).T
    plano = np.dot(K_inv, vec) % MOD
    return vector_a_texto(plano.T.flatten())[:longitud].replace("X", " ")

# ------------------------- RUTAS WEB -------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_clave', methods=['GET'])
def generar_clave():
    K = seleccionar_matriz_valida()
    return jsonify({
        'matriz': K.tolist(),
        'mensaje': 'Nueva matriz clave generada con éxito.',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/cifrar', methods=['POST'])
def cifrar():
    data = request.json
    texto = data['texto']
    K = np.array(data['matriz'])
    
    try:
        cifrado, longitud = cifrar_hill(texto, K)
        return jsonify({
            'status': 'success',
            'cifrado': cifrado,
            'longitud': longitud,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/descifrar', methods=['POST'])
def descifrar():
    data = request.json
    texto_cifrado = data['texto_cifrado']
    longitud = data['longitud']
    K_manual = np.array(data['matriz'])
    
    resultado = {
        'status': 'success',
        'iteraciones_jacobi': 0,
        'iteraciones_gauss': 0,
        'mensajes_jacobi': [],
        'mensajes_gauss': [],
        'inversa_jacobi': None,
        'inversa_gauss': None,
        'descifrado': None,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        # Intentar con Jacobi
        inv_jacobi, it_jacobi, msgs_jacobi = invertir_matriz_iterativa(K_manual, 'jacobi')
        resultado['iteraciones_jacobi'] = it_jacobi
        resultado['mensajes_jacobi'] = msgs_jacobi
        
        if inv_jacobi is not None and es_inversa_valida(K_manual, modulo_matriz(inv_jacobi, MOD)):
            K_inv_jacobi = modulo_matriz(inv_jacobi, MOD)
            resultado['inversa_jacobi'] = K_inv_jacobi.tolist()
            resultado['descifrado'] = descifrar_hill(texto_cifrado, K_inv_jacobi, longitud)
            return jsonify(resultado)
        
        # Si Jacobi falla, intentar con Gauss-Seidel
        inv_gauss, it_gauss, msgs_gauss = invertir_matriz_iterativa(K_manual, 'gauss')
        resultado['iteraciones_gauss'] = it_gauss
        resultado['mensajes_gauss'] = msgs_gauss
        
        if inv_gauss is not None and es_inversa_valida(K_manual, modulo_matriz(inv_gauss, MOD)):
            K_inv_gauss = modulo_matriz(inv_gauss, MOD)
            resultado['inversa_gauss'] = K_inv_gauss.tolist()
            resultado['descifrado'] = descifrar_hill(texto_cifrado, K_inv_gauss, longitud)
            return jsonify(resultado)
        
        # Si ambos métodos fallan
        resultado['status'] = 'error'
        resultado['message'] = "Ningún método logró obtener una inversa válida."
        return jsonify(resultado), 400
        
    except Exception as e:
        resultado['status'] = 'error'
        resultado['message'] = str(e)
        return jsonify(resultado), 400

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
