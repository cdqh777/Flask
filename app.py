from flask import Flask, render_template, redirect, url_for, request, session, abort, flash
import mysql.connector
from mysql.connector import Error
from datetime import date
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ventas'
app.secret_key = "miClaveSegura"

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return connection
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view

def roles_required(*roles_permitidos):
    def deco(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            rol_qhc = session.get('rol')
            if rol_qhc not in roles_permitidos:
                abort(403)
            return view(*args, **kwargs)
        return wrapped_view
    return deco

def solo_invitado_operator(view):
    """Decorador para permitir SOLO al usuario 'invitado' con rol 'operator'"""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        username = str(session.get('username', '')).strip().lower()
        rol = str(session.get('rol', '')).strip().lower()
        
        if username == 'invitado' and rol == 'operator':
            return view(*args, **kwargs)
        else:
            abort(403)
    return wrapped_view

def bloquear_invitado_operator(view):
    """Decorador para BLOQUEAR al usuario 'invitado' con rol 'operator'"""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        username = str(session.get('username', '')).strip().lower()
        rol = str(session.get('rol', '')).strip().lower()
        
        if username == 'invitado' and rol == 'operator':
            print(f"🚫 ACCESO BLOQUEADO: Usuario 'invitado' con rol 'operator'")
            abort(403)
        
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        nom_usuario_qhc = request.form["usuario"]
        password_qhc = request.form["password"]
        
        if not nom_usuario_qhc or not password_qhc:
            flash('Por favor ingrese usuario y contraseña')
            return redirect(url_for("login"))
        
        connection = get_db_connection()
        if connection is None:
            flash('Error de conexión a la base de datos')
            return redirect(url_for("login"))
            
        try:
            cursor_qhc = connection.cursor(dictionary=True)
            sql_qhc = "SELECT id, username, password_hash, nombre, activo, rol FROM usuarios WHERE username = %s"
            cursor_qhc.execute(sql_qhc, (nom_usuario_qhc,))
            usuario_qhc = cursor_qhc.fetchone()
            cursor_qhc.close()
            connection.close()
            
            if not usuario_qhc:
                flash('Usuario no encontrado')
                return redirect(url_for("login"))
            
            if not usuario_qhc["activo"]:
                flash('Usuario inactivo')
                return redirect(url_for("login"))
            
            if not check_password_hash(usuario_qhc["password_hash"], password_qhc):
                flash('Contraseña incorrecta')
                return redirect(url_for("login"))
            
            session["user_id"] = usuario_qhc["id"]
            session["username"] = usuario_qhc["username"]
            session["rol"] = usuario_qhc["rol"]
            session["nombre"] = usuario_qhc["nombre"]
            
            return redirect(url_for("lista_tiendas_qhc"))
            
        except Error as e:
            flash('Error en la base de datos')
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash('Ha cerrado sesión correctamente')
    return redirect(url_for("login"))

@app.route("/usuarios")
@roles_required('admin')
def lista_usuarios_qhc():
    connection = get_db_connection()
    cursor_qhc = connection.cursor(dictionary=True)
    sql_qhc = "SELECT id, username, nombre, activo, rol FROM usuarios"
    cursor_qhc.execute(sql_qhc)
    usuarios_qhc = cursor_qhc.fetchall()
    cursor_qhc.close()
    connection.close()
    return render_template("usuarios.html", datosUsuarios_qhc=usuarios_qhc)

@app.route("/usuarios/nuevo", methods=['GET', 'POST'])
@roles_required('admin')
def nuevo_usuario_qhc():
    if request.method == "POST":
        username_qhc = request.form['username_qhc']
        nombre_qhc = request.form['nombre_qhc']
        password_qhc = request.form['password_qhc']
        rol_qhc = request.form['rol_qhc']
        
        password_hash_qhc = generate_password_hash(password_qhc)
        
        connection = get_db_connection()
        cursor_qhc = connection.cursor()
        sql_qhc = "INSERT INTO usuarios (username, nombre, password_hash, rol, activo) VALUES (%s, %s, %s, %s, 1)"
        cursor_qhc.execute(sql_qhc, (username_qhc, nombre_qhc, password_hash_qhc, rol_qhc))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_usuarios_qhc'))
    else:
        return render_template("formulario_usuario.html")

@app.route("/usuarios/eliminar/<int:id_usuario_qhc>")
@roles_required('admin')
def elimina_usuario_qhc(id_usuario_qhc):
    try:
        connection = get_db_connection()
        cursor_qhc = connection.cursor()
        sql_qhc = "DELETE FROM usuarios WHERE id = %s"
        cursor_qhc.execute(sql_qhc, (id_usuario_qhc,))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_usuarios_qhc'))
    except:
        return "No se puede eliminar el usuario!!!"

@app.route("/tiendas")
@login_required
def lista_tiendas_qhc():
    connection = get_db_connection()
    cursor_qhc = connection.cursor(dictionary=True)
    sql_qhc = "SELECT * FROM tiendas"
    cursor_qhc.execute(sql_qhc)
    tiendas_qhc = cursor_qhc.fetchall()
    cursor_qhc.close()
    connection.close()
    return render_template("tiendas.html", datosTiendas_qhc=tiendas_qhc)

@app.route("/tiendas/nuevo", methods=['GET', 'POST'])
@roles_required('admin')
def nueva_tienda_qhc():
    if request.method == "POST":
        nombre_tda_qhc = request.form['nombre_tda_qhc']
        direccion_tda_qhc = request.form['direccion_tda_qhc']

        connection = get_db_connection()
        cursor_qhc = connection.cursor()
        sql_qhc = "INSERT INTO tiendas (nombre, direccion) VALUES (%s, %s)"
        cursor_qhc.execute(sql_qhc, (nombre_tda_qhc, direccion_tda_qhc))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_tiendas_qhc'))
    else:
        return render_template("formulario_tienda.html")

@app.route("/tiendas/eliminar/<int:id_tienda_qhc>")
@roles_required('admin')
def elimina_tienda_qhc(id_tienda_qhc):
    try:
        connection = get_db_connection()
        cursor_qhc = connection.cursor()
        sql_qhc = "DELETE FROM tiendas WHERE id_tienda = %s"
        cursor_qhc.execute(sql_qhc, (id_tienda_qhc,))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_tiendas_qhc'))
    except:
        return "No se puede eliminar la tienda!!!"

@app.route("/tiendas/modificar/<int:id_tienda_qhc>", methods=['GET', 'POST'])
@roles_required('admin')
def modificar_tienda_qhc(id_tienda_qhc):
    if request.method == 'POST':
        nombre_tda_qhc = request.form['nombre_tda_qhc']
        direccion_tda_qhc = request.form['direccion_tda_qhc']
        
        connection = get_db_connection()
        sql_qhc = "UPDATE tiendas SET nombre = %s, direccion = %s WHERE id_tienda = %s"
        cursor_qhc = connection.cursor()
        cursor_qhc.execute(sql_qhc, (nombre_tda_qhc, direccion_tda_qhc, id_tienda_qhc))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_tiendas_qhc'))
    else:
        connection = get_db_connection()
        sql_qhc = "SELECT * FROM tiendas WHERE id_tienda = %s"
        cursor_qhc = connection.cursor(dictionary=True)
        cursor_qhc.execute(sql_qhc, (id_tienda_qhc,))
        tienda_qhc = cursor_qhc.fetchone()
        cursor_qhc.close()
        connection.close()
        
        if tienda_qhc:
            return render_template("formulario_modificar_tienda.html", tienda_qhc=tienda_qhc)
        else:
            return render_template("formulario_modificar_tienda.html", tienda_qhc=None)

@app.route("/compras")
@login_required
def lista_compras_qhc():
    connection = get_db_connection()
    cursor_qhc = connection.cursor(dictionary=True)
    sql_qhc = """SELECT c.id_compra, cl.nombre as cliente_nombre, t.nombre as tienda_nombre, 
             c.monto, c.fecha 
             FROM compras c 
             JOIN clientes cl ON c.id_cliente = cl.id_cliente 
             JOIN tiendas t ON c.id_tienda = t.id_tienda"""
    cursor_qhc.execute(sql_qhc)
    compras_qhc = cursor_qhc.fetchall()
    cursor_qhc.close()
    connection.close()
    return render_template("compras.html", datosCompras_qhc=compras_qhc)

@app.route("/compras/nuevo", methods=['GET', 'POST'])
@roles_required('admin', 'operator')
def nueva_compra_qhc():
    if request.method == 'POST':
        id_cliente_cpr_qhc = request.form['id_cliente_cpr_qhc']
        id_tienda_cpr_qhc = request.form['id_tienda_cpr_qhc']
        monto_cpr_qhc = request.form['monto_cpr_qhc']
        fecha_compra_qhc = date.today()

        connection = get_db_connection()
        sql_qhc = "INSERT INTO compras (id_cliente, id_tienda, monto, fecha) VALUES (%s, %s, %s, %s)"
        cursor_qhc = connection.cursor()
        cursor_qhc.execute(sql_qhc, (id_cliente_cpr_qhc, id_tienda_cpr_qhc, monto_cpr_qhc, fecha_compra_qhc))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_compras_qhc'))
    else:
        clientes_qhc = listado_clientes_qhc()
        tiendas_qhc = listado_tiendas_qhc()
        return render_template("formulario_compra.html", clientes_qhc=clientes_qhc, tiendas_qhc=tiendas_qhc)

@app.route("/compras/eliminar/<int:id_compra_qhc>")
@roles_required('admin')
def elimina_compra_qhc(id_compra_qhc):
    try:
        connection = get_db_connection()
        cursor_qhc = connection.cursor()
        sql_qhc = "DELETE FROM compras WHERE id_compra = %s"
        cursor_qhc.execute(sql_qhc, (id_compra_qhc,))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_compras_qhc'))
    except:
        return "No se puede eliminar la compra!!!"

def listado_clientes_qhc():
    connection = get_db_connection()
    cursor_qhc = connection.cursor(dictionary=True)
    sql_qhc = "SELECT * FROM clientes"
    cursor_qhc.execute(sql_qhc)
    clientes_qhc = cursor_qhc.fetchall()
    cursor_qhc.close()
    connection.close()
    return clientes_qhc

def listado_tiendas_qhc():
    connection = get_db_connection()
    cursor_qhc = connection.cursor(dictionary=True)
    sql_qhc = "SELECT * FROM tiendas"
    cursor_qhc.execute(sql_qhc)
    tiendas_qhc = cursor_qhc.fetchall()
    cursor_qhc.close()
    connection.close()
    return tiendas_qhc

@app.route("/clientes")
@login_required
def lista_clientes_qhc():
    connection = get_db_connection()
    cursor_qhc = connection.cursor(dictionary=True)
    sql_qhc = "SELECT * FROM clientes"
    cursor_qhc.execute(sql_qhc)
    clientes_qhc = cursor_qhc.fetchall()
    cursor_qhc.close()
    connection.close()
    return render_template("clientes.html", datosClientes_qhc=clientes_qhc)

@app.route("/clientes/nuevo", methods=['GET', 'POST'])
@roles_required('admin', 'operator')
def nuevo_cliente_qhc():
    if request.method == "POST":
        nombre_cli_qhc = request.form['nombre']
        email_cli_qhc = request.form['email']
        
        connection = get_db_connection()
        cursor_qhc = connection.cursor()
        sql_qhc = "INSERT INTO clientes (nombre, email) VALUES (%s, %s)"
        cursor_qhc.execute(sql_qhc, (nombre_cli_qhc, email_cli_qhc))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_clientes_qhc'))
    else:
        return render_template("formulario_cliente.html")

@app.route("/clientes/eliminar/<int:id_cliente_qhc>")
@roles_required('admin')
def elimina_cliente_qhc(id_cliente_qhc):
    try:
        connection = get_db_connection()
        cursor_qhc = connection.cursor()
        sql_qhc = "DELETE FROM clientes WHERE id_cliente = %s"
        cursor_qhc.execute(sql_qhc, (id_cliente_qhc,))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_clientes_qhc'))
    except:
        return "No se puede eliminar el cliente!!!"

@app.route("/clientes/modificar/<int:id_cliente_qhc>", methods=['GET', 'POST'])
@roles_required('admin')
def modificar_cliente_qhc(id_cliente_qhc):
    if request.method == 'POST':
        nombre_cli_qhc = request.form['nombre']
        correo_cli_qhc = request.form['correo']
        
        connection = get_db_connection()
        sql_qhc = "UPDATE clientes SET nombre = %s, email = %s WHERE id_cliente = %s"
        cursor_qhc = connection.cursor()
        cursor_qhc.execute(sql_qhc, (nombre_cli_qhc, correo_cli_qhc, id_cliente_qhc))
        connection.commit()
        cursor_qhc.close()
        connection.close()
        return redirect(url_for('lista_clientes_qhc'))
    else:
        connection = get_db_connection()
        sql_qhc = "SELECT * FROM clientes WHERE id_cliente = %s"
        cursor_qhc = connection.cursor(dictionary=True)
        cursor_qhc.execute(sql_qhc, (id_cliente_qhc,))
        cliente_qhc = cursor_qhc.fetchone()
        cursor_qhc.close()
        connection.close()
        
        if cliente_qhc:
            return render_template("formulario_modificar_cliente.html", cliente_qhc=cliente_qhc)
        else:
            return "Cliente no encontrado"

@app.route("/reportes")
@login_required
def reportes_principal():
    return render_template("reportes_principal.html")

@app.route("/reportes/ventas-tiendas")
@roles_required('admin')
def reporte_ventas_tiendas():
    connection = get_db_connection()
    if connection is None:
        flash('Error de conexión a la base de datos')
        return redirect(url_for('inicio_qhc'))
    
    try:
        cursor_qhc = connection.cursor(dictionary=True)
        sql_qhc = """
        SELECT t.id_tienda, t.nombre AS sucursal, 
               COALESCE(SUM(c.monto), 0) AS total_ventas, 
               COALESCE(COUNT(c.id_compra), 0) AS total_compras
        FROM tiendas t
        LEFT JOIN compras c ON t.id_tienda = c.id_tienda
        GROUP BY t.id_tienda, t.nombre
        ORDER BY total_ventas DESC
        """
        cursor_qhc.execute(sql_qhc)
        ventas_tiendas = cursor_qhc.fetchall()
        cursor_qhc.close()
        connection.close()
        
        return render_template("reporte1.html", ventas_tiendas=ventas_tiendas)
        
    except Error as e:
        flash('Error al generar el reporte')
        return redirect(url_for('inicio_qhc'))
    
@app.route("/reportes/clientes-top")
@login_required
@bloquear_invitado_operator
@roles_required('admin', 'operator')
def reporte_clientes_top():
    connection = get_db_connection()
    if connection is None:
        flash('Error de conexión a la base de datos')
        return redirect(url_for('inicio_qhc'))
    
    try:
        cursor_qhc = connection.cursor(dictionary=True)
        sql_qhc = """
        SELECT cl.id_cliente, cl.nombre, SUM(c.monto) AS total_gastado 
        FROM clientes cl 
        JOIN compras c ON cl.id_cliente = c.id_cliente 
        GROUP BY cl.id_cliente, cl.nombre 
        ORDER BY total_gastado DESC 
        LIMIT 10
        """
        cursor_qhc.execute(sql_qhc)
        clientes_top = cursor_qhc.fetchall()
        cursor_qhc.close()
        connection.close()
        
        return render_template("reporte2.html", clientes_top=clientes_top)
        
    except Error as e:
        flash('Error al generar el reporte')
        return redirect(url_for('inicio_qhc'))

@app.route("/reportes/compras-fechas")
@login_required
@solo_invitado_operator
def reporte_compras_fechas():
    connection = get_db_connection()
    if connection is None:
        flash('Error de conexión a la base de datos')
        return redirect(url_for('inicio_qhc'))
    
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        cursor_qhc = connection.cursor(dictionary=True)
        if fecha_inicio and fecha_fin:
            sql_qhc = """
            SELECT fecha, COUNT(*) as total_compras, SUM(monto) as total_monto
            FROM compras 
            WHERE fecha BETWEEN %s AND %s
            GROUP BY fecha 
            ORDER BY fecha DESC
            """
            cursor_qhc.execute(sql_qhc, (fecha_inicio, fecha_fin))
        else:
            sql_qhc = """
            SELECT fecha, COUNT(*) as total_compras, SUM(monto) as total_monto
            FROM compras 
            GROUP BY fecha 
            ORDER BY fecha DESC
            """
            cursor_qhc.execute(sql_qhc)
        
        compras_por_fecha = cursor_qhc.fetchall()
        cursor_qhc.close()
        connection.close()
        
        return render_template("reporte_compras_fechas.html", 
                             compras_por_fecha=compras_por_fecha,
                             fecha_inicio=fecha_inicio,
                             fecha_fin=fecha_fin)
        
    except Error as e:
        flash('Error al generar el reporte de compras por fechas')
        return redirect(url_for('inicio_qhc'))

@app.route("/")
def inicio_qhc():
    return render_template("inicio.html")

if __name__ == "__main__":
    app.run(debug=True)