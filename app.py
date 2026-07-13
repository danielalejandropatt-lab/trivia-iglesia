from flask import Flask, request, render_template_string, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta_daniel'

# Tus preguntas se mantienen intactas
preguntas = [
    {"q": "¿Quién era el sumo sacerdote cuando Jesús fue juzgado?", "op": ["Caifás", "Anás", "Gamaliel", "Nicodemo"], "r": "Caifás", "info": "Fue el sumo sacerdote al momento de la crucifixión."},
    {"q": "¿En qué ciudad predicó Pablo sobre el 'Dios desconocido'?", "op": ["Corinto", "Éfeso", "Atenas", "Filipos"], "r": "Atenas", "info": "Pablo visitó una ciudad famosa por su filosofía."},
    {"q": "¿Cómo se llamaba el esclavo que Pablo envió de regreso a Filemón?", "op": ["Onésimo", "Tíquico", "Epafrodito", "Marcos"], "r": "Onésimo", "info": "Este hombre huyó de su amo pero se encontró con Pablo."},
    {"q": "¿Cuál es el libro que menciona a 'César' por primera vez?", "op": ["Mateo", "Marcos", "Lucas", "Juan"], "r": "Lucas", "info": "Es el mismo libro que detalla el nacimiento de Jesús."},
    {"q": "¿Quién fue el primer mártir cristiano?", "op": ["Pedro", "Esteban", "Santiago", "Felipe"], "r": "Esteban", "info": "Un hombre lleno de gracia y poder que fue apedreado."},
    {"q": "¿A qué iglesia escribió Pablo sobre la 'armadura de Dios'?", "op": ["Corinto", "Roma", "Éfeso", "Galacia"], "r": "Éfeso", "info": "Esta carta aborda la lucha espiritual."},
    {"q": "¿Quién acompañó a Pablo en su primer viaje misionero?", "op": ["Silas", "Bernabé", "Timoteo", "Lucas"], "r": "Bernabé", "info": "Conocido como el 'hijo de consolación'."},
    {"q": "¿Cómo se llamaba la mujer que Pablo resucitó en Jope?", "op": ["Lidia", "Dorcas", "Priscila", "Febe"], "r": "Dorcas", "info": "Una mujer admirada por su caridad."},
    {"q": "¿Qué apóstol escribió más libros en el Nuevo Testamento?", "op": ["Juan", "Pedro", "Pablo", "Lucas"], "r": "Pablo", "info": "Es el autor que más cartas escribió."},
    {"q": "¿En qué isla naufragó Pablo?", "op": ["Patmos", "Creta", "Malta", "Chipre"], "r": "Malta", "info": "Una isla del Mediterráneo."},
    {"q": "¿Quién escribió el libro de Hebreos?", "op": ["Pablo", "Apolos", "Desconocido", "Bernabé"], "r": "Desconocido", "info": "Su autoría es uno de los temas más debatidos."},
    {"q": "¿Qué significa el nombre 'Getsemaní'?", "op": ["Lugar de llanto", "Prensa de aceite", "Jardín santo", "Lugar de reposo"], "r": "Prensa de aceite", "info": "Hace referencia a la maquinaria de aceite."},
    {"q": "¿A qué ciudad se dirigía Saulo cuando vio la luz del cielo?", "op": ["Jericó", "Damasco", "Samaria", "Antioquía"], "r": "Damasco", "info": "Ciudad a la que Saulo iba con autoridad."},
    {"q": "¿Qué libro describe la nueva Jerusalén?", "op": ["Hebreos", "Santiago", "Apocalipsis", "Judas"], "r": "Apocalipsis", "info": "El libro profético que describe el final."},
    {"q": "¿Quién bautizó al eunuco etíope?", "op": ["Pedro", "Felipe", "Juan", "Esteban"], "r": "Felipe", "info": "Uno de los siete diáconos."},
    {"q": "¿Cuántas personas fueron alimentadas con cinco panes y dos peces?", "op": ["2,000", "5,000", "7,000", "10,000"], "r": "5,000", "info": "El gran milagro de provisión."},
    {"q": "¿Quién negó a Jesús tres veces antes de que el gallo cantara?", "op": ["Juan", "Judas", "Pedro", "Tomás"], "r": "Pedro", "info": "El discípulo que prometió lealtad absoluta."},
    {"q": "¿En qué ciudad se llamaron por primera vez 'cristianos'?", "op": ["Jerusalén", "Antioquía", "Roma", "Corinto"], "r": "Antioquía", "info": "Ciudad donde la comunidad se hizo notoria."},
    {"q": "¿Qué objeto se le cayó a Pablo de los ojos tras su conversión?", "op": ["Escamas", "Polvo", "Sangre", "Velo"], "r": "Escamas", "info": "Una señal física de que su ceguera terminó."},
    {"q": "¿Quién era el rey que mandó matar a los niños en Belén?", "op": ["César", "Herodes", "Pilato", "Agripa"], "r": "Herodes", "info": "Un gobernante celoso de su poder."}
]

