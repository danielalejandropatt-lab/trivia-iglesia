# -*- coding: utf-8 -*-
from flask import Flask, request, render_template_string, redirect, url_for, session, Response
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_daniel'

# --- MEMORIA VOLATIL PARA LAS METRICAS DE LA IGLESIA ---
HISTORIAL_CALIFICACIONES = []

# --- BANCO DE DATOS: DIFICULTAD REFORMULADA Y COMPLEJA (10 preguntas por bloque) ---
verdades_data = [
    {
        "nivel": 1,
        "titulo": "La Verdad del Amor",
        "versiculos": [
            "Porque de tal manera amo Dios al mundo, que ha dado a su Hijo unigenito, para que todo aquel que en el cree, no se pierda, mas tenga vida eterna. (Jn. 3:16)",
            "... yo he venido para que tengan vida, y para que la tengan en abundancia. (Jn. 10:10b)"
        ],
        "preguntas": [
            {
                "q": "Cual es el proposito central e inicial de Dios para la existence del ser humano segun la primera verdad?",
                "op": [
                    "Que el hombre experimente una vida abundante, definida por la comunion plena con el Creador y el desarrollo de Su diseno eterno.",
                    "La exigencia de una perfeccion moral absoluta e impecabilidad intrinseca previa a cualquier manifestation de Su favor.",
                    "Demandas un sacrificio perpetuo de privacion existencial como unico mecanismo para aplacar la distancia con la Deidad."
                ],
                "r": "Que el hombre experimente una vida abundante, definida por la comunion plena con el Creador y el desarrollo de Su diseno eterno."
            },
            {
                "q": "Que motivo de forma primaria a Dios a entregar voluntariamente a Su Hijo unigenito segun la declaracion de Juan 3:16?",
                "op": [
                    "Su inmenso e incondicional amor por el mundo, manifestado en una action proactiva de rescate y preservacion espiritual.",
                    "La necesidad urgente de apaciguar Su ira santa mediante un acto reactivo de justicia punitiva ajeno a la compasion.",
                    "El cumplimiento formal y exclusivo de las clausulas legales estipuladas de manera restrictiva en el pacto abrahamico."
                ],
                "r": "Su inmenso e incondicional amor por el mundo, manifestado en una action proactiva de rescate y preservacion espiritual."
            },
            {
                "q": "Cual es el don o regalo escatologico que Dios garantiza de manera inmediata a aquellos que ejercen fe en Su Hijo?",
                "op": [
                    "La vida eterna, caracterizada por la cualidad y permanencia de una comunion ininterrumpida con el Dios vivo.",
                    "Un perdòn condicional y mutable, sujeto a auditorias periodicas basadas en el rendimiento moral del creyente.",
                    "La exencion soberana e inmunidad civil ante cualquier tipo de tribulacion, padecimiento fisico o crisis terrenal."
                ],
                "r": "La vida eterna, caracterizada por la cualidad y permanencia de una comunion ininterrumpida con el Dios vivo."
            },
            {
                "q": "De acuerdo con la declaracion explicita de Jesus en Juan 10:10b, cual es el objetivo preciso de Su encarnacion y venida al mundo?",
                "op": [
                    "Para que tengan vida, y para que la tengan en abundancia, definiendo el proposito en los terminos textuales declarados por el Redentor.",
                    "Para que alcancen una vida plenamente autorrealizada en abundancia, modificando la centralidad de la vida dada por Cristo hacia la autogestion.",
                    "Para que posean vida y paz en abundancia, anadiendo conceptos conceptualmente validos pero ajenos a la precision exacta de la cita biblica."
                ],
                "r": "Para que tengan vida, y para que la tengan en abundancia, definiendo el proposito en los terminos textuales declarados por el Redentor."
            },
            {
                "q": "Como se describe la naturaleza operativa del amor de Dios in el marco de esta primera verdad?",
                "op": [
                    "Como un amor sacrificial y proactivo que entrega voluntariamente lo mas preciado con el proposito directo de salvar.",
                    "Como una disposicion afectiva pasiva que otorga misericordia unicamente motivada por la piedad o lastima ante la miseria humana.",
                    "Como un sistema asistencial de recompensas y privilegios cosmicos destinado de forma exclusiva a los ya declarados justos en la Tierra."
                ],
                "r": "Como un amor sacrificial y proactivo que entrega voluntariamente lo mas preciado con el proposito directo de salvar."
            },
            {
                "q": "Que significa poseer una 'vida abundante' en el estricto contexto espiritual y relacional de esta verdad?",
                "op": [
                    "Vivir en plenitud, experimentando de forma integral la comunion, el gozo y la alineacion directa con el proposito soberano de Dios.",
                    "Gozar de una garantia de prosperidad financiera, acumulacion material y estatus socioeconomico elevado mediante decretos de fe.",
                    "Alcanzar un estado metafisico de iluminacion mental superior que permite trascender las limitaciones de la realidad fisica."
                ],
                "r": "Vivir en plenitud, experimentando de forma integral la comunion, el gozo y la alineacion directa con el proposito soberano de Dios."
            },
            {
                "q": "Cual es el alcance del amor divino y la oferta de redencion explicitada en el texto de Juan 3:16?",
                "op": [
                    "Incluye de manera universal a todo el mundo, rompiendo barreras etnicas, temporales o de merito previo para el acceso a la gracia.",
                    "Se limita restrictivamente a los patriarcas, profetas y guardianes historicos de los oraculos sagrados.",
                    "Aplica unica y selectivamente sobre aquellos individuos que logran guardar de antemano la totalidad de los mandamientos."
                ],
                "r": "Incluye de manera universal a todo el mundo, rompiendo barreras etnicas, temporales o de merito previo para el acceso a la gracia."
            },
            {
                "q": "Respecto a la adquisicion de la vida eterna, cual es la dinamica teologica correcta segun se desprende de esta ley del amor?",
                "op": [
                    "Se recibe gratuitamente como el resultado directo del plan soberano y amoroso de Dios, operando bajo el principio de la gracia.",
                    "Se gana de manera meritoria como retribucion justa por el volumen acumulado de obras de piedad, filantropia y sacrificios personales.",
                    "Se adquiere mediante un process iniciatico basado en el conocimiento intelectual de misterios sagrados e informacion esoterica."
                ],
                "r": "Se recibe gratuitamente como el resultado directo del plan soberano y amoroso de Dios, operando bajo el principio de la gracia."
            },
            {
                "q": "Que condicion de vulnerabilidad eterna asegura de forma categorica Juan 3:16 que NO padecera el individuo que deposita su confianza en Cristo?",
                "op": [
                    "Que no se perdera, garantizando la preservacion judicial del creyente frente a la ruina y la condenacion del alma.",
                    "Que no experimentara la muerte fisica ni los efectos biologicos del envejecimiento en el plano terrenal.",
                    "Que quedara completamente inhabilitado para volver a cometer cualquier error o falta moral de manera absoluta."
                ],
                "r": "Que no se perdera, garantizando la preservacion judicial del creyente frente a la ruina y la condenacion del alma."
            },
            {
                "q": "Cual constituye el cimiento y la base inamovible de toda la relación entre Dios y el hombre propuesto en esta primera verdad?",
                "op": [
                    "El amor incondicional y la iniciativa del Creador, quien define el vinculo desde Su propia esencia y caracter santo.",
                    "El temor reverente y la sumision psicologica del ser humano ante la disparidad de poder con el Absoluto.",
                    "El pacto bilateral basado en el cumplimiento riguroso y milimetrico de estatutos, ordenanzas y codigos liturgicos."
                ],
                "r": "El amor incondicional y la iniciativa del Creador, quien define el vinculo desde Su propia esencia y caracter santo."
            }
        ]
    },
    {
        "nivel": 2,
        "titulo": "La Verdad del Pecado",
        "versiculos": [
            "Por cuanto todos pecaron, y estan destituidos de la gloria de Dios, (Rom 3:23)",
            "Buffer la paga del pecado es muerte... (Rom. 6:23a)"
        ],
        "preguntas": [
            {
                "q": "Que es lo que impide al hombre experimentar el amor de Dios?",
                "op": [
                    "El pecado en si mismo, operando como una condicion activa de transgresion que interrumpe la comunion vital con el Creador.",
                    "La falta de un conocimiento intelectual o de una conciencia moral desarrollada respecto a las leyes divinas.",
                    "La condicion ontologica de ser una criatura finita, limitada y propensa a debilidades naturales e involuntarias."
                ],
                "r": "El pecado en si mismo, operando como una condicion activa de transgresion que interrumpe la comunion vital con el Creador."
            },
            {
                "q": "Cuantas personas han pecado segun el axioma teologico de Romanos 3:23?",
                "op": [
                    "La totalidad de la raza humana sin excepcion alguna, estableciendo una condicion de culpabilidad universal.",
                    "Aquellos individuos que, teniendo pleno uso de razon, rechazan deliberadamente los mandatos expresos de la ley.",
                    "La humanidad en general, exceptuando a quienes han sido predestinados o adoptados soberanamente como hijos de Dios."
                ],
                "r": "La totalidad de la raza humana sin excepcion alguna, estableciendo una condicion de culpabilidad universal."
            },
            {
                "q": "Cual es el estado del pecador respecto a la gloria de Dios segun la declaracion paulina?",
                "op": [
                    "Esta destituido de ella, implicando una carencia absoluta del estandar santo requerido para la comunion.",
                    "Se encuentra bajo un estado de suspension y observacion juridica, a la espera de una evaluacion final de sus obras.",
                    "Permanece en una posicion de distanciamiento geografico o cosmico que se resuelve mediante la iluminacion intelectual."
                ],
                "r": "Esta destituido de ella, implicando una carencia absoluta del estandar santo requerido para la comunion."
            },
            {
                "q": "Cual es la consecuencia espiritual y legal que establece Romanos 6:23a como retribucion del pecado?",
                "op": [
                    "La muerte, entendida como la paga judicial y el salario irreversible que el pecado devenga por su propia naturaleza.",
                    "Un estado cronico de alienacion psicologica manifestado a traves de la ansiedad existencial y la angustia mental.",
                    "Una degradacion moral progresiva que debilita temporalmente la posicion del hombre dentro del orden de la creacion."
                ],
                "r": "La muerte, entendida como la paga judicial y el salario irreversible que el pecado devenga por su propia naturaleza."
            },
            {
                "q": "Por que el pecado produce intrinsecamente una separacion entre Dios y el hombre?",
                "op": [
                    "Because la santidad de Dios y la naturaleza del pecado son mutuamente excluyentes, levantando una barrera espiritual infranqueable para el ser humano.",
                    "Porque la soberania divina decide replegarse y apartarse ante la escasez de adoradores calificados en la Tierra.",
                    "Porque debilita las facultades del libre albedrio de tal manera que el hombre olvida de forma natural el camino de regreso a su Creador."
                ],
                "r": "Because la santidad de Dios y la naturaleza del pecado son mutuamente excluyentes, levantando una barrera espiritual infranqueable para el ser humano."
            },
            {
                "q": "Posee el ser humano la capacidad inherente para cruzar por su cuenta el abisco generado por el pecado?",
                "op": [
                    "No, puesto que el pecado establece una condicion de total incapacidad espiritual que anula cualquier esfuerzo autonomo de reconciliacion.",
                    "Sí, siempre y cuando aplique un sistema riguroso de compensacion moral mediante obras de justicia y caridad que equilibren su balanza ante Dios.",
                    "Sí, a traves de una metanoia puramente racional combinada con disciplinas misticas y ejercicios de meditacion profunda."
                ],
                "r": "No, puesto que el pecado establece una condicion de total incapacidad espiritual que anula cualquier esfuerzo autonomo de reconciliacion."
            },
            {
                "q": "Que naturaleza define a la 'muerte' dictaminada en la segunda verdad?",
                "op": [
                    "Una muerte espiritual y judicial que se traduce en la separacion total, absoluta y eterna de la fuente de la vida.",
                    "Un estado de letargo espiritual transitorio y reversible que se suspende automaticamente con cualquier acto de remordimiento humano.",
                    "La extincion ontologica definitiva de la conciencia, provocando que el individuo cese de existir por completo en el cosmos."
                ],
                "r": "Una muerte espiritual y judicial que se traduce en la separacion total, absoluta y eterna de la fuente de la vida."
            },
            {
                "q": "Por que se afirma categoricamente que el pecado nos priva del plan de Dios?",
                "op": [
                    "Porque actua como una barrera que bloquea el acceso al diseno original de comunion, imposibilitando el desarrollo de la vida abundante.",
                    "Porque altera permanentemente la estructura genetica y los talentos naturales que el Creador deposito originalmente en el individuo.",
                    "Porque invalida y cancela de manera retroactiva los decretos eternos del amor del Omnipotente hacia Su creacion."
                ],
                "r": "Porque actua como una barrera que bloquea el acceso al diseno original de comunion, imposibilitando el desarrollo de la vida abundante."
            },
            {
                "q": "Al analizar el alcance del pecado segun Romanos 3:23, cual es su dimension correcta?",
                "op": [
                    "Es estrictamente universal, afectando la raiz de la naturaleza humana de todo individuo que entra al mundo.",
                    "Es meramente individual, aplicando de forma restrictiva y aislada solo sobre aquellos que ejecutan actos flagrantemente inmorales.",
                    "Es un fenomeno sistemico-estructural, condicionado de manera exclusiva por las fallas del entorno socioeconomico del sujeto."
                ],
                "r": "Es estrictamente universal, afectando la raiz de la naturaleza humana de todo individuo que entra al mundo."
            },
            {
                "q": "Cual es el proposito pedagogico e introductorio de la segunda verdad en la arquitectura del plan de salvacion?",
                "op": [
                    "Operar como un diagnostico espiritual critico que expone la ruina absoluta del hombre, revelando su urgente necesidad de un Salvador.",
                    "Codificar un manual etico normativo con el proposito de regular la conducta humana y evitar mecanicamente la condenacion.",
                    "Evidenciar que la raza humana carece por completo de dignidad o valor intrinseco ante los ojos del Disenador divino."
                ],
                "r": "Operar como un diagnostico espiritual critico que expone la ruina absoluta del hombre, revelando su urgente necesidad de un Salvador."
            }
        ]
    },
    {
        "nivel": 3,
        "titulo": "La Verdad del Substituto",
        "versiculos": [
            "Mas Dios muestra su amor para con nosotros, en que siendo aun pecadores, Cristo murio por nosotros. (Rom. 5:8)",
            "Jesus le dijo: Yo soy el camino, y la verdad, y la vida; nadie viene al Padre, sino por mi. (Jn. 14:6)"
        ],
        "preguntas": [
            {
                "q": "Quien es el unico substituto calificado que Dios proveyo legal y espiritualmente para redimir al hombre?",
                "op": [
                    "Jesucristo, quien en Su doble naturaleza divina y humana posee los atributos necesarios para efectuar una expiacion perfecta.",
                    "El sistema sacrificial levitico, cuyos ritos y ofrendas de sangre poseians eficacia intrinseca y permanente para quitar el pecado.",
                    "La intercesion sumaria de los arcangeles y huestes celestiales, operando como mediadores cosmicos ante el trono de Dios."
                ],
                "r": "Jesucristo, quien en Su doble naturaleza divina y humana posee los atributos necesarios para efectuar una expiacion perfecta."
            },
            {
                "q": "De que manera objetiva demostro Dios la maxima expresion de Su amor por nosotros mientras nuestra condicion era de hostilidad y rebelion activa?",
                "op": [
                    "En que siendo aun pecadores, Cristo murio por nosotros, asumiendo el veredicto judicial que nos correspondia.",
                    "Un perdon condicional y mutable, sujeto a auditorias periodicas basadas en el rendimiento moral del creyente.",
                    "La exencion soberana e inmunidad civil ante cualquier tipo de tribulacion, padecimiento fisico o crisis terrenal."
                ],
                "r": "En que siendo aun pecadores, Cristo murio por nosotros, asumiendo el veredicto judicial que nos correspondia."
            },
            {
                "q": "Que alcance y validez juridica posee el pago efectuado por Jesus en la cruz del Calvario?",
                "op": [
                    "El precio completo de nuestra salvacion, cancelando de manera absoluta la deuda y satisfaciendo plenamente la justicia de Dios.",
                    "La cobertura exclusiva de los pecados cometidos con anterioridad a la conversion, dejando el futuro a expensas de la fidelidad del creyente.",
                    "La remision unica de la culpa heredada de Adan, requiriendo que el individuo pague por sus transgresiones personales voluntarias."
                ],
                "r": "El precio completo de nuestra salvacion, cancelando de manera absoluta la deuda y satisfaciendo plenamente la justicia de Dios."
            },
            {
                "q": "Al analizar la autoproclamacion de Jesus en Juan 14:6, que exclusividad se adjudica respecto a la dimension espiritual?",
                "op": [
                    "Que El es el camino, y la verdad, y la vida; constituyendose como la unica via ontologica de acceso al Padre.",
                    "Que se erige como el ejemplo moral supremo e ideal arquetipico que el hombre debe imitar para autogenerar su salvacion.",
                    "Que representa una de las multiples avenidas o puertas validas de iluminacion dentro del amplio espectro revelatorio de la Deidad."
                ],
                "r": "Que El es el camino, y la verdad, y la vida; constituyendose como la unica via ontologica de acceso al Padre."
            },
            {
                "q": "De acuerdo con el absoluto establecido por Cristo en Juan 14:6, existe alguna via alternativa para acceder a la comunion con el Padre?",
                "op": [
                    "No, puesto que el texto dictamina categoricamente que nadie viene al Padre sino estrictamente por medio de Su persona.",
                    "Sí, siempre y cuando se sinteticen y sigan con rigurosidad las directrices eticas de los antiguos codigos profeticos de Oriente.",
                    "Sí, a traves de una ascesis mistica y una vida contemplativa que logre purificar el alma de las pasiones terrenales."
                ],
                "r": "No, puesto que el texto dictamina categoricamente que nadie viene al Padre sino estrictamente por medio de Su persona."
            },
            {
                "q": "Por que la teologia biblica de esta tercera verdad le otorga a Jesus el titulo de 'Substituto'?",
                "op": [
                    "Refleja un amor sacrificial y proactivo que entrega voluntariamente lo mas preciado con el proposito directo de salvar.",
                    "Porque reemplazo la figura temporal del sumo sacerdote de la orden de Aaron para instaurar un modelo de liderazgo puramente administrativo.",
                    "Porque actuo como un embajador politico en representacion de las autoridades terrenales ante los tribunales del cosmos."
                ],
                "r": "Refleja un amor sacrificial y proactivo que entrega voluntariamente lo mas preciado con el proposito directo de salvar."
            },
            {
                "q": "En la arquitectura sistematica de las cinco verdades, que representa formalmente la muerte de Cristo?",
                "op": [
                    "La provision y solucion legal divina al problema de la separacion y la destitucion humana causadas por el pecado.",
                    "El desenlace tragico y circunstancial de un reformador social cuya doctrina fue incomprendida por los poderes de su epoca.",
                    "Una escenificacion simbolica disenada para ilustrar de forma pedagogica la fragilidad de la condicion humana ante la historia."
                ],
                "r": "La provision y solucion legal divina al problema de la separacion y la destitucion humana causadas por el pecado."
            },
            {
                "q": "Que criterio teologico e intrinseco garantiza que el sacrificio de Jesus en la cruz posee una suficiencia absoluta?",
                "op": [
                    "El hecho de que El pago el precio completo, consumando la redencion sin necesidad de anadiduras o contribuciones humanas.",
                    "La validacion legal, el consenso y el respaldo academico otorgado por las autoridades eclesiasticas y el sanedrin de la epoca.",
                    "Que el valor de la cruz queda ratificado y activado de manera retroactiva conforme la iglesia acumula buenas obras en la historia."
                ],
                "r": "El hecho de que El pago el precio completo, consumando la redencion sin necesidad de anadiduras o contribuciones humanas."
            },
            {
                "q": "Como se articula organicamente la verdad del Substituto con la verdad del Amor explicada previamente?",
                "op": [
                    "La cruz constituye la demostracion historica e irrefutable del amor de Dios, donde Su justicia y Su misericordia se juntan.",
                    "Evidencia que el amor divino estaba condicionado y requeria de un pago punitivo para poder continuar sintiendo afecto por la creacion.",
                    "Muestra que el afecto del Creador es una variable inestable que depende directamente del sufrimiento del Justo."
                ],
                "r": "La cruz constituye la demostracion historica e irrefutable del amor de Dios, donde Su justicia y Su misericordia se juntan."
            },
            {
                "q": "Cual constituye la funcion mediadora exclusiva que ejerce Jesucristo entre la santidad del Dios trino y la condicion del hombre caido?",
                "op": [
                    "El papel de unico puente viable y eterno, quien reconcilia ambas partes eliminando la barrera de la culpabilidad.",
                    "El de un observador neutral y testigo imparcial que registra el progreso etico de las civilizaciones a lo largo de las eras.",
                    "El de un juez ejecutor inmediato cuya unica mision en Su primera venida era aplicar la sentencia punitiva sobre el cosmos."
                ],
                "r": "El papel de unico puente viable y eterno, quien reconcilia ambas partes eliminando la barrera de la culpabilidad."
            }
        ]
    },
    {
        "nivel": 4,
        "titulo": "La Verdad del Arrepentimiento",
        "versiculos": [
            "Asi que, arrepentios y convertios, para que sean borrados vuestros pecados; para que vengan de la presencia del Señor tiempos de refrigerio, (Hechos 3:19)"
        ],
        "preguntas": [
            {
                "q": "Cual es el imperativo doble dictaminado en Hechos 3:19 para que el ser humano sea admitido en el proceso de remision de faltas?",
                "op": [
                    "Arrepentirse y convertirse, demandando una transformacion interior unida a un cambio radical de direccion y lealtad espiritual.",
                    "Someterse a una confesion publica y pormenorizada de cada transgresion cometida ante un tribunal o asamblea eclesiastica.",
                    "Ejecutar un programa de restituciones materiales y compensaciones civiles equivalentes al dano provocado a terceros."
                ],
                "r": "Arrepentirse y convertirse, demandando una transformacion interior unida a un cambio radical de direccion y lealtad espiritual."
            },
            {
                "q": "What constituye el beneficio judicial inmediato que se deriva directamente del arrepentimiento genuino segun el texto apostolico?",
                "op": [
                    "Que los pecados sean completamente borrados, eliminando de forma absoluta el registro legal de culpabilidad ante Dios.",
                    "La concesion de una inmunidad sobrenatural y permanente frente a futuras tentaciones e inclinaciones de la carne.",
                    "La activacion inmediata de un estado de prosperidad material, salud biologica y exito social en el plano terrenal."
                ],
                "r": "Que los pecados sean completamente borrados, eliminando de forma absoluta el registro legal de culpabilidad ante Dios."
            },
            {
                "q": "En el marco de la conversion consecuente al arrepentimiento, como se define teologicamente este movimiento del alma?",
                "op": [
                    "Como un cambio ontologico de direccion en la vida, donde el individuo da la espalda al pecado para volverse resueltamente hacia Dios.",
                    "Como la adopcion externa de una nueva identidad institucional, afiliacion eclesiastica o asimilacion de codigos liturgicos.",
                    "Como una modificacion de la conducta publica motivada puramente por el temor psicologico al castigo o al juicio venidero."
                ],
                "r": "Como un cambio ontológico de dirección en la vida, donde el individuo da la espalda al pecado para volverse resueltamente hacia Dios."
            },
            {
                "q": "Que providencia escatologica y relacional promete Hechos 3:19 que sobrevendra tras la conversion del pecador?",
                "op": [
                    "Que vendran de la presencia del Senor tiempos de refrigerio, caracterizados por la restauracion y vitalidad espiritual otorgada por Dios.",
                    "La disolucion automatica e inmediata de cualquier conflicto interpersonal o crisis contextual en el entorno diario del sujeto.",
                    "La adjudicacion de una recompensa de honor, reputacion y preeminencia social entre los estamentos de la comunidad humana."
                ],
                "r": "Que vendran de la presencia del Senor tiempos de refrigerio, caracterizados por la restauracion y vitalidad espiritual otorgada por Dios."
            },
            {
                "q": "Desde la perspectiva de esta cuarta verdad, puede reducirse el arrepentimiento biblico a un mero sentimiento de pesadumbre o remordimiento?",
                "op": [
                    "No, puesto que el concepto trasciende la emocion e involucra una decision voluntaria y consciente de volverse activamente a Dios.",
                    "Sí, es la afliccion emocional y el desgaste psicologico (atricion) que experimenta el sujeto ante las consecuencias adversas de su error.",
                    "Sí, consiste estrictamente en el llanto sacramental y la demostracion ritualizada de dolor requerida para validar la piedad ante los hombres."
                ],
                "r": "No, puesto que el concepto trasciende la emocion e involucra una decision voluntaria y consciente de volverse activamente a Dios."
            },
            {
                "q": "¿Por qué el arrepentimiento se erige como una condición indispensable y vital en la dinámica de la salvación?",
                "op": [
                    "Porque opera como el mecanismo indispensable para abandonar la condicion de pecado y posibilitar la reconciliacion con el Creador.",
                    "Debido a que constituye un formalismo protocolar y una norma estatutaria impuesta de manera arbitraria por la ley eclesial.",
                    "Porque cumple la funcion de convencer al intelecto de sus propios errores logicos dentro del plano de la filosofia moral."
                ],
                "r": "Porque opera como el mecanismo indispensable para abandonar la condicion de pecado y posibilitar la reconciliacion con el Creador."
            },
            {
                "q": "Atendiendo a la arquitectura teologica de Hechos 3:19, cual es la fuente soberana de donde emana la remision y la paz una vez que ocurre la conversion?",
                "op": [
                    "Del Senor, siendo una prerrogativa exclusiva de la gracia divina y de la presencia activa del Todopoderoso.",
                    "Del esfuerzo interior y de la capacidad de auto-renovacion etica autogestionada por las facultades del individuo.",
                    "De la absolucion sumaria otorgada por la aceptacion y el consenso comunitario del entorno social que rodea al sujeto."
                ],
                "r": "Del Senor, siendo una prerrogativa exclusiva de la gracia divina y de la presencia activa del Todopoderoso."
            },
            {
                "q": "Que destino sufre la barrera judicial del pecado cuando el ser humano ejerce un arrepentimiento genuino?",
                "op": [
                    "Las transgresiones son erradicadas o 'borradas', invalidando de raiz el muro de separacion que privaba al hombre de la vida abundante.",
                    "Sufre un debilitamiento paulatino y gradual que depende estrictamente del transcurso cronologico del tiempo.",
                    "Queda suspendida y archivada provisionalmente en un registro cosmico a la espera de ser evaluada en el juicio final."
                ],
                "r": "Las transgresiones son erradicadas o 'borradas', invalidando de raiz el muro de separación que privaba al hombre de la vida abundante."
            },
            {
                "q": "Como debe conceptualizarse el 'refrigerio' espiritual mencionado en el texto apostolico en relacion con el creyente?",
                "op": [
                    "Como el alivio, la restauracion ontologica y la paz sobrenatural que Dios infunde en el alma al liberarla de la carga de la culpa.",
                    "Como la adquisicion de una nueva estructura cognitiva o de un conocimiento gnostico de alta complejidad teologica.",
                    "Como un arrebato emocional de caracter mistico que suspende momentaneamente las capacidades racionales del individuo."
                ],
                "r": "Como el alivio, la restauracion ontologica y la paz sobrenatural que Dios infunde en el alma al liberarla de la carga de la culpa."
            },
            {
                "q": "Es teologicamente viable que un ser humano sea participe de la salvacion prescindiendo de la experiencia del arrepentimiento?",
                "op": [
                    "No, dado que las fuentes reveladas establecen el arrepentimiento como el paso condicional indispensable para que los pecados sean borrados.",
                    "Sí, siempre y cuando la persona mantenga un asentimiento meramente intelectual respecto a los dogmas e hitos historicos de la fe.",
                    "Sí, en virtud de que el amor incondicional del Creador anula cualquier demanda de transformacion moral o cambio de direccion en el hombre."
                ],
                "r": "No, dado que las fuentes reveladas establecen el arrepentimiento como el paso condicional indispensable para que los pecados sean borrados."
            }
        ]
    },
    {
        "nivel": 5,
        "titulo": "La Verdad de la Fe",
        "versiculos": [
            "Porque la paga del pecado es muerte, mas la dadiva de Dios es vida eterna en Cristo Jesus Senor nuestro. (Rom. 6:23)",
            "Mas a todos los que le recibieron, a los que creen en su nombre, les dio potestad de ser hechos hijos de Dios (Jn. 1:12)",
            "De cierto, de cierto os digo: El que oye mi palabra, y cree al que me envio, tiene vida eterna; y no vendra a condenacion, mas ha pasado de muerte a vida. (Jn. 5:24)"
        ],
        "preguntas": [
            {
                "q": "Tomando como referencia el contraste judicial establecido en Romanos 6:23, cual es la ontologia juridica de la vida eterna en relacion con el hombre?",
                "op": [
                    "Se define formalmente como una dadiva (regalo) de Dios, operando de manera enteramente gratuita y asimetrica respecto al merito humano.",
                    "Se configura como un premio y recompensa al esfuerzo acumulativo y a la fidelidad etica mostrada por el creyente.",
                    "Constituye una herencia natural, inherente e intrinseca a la raza humana por el simple hecho de su condicion de criatura."
                ],
                "r": "Se define formalmente como una dadiva (regalo) de Dios, operando de manera enteramente gratuita y asimetrica respecto al merito humano."
            },
            {
                "q": "Bajo que termino relacional y soteriologico define el Evangelio la accion consciente de aceptar activamente a Cristo por medio de la fe?",
                "op": [
                    "Recibirlo, implicando un acto voluntario de acogida, apropiacion personal y sumision a Su soberania.",
                    "Comprenderlo teologicamente, limitando el encuentro al asentimiento intelectual y a la asimilacion del dogma eclesiastico.",
                    "Imitar de manera exactas sus obras, pretendiendo reproducir de forma autónoma Su conducta sin antes experimentar la regeneración."
                ],
                "r": "Recibirlo, implicando un acto voluntario de acogida, apropiación personal y sumisión a Su soberanía."
            },
            {
                "q": "De acuerdo con las clausulas de adopcion espiritual plasmadas en Juan 1:12, que derecho legal y estatus adquieren aquellos que creen en Su nombre?",
                "op": [
                    "La potestad (autoridad legal) de ser hechos hijos de Dios, integrandose formalmente en la familia celestial mediante el nuevo nacimiento.",
                    "La garantia inmediata de infalibilidad espiritual, inhabilitando sus almas para cometer cualquier falta en el plano terenal.",
                    "El senorio inmediato y directo sobre las estructuras politicas y las potestades de los reinos terrenales."
                ],
                "r": "La potestad (autoridad legal) de ser hechos hijos de Dios, integrandose formalmente en la familia celestial mediante el nuevo nacimiento."
            },
            {
                "q": "Cual es el triple veredicto y la garantia inmediata que Jesus asegura en Juan 5:24 a aquel que atiende a Su palabra y confia en Quien lo envio?",
                "op": [
                    "Que tiene vida eterna, no vendra a condenacion judicial, y ha efectuado el paso inmediato e irreversible de muerte a vida.",
                    "Que sera librado de forma absoluta de toda tentacion caral y de padecer cualquier tipo de afliccion biologica o existencial.",
                    "Que sus meritos eticos y aciertos morales del pasado quedan validados y homologados ante los tribunales del cielo."
                ],
                "r": "Que tiene vida eterna, no vendra a condenacion judicial, y ha efectuado el paso inmediato e irreversible de muerte a vida."
            },
            {
                "q": "En el contexto de la invitacion relacional que se expone en Apocalipsis 3:20 para concretar la salvacion, cual es el paso final que Cristo solicita?",
                "op": [
                    "Que el individuo escuche Su voz y abra de par en par la puerta de su vida, permitiendo el ingreso soberano del Creador.",
                    "Que se cumplimente de forma exhaustiva una confesión eclesiástica formal ante un ministro ordenado.",
                    "Que se ejecute un ciclo riguroso de oraciones rituales y letanias sacramentales validadas por la tradicion."
                ],
                "r": "Que el individuo escuche Su voz y abra de par en par la puerta de su vida, permitiendo el ingreso soberano del Creador."
            },
            {
                "q": "Cual es el resultado inmediato e intimo prometido por Jesus en Apocalipsis 3:20 para quien decide abrir la puerta a Su llamado?",
                "op": [
                    "Entrara a el, y cenara con el, y el conmigo; inaugurando una comunion, intimidad y mutua comunion eterna en el espiritu.",
                    "Comisionara de manera expedita una hueste o espiritu guardian encargado de custodiar los bienes materiales del hogar terrenal.",
                    "Reescribira los marcos del destino temporal del individuo, suprimiendo de su historia cualquier libre albedrio posterior."
                ],
                "r": "Entrara a el, y cenara con el, y el conmigo; inaugurando una comunion, intimidad y mutua comunion eterna en el espiritu."
            },
            {
                "q": "Al examinar la mecanica operativa de la fe salvifica planteada en esta quinta ley, cual es su verdadera naturaleza?",
                "op": [
                    "Una decision personal e integral de la voluntad que consiste en creer en la veracidad de Dios y recibir a Cristo como Senor y Salvador.",
                    "Un estado emocional transitorio y de efervescencia psicologica estimulado de forma exclusiva por el ambiente liturgico.",
                    "Una conviccion abstracta, puramente racional y especulativa que prescinde del compromiso practico de la existencia."
                ],
                "r": "Una decision personal e integral de la voluntad que consiste en creer en la veracidad de Dios y recibir a Cristo como Senor y Salvador."
            },
            {
                "q": "Atendiendo a la afirmacion explicita de Juan 5:24, que seguridad juridica e historica recibe el creyente respecto a su condicion espiritual anterior?",
                "op": [
                    "Que ha pasado de muerte a vida, sufriendo una traslacion de estado legal donde el pasado de condenacion queda cancelado ante Dios.",
                    "Que las consecuencias civiles, penales y fisicas en la Tierra quedan completamente anuladas por intervencion magica.",
                    "Que sus obras pasadas seran pesadas rigurosamente en una balanza cosmica al final de los tiempos para determinar su estatus."
                ],
                "r": "Que ha pasado de muerte a vida, sufriendo una traslacion de estado legal donde el pasado de condenacion queda cancelado ante Dios."
            },
            {
                "q": "Por que la teologia de esta quinta verdad insiste en catalogar categoricamente a la salvacion bajo la rubrica de una 'dadiva'?",
                "op": [
                    "Because representa un don inmeritado provisto por el amor de Dios, el cual solo puede ser apropiado mediante la fe en la persona de Cristo Jesus.",
                    "Debido a que constituye una oferta comercial temporal y revocable sujeta a las fluctuaciones del mercado espiritual.",
                    "Porque exige del ser humano un intercambio perfectamente simetrico de devocion y sacrificios equivalentes al valor del regalo."
                ],
                "r": "Porque representa un don inmeritado provisto por el amor de Dios, el cual solo puede ser apropiado mediante la fe en la persona de Cristo Jesus."
            },
            {
                "q": "Que implicacion ontologica y relacional conlleva el ser constituido 'hijo de Dios' a traves de la instrumentalidad de la fe segun Juan 1:12?",
                "op": [
                    "Entrar en una nueva identidad y en un vinculo de paternidad familiar inquebrantable y eterno con el Creador.",
                    "Adquirir inmunidad civil frente a los codigos legislativos y las autoridades juridicas del plano de la Tierra.",
                    "Lograr una metamorfosis metafisica hacia una condicion angelical o espectral superior a la naturaleza humana."
                ],
                "r": "Entrar en una nueva identidad y en un vinculo de paternidad familiar inquebrantable y eterno con el Creador."
            }
        ]
    }
]

