from flask import Flask, request, render_template_string, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta_daniel'

# --- 20 PREGUNTAS ---
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

# --- 20 PERSONAJES ---
personajes = [
    {"pista": "Fui arrojado a un foso con leones por orar a mi Dios.", "op": ["Daniel", "Noé", "David", "José"], "r": "Daniel"},
    {"pista": "Construí un arca gigante por mandato divino antes del diluvio.", "op": ["Moisés", "Noé", "Abraham", "Elías"], "r": "Noé"},
    {"pista": "Fui vendido por mis hermanos y terminé siendo gobernador en Egipto.", "op": ["José", "Benjamín", "Judá", "Rubén"], "r": "José"},
    {"pista": "Lideré al pueblo de Israel fuera de la esclavitud en Egipto.", "op": ["Josué", "Moisés", "Aarón", "Caleb"], "r": "Moisés"},
    {"pista": "Derroté a un gigante filisteo usando solo una honda y una piedra.", "op": ["Sansón", "David", "Saúl", "Gedeón"], "r": "David"},
    {"pista": "Fui el hombre más fuerte del mundo, pero mi fuerza estaba en mi cabello.", "op": ["Sansón", "Goliat", "Joab", "Nabucodonosor"], "r": "Sansón"},
    {"pista": "Fui el primer hombre creado por Dios y viví en el Jardín del Edén.", "op": ["Caín", "Abel", "Adán", "Set"], "r": "Adán"},
    {"pista": "Fui llamado el padre de la fe por obedecer a Dios al dejar mi tierra.", "op": ["Isaac", "Jacob", "Abraham", "Lot"], "r": "Abraham"},
    {"pista": "Fui tragado por un gran pez por intentar huir de la misión de Dios.", "op": ["Jonás", "Pedro", "Pablo", "Esteban"], "r": "Jonás"},
    {"pista": "Fui una reina que salvó a mi pueblo judío de la destrucción en Persia.", "op": ["Rut", "Ester", "Sara", "Raquel"], "r": "Ester"},
    {"pista": "Tuve muchos problemas y enfermedades, pero nunca maldije a Dios.", "op": ["Salomón", "Job", "Isaías", "Jeremías"], "r": "Job"},
    {"pista": "Fui el sucesor de Moisés y guié al pueblo a conquistar Jericó.", "op": ["Caleb", "Josué", "Aarón", "Samuel"], "r": "Josué"},
    {"pista": "Conocido por mi gran sabiduría y por construir el primer Templo.", "op": ["David", "Salomón", "Roboam", "Ezequías"], "r": "Salomón"},
    {"pista": "Fui la mujer que decidió quedarse con su suegra Noemí en Belén.", "op": ["Ester", "Rut", "Débora", "Ana"], "r": "Rut"},
    {"pista": "Fui el último juez de Israel y ungí a los dos primeros reyes.", "op": ["Elías", "Samuel", "Eliseo", "Natán"], "r": "Samuel"},
    {"pista": "Profeticé sobre la venida del Mesías siglos antes de que naciera.", "op": ["Isaías", "Amós", "Miqueas", "Joel"], "r": "Isaías"},
    {"pista": "Fui un recaudador de impuestos que dejó todo para seguir a Jesús.", "op": ["Mateo", "Marcos", "Lucas", "Juan"], "r": "Mateo"},
    {"pista": "Fui el discípulo que caminó sobre las aguas hacia Jesús.", "op": ["Juan", "Pedro", "Andrés", "Felipe"], "r": "Pedro"},
    {"pista": "Fui el apóstol de los gentiles y escribí gran parte del Nuevo Testamento.", "op": ["Bernabé", "Pablo", "Marcos", "Tomás"], "r": "Pablo"},
    {"pista": "Preparé el camino para Jesús bautizando en el río Jordán.", "op": ["Juan el Bautista", "Elías", "Enoc", "Jeremías"], "r": "Juan el Bautista"}
]

CSS_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { background: #1a1a2e; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
    .card { background: #16213e; padding: 25px; border-radius: 20px; width: 90%; max-width: 450px; margin: auto; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
    .info-box { background: #0f3460; padding: 15px; border-radius: 10px; margin-top: 15px; font-size: 16px; border: 1px solid #4ecca3; }
    button { width: 100%; padding: 15px; margin: 8px 0; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; color: black; font-weight: bold; background: #4ecca3; }
</style>
"""

# --- INICIO ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nombre'] = request.form['nombre']
        return redirect(url_for('menu'))
    return render_template_string(CSS_STYLE + """
        <div class="card"><h1>🎮 Bienvenido</h1><form method="POST">
        <input type="text" name="nombre" placeholder="Tu nombre" style="padding:15px; width:80%; border-radius:10px; font-size:18px" required>
        <button type="submit">Entrar</button></form></div>
    """)

@app.route('/menu')
def menu():
    return render_template_string(CSS_STYLE + f"""
        <div class="card"><h1>Hola, {session.get('nombre')}</h1><p>Elige tu reto:</p>
        <a href="/trivia_init"><button>Trivia Bíblica</button></a>
        <a href="/personaje_init"><button>Adivina el Personaje</button></a>
        <br><a href="/"><button style="background:#888">Cambiar nombre</button></a></div>
    """)

# --- TRIVIA LOGIC ---
@app.route('/trivia_init')
def trivia_init():
    session['idx'] = 0; session['puntos'] = 0; session['tipo'] = 'trivia'
    return redirect(url_for('juego'))

# --- PERSONAJE LOGIC ---
@app.route('/personaje_init')
def personaje_init():
    session['idx'] = 0; session['puntos'] = 0; session['tipo'] = 'personaje'
    random.shuffle(personajes) # Orden aleatorio de personajes
    return redirect(url_for('juego'))

# --- JUEGO UNIFICADO ---
@app.route('/juego')
def juego():
    idx = session.get('idx', 0)
    tipo = session.get('tipo')
    items = preguntas if tipo == 'trivia' else personajes
    
    if idx >= len(items):
        cal = round((session.get('puntos') / len(items)) * 10, 1)
        return render_template_string(CSS_STYLE + f"""
            <div class="card"><h1>🎉 ¡Completado!</h1><h2>{session.get('nombre')}</h2>
            <p>Aciertos: {session.get('puntos')} de {len(items)}</p>
            <h1>Calificación: {cal}</h1><a href="/menu"><button>Volver al Menú</button></a></div>
        """)
    
    item = items[idx]
    opciones = item['op'][:]
    random.shuffle(opciones)
    btns = "".join([f'<a href="/resp?op={o}"><button>{o}</button></a>' for o in opciones])
    
    pregunta_o_pista = item['q'] if tipo == 'trivia' else f"Pista: {item['pista']}"
    info = f'<div class="info-box">{item["info"]}</div>' if tipo == 'trivia' else ""
    
    return render_template_string(CSS_STYLE + f"""
        <div class="card"><p>{tipo.capitalize()} - Pregunta {idx + 1}</p><h2>{pregunta_o_pista}</h2>{btns}{info}</div>
    """)

@app.route('/resp')
def resp():
    op = request.args.get('op')
    idx = session.get('idx')
    tipo = session.get('tipo')
    items = preguntas if tipo == 'trivia' else personajes
    if op == items[idx]['r']: session['puntos'] += 1
    session['idx'] += 1
    return redirect(url_for('juego'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
