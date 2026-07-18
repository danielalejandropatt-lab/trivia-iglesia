from flask import Flask, request, render_template_string, redirect, url_for, session, Response
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_daniel'

# --- MEMORIA VOLÁTIL PARA LAS MÉTRICAS DE LA IGLESIA ---
HISTORIAL_CALIFICACIONES = []

# --- BANCO DE DATOS: DIFICULTAD ELEVADA (10 preguntas por bloque) ---
verdades_data = [
    {
        "nivel": 1,
        "titulo": "La Verdad del Amor",
        "versiculos": [
            "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna. (Jn. 3:16)",
            "... yo he venido para que tengan vida, y para que la tengan en abundancia. (Jn. 10:10b)"
        ],
        "preguntas": [
            {"q": "¿Cuál es el propósito original de Dios para tu vida?", "op": ["Que tengas una vida abundante.", "Que alcances la perfección moral absoluta.", "Que ganes la salvación por medio de sacrificios."], "r": "Que tengas una vida abundante."},
            {"q": "¿Qué motivó a Dios a entregar a su Hijo según Juan 3:16?", "op": ["Su inmenso amor por el mundo.", "La necesidad de apaciguar su ira legal.", "El cumplimiento estricto del pacto abrahámico."], "r": "Su inmenso amor por el mundo."},
            {"q": "¿Cuál es el regalo que Dios ofrece a quienes creen en su Hijo?", "op": ["La vida eterna.", "El perdón condicional y temporal.", "La exención de toda tribulación terrenal."], "r": "La vida eterna."},
            {"q": "Según Juan 10:10, ¿para qué vino Jesús al mundo?", "op": ["Para que tengamos vida en abundancia.", "Para instituir un nuevo orden de sacerdotes.", "Para abolir de manera inmediata la ley mosaica."], "r": "Para que tengamos vida en abundancia."},
            {"q": "¿Cómo se describe la naturaleza del amor de Dios en la primera verdad?", "op": ["Como un amor que da lo más preciado (a su Hijo) para salvarnos.", "Como un afecto pasivo que depende de la piedad humana.", "Como una recompensa destinada a los justos de la Tierra."], "r": "Como un amor que da lo más preciado (a su Hijo) para salvarnos."},
            {"q": "¿Qué significa tener 'vida abundante' en el contexto espiritual?", "op": ["Vivir en plenitud y en relación con el propósito de Dios.", "Gozar de prosperidad financiera y ausencia de padecimientos.", "Alcanzar un estado de iluminación mental superior."], "r": "Vivir en plenitud y en relación con el propósito de Dios."},
            {"q": "¿A quiénes incluye el amor de Dios mencionado en Juan 3:16?", "op": ["A todo el mundo ('de tal manera amó Dios al mundo').", "Exclusivamente a los remanentes elegidos de Israel.", "Únicamente a quienes guardan fielmente los mandamientos."], "r": "A todo el mundo ('de tal manera amó Dios al mundo')."},
            {"q": "¿Es la vida eterna algo que se gana o que se recibe por amor?", "op": ["Se recibe como resultado del plan amoroso de Dios.", "Se gana acumulando méritos espirituales y obras rectas.", "Se adquiere a través del conocimiento de misterios sagrados."], "r": "Se recibe como resultado del plan amoroso de Dios."},
            {"q": "¿Qué asegura Juan 3:16 que NO le pasará a quien cree?", "op": ["Que no se perderá.", "Que no experimentará la muerte física terrenal.", "Que no volverá a ser tentado por el pecado."], "r": "Que no se perderá."},
            {"q": "¿Cuál es la base de toda la relación entre Dios y el hombre en esta primera ley?", "op": ["El amor incondicional del Creador.", "El temor reverente al juicio inminente.", "La observancia rigurosa de ordenanzas y ritos."], "r": "El amor incondicional del Creador."}
        ]
    },
    {
        "nivel": 2,
        "titulo": "La Verdad del Pecado",
        "versiculos": [
            "Por cuanto todos pecaron, y están destituidos de la gloria de Dios, (Rom 3:23)",
            "Porque la paga del pecado es muerte... (Rom. 6:23a)"
        ],
        "preguntas": [
            {"q": "¿Qué es lo que impide al hombre experimentar el amor de Dios?", "op": ["El pecado.", "La falta de iluminación teológica.", "Las debilidades físicas y la naturaleza finita."], "r": "El pecado."},
            {"q": "¿Cuántas personas han pecado según el texto de Romanos 3:23?", "op": ["Todos, sin excepción.", "Únicamente aquellos que no conocen la Ley.", "La mayoría de la humanidad, exceptuando los santos."], "r": "Todos, sin excepción."},
            {"q": "¿Cuál es el estado del pecador respecto a la gloria de Dios?", "op": ["Está destituido de ella.", "Se encuentra bajo un velo de ignorancia remediable.", "Permanece en un estado de juicio en suspenso."], "r": "Está destituido de ella."},
            {"q": "¿Cuál es la consecuencia legal y espiritual del pecado según Romanos 6:23?", "op": ["La muerte.", "Una corrección pedagógica en el alma.", "La pérdida temporal del favor divino."], "r": "La muerte."},
            {"q": "¿Por qué el pecado causa una separación?", "op": ["Refleja una barrera entre la santidad de Dios y la condición humana.", "Porque Dios decide apartarse por falta de adoradores.", "Porque debilitar el libre albedrío del individuo de forma natural."], "r": "Refleja una barrera entre la santidad de Dios y la condición humana."},
            {"q": "¿Puede el hombre por su cuenta cruzar el abismo del pecado?", "op": ["No, el pecado nos mantiene separados por completo.", "Sí, si equilibra sus faltas mediante actos de caridad extrema.", "Sí, a través de la meditación y el arrepentimiento intelectual."], "r": "No, el pecado nos mantiene separados por completo."},
            {"q": "¿Qué tipo de 'muerte' se menciona en la segunda verdad?", "op": ["La muerte espiritual como paga por el pecado.", "La cesación absoluta de la existencia del alma.", "El deterioro físico progresivo del ser humano."], "r": "La muerte espiritual como paga por el pecado."},
            {"q": "¿Por qué se dice que el pecado nos priva del plan de Dios?", "op": ["Refleja una barrera que impide la vida abundante.", "Porque invalida los dones genéticos del hombre.", "Porque cancela de forma retroactiva el amor del Creador."], "r": "Refleja una barrera que impide la vida abundante."},
            {"q": "¿Es el pecado un problema individual o universal?", "op": ["Universal, pues todos pecaron.", "Individual, afectando únicamente a quienes cometen actos inmorales.", "Estructural, dependiente del entorno social del individuo."], "r": "Universal, pues todos pecaron."},
            {"q": "Cuál es la función de la segunda verdad en el plan de salvación?", "op": ["Servir como diagnóstico de la necesidad humana de un Salvador.", "Establecer las normas de conducta para evitar el infierno.", "Demostrar que la raza humana carece de valor intrínseco."], "r": "Servir como diagnóstico de la necesidad humana de un Salvador."}
        ]
    },
    {
        "nivel": 3,
        "titulo": "La Verdad del Substituto",
        "versiculos": [
            "Mas Dios muestra su amor para con nosotros, en que siendo aún pecadores, Cristo murió por nosotros. (Rom. 5:8)",
            "Jesús le dijo: Yo soy el camino, y la verdad, y la vida; nadie viene al Padre, sino por mí. (Jn. 14:6)"
        ],
        "preguntas": [
            {"q": "¿Quién es el sustituto que Dios proveyó para el hombre?", "op": ["Jesucristo.", "El sistema de sacrificios levíticos.", "La intercesión de los arcángeles."], "r": "Jesucristo."},
            {"q": "¿Cómo demostró Dios su amor mientras aún éramos pecadores?", "op": ["Haciendo que Cristo muriera por nosotros.", "Manifestando señales portentosas en el templo.", "Enviando bendiciones a través de emisarios celestiales."], "r": "Haciendo que Cristo muriera por nosotros."},
            {"q": "¿Qué pagó Jesús específicamente en la cruz?", "op": ["El precio completo de nuestra salvación.", "La deuda de los pecados cometidos en el pasado únicamente.", "La culpa original adquirida en el Edén."], "r": "El precio completo de nuestra salvación."},
            {"q": "¿Qué afirma Jesús sobre sí mismo en Juan 14:6?", "op": ["Que Él es el camino, la verdad y la vida.", "Que es el ejemplo moral supremo a seguir.", "Que representa una de las puertas de acceso a la presencia de Dios."], "r": "Que Él es el camino, la verdad y la vida."},
            {"q": "¿Es posible llegar al Padre a través de alguien que no sea Jesús?", "op": ["No, nadie viene al Padre sino por Él.", "Sí, si se sigue la doctrina de los profetas antiguos.", "Sí, mediante una vida de perfecta contemplación ascética."], "r": "No, nadie viene al Padre sino por Él."},
            {"q": "¿Por qué se llama a Jesús el 'Substituto'?", "op": ["Logró tomar el lugar del pecador y pagó su deuda de muerte.", "A causa de que reemplazó las antiguas figuras del sacerdocio humano.", "Debido a que actuó en representación de los reyes terrenales."], "r": "Logró tomar el lugar del pecador y pagó su deuda de muerte."},
            {"q": "¿Qué representa la muerte de Cristo en el esquema de las cinco verdades?", "op": ["La solución divina al problema del pecado.", "El final trágico de un mensajero de paz.", "Una demostración simbólica del juicio histórico."], "r": "La solución divina al problema del pecado."},
            {"q": "¿Qué garantiza que el sacrificio de Jesús fue suficiente?", "op": ["Que Él pagó el precio completo.", "El respaldo y la validación de los líderes de la época.", "Que fue ratificado posteriormente por las buenas obras de la iglesia."], "r": "Que Él pagó el precio completo."},
            {"q": "¿Cómo se relaciona la tercera verdad con el amor de Dios?", "op": ["Es la prueba máxima de su amor (Romanos 5:8).", "Evidencia que el amor requería un pago para seguir existiendo.", "Muestra que el amor divino es condicional al sacrificio."], "r": "Es la prueba máxima de su amor (Romanos 5:8)."},
            {"q": "¿Qué papel juega Jesús entre el hombre pecador y el Dios santo?", "op": ["El de único puente o mediador.", "El de un testigo imparcial del desarrollo humano.", "El de un juez ejecutor de la sentencia divina."], "r": "El de único puente o mediador."}
        ]
    },
    {
        "nivel": 4,
        "titulo": "La Verdad del Arrepentimiento",
        "versiculos": [
            "Así que, arrepentíos y convertíos, para que sean borrados vuestros pecados; para que vengan de la presencia del Señor tiempos de refrigerio, (Hechos 3:19)"
        ],
        "preguntas": [
            {"q": "¿Qué mandato se da en Hechos 3:19 para recibir el perdón?", "op": ["Arrepentirse y convertirse.", "Confesar públicamente cada falta cometida.", "Ofrecer restituciones materiales a los afectados."], "r": "Arrepentirse y convertirse."},
            {"q": "¿Cuál es el beneficio directo del arrepentimiento?", "op": ["Que los pecados sean borrados.", "La inmunidad frente a futuras tentaciones.", "Un estado inmediato de prosperidad material."], "r": "Que los pecados sean borrados."},
            {"q": "¿Qué significa 'convertirse' tras el arrepentimiento?", "op": ["Cambiar de dirección hacia Dios.", "Adoptar una nueva identidad eclesiástica o rito.", "Modificar la conducta externa por temor."], "r": "Cambiar de dirección hacia Dios."},
            {"q": "¿Qué prometen las fuentes que viene tras el arrepentimiento?", "op": ["Tiempos de refrigerio de la presencia del Señor.", "La eliminación de los conflictos en la vida diaria.", "Una recompensa de honor entre los hombres."], "r": "Tiempos de refrigerio de la presencia del Señor."},
            {"q": "¿Es el arrepentimiento solo sentir pena por el pecado?", "op": ["No, implica una decisión de volver a Dios.", "Sí, es el remordimiento emocional por las consecuencias del error.", "Sí, es el llanto sacramental requerido."], "r": "No, implica una decisión de volver a Dios."},
            {"q": "¿Por qué el arrepentimiento es vital para la salvación?", "op": ["Porque permite abandonar la vida de pecado y reconciliarse con el Creador.", "Debido a que es el requisito formal exigido por la ley eclesial.", "Porque convence al intelecto de sus propios errores morales."], "r": "Porque permite abandonar la vida de pecado y reconciliarse con el Creador."},
            {"q": "¿De quién proviene el perdón una vez que nos arrepentimos?", "op": ["Del Señor.", "Del esfuerzo interior del individuo.", "De la absolución comunitaria."], "r": "Del Señor."},
            {"q": "¿Qué le sucede a la barrera del pecado cuando hay arrepentimiento genuino?", "op": ["Los pecados son eliminados o 'borrados'.", "Se debilita gradualmente con el paso del tiempo.", "Queda archivada hasta el juicio final."], "r": "Los pecados son eliminados o 'borrados'."},
            {"q": "What significa experimentar 'refrigerio' espiritual?", "op": ["Es el alivio y paz que Dios otorga al perdonar.", "La adquisición de un nuevo conocimiento teológico profundo.", "Un arrebato emocional místico."], "r": "Es el alivio y paz que Dios otorga al perdonar."},
            {"q": "¿Se puede ser salvo sin arrepentirse?", "op": ["No, según las fuentes, el arrepentimiento es el paso esencial para que los pecados sean borrados.", "Sí, siempre y cuando la persona mantenga una postura intelectual de fe.", "Sí, porque el amor de Dios cubre todo sin requerir cambios."], "r": "No, según las fuentes, el arrepentimiento es el paso esencial para que los pecados sean borrados."}
        ]
    },
    {
        "nivel": 5,
        "titulo": "La Verdad de la Fe",
        "versiculos": [
            "Porque la paga del pecado es muerte, mas la dádiva de Dios es vida eterna en Cristo Jesús Señor nuestro. (Rom. 6:23)",
            "Más a todos los que le recibieron, a los que creen en su nombre, les dio potestad de ser hechos hijos de Dios (Jn. 1:12)",
            "De cierto, de cierto os digo: El que oye mi palabra, y cree al que me envió, tiene vida eterna; y no vendrá a condenación, mas ha pasado de muerte a vida. (Jn. 5:24)"
        ],
        "preguntas": [
            {"q": "¿Cómo describe Romanos 6:23 a la vida eterna?", "op": ["Como una dádiva (regalo) de Dios.", "Como un premio al esfuerzo del creyente.", "Como una herencia natural de la raza humana."], "r": "Como una dádiva (regalo) de Dios."},
            {"q": "¿Cuál es el nombre de la acción de aceptar a Jesús por fe?", "op": ["Recibirlo.", "Comprenderlo teológicamente.", "Imitar de manera exacta sus obras."], "r": "Recibirlo."},
            {"q": "¿Qué derecho adquieren quienes reciben a Jesús según Juan 1:12?", "op": ["La potestad de ser hechos hijos de Dios.", "La garantía de infalibilidad espiritual.", "El señorío sobre potestades terrenales."], "r": "La potestad de ser hechos hijos de Dios."},
            {"q": "¿Qué promete Jesús a quien oye su palabra y cree en Dios en Juan 5:24?", "op": ["Que tiene vida eterna y no vendrá a condenación.", "Que será librado de toda tentación carnal.", "Que sus méritos pasados quedarán validados ante el cielo."], "r": "Que tiene vida eterna y no vendrá a condenación."},
            {"q": "¿Cuál es el paso final que Jesús pide en Apocalipsis 3:20?", "op": ["Que se le abra la puerta de la vida.", "Que se realice una confesión eclesiástica formal.", "Que se cumpla un ciclo de oraciones rituales."], "r": "Que se le abra la puerta de la vida."},
            {"q": "¿Qué sucede si alguien abre la puerta de su corazón a Jesús?", "op": ["Él entrará y tendrá comunión íntima con esa persona.", "Él enviará su espíritu guardián a custodiar el hogar.", "Él reescribirá el destino temporal del individuo."], "r": "Él entrará y tendrá comunión íntima con esa persona."},
            {"q": "¿La fe es un sentimiento o una decisión personal?", "op": ["Es una decisión de creer y recibir a Cristo como Salvador.", "Es un estado emocional generado por el ambiente litúrgico.", "Es una convicción intelectual puramente teórica."], "r": "Es una decisión de creer y recibir a Cristo como Salvador."},
            {"q": "¿Qué seguridad tiene el creyente respecto a su pasado?", "op": ["Que ha pasado de muerte a vida.", "Que sus consecuencias terrenales quedarán completamente annuladas.", "Que será pesado en una balanza al final de los días."], "r": "Que ha pasado de muerte a vida."},
            {"q": "¿Por qué la salvación se considera una 'dádiva'?", "op": ["Refleja un regalo recibido por fe en Cristo Jesús.", "Debido a que representa una oferta temporal del Creador.", "Porque requiere un intercambio simétrico de devoción."], "r": "Refleja un regalo recibido por fe en Cristo Jesús."},
            {"q": "¿Qué significa ser hecho 'hijo de Dios' mediante la fe?", "op": ["Entrar en una nueva identidad y relación familiar con el Creador.", "Adquirir inmunidad frente a las leyes de la Tierra.", "Lograr una condición angelical superior."], "r": "Entrar en una nueva identidad y relación familiar con el Creador."}
        ]
    }
]