preguntas = [
    {"q": "Quien era el sumo sacerdote cuando Jesus fue juzgado?", "op": ["Caifas", "Anas", "Gamaliel", "Nicodemo"], "r": "Caifas", "info": "Fue el sumo sacerdote al momento de la crucifixion."},
    {"q": "En que ciudad predico Pablo sobre el 'Dios desconocido'?", "op": ["Corinto", "Efeso", "Atenas", "Filipos"], "r": "Atenas", "info": "Pablo visito una ciudad famosa por su filosofia."},
    {"q": "Como se llamaba el esclavo que Pablo envio de regreso a Filemon?", "op": ["Onesimo", "Tiquico", "Epafrodito", "Marcos"], "r": "Onesimo", "info": "Este hombre huyo de su amo pero se encontro con Pablo."},
    {"q": "Cual es el libro que menciona a 'Cesar' por primera vez?", "op": ["Mateo", "Marcos", "Lucas", "Juan"], "r": "Lucas", "info": "Es el mismo libro que detalla el nacimiento de Jesus."},
    {"q": "Quien fue el primer martir cristiano?", "op": ["Pedro", "Esteban", "Santiago", "Felipe"], "r": "Esteban", "info": "Un hombre lleno de gracia y poder que fue apedreado."},
    {"q": "A que iglesia escribio Pablo sobre la 'armadura de Dios'?", "op": ["Corinto", "Roma", "Efeso", "Galacia"], "r": "Efeso", "info": "Esta carta aborda la lucha espiritual."},
    {"q": "Quien acompano a Pablo en su primer viaje misionero?", "op": ["Silas", "Bernabe", "Timoteo", "Lucas"], "r": "Bernabe", "info": "Conocido como el 'hijo de consolacion'."},
    {"q": "Como se llamaba la mujer que Pedro resucito en Jope?", "op": ["Lidia", "Dorcas", "Priscila", "Febe"], "r": "Dorcas", "info": "Una mujer admirada por su caridad."},
    {"q": "Que apostol escribio mas libros en el Nuevo Testamento?", "op": ["Juan", "Pedro", "Pablo", "Lucas"], "r": "Pablo", "info": "Es el autor que mas cartas escribio."},
    {"q": "En que isla naufrago Pablo?", "op": ["Patmos", "Creta", "Malta", "Chipre"], "r": "Malta", "info": "Una isla del Mediterraneo."},
    {"q": "Quien escribio el libro de Hebreos?", "op": ["Pablo", "Apolos", "Desconocido", "Bernabe"], "r": "Desconocido", "info": "Su autoria es uno de los temas mas debatidos."},
    {"q": "Que significa el nombre 'Getsemani'?", "op": ["Lugar de llanto", "Prensa de aceite", "Jardin santo", "Lugar de reposo"], "r": "Prensa de aceite", "info": "Hace referencia a la maquinaria de aceite."},
    {"q": "A que ciudad se dirigia Saulo cuando vio la luz del cielo?", "op": ["Jerico", "Damasco", "Samaria", "Antioquia"], "r": "Damasco", "info": "Saulo iba con autoridad a esta ciudad antigua."},
    {"q": "Que libro describe la nueva Jerusalen?", "op": ["Hebreos", "Santiago", "Apocalipsis", "Judas"], "r": "Apocalipsis", "info": "El libro profetico que describe el final."},
    {"q": "Quien bautizo al eunuco etiope?", "op": ["Pedro", "Felipe", "Juan", "Esteban"], "r": "Felipe", "info": "Uno de los siete diaconos."},
    {"q": "Cuantas personas fueron alimentadas con cinco panes y dos peces?", "op": ["2,000", "5,000", "7,000", "10,000"], "r": "5,000", "info": "El gran milagro de provision."},
    {"q": "Quien nego a Jesus tres veces antes de que el gallo cantara?", "op": ["Juan", "Judas", "Pedro", "Tomas"], "r": "Pedro", "info": "El discipulo que prometio lealtad absoluta."},
    {"q": "En que ciudad se llamaron por primera vez 'cristianos'?", "op": ["Jerusalen", "Antioquia", "Roma", "Corinto"], "r": "Antioquia", "info": "Ciudad donde la comunidad se hizo notoria."},
    {"q": "Que objeto se le cayo a Pablo de los ojos tras su conversion?", "op": ["Escamas", "Polvo", "Sangre", "Velo"], "r": "Escamas", "info": "Una senal fisica de que su ceguera termino."},
    {"q": "Quién era el rey que mando matar a los niños en Belén?", "op": ["César", "Herodes", "Pilato", "Agripa"], "r": "Herodes", "info": "Un gobernante celoso de su poder."},
    {"q": "En que valle fue traicionado Sanson por Dalila?", "op": ["Valle de Sorec", "Valle de Elah", "Valle de Ajalon", "Valle de Refaim"], "r": "Valle de Sorec", "info": "Dalila vivia en este valle."},
    {"q": "Como se llamaba el padre de Juan el Bautista?", "op": ["Zacarias", "Simeon", "Jose", "Elias"], "r": "Zacarias", "info": "Era sacerdote del grupo de Abias."},
    {"q": "Que nombre recibio el lugar donde Jacob sono con la escalera al cielo?", "op": ["Betel", "Hebron", "Siquem", "Beerseba"], "r": "Betel", "info": "Significa 'Casa de Dios'."},
    {"q": "Quien fue el rey que pidio sabiduria a Dios para gobernar?", "op": ["Saul", "David", "Salomon", "Roboam"], "r": "Salomon", "info": "Dios le dio sabiduria y riquezas por no pedir fama."},
    {"q": "Como se llamaba la esposa de Isaac?", "op": ["Rebeca", "Raquel", "Lea", "Bilha"], "r": "Rebeca", "info": "Fue elegida mediante una senal junto al pozo."},
    {"q": "Que profeta fue enviado a Ninive pero huyo a Tarsis?", "op": ["Amos", "Jonas", "Oseas", "Miqueas"], "r": "Jonas", "info": "Su historia nos ensena sobre la obediencia."},
    {"q": "Cual es el nombre del lugar donde Jesus multiplico los panes y peces por segunda vez?", "op": ["Galilea", "Decapolis", "Judea", "Samaria"], "r": "Decapolis", "info": "La region de las diez ciudades."},
    {"q": "Como se llamaba el oficial etiope que bautizo Felipe?", "op": ["Ebed-melec", "Cus", "Candace", "Eunuco sin nombre"], "r": "Eunuco sin nombre", "info": "La Biblia solo se refiere a el por su cargo y origen."},
    {"q": "🏠 Que montana fue el lugar donde murio Moises?", "op": ["Sinai", "Ararat", "Nebo", "Carmelo"], "r": "Nebo", "info": "Desde alli pudo ver la Tierra Prometida."},
    {"q": "Como se llamaban los dos hijos de Eli que actuaban mal en el templo?", "op": ["Ofni y Finees", "Jacob y Esau", "Pedro y Juan", "Cain y Abel"], "r": "Ofni y Finees", "info": "Su mal comportamiento trajo juicio sobre la casa de Eli."}
]