CSS_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { background: #1a1a2e; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
    .card { background: #16213e; padding: 25px; border-radius: 20px; width: 90%; max-width: 450px; margin: auto; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
    .info-box { background: #0f3460; padding: 20px; border-radius: 15px; margin-top: 25px; font-size: 18px; color: #ffffff; border: 1px solid #4ecca3; line-height: 1.4; }
    button { width: 100%; padding: 18px; margin: 10px 0; border: none; border-radius: 12px; font-size: 18px; cursor: pointer; color: black; font-weight: bold; background: #4ecca3; }
</style>
"""

# --- CENTRO DE JUEGOS ---
@app.route('/')
def index():
    return render_template_string(CSS_STYLE + """
        <div class="card">
            <h1>🎮 Centro de Juegos</h1>
            <p>Elige tu reto de hoy:</p>
            <a href="/trivia"><button>Trivia Bíblica</button></a>
            <br><br>
            <button style="background:#555">Próximamente...</button>
        </div>
    """)

# --- TRIVIA BÍBLICA ---
@app.route('/trivia', methods=['GET', 'POST'])
def inicio_trivia():
    if request.method == 'POST':
        session['nombre'] = request.form['nombre']
        session['idx'] = 0
        session['puntos'] = 0
        return redirect(url_for('juego'))
    return render_template_string(CSS_STYLE + """
        <div class="card"><h1>🎮 Trivia Bíblica</h1><form method="POST"><input type="text" name="nombre" placeholder="Tu nombre" style="padding:15px; width:80%; border-radius:10px; font-size:18px" required><button type="submit">¡Empezar!</button></form>
        <br><a href="/"><button style="background:#888">Volver al Menú</button></a></div>
    """)

@app.route('/juego')
def juego():
    idx = session.get('idx', 0)
    if idx >= len(preguntas):
        calificacion = round((session.get('puntos') / len(preguntas)) * 10, 1)
        return render_template_string(CSS_STYLE + f"""
            <div class="card"><h1>🎉 ¡Reto Completado!</h1><h2>{session.get('nombre')}</h2>
            <p style="font-size:20px">Aciertos: {session.get('puntos')} de {len(preguntas)}</p>
            <h1 style="font-size:40px">Calificación: {calificacion}</h1>
            <a href="/trivia"><button>Volver a jugar</button></a>
            <a href="/"><button style="background:#888">Ir al Menú</button></a></div>
        """)
    
    p = preguntas[idx]
    opciones = p['op'][:]
    random.shuffle(opciones)
    
    return render_template_string(CSS_STYLE + f"""
        <div class="card"><p style="font-size:18px">Pregunta {idx + 1} de {len(preguntas)}</p><h2 style="font-size:24px">{p['q']}</h2>
            <a href="/respuesta?op={opciones[0]}"><button>{opciones[0]}</button></a>
            <a href="/respuesta?op={opciones[1]}"><button>{opciones[1]}</button></a>
            <a href="/respuesta?op={opciones[2]}"><button>{opciones[2]}</button></a>
            <a href="/respuesta?op={opciones[3]}"><button>{opciones[3]}</button></a>
            <div class="info-box">{p['info']}</div>
        </div>
    """)

@app.route('/respuesta')
def respuesta():
    opcion_elegida = request.args.get('op')
    idx = session.get('idx', 0)
    if idx < len(preguntas) and opcion_elegida == preguntas[idx]['r']:
        session['puntos'] += 1
    session['idx'] += 1
    return redirect(url_for('juego'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