preguntas = [
    {"q": "¿Quién era el sumo sacerdote cuando Jesús fue juzgado?", "op": ["Caifás", "Anás", "Gamaliel", "Nicodemo"], "r": "Caifás", "info": "Fue el sumo sacerdote al momento de la crucifixión."},
    {"q": "¿En qué ciudad predicó Pablo sobre el 'Dios desconocido'?", "op": ["Corinto", "Éfeso", "Atenas", "Filipos"], "r": "Atenas", "info": "Pablo visitó una ciudad famosa por su filosofía."},
    {"q": "¿Cómo se llamaba el esclavo que Pablo envió de regreso a Filemón?", "op": ["Onésimo", "Tíquico", "Epafrodito", "Marcos"], "r": "Onésimo", "info": "Este hombre huyó de su amo pero se encontró con Pablo."},
    {"q": "¿Cuál es el libro que menciona a 'César' por primera vez?", "op": ["Mateo", "Marcos", "Lucas", "Juan"], "r": "Lucas", "info": "Es el mismo libro que detalla el nacimiento de Jesús."},
    {"q": "¿Quién fue el primer mártir cristiano?", "op": ["Pedro", "Esteban", "Santiago", "Felipe"], "r": "Esteban", "info": "Un hombre lleno de gracia y poder que fue apedreado."},
    {"q": "¿A qué iglesia escribió Pablo sobre la 'armadura de Dios'?", "op": ["Corinto", "Roma", "Éfeso", "Galacia"], "r": "Éfeso", "info": "Esta carta aborda la lucha espiritual."},
    {"q": "¿Quién acompañó a Pablo en su primer viaje misionero?", "op": ["Silas", "Bernabé", "Timoteo", "Lucas"], "r": "Bernabé", "info": "Conocido como el 'hijo de consolación'."},
    {"q": "¿Cómo se llamaba la mujer que Pablo resucitó en Jope?", "op": ["Lidia", "Dorcas", "Priscila", "Febe"], "r": "Dorcas", "info": "Una mujer admirada por su caridad."},
    {"q": "What apóstol escribió más libros en el Nuevo Testamento?", "op": ["Juan", "Pedro", "Pablo", "Lucas"], "r": "Pablo", "info": "Es el autor que más cartas escribió."},
    {"q": "¿En qué isla naufragó Pablo?", "op": ["Patmos", "Creta", "Malta", "Chipre"], "r": "Malta", "info": "Una isla del Mediterráneo."},
    {"q": "¿Quién escribió el libro de Hebreos?", "op": ["Pablo", "Apolos", "Desconocido", "Bernabé"], "r": "Desconocido", "info": "Su autoría es uno de los temas más debatidos."},
    {"q": "¿Qué significa el nombre 'Getsemaní'?", "op": ["Lugar de llanto", "Prensa de aceite", "Jardín santo", "Lugar de reposo"], "r": "Prensa de aceite", "info": "Hace referencia a la maquinaria de aceite."},
    {"q": "¿A qué ciudad se dirigía Saulo cuando vio la luz del cielo?", "op": ["Jericó", "Damasco", "Samaria", "Antioquía"], "r": "Damasco", "info": "Saulo iba con autoridad a esta ciudad antigua."},
    {"q": "¿Qué libro describe la nueva Jerusalén?", "op": ["Hebreos", "Santiago", "Apocalipsis", "Judas"], "r": "Apocalipsis", "info": "El libro profético que describe el final."},
    {"q": "¿Quién bautizó al eunuco etíope?", "op": ["Pedro", "Felipe", "Juan", "Esteban"], "r": "Felipe", "info": "Uno de los siete diáconos."},
    {"q": "¿Cuántas personas fueron alimentadas con cinco panes y dos peces?", "op": ["2,000", "5,000", "7,000", "10,000"], "r": "5,000", "info": "El gran milagro de provisión."},
    {"q": "¿Quién negó a Jesús tres veces antes de que el gallo cantara?", "op": ["Juan", "Judas", "Pedro", "Tomás"], "r": "Pedro", "info": "El discípulo que prometió lealtad absoluta."},
    {"q": "¿En qué ciudad se llamaron por primera vez 'cristianos'?", "op": ["Jerusalén", "Antioquía", "Roma", "Corinto"], "r": "Antioquía", "info": "Ciudad donde la comunidad se hizo notoria."},
    {"q": "¿Qué objeto se le cayó a Pablo de los ojos tras su conversión?", "op": ["Escamas", "Polvo", "Sangre", "Velo"], "r": "Escamas", "info": "Una señal física de que su ceguera terminó."},
    {"q": "¿Quién era el rey que mandó matar a los niños en Belén?", "op": ["César", "Herodes", "Pilato", "Agripa"], "r": "Herodes", "info": "Un gobernante celoso de su poder."},
    {"q": "¿En qué valle fue traicionado Sansón por Dalila?", "op": ["Valle de Sorec", "Valle de Elah", "Valle de Ajalón", "Valle de Refaim"], "r": "Valle de Sorec", "info": "Dalila vivía en este valle."},
    {"q": "¿Cómo se llamaba el padre de Juan el Bautista?", "op": ["Zacarías", "Simeón", "José", "Elías"], "r": "Zacarías", "info": "Era sacerdote del grupo de Abías."},
    {"q": "¿Qué nombre recibió el lugar donde Jacob soñó con la escalera al cielo?", "op": ["Betel", "Hebrón", "Siquem", "Beerseba"], "r": "Betel", "info": "Significa 'Casa de Dios'."},
    {"q": "¿Quién fue el rey que pidió sabiduría a Dios para gobernar?", "op": ["Saúl", "David", "Salomón", "Roboam"], "r": "Salomón", "info": "Dios le dio sabiduría y riquezas por no pedir fama."},
    {"q": "¿Cómo se llamaba la esposa de Isaac?", "op": ["Rebeca", "Raquel", "Lea", "Bilha"], "r": "Rebeca", "info": "Fue elegida mediante una señal junto al pozo."},
    {"q": "¿Qué profeta fue enviado a Nínive pero huyó a Tarsis?", "op": ["Amós", "Jonás", "Oseas", "Miqueas"], "r": "Jonás", "info": "Su historia nos enseña sobre la obediencia."},
    {"q": "¿Cuál es el nombre del lugar donde Jesús multiplicó los panes y peces por segunda vez?", "op": ["Galilea", "Decápolis", "Judea", "Samaria"], "r": "Decápolis", "info": "La región de las diez ciudades."},
    {"q": "¿Cómo se llamaba el oficial etíope que bautizó Felipe?", "op": ["Ebed-melec", "Cus", "Candace", "Eunuco sin nombre"], "r": "Eunuco sin nombre", "info": "La Biblia solo se refiere a él por su cargo y origen."},
    {"q": "🏠 ¿Qué montaña fue el lugar donde murió Moisés?", "op": ["Sinaí", "Ararat", "Nebo", "Carmelo"], "r": "Nebo", "info": "Desde allí pudo ver la Tierra Prometida."},
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
    {"pista": "Preparé el camino para Jesús bautizando en el río Jordán.", "op": ["Juan el Bautista", "Elías", "Enoc", "Jeremías"], "r": "Juan el Bautista"},
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
        <a href="/personaje_init"><button style="background: #0f3460; color: white; border: 1px solid #4ecca3;">Adivina el Personaje</button></a>
        <a href="/verdades_init"><button style="background: #e94560; color: white;">El reto de las 5 Verdades</button></a></div>
    """)

# --- TRIVIA BÍBLICA ---
@app.route('/trivia_init')
def trivia_init():
    session['idx'] = 0; session['puntos'] = 0
    return redirect(url_for('juego'))

@app.route('/juego')
def juego():
    idx = session.get('idx', 0)
    if idx >= len(preguntas):
        cal = round((session.get('puntos', 0) / len(preguntas)) * 10, 1)
        HISTORIAL_CALIFICACIONES.append({
            "nombre": session.get('nombre', 'Desconocido'),
            "juego": "Trivia Bíblica",
            "calificacion": cal,
            "detalles": f"{session.get('puntos', 0)} de {len(preguntas)}",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return render_template_string(CSS_STYLE + f"""
            <div class="card">
                <h1>🎉 ¡Terminaste, {session.get('nombre')}!</h1>
                <p>Aciertos: {session.get('puntos', 0)} de {len(preguntas)}</p>
                <h1>Calificación: {cal}</h1>
                <a href="/trivia_init"><button>Volver a jugar</button></a>
                <a href="/"><button style="background:#ffd700">Registrar nuevo jugador 👤</button></a>
                <a href="/menu"><button style="background:#888">Menú</button></a>
            </div>
        """)
    p = preguntas[idx]
    ops = p['op'][:]; random.shuffle(ops)
    btns = "".join([f'<a href="/res?op={o}"><button>{o}</button></a>' for o in ops])
    return render_template_string(CSS_STYLE + f"""<div class="card"><p>Pregunta {idx + 1} de {len(preguntas)}</p><h2>{p['q']}</h2>{btns}<div class="info-box">{p['info']}</div></div>""")

@app.route('/res')
def res():
    if request.args.get('op') == preguntas[session.get('idx', 0)]['r']:
        session['puntos'] = session.get('puntos', 0) + 1
    session['idx'] = session.get('idx', 0) + 1
    return redirect(url_for('juego'))

# --- ADIVINA EL PERSONAJE ---
@app.route('/personaje_init')
def personaje_init():
    session['idx_p'] = 0; session['puntos_p'] = 0
    return redirect(url_for('juego_personaje'))

@app.route('/juego_personaje')
def juego_personaje():
    idx = session.get('idx_p', 0)
    if idx >= len(personajes):
        cal = round((session.get('puntos_p', 0) / len(personajes)) * 10, 1)
        HISTORIAL_CALIFICACIONES.append({
            "nombre": session.get('nombre', 'Desconocido'),
            "juego": "Adivina el Personaje",
            "calificacion": cal,
            "detalles": f"{session.get('puntos_p', 0)} de {len(personajes)}",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return render_template_string(CSS_STYLE + f"""
            <div class="card">
                <h1>🎉 ¡Terminaste, {session.get('nombre')}!</h1>
                <p>Aciertos: {session.get('puntos_p', 0)} de {len(personajes)}</p>
                <h1>Calificación: {cal}</h1>
                <a href="/personaje_init"><button>Volver a jugar</button></a>
                <a href="/"><button style="background:#ffd700">Registrar nuevo jugador 👤</button></a>
                <a href="/menu"><button style="background:#888">Menú</button></a>
            </div>
        """)
    p = personajes[idx]; session['r_p'] = p['r']; ops = p['op'][:]; random.shuffle(ops)
    btns = "".join([f'<a href="/res_p?op={o}"><button>{o}</button></a>' for o in ops])
    return render_template_string(CSS_STYLE + f"""<div class="card"><p>Personaje {idx + 1} de {len(personajes)}</p><h1>👤 ¿Quién soy?</h1><p style="font-size:20px">{p['pista']}</p>{btns}</div>""")

@app.route('/res_p')
def res_p():
    if request.args.get('op') == session.get('r_p'):
        session['puntos_p'] = session.get('puntos_p', 0) + 1
    session['idx_p'] = session.get('idx_p', 0) + 1
    return redirect(url_for('juego_personaje'))


# =====================================================================
# --- SECCIÓN: EL RETO DE LAS 5 VERDADES (TOTALMENTE CORREGIDO E INFALIBLE) ---
# =====================================================================

@app.route('/verdades_init')
def verdades_init():
    session['v_bloque'] = 0  
    session['v_pregunta_idx'] = 0  
    session['v_fase'] = 'juego'  
    session['v_intento_corregir'] = False
    session['v_respuestas_usuario'] = [None] * 10
    session['v_indices_erroneos'] = []
    return redirect(url_for('verdades_juego'))

@app.route('/verdades_juego')
def verdades_juego():
    bloque_idx = session.get('v_bloque', 0)
    
    if bloque_idx >= len(verdades_data):
        HISTORIAL_CALIFICACIONES.append({
            "nombre": session.get('nombre', 'Desconocido'),
            "juego": "El Reto de las 5 Verdades",
            "calificacion": 10.0,
            "detalles": "⭐⭐⭐⭐⭐ Reto Superado Completo",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return render_template_string(CSS_STYLE + f"""
            <div class="card" style="border: 2px solid #ffd700;">
                <h1 style="color: #ffd700;">🏆 ¡RETO COMPLETADO! 🏆</h1>
                <p style="font-size: 1.1em;">Felicidades <b>{session.get('nombre')}</b>, has superado las 5 Verdades Espirituales ganando tus 5 Estrellas ⭐⭐⭐⭐⭐</p>
                <div class="info-box" style="background: #1b4332; border-color: #ffd700;">
                    <h3 style="margin-top:0;">📖 Apocalipsis 3:20</h3>
                    <p>"He aquí, yo estoy a la puerta y llamo; si alguno oye mi voz y abre la puerta, entraré a él, y cenaré con él, y él conmigo."</p>
                </div>
                <p style="color: #4ecca3; font-weight: bold; font-size: 1.2em;">✨ Propósito: Oración de ACEPTACIÓN ✨</p>
                <a href="/"><button style="background:#ffd700">Registrar nuevo jugador 👤</button></a>
                <a href="/menu"><button style="background:#888; color:white;">Ir al Menú</button></a>
            </div>
        """)
        
    fase = session.get('v_fase', 'juego')
    bloque_actual = verdades_data[bloque_idx]
    preguntas_bloque = bloque_actual['preguntas']
    
    if fase == 'juego':
        q_idx = session.get('v_pregunta_idx', 0)
        p = preguntas_bloque[q_idx]
        ops = p['op'][:]
        
        # Validamos por índice en la URL en lugar de texto plano largo para asegurar exactitud total
        btns = "".join([f'<a href="/verdades_res?ans_idx={i}"><button>{o}</button></a>' for i, o in enumerate(ops)])
        return render_template_string(CSS_STYLE + f"""
            <div class="card">
                <p style="color: #4ecca3; font-weight: bold;">Nivel {bloque_idx + 1}: {bloque_actual['titulo']}</p>
                <p>Pregunta {q_idx + 1} de 10</p>
                <h2>{p['q']}</h2>
                {btns}
            </div>
        """)
        
    elif fase == 'repaso':
        indices_mal = session.get('v_indices_erroneos', [])
        if not indices_mal:
            session['v_bloque'] = session.get('v_bloque', 0) + 1
            session['v_pregunta_idx'] = 0
            session['v_fase'] = 'juego'
            return redirect(url_for('verdades_juego'))
            
        q_idx = indices_mal[0]
        p = preguntas_bloque[q_idx]
        ops = p['op'][:]
        btns = "".join([f'<a href="/verdades_res?ans_idx={i}"><button style="background:#e94560; color:white;">{o}</button></a>' for i, o in enumerate(ops)])
        return render_template_string(CSS_STYLE + f"""
            <div class="card" style="border: 2px solid #e94560;">
                <p style="color: #e94560; font-weight: bold;">⚠️ ¡CORRECCIÓN DE STRIKE! ❌</p>
                <p>Corrija un error cometido en el bloque (Última Oportunidad)</p>
                <h2>{p['q']}</h2>
                {btns}
            </div>
        """)

@app.route('/verdades_res')
def verdades_res():
    bloque_idx = session.get('v_bloque', 0)
    fase = session.get('v_fase', 'juego')
    preguntas_bloque = verdades_data[bloque_idx]['preguntas']
    
    # Leemos la opción elegida mediante su índice numérico
    ans_idx = int(request.args.get('ans_idx', 0))
    opcion_elegida = preguntas_bloque[session.get('v_pregunta_idx', 0) if fase == 'juego' else session.get('v_indices_erroneos', [0])[0]]['op'][ans_idx]
    
    if fase == 'juego':
        q_idx = session.get('v_pregunta_idx', 0)
        
        if 'v_respuestas_usuario' not in session or not session['v_respuestas_usuario']:
            session['v_respuestas_usuario'] = [None] * 10
            
        respuestas = session['v_respuestas_usuario']
        respuestas[q_idx] = opcion_elegida
        session['v_respuestas_usuario'] = respuestas
        
        if q_idx + 1 < 10:
            session['v_pregunta_idx'] = q_idx + 1
            return redirect(url_for('verdades_juego'))
        else:
            errores = []
            for i in range(10):
                if session['v_respuestas_usuario'][i] != preguntas_bloque[i]['r']:
                    errores.append(i)
            
            if len(errores) == 0:
                return redirect(url_for('verdades_completar_nivel'))
            else:
                session['v_indices_erroneos'] = errores
                session['v_fase'] = 'repaso'
                session['v_intento_corregir'] = True
                
                html_error = CSS_STYLE + f"""
                    <div class="card" style="border: 2px solid #e94560;">
                        <h1 style="color: #e94560; margin-bottom: 0;">❌ STRIKE EN EL BLOQUE ❌</h1>
                        <p style="font-size: 1.2em;">Has tenido {len(errores)} respuesta(s) incorrecta(s) de las 10.</p>
                        <p>El sistema te presentará únicamente las preguntas fallidas. ¡Tienes <b>una sola oportunidad</b> para corregir cada una o será Fin del Juego!</p>
                        <a href="/verdades_juego"><button style="background: #e94560; color: white;">Iniciar Corrección</button></a>
                    </div>
                """
                return render_template_string(html_error)
                
    elif fase == 'repaso':
        indices_mal = session.get('v_indices_erroneos', [])
        if not indices_mal:
            return redirect(url_for('verdades_completar_nivel'))
            
        q_idx = indices_mal[0]
        
        if opcion_elegida == preguntas_bloque[q_idx]['r']:
            indices_mal.pop(0)
            session['v_indices_erroneos'] = indices_mal
            
            if len(indices_mal) == 0:
                return redirect(url_for('verdades_completar_nivel'))
            else:
                return redirect(url_for('verdades_juego'))
        else:
            return redirect(url_for('verdades_gameover'))

@app.route('/verdades_completar_nivel')
def verdades_completar_nivel():
    bloque_idx = session.get('v_bloque', 0)
    bloque_actual = verdades_data[bloque_idx]
    versiculos_html = "".join([f"<p><i>\"{v}\"</i></p>" for v in bloque_actual['versiculos']])
    
    titulo_pantalla = "⭐ ¡TE HAS SALVADO! ⭐" if session.get('v_intento_corregir') else "⭐ ¡NIVEL SUPERADO! ⭐"
    borde_color = "#4ecca3" if session.get('v_intento_corregir') else "#ffd700"
    
    html_exito = CSS_STYLE + f"""
        <div class="card" style="border: 2px solid {borde_color};">
            <h1 style="color: {borde_color}; margin-bottom: 0;">{titulo_pantalla}</h1>
            <p style="color: #4ecca3; font-weight: bold; font-size: 1.2em; margin-top:5;">¡Recibiste una Estrella por completar las 10 preguntas!</p>
            <div class="info-box">
                <h3 style="margin-top: 0; color: #4ecca3;">📖 Versículos Desbloqueados:</h3>
                {versiculos_html}
            </div>
            <a href="/verdades_avanzar"><button>Avanzar al Siguiente Nivel</button></a>
        </div>
    """
    return render_template_string(html_exito)

@app.route('/verdades_avanzar')
def verdades_avanzar():
    session['v_bloque'] = session.get('v_bloque', 0) + 1
    session['v_pregunta_idx'] = 0
    session['v_fase'] = 'juego'
    session['v_intento_corregir'] = False
    session['v_respuestas_usuario'] = [None] * 10
    session['v_indices_erroneos'] = []
    return redirect(url_for('verdades_juego'))

@app.route('/verdades_gameover')
def verdades_gameover():
    HISTORIAL_CALIFICACIONES.append({
        "nombre": session.get('nombre', 'Desconocido'),
        "juego": "El Reto de las 5 Verdades",
        "calificacion": round((session.get('v_bloque', 0) / 5) * 10, 1),
        "detalles": f"💀 Game Over en Nivel {session.get('v_bloque', 0) + 1}",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return render_template_string(CSS_STYLE + f"""
        <div class="card" style="border: 2px solid #e94560;">
            <h1 style="color: #e94560; font-size: 45px;">💀 GAME OVER 💀</h1>
            <p style="font-size: 1.2em;">Lo sentimos, <b>{session.get('nombre')}</b>. Fallaste en tu oportunidad de corrección.</p>
            <p>Debes conocer bien las verdades antes de avanzar.</p>
            <a href="/verdades_init"><button style="background: #e94560; color: white;">Reiniciar Reto</button></a>
            <a href="/"><button style="background: #ffd700">Registrar nuevo jugador 👤</button></a>
            <a href="/menu"><button style="background: #888;">Volver al Menú</button></a>
        </div>
    """)


# =====================================================================
# --- PANEL SECRETO DE ADMINISTRACIÓN Y MÉTRICAS ---
# =====================================================================

@app.route('/admin_daniel', methods=['GET', 'POST'])
def admin_daniel():
    if request.method == 'POST':
        if request.form.get('clave') == 'dpatt#admon2026':
            session['es_admin'] = True
        else:
            return render_template_string(CSS_STYLE + """
                <div class="card" style="border: 2px solid #e94560;">
                    <h2 style="color:#e94560;">Clave Incorrecta</h2>
                    <a href="/admin_daniel"><button>Intentar de nuevo</button></a>
                </div>
            """)

    if not session.get('es_admin', False):
        return render_template_string(CSS_STYLE + """
            <div class="card">
                <h2>🔐 Panel de Control de la Iglesia</h2>
                <p>Por favor, introduce la clave secreta de acceso:</p>
                <form method="POST">
                    <input type="password" name="clave" placeholder="Contraseña de administrador" style="padding:15px; width:80%; border-radius:10px; font-size:18px; margin-bottom: 15px;" required>
                    <button type="submit">Iniciar Sesión</button>
                </form>
                <a href="/menu"><button style="background:#888">Volver al Juego</button></a>
            </div>
        """)

    tabla_filas = ""
    for idx, reg in enumerate(HISTORIAL_CALIFICACIONES):
        tabla_filas += f"""
            <tr style="border-bottom: 1px solid #454d66;">
                <td style="padding:10px;">{reg['fecha']}</td>
                <td style="padding:10px; font-weight:bold;">{reg['nombre']}</td>
                <td style="padding:10px; color:#4ecca3;">{reg['juego']}</td>
                <td style="padding:10px;">{reg['detalles']}</td>
                <td style="padding:10px; font-weight:bold; color:#ffd700;">{reg['calificacion']}</td>
            </tr>
        """

    return render_template_string("""
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #1a1a2e; color: white; font-family: sans-serif; padding: 20px; }
            .container { width: 95%; max-width: 800px; margin: auto; background: #16213e; padding: 25px; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
            button { padding: 12px 20px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; font-weight: bold; background: #4ecca3; margin: 10px 5px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #0f3460; border-radius: 10px; overflow: hidden; }
            th { background: #4ecca3; color: black; padding: 12px; }
        </style>
        <div class="container">
            <h2>📊 Métricas y Calificaciones - "Cristo te Ama"</h2>
            <p>Monitoreo de participación en la aplicación web.</p>
            <a href="/admin_descargar"><button style="background: #ffd700; color: black;">📥 Descargar Reporte Excel (CSV)</button></a>
            <a href="/admin_logout"><button style="background: #e94560; color: white;">Cerrar Sesión</button></a>
            <a href="/menu"><button style="background: #888; color: white;">Ir al Menú principal</button></a>
            
            <table>
                <thead>
                    <tr>
                        <th>Fecha y Hora</th>
                        <th>Nombre</th>
                        <th>Juego</th>
                        <th>Progreso / Detalles</th>
                        <th>Calificación</th>
                    </tr>
                </thead>
                <tbody>
                    """ + (tabla_filas if tabla_filas else "<tr><td colspan='5' style='padding:20px; text-align:center; color:#888;'>Aún no hay registros de partidas completadas.</td></tr>") + """
                </tbody>
            </table>
        </div>
    """)

@app.route('/admin_descargar')
def admin_descargar():
    if not session.get('es_admin', False):
        return redirect(url_for('admin_daniel'))
        
    csv_data = "\uFEFFFecha,Nombre,Juego,Detalles,Calificacion\n"
    for r in HISTORIAL_CALIFICACIONES:
        csv_data += f"{r['fecha']},{r['nombre']},{r['juego']},{r['detalles']},{r['calificacion']}\n"
        
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=reporte_juegos_iglesia.csv"}
    )

@app.route('/admin_logout')
def admin_logout():
    session['es_admin'] = False
    return redirect(url_for('admin_daniel'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