personajes = [
    {"pista": "Fui arrojado a un foso con leones por orar a mi Dios.", "op": ["Daniel", "Noe", "David", "Jose"], "r": "Daniel"},
    {"pista": "Construi un arca gigante por mandato divino antes del diluvio.", "op": ["Moises", "Noe", "Abraham", "Elias"], "r": "Noe"},
    {"pista": "Fui vendido por mis hermanos y termine siendo gobernador en Egipto.", "op": ["Jose", "Benjamin", "Juda", "Ruben"], "r": "Jose"},
    {"pista": "Lidere al pueblo de Israel fuera de la esclavitud en Egipto.", "op": ["Josue", "Moises", "Aaron", "Caleb"], "r": "Moises"},
    {"pista": "Derrote a un gigante filisteo usando solo una honda y una piedra.", "op": ["Sanson", "David", "Saul", "Gedeon"], "r": "David"},
    {"pista": "Fui el hombre mas fuerte del mundo, pero mi fuerza estaba en mi cabello.", "op": ["Sanson", "Goliat", "Joab", "Nabucodonosor"], "r": "Sanson"},
    {"pista": "Fui el primer hombre creado por Dios y vivi en el Jardin del Eden.", "op": ["Cain", "Abel", "Adan", "Set"], "r": "Adan"},
    {"pista": "Fui llamado el padre de la fe por obedecer a Dios al dejar mi tierra.", "op": ["Isaac", "Jacob", "Abraham", "Lot"], "r": "Abraham"},
    {"pista": "Fui tragado por un gran pez por intentar huir de la mision de Dios.", "op": ["Jonas", "Pedro", "Pablo", "Esteban"], "r": "Jonas"},
    {"pista": "Fui una reina que salvo a mi pueblo judio de la destruccion en Persia.", "op": ["Rut", "Ester", "Sara", "Raquel"], "r": "Ester"},
    {"pista": "Tuve muchos problemas y enfermedades, pero nunca maldije a Dios.", "op": ["Salomon", "Job", "Isaias", "Jeremias"], "r": "Job"},
    {"pista": "Fui el sucesor de Moises y guie al pueblo a conquistar Jerico.", "op": ["Caleb", "Josue", "Aaron", "Samuel"], "r": "Josue"},
    {"pista": "Conocido por mi gran sabiduria y por construir el primer Templo.", "op": ["David", "Salomon", "Roboam", "Ezequias"], "r": "Salomon"},
    {"pista": "Fui la mujer que decidio quedarse con su suegra Noemi en Belen.", "op": ["Ester", "Rut", "Debora", "Ana"], "r": "Rut"},
    {"pista": "Fui el ultimo juez de Israel y ungi a los dos primeros reyes.", "op": ["Elias", "Samuel", "Eliseo", "Natan"], "r": "Samuel"},
    {"pista": "Profetice que el Mesias naceria de una virgen siglos antes de que sucediera, y describi su sacrificio como un siervo suficiente.", "op": ["Isaias", "Amos", "Miqueas", "Joel"], "r": "Isaias"},
    {"pista": "Fui un recaudador de impuestos que dejo todo para seguir a Jesus.", "op": ["Mateo", "Marcos", "Lucas", "Juan"], "r": "Mateo"},
    {"pista": "Fui el discipulo que camino sobre las aguas hacia Jesus.", "op": ["Juan", "Pedro", "Andres", "Felipe"], "r": "Pedro"},
    {"pista": "Fui el apostol de los gentiles y escribi gran parte del Nuevo Testamento.", "op": ["Bernabe", "Pablo", "Marcos", "Tomas"], "r": "Pablo"},
    {"pista": "Prepare el camino para Jesus bautizando en el rio Jordan.", "op": ["Juan el Bautista", "Elias", "Enoc", "Jeremias"], "r": "Juan el Bautista"},
    {"pista": "Fui la madre que se alejo a la distancia de un tiro de arcopara no ver morir a su hijo, pero este lloro, y Dios escucho su voz.", "op": ["Agar", "Sara", "Lea", "Raquel"], "r": "Agar"},
    {"pista": "Fui el profeta que desafio a los 450 profetas de Baal en el Monte Carmelo.", "op": ["Eliseo", "Elias", "Isaias", "Jeremias"], "r": "Elías"},
    {"pista": "Fui el unico que permanecio fiel al rey David cuando su propio hijo Absalon intento robarle el trono.", "op": ["Joab", "Itai", "Natan", "Mefiboset"], "r": "Itai"},
    {"pista": "Fui el personaje que, siendo un niño, escuchó la voz de Dios llamándole en el templo...", "op": ["Samuel", "David", "José", "Benjamín"], "r": "Samuel"},
    {"pista": "Fui el rey que ordeno la construccion de un muro alrededor de Jerusalen en tiempo record.", "op": ["Salomon", "Ezequias", "Nehemias", "Josias"], "r": "Nehemias"},
    {"pista": "Fui la mujer que escondio a los espias de Israel en Jerico para salvar a mi familia.", "op": ["Rahab", "Rut", "Debora", "Ester"], "r": "Rahab"},
    {"pista": "Me quede mudo por no creer el mensaje del angel que me anunciaba el nacimiento de mi hijo.", "op": ["Simeon", "Zacarias", "Jose", "Nicodemo"], "r": "Zacarias"},
    {"pista": "Fui el juez que vencio a los madianitas usando solo a 300 hombres con trompetas y cantarros.", "op": ["Sanson", "Gedeon", "Barac", "Josue"], "r": "Gedeon"},
    {"pista": "Fui el apostol que tuvo dudas y necesito tocar las heridas de Jesus para creer que habia resucitado.", "op": ["Pedro", "Felipe", "Tomas", "Juan"], "r": "Tomas"},
    {"pista": "Fui el profeta que tuvo que casarse con una mujer infiel como simbolo del amor de Dios por su pueblo.", "op": ["Amos", "Oseas", "Joel", "Malaquias"], "r": "Oseas"}
]

