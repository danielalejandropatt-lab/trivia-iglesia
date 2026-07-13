from flask import Flask, request, render_template_string, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta_daniel'

# --- DATOS ---
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
    {"q": "¿En qué valle fue traicionado Sansón por Dalila?", "op": ["Valle de Sorec", "Valle de Elah", "Valle de Ajalón", "Valle de Refaim"], "r": "Valle de Sorec", "info": "Dalila vivía en este valle."},
    {"q": "¿Cómo se llamaba el padre de Juan el Bautista?", "op": ["Zacarías", "Simeón", "José", "Elías"], "r": "Zacarías", "info": "Era sacerdote del grupo de Abías."},
    {"q": "¿Qué nombre recibió el lugar donde Jacob soñó con la escalera al cielo?", "op": ["Betel", "Hebrón", "Siquem", "Beerseba"], "r": "Betel", "info": "Significa 'Casa de Dios'."},
    {"q": "¿Quién fue el rey que pidió sabiduría a Dios para gobernar?", "op": ["Saúl", "David", "Salomón", "Roboam"], "r": "Salomón", "info": "Dios le dio sabiduría y riquezas por no pedir fama."},
    {"q": "¿Cómo se llamaba la esposa de Isaac?", "op": ["Rebeca", "Raquel", "Lea", "Bilha"], "r": "Rebeca", "info": "Fue elegida mediante una señal junto al pozo."},
    {"q": "¿Qué profeta fue enviado a Nínive pero huyó a Tarsis?", "op": ["Amós", "Jonás", "Oseas", "Miqueas"], "r": "Jonás", "info": "Su historia nos enseña sobre la obediencia."},
    {"q": "¿Cuál es el nombre del lugar donde Jesús multiplicó los panes y peces por segunda vez?", "op": ["Galilea", "Decápolis", "Judea", "Samaria"], "r": "Decápolis", "info": "La región de las diez ciudades."},
    {"q": "¿Cómo se llamaba el oficial etíope que bautizó Felipe?", "op": ["Ebed-melec", "Cus", "Candace", "Eunuco sin nombre"], "r": "Eunuco sin nombre", "info": "La Biblia solo se refiere a él por su cargo y origen."},
    {"q": "¿Qué montaña fue el lugar donde murió Moisés?", "op": ["Sinaí", "Ararat", "Nebo", "Carmelo"], "r": "Nebo", "info": "Desde allí pudo ver la Tierra Prometida."},
    {"q": "¿Cómo se llamaban los dos hijos de Elí que actuaban mal en el templo?", "op": ["Ofni y Finees", "Jacob y Esaú", "Pedro y Juan", "Caín y Abel"], "r": "Ofni y Finees", "info": "Su mal comportamiento trajo juicio sobre la casa de Elí."}
]

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
    {"pista": "Fui la madre que vio morir a su hijo en el desierto y lloró, pero Dios escuchó su voz.", "op": ["Agar", "Sara", "Lea", "Raquel"], "r": "Agar"},
    {"pista": "Fui el profeta que desafió a los 450 profetas de Baal en el Monte Carmelo.", "op": ["Eliseo", "Elías", "Isaías", "Jeremías"], "r": "Elías"},
    {"pista": "Fui el único que permaneció fiel al rey David cuando su propio hijo Absalón intentó robarle el trono.", "op": ["Joab", "Itai", "Natán", "Mefiboset"], "r": "Itai"},
    {"pista": "Fui el personaje que, siendo un niño, escuchó la voz de Dios llamándole en el templo mientras dormía.", "op": ["Samuel", "David", "José", "Benjamín"], "r": "Samuel"},
    {"pista": "Fui el rey que ordenó la construcción de un muro alrededor de Jerusalén en tiempo récord.", "op": ["Salomón", "Ezequías", "Nehemías", "Josías"], "r": "Nehemías"},
    {"pista": "Fui la mujer que escondió a los espías de Israel en Jericó para salvar a mi familia.", "op": ["Rahab", "Rut", "Débora", "Ester"], "r": "Rahab"},
    {"pista": "Me quedé mudo por no creer el mensaje del ángel que me anunciaba el nacimiento de mi hijo.", "op": ["Simeón", "Zacarías", "José", "Nicodemo"], "r": "Zacarías"},
    {"pista": "Fui el juez que venció a los madianitas usando solo a 300 hombres con trompetas y cántaros.", "op": ["Sansón", "Gedeón", "Barac", "Josué"], "r": "Gedeón"},
    {"pista": "Fui el apóstol que tuvo dudas y necesitó tocar las heridas de Jesús para creer que había resucitado.", "op": ["Pedro", "Felipe", "Tomás", "Juan"], "r": "Tomás"},
    {"pista": "Fui el profeta que tuvo que casarse con una mujer infiel como símbolo del amor de Dios por su pueblo.", "op": ["Amós", "Oseas", "Joel", "Malaquías"], "r": "Oseas"}
]

