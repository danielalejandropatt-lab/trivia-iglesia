from flask import Flask, request, render_template_string, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta_daniel'

# --- BANCO DE DATOS: 5 VERDADES (10 preguntas por bloque) ---
verdades_data = [
    {
        "nivel": 1,
        "titulo": "La Verdad del Amor",
        "versiculos": [
            "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna. (Jn. 3:16)",
            "... yo he venido para que tengan vida, y para que la tengan en abundancia. (Jn. 10:10b)"
        ],
        "preguntas": [
            {"q": "¿Cuál es el propósito original de Dios para tu vida?", "op": ["A) Que tengas una vida abundante.", "B) Que consigas riquezas materiales y éxito terrenal.", "C) Que vivas sin ningún tipo de problema."], "r": "A) Que tengas una vida abundante."},
            {"q": "¿Qué motivó a Dios a entregar a su Hijo según Juan 3:16?", "op": ["A) El cumplimiento de una ley antigua.", "B) Su inmenso amor por el mundo.", "C) La necesidad de juzgar a la humanidad."], "r": "B) Su inmenso amor por el mundo."},
            {"q": "¿Cuál es el regalo que Dios ofrece a quienes creen en su Hijo?", "op": ["A) La vida eterna.", "B) Sabiduría y conocimiento humano.", "C) Prosperidad en todos tus negocios."], "r": "A) La vida eterna."},
            {"q": "Según Juan 10:10, ¿para qué vino Jesús al mundo?", "op": ["A) Para fundar una nueva religión.", "B) Para abolir las escrituras del pasado.", "C) Para que tengamos vida en abundancia."], "r": "C) Para que tengamos vida en abundancia."},
            {"q": "¿Cómo se describe la naturaleza del amor de Dios en la primera verdad?", "op": ["A) Como un amor condicionado a nuestro comportamiento.", "B) Como un amor que da lo más preciado (a su Hijo) para salvarnos.", "C) Como un amor distante que no interviene en la Tierra."], "r": "B) Como un amor que da lo más preciado (a su Hijo) para salvarnos."},
            {"q": "¿Qué significa tener 'vida abundante' en el contexto espiritual?", "op": ["A) Vivir en plenitud y en relación con el propósito de Dios.", "B) Tener una vida libre de cualquier dolor físico.", "C) Acumular bienes para asegurar el futuro terrenal."], "r": "A) Vivir en plenitud y en relación con el propósito de Dios."},
            {"q": "¿A quiénes incluye el amor de Dios mencionado en Juan 3:16?", "op": ["A) Exclusivamente a las personas del pueblo de Israel.", "B) A todo el mundo ('de tal manera amó Dios al mundo').", "C) Únicamente a aquellos que nunca han cometido errores."], "r": "B) A todo el mundo ('de tal manera amó Dios al mundo')."},
            {"q": "¿Es la vida eterna algo que se gana o que se recibe por amor?", "op": ["A) Se gana acumulando buenas obras durante la vida.", "B) Se compra a través de sacrificios religiosos.", "C) Se recibe como resultado del plan amoroso de Dios."], "r": "C) Se recibe como resultado del plan amoroso de Dios."},
            {"q": "¿Qué asegura Juan 3:16 que NO le pasará a quien cree?", "op": ["A) Que no se perderá.", "B) Que no tendrá ninguna tristeza en la Tierra.", "C) Que sus problemas económicos desaparecerán."], "r": "A) Que no se perderá."},
            {"q": "¿Cuál es la base de toda la relación entre Dios y el hombre en esta primera ley?", "op": ["A) El miedo al castigo divino.", "B) El amor incondicional del Creador.", "C) El cumplimiento estricto de rituales."], "r": "B) El amor incondicional del Creador."}
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
            {"q": "¿Qué es lo que impide al hombre experimentar el amor de Dios?", "op": ["A) La distancia física con el cielo.", "B) Las pocas buenas obras que realiza.", "C) El pecado."], "r": "C) El pecado."},
            {"q": "¿Cuántas personas han pecado según el texto de Romanos 3:23?", "op": ["A) Todos, sin excepción.", "B) Solo aquellas que no asisten a la iglesia.", "C) Únicamente los criminales."], "r": "A) Todos, sin excepción."},
            {"q": "¿Cuál es el estado del pecador respecto a la gloria de Dios?", "op": ["A) Está en constante evaluación.", "B) Está destituido de ella.", "C) Se mantiene neutral ante ella."], "r": "B) Está destituido de ella."},
            {"q": "¿Cuál es la consecuencia legal y espiritual del pecado según Romanos 6:23?", "op": ["A) Una simple llamada de atención.", "B) La muerte.", "C) El olvido temporal."], "r": "B) La muerte."},
            {"q": "¿Por qué el pecado causa una separación?", "op": ["A) Porque crea una barrera entre la santidad de Dios y la condición humana.", "B) Porque a Dios no le interesa la humanidad.", "C) Porque los hombres decidieron mudarse de planeta."], "r": "A) Porque crea una barrera entre la santidad de Dios y la condición humana."},
            {"q": "¿Puede el hombre por su cuenta cruzar el abismo del pecado?", "op": ["A) Sí, mediante la meditación profunda.", "B) Sí, si se esfuerza lo suficiente en hacer el bien.", "C) No, el pecado nos mantiene separados por completo."], "r": "C) No, el pecado nos mantiene separados por completo."},
            {"q": "¿Qué tipo de 'muerte' se menciona en la segunda verdad?", "op": ["A) La muerte física del cuerpo al final de los tiempos.", "B) La muerte espiritual como paga por el pecado.", "C) El cese total de la existencia humana."], "r": "B) La muerte espiritual como paga por el pecado."},
            {"q": "¿Por qué se dice que el pecado nos priva del plan de Dios?", "op": ["A) Porque nos impide vivir la vida abundante que Él diseñó.", "B) Porque borra nuestros nombres de la historia humana.", "C) Porque detiene el reloj del tiempo divino."], "r": "A) Porque nos impide vivir la vida abundante que Él diseñó."},
            {"q": "¿Es el pecado un problema individual o universal?", "op": ["A) Individual, pues afecta solo a unos pocos.", "B) Universal, pues todos pecaron.", "C) Temporal, porque desaparece con la edad."], "r": "B) Universal, pues todos pecaron."},
            {"q": "¿Cuál es la función de la segunda verdad en el plan de salvación?", "op": ["A) Asustar a las personas para que sigan reglas.", "B) Servir como diagnóstico de la necesidad humana de un Salvador.", "C) Demostrar que no hay ninguna esperanza."], "r": "B) Servir como diagnóstico de la necesidad humana de un Salvador."}
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
            {"q": "¿Quién es el sustituto que Dios proveyó para el hombre?", "op": ["A) Un ángel celestial.", "B) Jesucristo.", "C) Los profetas del Antiguo Testamento."], "r": "B) Jesucristo."},
            {"q": "¿Cómo demostró Dios su amor mientras aún éramos pecadores?", "op": ["A) Haciendo que Cristo muriera por nosotros.", "B) Enviando bendiciones materiales a la Tierra.", "C) Ignorando por completo nuestras faltas."], "r": "A) Haciendo que Cristo muriera por nosotros."},
            {"q": "¿Qué pagó Jesús específicamente en la cruz?", "op": ["A) Una parte de las deudas del pueblo.", "B) El precio completo de nuestra salvación.", "C) El permiso para construir nuevos templos."], "r": "B) El precio completo de nuestra salvación."},
            {"q": "¿Qué afirma Jesús sobre sí mismo en Juan 14:6?", "op": ["A) Que Él es uno de los tantos maestros espirituales.", "B) Que Él vino a aprender de la humanidad.", "C) Que Él es el camino, la verdad y la vida."], "r": "C) Que Él es el camino, la verdad y la vida."},
            {"q": "¿Es posible llegar al Padre a través de alguien que no sea Jesús?", "op": ["A) Sí, haciendo suficientes obras buenas.", "B) No, nadie viene al Padre sino por Él.", "C) Sí, a través de otros líderes religiosos."], "r": "B) No, nadie viene al Padre sino por Él."},
            {"q": "¿Por qué se llama a Jesús el 'Substituto'?", "op": ["A) Porque vino a cambiar las leyes políticas.", "B) Porque tomó el lugar del pecador y pagó su deuda de muerte.", "C) Porque reemplazó a los reyes de la Tierra."], "r": "B) Porque tomó el lugar del pecador y pagó su deuda de muerte."},
            {"q": "¿Qué representa la muerte de Cristo en el esquema de las cinco verdades?", "op": ["A) Una tragedy sin explicación.", "B) Un ejemplo moral de buena conducta.", "C) La solución divina al problema del pecado."], "r": "C) La solución divina al problema del pecado."},
            {"q": "¿Qué garantiza que el sacrificio de Jesús fue suficiente?", "op": ["A) Que Él pagó el precio 'completo'.", "B) Que se repite todos los años.", "C) Que dependía del esfuerzo del hombre."], "r": "A) Que Él pagó el precio 'completo'."},
            {"q": "¿Cómo se relaciona la tercera verdad con el amor de Dios?", "op": ["A) Es la prueba máxima de su amor (Romanos 5:8).", "B) Muestra que el amor se había terminado.", "C) No guarda ninguna relación directa."], "r": "A) Es la prueba máxima de su amor (Romanos 5:8)."},
            {"q": "¿Qué papel juega Jesús entre el hombre pecador y el Dios santo?", "op": ["A) El de un observador distante.", "B) El de único puente o mediador.", "C) El de un juez implacable."], "r": "B) El de único puente o mediador."}
        ]
    },
    {
        "nivel": 4,
        "titulo": "La Verdad del Arrepentimiento",
        "versiculos": [
            "Así que, arrepentíos y convertíos, para que sean borrados vuestros pecados; para que vengan de la presencia del Señor tiempos de refrigerio, (Hechos 3:19)"
        ],
        "preguntas": [
            {"q": "¿Qué mandato se da en Hechos 3:19 para recibir el perdón?", "op": ["A) Cumplir con penitencias severas.", "B) Arrepentirse y convertirse.", "C) Memorizar todas las leyes antiguas."], "r": "B) Arrepentirse y convertirse."},
            {"q": "¿Cuál es el beneficio directo del arrepentimiento?", "op": ["A) Que los pecados sean borrados.", "B) Conseguir fama y reconocimiento.", "C) Evitar cualquier malentendido humano."], "r": "A) Que los pecados sean borrados."},
            {"q": "¿Qué significa 'convertirse' tras el arrepentimiento?", "op": ["A) Cambiar de religión o de costumbres culturales.", "B) Cambiar de dirección hacia Dios.", "C) Modificar el aspecto físico."], "r": "B) Cambiar de dirección hacia Dios."},
            {"q": "¿Qué prometen las fuentes que viene tras el arrepentimiento?", "op": ["A) Tiempos de refrigerio de la presencia del Señor.", "B) Riquezas y posesiones en la Tierra.", "C) Una vida sin ningún tipo de esfuerzo."], "r": "A) Tiempos de refrigerio de la presencia del Señor."},
            {"q": "¿Es el arrepentimiento solo sentir pena por el pecado?", "op": ["A) Sí, es llorar y lamentarse por lo hecho.", "B) No, implica una decisión de volver a Dios.", "C) Sí, es un sentimiento puramente emocional."], "r": "B) No, implica una decisión de volver a Dios."},
            {"q": "¿Por qué el arrepentimiento es vital para la salvación?", "op": ["A) Porque permite abandonar la vida de pecado y reconciliarse con el Creador.", "B) Porque es una regla impuesta por los reyes.", "C) Porque nos hace lucir mejores ante la sociedad."], "r": "A) Porque permite abandonar la vida de pecado y reconciliarse con el Creador."},
            {"q": "Organizaciones divinas: ¿De quién proviene el perdón una vez que nos arrepentimos?", "op": ["A) De nuestras propias fuerzas.", "B) Del Señor.", "C) De la aprobación de los demás."], "r": "B) Del Señor."},
            {"q": "¿Qué le sucede a la barrera del pecado cuando hay arrepentimiento genuino?", "op": ["A) Los pecados son eliminados o 'borrados'.", "B) Se oculta temporalmente.", "C) Se mantiene exactamente igual."], "r": "A) Los pecados son eliminados o 'borrados'."},
            {"q": "¿Qué significa experimentar 'refrigerio' espiritual?", "op": ["A) Una sensación física de frío.", "B) Es el alivio y paz que Dios otorga al perdonar.", "C) El olvido absoluto del pasado."], "r": "B) Es el alivio y paz que Dios otorga al perdonar."},
            {"q": "¿Se puede ser salvo sin arrepentirse?", "op": ["A) Sí, la salvación no requiere ningún cambio.", "B) No, según las fuentes, el arrepentimiento es el paso esencial para que los pecados sean borrados.", "C) Sí, con que la persona crea que es buena es suficiente."], "r": "B) No, según las fuentes, el arrepentimiento es el paso esencial para que los pecados sean borrados."}
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
            {"q": "¿Cómo describe Romanos 6:23 a la vida eterna?", "op": ["A) Como una dádiva (regalo) de Dios.", "B) Como una recompensa por cumplir la ley.", "C) Como un beneficio exclusivo para unos pocos."], "r": "A) Como una dádiva (regalo) de Dios."},
            {"q": "¿Cuál es el nombre de la action de aceptar a Jesús por fe?", "op": ["A) Estudiarlo.", "B) Recibirlo.", "C) Imitarlo."], "r": "B) Recibirlo."},
            {"q": "¿Qué derecho adquieren quienes reciben a Jesús según Juan 1:12?", "op": ["A) La potestad de ser hechos hijos de Dios.", "B) La capacidad de no volver a fallar.", "C) El derecho a gobernar naciones terrenales."], "r": "A) La potestad de ser hechos hijos de Dios."},
            {"q": "¿Qué promete Jesús a quien oye su palabra y cree en Dios en Juan 5:24?", "op": ["A) Que tendrá éxito material garantizado.", "B) Que su vida en la Tierra será perfecta.", "C) Que tiene vida eterna y no vendrá a condenación."], "r": "C) Que tiene vida eterna y no vendrá a condenación."},
            {"q": "¿Cuál es el paso final que Jesús pide en Apocalipsis 3:20?", "op": ["A) Que se le construya un altar físico.", "B) Que se le abra la puerta de la vida.", "C) Que se sigan estrictas penitencias."], "r": "B) Que se le abra la puerta de la vida."},
            {"q": "¿Qué sucede si alguien abre la puerta de su corazón a Jesús?", "op": ["A) Él entrará y tendrá comunión íntima con esa persona.", "B) Él observará desde lejos el comportamiento.", "C) Él cambiará instantáneamente sus bienes terrenales."], "r": "A) Él entrará y tendrá comunión íntima con esa persona."},
            {"q": "¿La fe es un sentimiento o una decisión personal?", "op": ["A) Es una emoción pasajera del momento.", "B) Es una decisión de creer y recibir a Cristo como Salvador.", "C) Es un pensamiento puramente intelectual."], "r": "B) Es una decisión de creer y recibir a Cristo como Salvador."},
            {"q": "¿Qué seguridad tiene el creyente respecto a su pasado?", "op": ["A) Que ha pasado de muerte a vida.", "B) Que tendrá que pagar por sus errores anteriores.", "C) Que sus recuerdos serán completamente borrados."], "r": "A) Que ha pasado de muerte a vida."},
            {"q": "¿Por qué la salvación se considera una 'dádiva'?", "op": ["A) Porque se puede comprar si se tiene suficiente dinero.", "B) Porque no se compra ni se merece, se recibe por fe en Cristo Jesús.", "C) Porque exige un intercambio de bienes espirituales."], "r": "B) Porque no se compra ni se merece, se recibe por fe en Cristo Jesús."},
            {"q": "Qué significa ser hecho 'hijo de Dios' mediante la fe?", "op": ["A) Adquirir un estatus de superioridad social.", "B) Entrar en una nueva identidad y relación familiar con el Creador.", "C) Olvidar las responsabilidades humanas."], "r": "B) Entrar en una nueva identidad y relación familiar con el Creador."}
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
    {"pista": "Fui el rey que ordenó la construction de un muro alrededor de Jerusalén en tiempo récord.", "op": ["Salomón", "Ezequías", "Nehemías", "Josías"], "r": "Nehemías"},
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
        <a href="/personaje_init"><button>Adivina el Personaje</button></a>
        <a href="/verdades_init"><button style="background: #e94560; color: white;">El reto de las 5 Verdades</button></a></div>
    """)

# --- TRIVIA ORIGINAL ---
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

# --- PERSONAJES ORIGINAL ---
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


# =====================================================================
# --- NUEVA SECCIÓN: EL RETO DE LAS 5 VERDADES ---
# =====================================================================

@app.route('/verdades_init')
def verdades_init():
    session['v_bloque'] = 0  # Bloque/Nivel actual (0 a 4)
    session['v_fase'] = 'pregunta1'  # 'pregunta1', 'pregunta2', 'evaluacion', 'repaso'
    session['v_intento_corregir'] = False  # Si está en su segunda oportunidad
    
    # Seleccionar 2 preguntas al azar para cada uno de los 5 bloques
    preguntas_seleccionadas = []
    for b in verdades_data:
        pool = b['preguntas'][:]
        elegidas = random.sample(pool, 2)
        preguntas_seleccionadas.append(elegidas)
    
    session['v_seleccionadas'] = preguntas_seleccionadas
    session['v_respuestas_usuario'] = [None, None]  # Guardar las 2 respuestas
    return redirect(url_for('verdades_juego'))

@app.route('/verdades_juego')
def verdades_juego():
    bloque_idx = session.get('v_bloque', 0)
    
    # Pantalla final de Aceptación (Apocalipsis 3:20)
    if bloque_idx >= len(verdades_data):
        return render_template_string(CSS_STYLE + f"""
            <div class="card" style="border: 2px solid #ffd700;">
                <h1 style="color: #ffd700;">🏆 ¡RETO COMPLETADO! 🏆</h1>
                <p style="font-size: 1.1em;">Felicidades <b>{session.get('nombre')}</b>, has superado las 5 Verdades Espirituales ganando tus 5 Estrellas ⭐⭐⭐⭐⭐</p>
                <div class="info-box" style="background: #1b4332; border-color: #ffd700;">
                    <h3 style="margin-top:0;">📖 Apocalipsis 3:20</h3>
                    <p>"He aquí, yo estoy a la puerta y llamo; si alguno oye mi voz y abre la puerta, entraré a él, y cenaré con él, y él conmigo."</p>
                </div>
                <p style="color: #4ecca3; font-weight: bold; font-size: 1.2em;">✨ Propósito: Oración de ACEPTACIÓN ✨</p>
                <a href="/menu"><button style="background:#ffd700">Regresar al Menú</button></a>
            </div>
        """)
        
    fase = session.get('v_fase', 'pregunta1')
    bloque_actual = verdades_data[bloque_idx]
    preguntas_bloque = session['v_seleccionadas'][bloque_idx]
    
    # FASE: PREGUNTA 1
    if fase == 'pregunta1':
        p = preguntas_bloque[0]
        ops = p['op'][:]
        btns = "".join([f'<a href="/verdades_res?op={o}"><button>{o}</button></a>' for o in ops])
        return render_template_string(CSS_STYLE + f"""
            <div class="card">
                <p style="color: #4ecca3; font-weight: bold;">Nivel {bloque_idx + 1}: {bloque_actual['titulo']}</p>
                <p>Pregunta 1 de 2</p>
                <h2>{p['q']}</h2>
                {btns}
            </div>
        """)
        
    # FASE: PREGUNTA 2
    elif fase == 'pregunta2':
        p = preguntas_bloque[1]
        ops = p['op'][:]
        btns = "".join([f'<a href="/verdades_res?op={o}"><button>{o}</button></a>' for o in ops])
        return render_template_string(CSS_STYLE + f"""
            <div class="card">
                <p style="color: #4ecca3; font-weight: bold;">Nivel {bloque_idx + 1}: {bloque_actual['titulo']}</p>
                <p>Pregunta 2 de 2</p>
                <h2>{p['q']}</h2>
                {btns}
            </div>
        """)

    # FASE: REPASO / CORRECCIÓN DE ERRORES CORRESPONDIENTES
    elif fase == 'repaso':
        p1_correcta = session['v_respuestas_usuario'][0] == preguntas_bloque[0]['r']
        p2_correcta = session['v_respuestas_usuario'][1] == preguntas_bloque[1]['r']
        
        # Si falló la primera y aún no se corrige
        if not p1_correcta:
            p = preguntas_bloque[0]
            ops = p['op'][:]
            btns = "".join([f'<a href="/verdades_res?op={o}"><button style="background:#e94560; color:white;">{o}</button></a>' for o in ops])
            return render_template_string(CSS_STYLE + f"""
                <div class="card" style="border: 2px solid #e94560;">
                    <p style="color: #e94560; font-weight: bold;">⚠️ ¡CORRECCIÓN DE STRIKE! ❌</p>
                    <p>Corrige la Pregunta 1 (Última Oportunidad)</p>
                    <h2>{p['q']}</h2>
                    {btns}
                </div>
            """)
        # Si la primera estuvo bien pero falló la segunda
        elif not p2_correcta:
            p = preguntas_bloque[1]
            ops = p['op'][:]
            btns = "".join([f'<a href="/verdades_res?op={o}"><button style="background:#e94560; color:white;">{o}</button></a>' for o in ops])
            return render_template_string(CSS_STYLE + f"""
                <div class="card" style="border: 2px solid #e94560;">
                    <p style="color: #e94560; font-weight: bold;">⚠️ ¡CORRECCIÓN DE STRIKE! ❌</p>
                    <p>Corrige la Pregunta 2 (Última Oportunidad)</p>
                    <h2>{p['q']}</h2>
                    {btns}
                </div>
            """)

@app.route('/verdades_res')
def verdades_res():
    bloque_idx = session['v_bloque']
    fase = session['v_fase']
    preguntas_bloque = session['v_seleccionadas'][bloque_idx]
    opcion_elegida = request.args.get('op')
    
    if fase == 'pregunta1':
        session['v_respuestas_usuario'][0] = opcion_elegida
        session['v_fase'] = 'pregunta2'
        return redirect(url_for('verdades_juego'))
        
    elif fase == 'pregunta2':
        session['v_respuestas_usuario'][1] = opcion_elegida
        
        # Evaluar ambas respuestas
        p1_correcta = session['v_respuestas_usuario'][0] == preguntas_bloque[0]['r']
        p2_correcta = session['v_respuestas_usuario'][1] == preguntas_bloque[1]['r']
        
        if p1_correcta and p2_correcta:
            # CASO PERFECTO: Ambas bien -> Pantalla de Desbloqueo y Estrella
            bloque_actual = verdades_data[bloque_idx]
            versiculos_html = "".join([f"<p><i>\"{v}\"</i></p>" for v in bloque_actual['versiculos']])
            
            html_exito = CSS_STYLE + f"""
                <div class="card" style="border: 2px solid #ffd700;">
                    <h1 style="color: #ffd700; margin-bottom: 0;">⭐ ¡NIVEL SUPERADO! ⭐</h1>
                    <p style="color: #4ecca3; font-weight: bold; font-size: 1.2em; margin-top:5;">¡Recibiste una Estrella!</p>
                    <div class="info-box">
                        <h3 style="margin-top: 0; color: #4ecca3;">📖 Versículos Desbloqueados:</h3>
                        {versiculos_html}
                    </div>
                    <a href="/verdades_avanzar"><button>Avanzar al Siguiente Nivel</button></a>
                </div>
            """
            return render_template_string(html_exito)
        else:
            # CASO ERROR: Strike y redirección a corregir
            session['v_fase'] = 'repaso'
            session['v_intento_corregir'] = True
            
            html_error = CSS_STYLE + f"""
                <div class="card" style="border: 2px solid #e94560;">
                    <h1 style="color: #e94560; margin-bottom: 0;">❌ STRIKE ❌</h1>
                    <p style="font-size: 1.2em;">Una o ambas respuestas fueron incorrectas.</p>
                    <p>El juego te regresará a la(s) pregunta(s) fallida(s). ¡Tienes <b>una sola oportunidad</b> para corregir o será Fin del Juego!</p>
                    <a href="/verdades_juego"><button style="background: #e94560; color: white;">Corregir Errores</button></a>
                </div>
            """
            return render_template_string(html_error)
            
    elif fase == 'repaso':
        # Procesando el intento de corrección
        p1_correcta = session['v_respuestas_usuario'][0] == preguntas_bloque[0]['r']
        
        if not p1_correcta:
            # Corrigiendo la primera
            if opcion_elegida == preguntas_bloque[0]['r']:
                session['v_respuestas_usuario'][0] = opcion_elegida
                # Verificar si la segunda también estaba mal
                if session['v_respuestas_usuario'][1] != preguntas_bloque[1]['r']:
                    return redirect(url_for('verdades_juego')) # Va a corregir la segunda
            else:
                return redirect(url_for('verdades_gameover')) # Volvió a fallar -> Fin del juego
        else:
            # Corrigiendo la segunda
            if opcion_elegida == preguntas_bloque[1]['r']:
                session['v_respuestas_usuario'][1] = opcion_elegida
            else:
                return redirect(url_for('verdades_gameover')) # Volvió a fallar -> Fin del juego
                
        # Si llega aquí es porque ya corrigió todo con éxito
        bloque_actual = verdades_data[bloque_idx]
        versiculos_html = "".join([f"<p><i>\"{v}\"</i></p>" for v in bloque_actual['versiculos']])
        html_salvado = CSS_STYLE + f"""
            <div class="card" style="border: 2px solid #4ecca3;">
                <h1 style="color: #4ecca3; margin-bottom: 0;">⭐ ¡TE HAS SALVADO! ⭐</h1>
                <p>Corregiste con éxito y desbloqueaste el nivel.</p>
                <div class="info-box">
                    <h3 style="margin-top: 0; color: #4ecca3;">📖 Versículos Desbloqueados:</h3>
                    {versiculos_html}
                </div>
                <a href="/verdades_avanzar"><button>Avanzar al Siguiente Nivel</button></a>
            </div>
        """
        return render_template_string(html_salvado)

@app.route('/verdades_avanzar')
def verdades_avanzar():
    session['v_bloque'] += 1
    session['v_fase'] = 'pregunta1'
    session['v_intento_corregir'] = False
    session['v_respuestas_usuario'] = [None, None]
    return redirect(url_for('verdades_juego'))

@app.route('/verdades_gameover')
def verdades_gameover():
    return render_template_string(CSS_STYLE + f"""
        <div class="card" style="border: 2px solid #e94560;">
            <h1 style="color: #e94560; font-size: 45px;">💀 GAME OVER 💀</h1>
            <p style="font-size: 1.2em;">Lo sentimos, <b>{session.get('nombre')}</b>. Fallaste en tu oportunidad de corrección.</p>
            <p>Debes conocer bien las verdades antes de avanzar.</p>
            <a href="/verdades_init"><button style="background: #e94560; color: white;">Reiniciar Reto</button></a>
            <a href="/menu"><button style="background: #888;">Volver al Menú</button></a>
        </div>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