# --- BANCO DE VERSÍCULOS RVR1960 PARA EL JUEGO DE MEMORIZAR ---
versiculos_memoria = [
    {"cita": "Juan 3:16", "texto": "Porque de tal manera amo Dios al mundo que ha dado a su Hijo unigenito para que todo aquel que en el cree no se pierda mas tenga vida eterna"},
    {"cita": "Salmos 23:1", "texto": "Jehova es mi pastor nada me faltara"},
    {"cita": "Filipenses 4:13", "texto": "Todo lo puedo en Cristo que me fortalece"},
    {"cita": "Romanos 8:28", "texto": "Y sabemos que a los que aman a Dios todas las cosas les ayudan a bien"},
    {"cita": "Proverbios 3:5", "texto": "Fiate de Jehova de todo tu corazon y no te apoyes en tu propia prudencia"},
    {"cita": "Isaias 41:10", "texto": "No temas porque yo estoy contigo no desmayes porque yo soy tu Dios que te esfuerzo siempre te ayudare siempre te sustentare con la diestra de mi justicia"},
    {"cita": "Josue 1:9", "texto": "Mira que te mando que te esfuerces y seas valiente no temas ni desmayes porque Jehova tu Dios estara contigo en dondequiera que vayas"},
    {"cita": "Salmos 119:105", "texto": "Lampara es a mis pies tu palabra y lumbrera a mi camino"},
    {"cita": "Galatas 2:20", "texto": "Con Cristo estoy juntamente crucificado y ya no vivo yo mas vive Cristo en mi"},
    {"cita": "Mateo 6:33", "texto": "Mas buscad primeramente el reino de Dios y su justicia y todas estas cosas os seran anadidas"}
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
        <a href="/verdades_init"><button style="background: #e94560; color: white;">El reto de las 5 Verdades</button></a>
        <a href="/memoriza_menu"><button style="background: #2b2d42; color: #4ecca3; border: 2px solid #4ecca3;">🧠 Memoriza el Versículo</button></a></div>
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
# --- SECCIÓN: EL RETO DE LAS 5 VERDADES (CON BARAJADO DINÁMICO FIABLE) ---
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
                    <p>"He aquí, yo estoy a la puerta y llamo; si alguno oye mi voz y abre la puerta, entreré a él, y cenaré con él, y él conmigo."</p>
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
        
        ops_barajadas = p['op'][:]
        random.shuffle(ops_barajadas)
        
        session['v_opciones_actuales'] = ops_barajadas
        
        btns = "".join([f'<a href="/verdades_res?ans_idx={i}"><button>{o}</button></a>' for i, o in enumerate(ops_barajadas)])
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
        
        ops_barajadas = p['op'][:]
        random.shuffle(ops_barajadas)
        session['v_opciones_actuales'] = ops_barajadas
        
        btns = "".join([f'<a href="/verdades_res?ans_idx={i}"><button style="background:#e94560; color:white;">{o}</button></a>' for i, o in enumerate(ops_barajadas)])
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
    
    ans_idx = int(request.args.get('ans_idx', 0))
    opciones_turno = session.get('v_opciones_actuales', [])
    
    if opciones_turno and ans_idx < len(opciones_turno):
        opcion_elegida = opciones_turno[ans_idx]
    else:
        q_fallback = session.get('v_pregunta_idx', 0) if fase == 'juego' else session.get('v_indices_erroneos', [0])[0]
        opcion_elegida = preguntas_bloque[q_fallback]['op'][0]
    
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
# --- JUEGO 4: MEMORIZA EL VERSÍCULO (INTERACTIVO RVR1960) ---
# =====================================================================

@app.route('/memoriza_menu')
def memoriza_menu():
    return render_template_string(CSS_STYLE + """
        <div class="card">
            <h2>🧠 Memoriza el Versículo</h2>
            <p>Selecciona la modalidad de juego:</p>
            <a href="/memoriza_init/dia"><button style="background: #4ecca3; color: black;">📆 Versículo del Día</button></a>
            <a href="/memoriza_init/random"><button style="background: #0f3460; color: white; border: 1px solid #4ecca3;">🎲 Versículo Random</button></a>
            <a href="/menu"><button style="background: #888; color: white;">Volver al Menú</button></a>
        </div>
    """)

@app.route('/memoriza_init/<modo>')
def memoriza_init(modo):
    if modo == 'dia':
        indice_dia = datetime.now().timetuple().tm_yday % len(versiculos_memoria)
        v_seleccionado = versiculos_memoria[indice_dia]
        session['mem_modo'] = "Versículo del Día"
    else:
        v_seleccionado = random.choice(versiculos_memoria)
        session['mem_modo'] = "Versículo Random"
        
    session['mem_cita'] = v_seleccionado['cita']
    session['mem_texto'] = v_seleccionado['texto']
    return redirect(url_for('memoriza_juego'))

@app.route('/memoriza_juego')
def memoriza_juego():
    cita = session.get('mem_cita', '')
    texto_original = session.get('mem_texto', '')
    modo = session.get('mem_modo', 'Juego')
    
    palabras_originales = texto_original.split()
    palabras_barajadas = palabras_originales[:]
    
    seed = random.randint(1, 1000)
    random.Random(seed).shuffle(palabras_barajadas)
    
    html_memoriza = """
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #1a1a2e; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
        .card { background: #16213e; padding: 25px; border-radius: 20px; width: 90%; max-width: 500px; margin: auto; box-shadow: 0 8px 16px rgba(0,0,0,0.5); }
        .area-construccion { min-height: 80px; background: #0f3460; border: 2px dashed #4ecca3; border-radius: 12px; margin: 20px 0; padding: 10px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; align-content: center; }
        .contenedor-palabras { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 20px; background: #1a1a2e; padding: 15px; border-radius: 12px; }
        .palabra-btn { padding: 10px 16px; background: #e94560; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.2s; }
        .palabra-btn.usada { opacity: 0.3; pointer-events: none; background: #555; }
        .palabra-construida { padding: 10px 16px; background: #4ecca3; color: black; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; }
        .mensaje-error { color: #e94560; font-weight: bold; margin-top: 10px; min-height: 20px; }
        .btn-accion { width: 48%; padding: 12px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; font-weight: bold; margin-top: 15px; }
    </style>
    
    <div class="card">
        <p style="color: #4ecca3; font-weight: bold; margin-bottom: 5px;">🧠 Modo: """ + modo + """</p>
        <h2 style="margin-top: 5px;">📖 """ + cita + """</h2>
        <p style="font-size: 0.9em; color: #ccc;">Haz clic en las palabras de abajo en el orden correcto para reconstruir el versículo:</p>
        
        <div class="area-construccion" id="areaConstruccion"></div>
        <div class="mensaje-error" id="mensajeError"></div>
        <div class="contenedor-palabras" id="bloqueOpciones"></div>
        
        <div style="display: flex; justify-content: space-between;">
            <button class="btn-accion" style="background: #888; color: white;" onclick="reiniciarOrden()">Borrar todo ↩️</button>
            <button class="btn-accion" style="background: #4ecca3; color: black;" id="btnVerificar" onclick="verificarResultado()" disabled>Comprobar ✔️</button>
        </div>
    </div>

    <script>
        const textoCorrecto = """ + str(palabras_originales) + """;
        const palabrasDesordenadas = """ + str(palabras_barajadas) + """;
        let respuestasUsuario = [];

        const areaConstruccion = document.getElementById('areaConstruccion');
        const bloqueOpciones = document.getElementById('bloqueOpciones');
        const mensajeError = document.getElementById('mensajeError');
        const btnVerificar = document.getElementById('btnVerificar');

        function inicializarBotones() {
            bloqueOpciones.innerHTML = '';
            palabrasDesordenadas.forEach((palabra, index) => {
                let btn = document.createElement('button');
                btn.className = 'palabra-btn';
                btn.innerText = palabra;
                btn.id = 'opcion-' + index;
                btn.onclick = () => seleccionarPalabra(palabra, index);
                bloqueOpciones.appendChild(btn);
            });
        }

        function seleccionarPalabra(palabra, index) {
            mensajeError.innerText = '';
            respuestasUsuario.push({ palabra: palabra, origIndex: index });
            document.getElementById('opcion-' + index).classList.add('usada');
            renderizarConstruccion();
            
            if (respuestasUsuario.length === textoCorrecto.length) {
                btnVerificar.disabled = false;
            }
        }

        function renderizarConstruccion() {
            areaConstruccion.innerHTML = '';
            respuestasUsuario.forEach((item, pos) => {
                let span = document.createElement('span');
                span.className = 'palabra-construida';
                span.innerText = item.palabra;
                areaConstruccion.appendChild(span);
            });
        }

        function reiniciarOrden() {
            respuestasUsuario = [];
            mensajeError.innerText = '';
            btnVerificar.disabled = true;
            areaConstruccion.innerHTML = '';
            inicializarBotones();
        }

        function verificarResultado() {
            let esCorrecto = true;
            for(let i = 0; i < textoCorrecto.length; i++) {
                if (respuestasUsuario[i].palabra !== textoCorrecto[i]) {
                    esCorrecto = false;
                    break;
                }
            }

            if (esCorrecto) {
                window.location.href = "/memoriza_ganado";
            } else {
                mensajeError.innerText = "❌ El orden no es correcto. Por favor, inténtalo de nuevo.";
            }
        }

        inicializarBotones();
    </script>
    """
    return html_memoriza

@app.route('/memoriza_ganado')
def memoriza_ganado():
    modo = session.get('mem_modo', 'Memoriza el Versículo')
    cita = session.get('mem_cita', 'Cita')
    
    HISTORIAL_CALIFICACIONES.append({
        "nombre": session.get('nombre', 'Desconocido'),
        "juego": modo,
        "calificacion": 10.0,
        "detalles": f"Memorizó con éxito {cita}",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    return render_template_string(CSS_STYLE + f"""
        <div class="card" style="border: 2px solid #4ecca3;">
            <h1 style="color: #4ecca3;">🎉 ¡EXCELENTE MEMORIA! 🎉</h1>
            <p>Has ordenado correctamente el texto de <b>{cita}</b>.</p>
            <p style="color: #ffd700; font-weight: bold;">¡Palabra guardada en el corazón!</p>
            <a href="/memoriza_menu"><button>Jugar otra vez</button></a>
            <a href="/menu"><button style="background: #888; color: white;">Ir al Menú principal</button></a>
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