CSS_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { background: #1a1a2e; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
    .card { background: #16213e; padding: 25px; border-radius: 20px; width: 90%; max-width: 450px; margin: auto; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
    .info-box { background: #0f3460; padding: 20px; border-radius: 15px; margin-top: 25px; font-size: 18px; color: #ffffff; border: 1px solid #4ecca3; }
    button { width: 100%; padding: 18px; margin: 10px 0; border: none; border-radius: 12px; font-size: 18px; cursor: pointer; color: black; font-weight: bold; background: #4ecca3; }
</style>
"""

# --- INICIO ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nombre'] = request.form['nombre']
        return redirect(url_for('menu'))
    return render_template_string(CSS_STYLE + """
        <div class="card"><h1 style="font-size: 50px;">✝️</h1><h1 style="color: white; margin-bottom: 5px;">Bienvenido</h1>
        <p style="color: white; font-size: 1.2em; width: 85%; margin: 10px auto; border-bottom: 1px solid #4ecca3; padding-bottom: 10px;">"Cristo te Ama"</p>
        <form method="POST"><input type="text" name="nombre" placeholder="Tu nombre" style="padding:15px; width:80%; border-radius:10px; font-size:18px; margin-bottom: 15px;" required><button type="submit">Entrar</button></form></div>
    """)

@app.route('/menu')
def menu():
    return render_template_string(CSS_STYLE + f"""
        <div class="card"><h1>Hola, {session.get('nombre', 'Amigo')}</h1><p>Elige tu reto:</p>
        <a href="/trivia_init"><button>Trivia Bíblica</button></a>
        <a href="/personaje_init"><button>Adivina el Personaje</button></a></div>
    """)

# --- TRIVIA ---
@app.route('/trivia_init')
def trivia_init():
    session['idx'] = 0; session['puntos'] = 0
    return redirect(url_for('juego'))

@app.route('/juego')
def juego():
    idx = session.get('idx', 0)
    if idx >= len(preguntas):
        cal = round((session.get('puntos') / len(preguntas)) * 10, 1)
        return render_template_string(CSS_STYLE + f"""<div class="card"><h1>🎉 ¡Terminaste, {session.get('nombre')}!</h1><p>Aciertos: {session.get('puntos')} de {len(preguntas)}</p><h1>Calificación: {cal}</h1><a href="/trivia_init"><button>Volver a jugar</button></a><a href="/menu"><button style="background:#888">Menú</button></a></div>""")
    p = preguntas[idx]
    ops = p['op'][:]; random.shuffle(ops)
    btns = "".join([f'<a href="/res?op={o}"><button>{o}</button></a>' for o in ops])
    return render_template_string(CSS_STYLE + f"""<div class="card"><p>Pregunta {idx + 1} de {len(preguntas)}</p><h2>{p['q']}</h2>{btns}<div class="info-box">{p['info']}</div></div>""")

@app.route('/res')
def res():
    if request.args.get('op') == preguntas[session.get('idx')]['r']: session['puntos'] += 1
    session['idx'] += 1
    return redirect(url_for('juego'))

# --- PERSONAJES ---
@app.route('/personaje_init')
def personaje_init():
    session['idx_p'] = 0; session['puntos_p'] = 0
    return redirect(url_for('juego_personaje'))

@app.route('/personaje')
def juego_personaje():
    idx = session.get('idx_p', 0)
    if idx >= len(personajes):
        return render_template_string(CSS_STYLE + f"""<div class="card"><h1>🎉 ¡Terminaste, {session.get('nombre')}!</h1><p>Aciertos: {session.get('puntos_p')} de {len(personajes)}</p><a href="/personaje_init"><button>Volver a jugar</button></a><a href="/menu"><button style="background:#888">Menú</button></a></div>""")
    p = personajes[idx]; session['r_p'] = p['r']; ops = p['op'][:]; random.shuffle(ops)
    btns = "".join([f'<a href="/res_p?op={o}"><button>{o}</button></a>' for o in ops])
    return render_template_string(CSS_STYLE + f"""<div class="card"><p>Personaje {idx + 1} de {len(personajes)}</p><h1>👤 ¿Quién soy?</h1><p style="font-size:20px">{p['pista']}</p>{btns}</div>""")

@app.route('/res_p')
def res_p():
    if request.args.get('op') == session.get('r_p'): session['puntos_p'] += 1
    session['idx_p'] += 1
    return redirect(url_for('juego_personaje'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
