from flask import Flask, request, render_template_string, redirect, url_for, session, Response
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_daniel'

# --- MEMORIA VOLÁTIL PARA LAS MÉTRICAS DE LA IGLESIA ---
HISTORIAL_CALIFICACIONES = []

# --- BANCO DE DATOS: DIFICULTAD REFORMULADA Y COMPLEJA (10 preguntas por bloque) ---
verdades_data = [
    {
        "nivel": 1,
        "titulo": "La Verdad del Amor",
        "versiculos": [
            "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna. (Jn. 3:16)",
            "... yo he venido para que tengan vida, y para que la tengan en abundancia. (Jn. 10:10b)"
        ],
        "preguntas": [
            {
                "q": "¿Cuál es el propósito central e inicial de Dios para la existencia del ser humano según la primera verdad?",
                "op": [
                    "Que el hombre experimente una vida abundante, definida por la comunión plena con el Creador y el desarrollo de Su diseño eterno.",
                    "La exigencia de una perfección moral absoluta e impecabilidad intrínseca previa a cualquier manifestation de Su favor.",
                    "Demandas un sacrificio perpetuo de privación existencial como único mecanismo para aplacar la distancia con la Deidad."
                ],
                "r": "Que el hombre experimente una vida abundante, definida por la comunión plena con el Creador y el desarrollo de Su diseño eterno."
            },
            {
                "q": "¿Qué motivó de forma primaria a Dios a entregar voluntariamente a Su Hijo unigénito según la declaración de Juan 3:16?",
                "op": [
                    "Su inmenso e incondicional amor por el mundo, manifestado en una acción proactiva de rescate y preservación espiritual.",
                    "La necesidad urgente de apaciguar Su ira santa mediante un acto reactivo de justicia punitiva ajeno a la compasión.",
                    "El cumplimiento formal y exclusivo de las cláusulas legales estipuladas de manera restrictiva en el pacto abrahámico."
                ],
                "r": "Su inmenso e incondicional amor por el mundo, manifestado en una acción proactiva de rescate y preservación espiritual."
            },
            {
                "q": "¿Cuál es el don o regalo escatológico que Dios garantiza de manera inmediata a aquellos que ejercen fe en Su Hijo?",
                "op": [
                    "La vida eterna, caracterizada por la cualidad y permanencia de una comunión ininterrumpida con el Dios vivo.",
                    "Un perdón condicional y mutable, sujeto a auditorías periódicas basadas en el rendimiento moral del creyente.",
                    "La exención soberana e inmunidad civil ante cualquier tipo de tribulación, padecimiento físico o crisis terrenal."
                ],
                "r": "La vida eterna, caracterizada por la cualidad y permanencia de una comunión ininterrumpida con el Dios vivo."
            },
            {
                "q": "De acuerdo con la declaración explícita de Jesús en Juan 10:10b, ¿cuál es el objetivo preciso de Su encarnación y venida al mundo?",
                "op": [
                    "Para que tengan vida, y para que la tengan en abundancia, definiendo el propósito en los términos textuales declarados por el Redentor.",
                    "Para que alcancen una vida plenamente autorrealizada en abundancia, modificando la centralidad de la vida dada por Cristo hacia la autogestión.",
                    "Para que posean vida y paz en abundancia, añadiendo conceptos conceptualmente válidos pero ajenos a la precisión exacta de la cita bíblica."
                ],
                "r": "Para que tengan vida, y para que la tengan en abundancia, definiendo el propósito en los términos textuales declarados por el Redentor."
            },
            {
                "q": "¿Cómo se describe la naturaleza operativa del amor de Dios en el marco de esta primera verdad?",
                "op": [
                    "Como un amor sacrificial y proactivo que entrega voluntariamente lo más preciado con el propósito directo de salvar.",
                    "Como una disposición afectiva pasiva que otorga misericordia únicamente motivada por la piedad o lástima ante la miseria humana.",
                    "Como un sistema asistencial de recompensas y privilegios cósmicos destinado de forma exclusiva a los ya declarados justos en la Tierra."
                ],
                "r": "Como un amor sacrificial y proactivo que entrega voluntariamente lo más preciado con el propósito directo de salvar."
            },
            {
                "q": "¿Qué significa poseer una 'vida abundante' en el estricto contexto espiritual y relacional de esta verdad?",
                "op": [
                    "Vivir en plenitud, experimentando de forma integral la comunión, el gozo y la alineación directa con el propósito soberano de Dios.",
                    "Gozar de una garantía de prosperidad financiera, acumulación material y estatus socioeconómico elevado mediante decretos de fe.",
                    "Alcanzar un estado metafísico de iluminación mental superior que permite trascender las limitaciones de la realidad física."
                ],
                "r": "Vivir en plenitud, experimentando de forma integral la comunión, el gozo y la alineación directa con el propósito soberano de Dios."
            },
            {
                "q": "¿Cuál es el alcance del amor divino y la oferta de redención explicitada en el texto de Juan 3:16?",
                "op": [
                    "Incluye de manera universal a todo el mundo, rompiendo barreras étnicas, temporales o de mérito previo para el acceso a la gracia.",
                    "Se limita restrictivamente a los patriarcas, profetas y guardianes históricos de los oráculos sagrados.",
                    "Aplica única y selectivamente sobre aquellos individuos que logran guardar de antemano la totalidad de los mandamientos."
                ],
                "r": "Incluye de manera universal a todo el mundo, rompiendo barreras étnicas, temporales o de mérito previo para el acceso a la gracia."
            },
            {
                "q": "Respecto a la adquisición de la vida eterna, ¿cuál es la dinámica teológica correcta según se desprende de esta ley del amor?",
                "op": [
                    "Se recibe gratuitamente como el resultado directo del plan soberano y amoroso de Dios, operando bajo el principio de la gracia.",
                    "Se gana de manera meritoria como retribución justa por el volumen acumulado de obras de piedad, filantropía y sacrificios personales.",
                    "Se adquiere mediante un proceso iniciático basado en el conocimiento intelectual de misterios sagrados e información esotérica."
                ],
                "r": "Se recibe gratuitamente como el resultado directo del plan soberano y amoroso de Dios, operando bajo el principio de la gracia."
            },
            {
                "q": "¿Qué condición de vulnerabilidad eterna asegura de forma categórica Juan 3:16 que NO padecerá el individuo que deposita su confianza en Cristo?",
                "op": [
                    "Que no se perderá, garantizando la preservación judicial del creyente frente a la ruina y la condenación del alma.",
                    "Que no experimentará la muerte física ni los efectos biológicos del envejecimiento en el plano terrenal.",
                    "Que quedará completamente inhabilitado para volver a cometer cualquier error o falta moral de manera absoluta."
                ],
                "r": "Que no se perderá, guaranteeing la preservación judicial del creyente frente a la ruina y la condenación del alma."
            },
            {
                "q": "¿Cuál constituye el cimiento y la base inamovible de toda la relación entre Dios y el hombre propuesto en esta primera verdad?",
                "op": [
                    "El amor incondicional y la iniciativa del Creador, quien define el vínculo desde Su propia esencia y carácter santo.",
                    "El temor reverente y la sumisión psicológica del ser humano ante la disparidad de poder con el Absoluto.",
                    "El pacto bilateral basado en el cumplimiento riguroso y milimétrico de estatutos, ordenanzas y códigos litúrgicos."
                ],
                "r": "El amor incondicional y la iniciativa del Creador, quien define el vínculo desde Su propia esencia y carácter santo."
            }
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
            {
                "q": "¿Qué es lo que impide al hombre experimentar el amor de Dios?",
                "op": [
                    "El pecado en sí mismo, operando como una condición activa de transgresión que interrumpe la comunión vital con el Creador.",
                    "La falta de un conocimiento intelectual o de una conciencia moral desarrollada respecto a las leyes divinas.",
                    "La condición ontológica de ser una criatura finita, limitada y propensa a debilidades naturales e involuntarias."
                ],
                "r": "El pecado en sí mismo, operando como una condición activa de transgresión que interrumpe la comunión vital con el Creador."
            },
            {
                "q": "¿Cuántas personas han pecado según el axioma teológico de Romanos 3:23?",
                "op": [
                    "La totalidad de la raza humana sin excepción alguna, estableciendo una condición de culpabilidad universal.",
                    "Aquellos individuos que, teniendo pleno uso de razón, rechazan deliberadamente los mandatos expresos de la ley.",
                    "La humanidad en general, exceptuando a quienes han sido predestinados o adoptados soberanamente como hijos de Dios."
                ],
                "r": "La totalidad de la raza humana sin excepción alguna, estableciendo una condición de culpabilidad universal."
            },
            {
                "q": "¿Cuál es el estado del pecador respecto a la gloria de Dios según la declaración paulina?",
                "op": [
                    "Está destituido de ella, implicando una carencia absoluta del estándar santo requerido para la comunión.",
                    "Se encuentra bajo un estado de suspensión y observación jurídica, a la espera de una evaluación final de sus obras.",
                    "Permanece en una posición de distanciamiento geográfico o cósmico que se resuelve mediante la iluminación intelectual."
                ],
                "r": "Está destituido de ella, implicando una carencia absoluta del estándar santo requerido para la comunión."
            },
            {
                "q": "¿Cuál es la consecuencia espiritual y legal que establece Romanos 6:23a como retribución del pecado?",
                "op": [
                    "La muerte, entendida como la paga judicial y el salario irreversible que el pecado devenga por su propia naturaleza.",
                    "Un estado crónico de alienación psicológica manifestado a través de la ansiedad existencial y la angustia mental.",
                    "Una degradación moral progresiva que debilita temporalmente la posición del hombre dentro del orden de la creación."
                ],
                "r": "La muerte, entendida como la paga judicial y el salario irreversible que el pecado devenga por su propia naturaleza."
            },
            {
                "q": "¿Por qué el pecado produce intrínsecamente una separación entre Dios y el hombre?",
                "op": [
                    "Porque la santidad de Dios y la naturaleza del pecado son mutuamente excluyentes, levantando una barrera espiritual infranqueable para el ser humano.",
                    "Porque la soberanía divina decide replegarse y apartarse ante la escasez de adoradores calificados en la Tierra.",
                    "Porque debilita las facultades del libre albedrío de tal manera que el hombre olvida de forma natural el camino de regreso a su Creador."
                ],
                "r": "Porque la santidad de Dios y la naturaleza del pecado son mutuamente excluyentes, levantando una barrera espiritual infranqueable para el ser humano."
            },
            {
                "q": "¿Posee el ser humano la capacidad inherente para cruzar por su cuenta el abismo generado por el pecado?",
                "op": [
                    "No, puesto que el pecado establece una condición de total incapacidad espiritual que anula cualquier esfuerzo autónomo de reconciliación.",
                    "Sí, siempre y cuando aplique un sistema riguroso de compensación moral mediante obras de justicia y caridad que equilibren su balanza ante Dios.",
                    "Sí, a través de una metanoia puramente racional combinada con disciplinas místicas y ejercicios de meditación profunda."
                ],
                "r": "No, puesto que el pecado establece una condición de total incapacidad espiritual que anula cualquier esfuerzo autónomo de reconciliación."
            },
            {
                "q": "¿Qué naturaleza define a la 'muerte' dictaminada en la segunda verdad?",
                "op": [
                    "Una muerte espiritual y judicial que se traduce en la separación total, absoluta y eterna de la fuente de la vida.",
                    "Un estado de letargo espiritual transitorio y reversible que se suspende automáticamente con cualquier acto de remordimiento humano.",
                    "La extinción ontológica definitiva de la conciencia, provocando que el individuo cese de existir por completo en el cosmos."
                ],
                "r": "Una muerte espiritual y judicial que se traduce en la separación total, absoluta y eterna de la fuente de la vida."
            },
            {
                "q": "¿Por qué se afirma categóricamente que el pecado nos priva del plan de Dios?",
                "op": [
                    "Porque actúa como una barrera que bloquea el acceso al diseño original de comunión, imposibilitando el desarrollo de la vida abundante.",
                    "Porque altera permanentemente la estructura genética y los talentos naturales que el Creador depositó originalmente en el individuo.",
                    "Porque invalida y cancela de manera retroactiva los decretos eternos del amor del Omnipotente hacia Su creación."
                ],
                "r": "Porque actúa como una barrera que bloquea el acceso al diseño original de comunión, imposibilitando el desarrollo de la vida abundante."
            },
            {
                "q": "Al analizar el alcance del pecado según Romanos 3:23, ¿cuál es su dimensión correcta?",
                "op": [
                    "Es strictly universal, afectando la raíz de la naturaleza humana de todo individuo que entra al mundo.",
                    "Es meramente individual, aplicando de forma restrictiva y aislada solo sobre aquellos que ejecutan actos flagrantemente inmorales.",
                    "Es un fenómeno sistémico-estructural, condicionado de manera exclusiva por las fallas del entorno socioeconómico del sujeto."
                ],
                "r": "Es estrictamente universal, afectando la raíz de la naturaleza humana de todo individuo que entra al mundo."
            },
            {
                "q": "¿Cuál es el propósito pedagógico e introductorio de la segunda verdad en la arquitectura del plan de salvación?",
                "op": [
                    "Operar como un diagnóstico espiritual crítico que expone la ruina absoluta del hombre, revelando su urgente necesidad de un Salvador.",
                    "Codificar un manual ético normativo con el propósito de regular la conducta humana y evitar mecánicamente la condenación.",
                    "Evidenciar que la raza humana carece por completo de dignidad o valor intrínseco ante los ojos del Diseñador divino."
                ],
                "r": "Operar como un diagnóstico espiritual crítico que expone la ruina absoluta del hombre, revelando su urgente necesidad de un Salvador."
            }
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
            {
                "q": "¿Quién es el único substituto calificado que Dios proveyó legal y espiritualmente para redimir al hombre?",
                "op": [
                    "Jesucristo, quien en Su doble naturaleza divina y humana posee los atributos necesarios para efectuar una expiación perfecta.",
                    "El sistema sacrificial levítico, cuyos ritos y ofrendas de sangre poseían eficacia intrínseca y permanente para quitar el pecado.",
                    "La intercesión sumaria de los arcángeles y huestes celestiales, operando como mediadores cósmicos ante el trono de Dios."
                ],
                "r": "Jesucristo, quien en Su doble naturaleza divina y humana posee los atributos necesarios para efectuar una expiación perfecta."
            },
            {
                "q": "¿De qué manera objetiva demostró Dios la máxima expresión de Su amor por nosotros mientras nuestra condición era de hostilidad y rebelión activa?",
                "op": [
                    "En que siendo aún pecadores, Cristo murió por nosotros, asumiendo el veredicto judicial que nos correspondía.",
                    "Suspendiendo temporalmente las demandas de Su justicia santísima mediante la manifestación de señales portentosas en el templo.",
                    "Otorgando una amnistía incondicional a la humanidad a través de decretos y proclamas de emisarios celestiales."
                ],
                "r": "En que siendo aún pecadores, Cristo murió por nosotros, asumiendo el veredicto judicial que nos correspondía."
            },
            {
                "q": "¿Qué alcance y validez jurídica posee el pago efectuado por Jesús en la cruz del Calvario?",
                "op": [
                    "El precio completo de nuestra salvación, cancelando de manera absoluta la deuda y satisfaciendo plenamente la justicia de Dios.",
                    "La cobertura exclusiva de los pecados cometidos con anterioridad a la conversión, dejando el futuro a expensas de la fidelidad del creyente.",
                    "La remisión única de la culpa heredada de Adán, requiriendo que el individuo pague por sus transgresiones personales voluntarias."
                ],
                "r": "El precio completo de nuestra salvación, cancelando de manera absoluta la deuda y satisfaciendo plenamente la justicia de Dios."
            },
            {
                "q": "Al analizar la autoproclamación de Jesús en Juan 14:6, ¿qué exclusividad se adjudica respecto a la dimensión espiritual?",
                "op": [
                    "Que Él es el camino, y la verdad, y la vida; constituyéndose como la única vía ontológica de acceso al Padre.",
                    "Que se erige como el ejemplo moral supremo e ideal arquetípico que el hombre debe imitar para autogenerar su salvación.",
                    "Que representa una de las múltiples avenidas o puertas válidas de iluminación dentro del amplio espectro revelatorio de la Deidad."
                ],
                "r": "Que Él es el camino, y la verdad, y la vida; constituyéndose como la única vía ontológica de acceso al Padre."
            },
            {
                "q": "De acuerdo con el absoluto establecido por Cristo en Juan 14:6, ¿existe alguna vía alternativa para acceder a la comunión con el Padre?",
                "op": [
                    "No, puesto que el texto dictamina categóricamente que nadie viene al Padre sino estrictamente por medio de Su persona.",
                    "Sí, siempre y cuando se sinteticen y sigan con rigurosidad las directrices éticas de los antiguos códigos proféticos de Oriente.",
                    "Sí, a través de una ascesis mística y una vida contemplativa que logre purificar el alma de las pasiones terrenales."
                ],
                "r": "No, puesto que el texto dictamina categóricamente que nadie viene al Padre sino estrictamente por medio de Su persona."
            },
            {
                "q": "¿Por qué la teología bíblica de esta tercera verdad le otorga a Jesús el título de 'Substituto'?",
                "op": [
                    "Porque tomó de forma vicaria el lugar del pecador en la cruz, absorbiendo la ira divina y pagando la deuda de muerte que la ley exigía.",
                    "Porque reemplazó la figura temporal del sumo sacerdote de la orden de Aarón para instaurar un modelo de liderazgo puramente administrativo.",
                    "Porque actuó como un embajador político en representación de las autoridades terrenales ante los tribunales del cosmos."
                ],
                "r": "Porque tomó de forma vicaria el lugar del pecador en la cruz, absorbiendo la ira divina y pagando la deuda de muerte que la ley exigía."
            },
            {
                "q": "En la arquitectura sistemática de las cinco verdades, ¿qué representa formalmente la muerte de Cristo?",
                "op": [
                    "La provisión y solución legal divina al problema de la separación y la destitución humana causadas por el pecado.",
                    "El desenlace trágico y circunstancial de un reformador social cuya doctrina fue incomprendida por los poderes de su época.",
                    "Una escenificación simbólica diseñada para ilustrar de forma pedagógica la fragilidad de la condición humana ante la historia."
                ],
                "r": "La provisión y solución legal divina al problema de la separación y la destitución humana causadas por el pecado."
            },
            {
                "q": "¿Qué criterio teológico e intrínseco garantiza que el sacrificio de Jesús en la cruz posee una suficiencia absoluta?",
                "op": [
                    "El hecho de que Él pagó el precio completo, consumando la redención sin necesidad de añadiduras o contribuciones humanas.",
                    "La validación legal, el consenso y el respaldo académico otorgado por las autoridades eclesiásticas y el sanedrín de la época.",
                    "Que el valor de la cruz queda ratificado y activado de manera retroactiva conforme la iglesia acumula buenas obras en la historia."
                ],
                "r": "El hecho de que Él pagó el precio completo, consumando la redención sin necesidad de añadiduras o contribuciones humanas."
            },
            {
                "q": "¿Cómo se articula orgánicamente la verdad del Substituto con la verdad del Amor explicada previamente?",
                "op": [
                    "La cruz constituye la demostración histórica e irrefutable del amor de Dios, donde Su justicia y Su misericordia se juntan.",
                    "Evidencia que el amor divino estaba condicionado y requería de un pago punitivo para poder continuar sintiendo afecto por la creación.",
                    "Muestra que el afecto del Creador es una variable inestable que depende directamente del sufrimiento del Justo."
                ],
                "r": "La cruz constituye la demostración histórica e irrefutable del amor de Dios, donde Su justicia y Su misericordia se juntan."
            },
            {
                "q": "¿Cuál es la función mediadora exclusiva que ejerce Jesucristo entre la santidad del Dios trino y la condición del hombre caído?",
                "op": [
                    "El papel de único puente viable y eterno, quien reconcilia ambas partes eliminando la barrera de la culpabilidad.",
                    "El de un observador neutral y testigo imparcial que registra el progreso ético de las civilizaciones a lo largo de las eras.",
                    "El de un juez ejecutor inmediato cuya única misión en Su primera venida era aplicar la sentencia punitiva sobre el cosmos."
                ],
                "r": "El papel de único puente viable y eterno, quien reconcilia ambas partes eliminando la barrera de la culpabilidad."
            }
        ]
    },
    {
        "nivel": 4,
        "titulo": "La Verdad del Arrepentimiento",
        "versiculos": [
            "Así que, arrepentíos y convertíos, para que sean borrados vuestros pecados; para que vengan de la presencia del Señor tiempos de refrigerio, (Hechos 3:19)"
        ],
        "preguntas": [
            {
                "q": "¿Cuál es el imperativo doble dictaminado en Hechos 3:19 para que el ser humano sea admitido en el proceso de remisión de faltas?",
                "op": [
                    "Arrepentirse y convertirse, demandando una transformación interior unida a un cambio radical de dirección y lealtad espiritual.",
                    "Someterse a una confesión pública y pormenorizada de cada transgresión cometida ante un tribunal o asamblea eclesiástica.",
                    "Ejecutar un programa de restituciones materiales y compensaciones civiles equivalentes al daño provocado a terceros."
                ],
                "r": "Arrepentirse y convertirse, demandando una transformación interior unida a un cambio radical de dirección y lealtad espiritual."
            },
            {
                "q": "What constituye el beneficio judicial inmediato que se deriva directamente del arrepentimiento genuino según el texto apostólico?",
                "op": [
                    "Que los pecados sean completamente borrados, eliminando de forma absoluta el registro legal de culpabilidad ante Dios.",
                    "La concesión de una inmunidad sobrenatural y permanente frente a futuras tentaciones e inclinaciones de la carne.",
                    "La activación inmediata de un estado de prosperidad material, salud biológica y éxito social en el plano terrenal."
                ],
                "r": "Que los pecados sean completamente borrados, eliminando de forma absoluta el registro legal de culpabilidad ante Dios."
            },
            {
                "q": "En el marco de la conversión consecuente al arrepentimiento, ¿cómo se define teológicamente este movimiento del alma?",
                "op": [
                    "Como un cambio ontológico de dirección en la vida, donde el individuo da la espalda al pecado para volverse resueltamente hacia Dios.",
                    "Como la adopción externa de una nueva identidad institucional, afiliación eclesiástica o asimilación de códigos litúrgicos.",
                    "Como una modificación de la conducta pública motivada puramente por el temor psicológico al castigo o al juicio venidero."
                ],
                "r": "Como un cambio ontológico de dirección en la vida, donde el individuo da la espalda al pecado para volverse resueltamente hacia Dios."
            },
            {
                "q": "¿Qué providencia escatológica y relacional promete Hechos 3:19 que sobrevendrá tras la conversión del pecador?",
                "op": [
                    "Que vendrán de la presencia del Señor tiempos de refrigerio, caracterizados por la restauración y vitalidad espiritual otorgada por Dios.",
                    "La disolución automática e inmediata de cualquier conflicto interpersonal o crisis contextual en el entorno diario del sujeto.",
                    "La adjudicación de una recompensa de honor, reputación y preeminencia social entre los estamentos de la comunidad humana."
                ],
                "r": "Que vendrán de la presencia del Señor tiempos de refrigerio, caracterizados por la restauración y vitalidad espiritual otorgada por Dios."
            },
            {
                "q": "Desde la perspectiva de esta cuarta verdad, ¿puede reducirse el arrepentimiento bíblico a un mero sentimiento de pesadumbre o remordimiento?",
                "op": [
                    "No, puesto que el concepto trasciende la emoción e involucra una decisión voluntaria y consciente de volverse activamente a Dios.",
                    "Sí, es la aflicción emocional y el desgaste psicológico (atrición) que experimenta el sujeto ante las consecuencias adversas de su error.",
                    "Sí, consiste estrictamente en el llanto sacramental y la demostración ritualizada de dolor requerida para validar la piedad ante los hombres."
                ],
                "r": "No, puesto que el concepto trasciende la emoción e involucra una decisión voluntaria y consciente de volverse activamente a Dios."
            },
            {
                "q": "¿Por qué el arrepentimiento se erige como una condición indispensable y vital en la dinámica de la salvación?",
                "op": [
                    "Porque opera como el mecanismo indispensable para abandonar la condición de pecado y posibilitar la reconciliación con el Creador.",
                    "Debido a que constituye un formalismo protocolar y una norma estatutaria impuesta de manera arbitraria por la ley eclesial.",
                    "Porque cumple la función de convencer al intelecto de sus propios errores lógicos dentro del plano de la filosofía moral."
                ],
                "r": "Porque opera como el mecanismo indispensable para abandonar la condición de pecado y posibilitar la reconciliación con el Creador."
            },
            {
                "q": "Atendiendo a la arquitectura teológica de Hechos 3:19, ¿cuál es la fuente soberana de donde emana la remisión y la paz una vez que ocurre la conversión?",
                "op": [
                    "Del Señor, siendo una prerrogativa exclusiva de la gracia divina y de la presencia activa del Todopoderoso.",
                    "Del esfuerzo interior y de la capacidad de auto-renovación ética autogestionada por las facultades del individuo.",
                    "De la absolución sumaria otorgada por la aceptación y el consenso comunitario del entorno social que rodea al sujeto."
                ],
                "r": "Del Señor, siendo una prerrogativa exclusiva de la gracia divina y de la presencia activa del Todopoderoso."
            },
            {
                "q": "¿Qué destino sufre la barrera judicial del pecado cuando el ser humano ejerce un arrepentimiento genuino?",
                "op": [
                    "Las transgresiones son erradicadas o 'borradas', invalidando de raíz el muro de separación que privaba al hombre de la vida abundante.",
                    "Sufre un debilitamiento paulatino y gradual que depende estrictamente del transcurso cronológico del tiempo.",
                    "Queda suspendida y archivada provisionalmente en un registro cósmico a la espera de ser evaluada en el juicio final."
                ],
                "r": "Las transgresiones son erradicadas o 'borradas', invalidando de raíz el muro de separación que privaba al hombre de la vida abundante."
            },
            {
                "q": "¿Cómo debe conceptualizarse el 'refrigerio' espiritual mencionado en el texto apostólico en relación con el creyente?",
                "op": [
                    "Como el alivio, la restauración ontológica y la paz sobrenatural que Dios infunde en el alma al liberarla de la carga de la culpa.",
                    "Como la adquisición de una nueva estructura cognitiva o de un conocimiento gnóstico de alta complejidad teológica.",
                    "Como un arrebato emocional de carácter místico que suspende momentáneamente las capacidades racionales del individuo."
                ],
                "r": "Como el alivio, la restauración ontológica y la paz sobrenatural que Dios infunde en el alma al liberarla de la carga de la culpa."
            },
            {
                "q": "¿Es teológicamente viable que un ser humano sea partícipe de la salvación prescindiendo de la experiencia del arrepentimiento?",
                "op": [
                    "No, dado que las fuentes reveladas establecen el arrepentimiento como el paso condicional indispensable para que los pecados sean borrados.",
                    "Sí, siempre y cuando la persona mantenga un asentimiento meramente intelectual respecto a los dogmas e hitos históricos de la fe.",
                    "Sí, en virtud de que el amor incondicional del Creador anula cualquier demanda de transformación moral o cambio de dirección en el hombre."
                ],
                "r": "No, dado que las fuentes reveladas establecen el arrepentimiento como el paso condicional indispensable para que los pecados sean borrados."
            }
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
            {
                "q": "Tomando como referencia el contraste judicial establecido en Romanos 6:23, ¿cuál es la ontología jurídica de la vida eterna en relación con el hombre?",
                "op": [
                    "Se define formalmente como una dádiva (regalo) de Dios, operando de manera enteramente gratuita y asimétrica respecto al mérito humano.",
                    "Se configura como un premio y recompensa al esfuerzo acumulativo y a la fidelidad ética mostrada por el creyente.",
                    "Constituye una herencia natural, inherente e intrínseca a la raza humana por el simple hecho de su condición de criatura."
                ],
                "r": "Se define formalmente como una dádiva (regalo) de Dios, operando de manera enteramente gratuita y asimétrica respecto al mérito humano."
            },
            {
                "q": "¿Bajo qué término relacional y soteriológico define el Evangelio la acción consciente de aceptar activamente a Cristo por medio de la fe?",
                "op": [
                    "Recibirlo, implicando un acto voluntario de acogida, apropiación personal y sumisión a Su soberanía.",
                    "Comprenderlo teológicamente, limitando el encuentro al asentimiento intelectual y a la asimilación del dogma eclesiástico.",
                    "Imitar de manera exacta sus obras, pretendiendo reproducir de forma autónoma Su conducta sin antes experimentar la regeneración."
                ],
                "r": "Recibirlo, implicando un acto voluntario de acogida, apropiación personal y sumisión a Su soberanía."
            },
            {
                "q": "De acuerdo con las cláusulas de adopción espiritual plasmadas en Juan 1:12, ¿qué derecho legal y estatus adquieren aquellos que creen en Su nombre?",
                "op": [
                    "La potestad (autoridad legal) de ser hechos hijos de Dios, integrándose formalmente en la familia celestial mediante el nuevo nacimiento.",
                    "La garantía inmediata de infalibilidad espiritual, inhabilitando sus almas para cometer cualquier falta en el plano terrenal.",
                    "El señorío inmediato y directo sobre las estructuras políticas y las potestades de los reinos terrenales."
                ],
                "r": "La potestad (autoridad legal) de ser hechos hijos de Dios, integrándose formalmente en la familia celestial mediante el nuevo nacimiento."
            },
            {
                "q": "¿Cuál es el triple veredicto y la garantía inmediata que Jesús asegura en Juan 5:24 a aquel que atiende a Su palabra y confía en Quien lo envió?",
                "op": [
                    "Que tiene vida eterna, no vendrá a condenación judicial, y ha efectuado el paso inmediato e irreversible de muerte a vida.",
                    "Que será librado de forma absoluta de toda tentación carnal y de padecer cualquier tipo de aflicción biológica o existencial.",
                    "Que sus méritos éticos y aciertos morales del pasado quedan validados y homologados ante los tribunales del cielo."
                ],
                "r": "Que tiene vida eterna, no vendrá a condenación judicial, y ha efectuado el paso inmediato e irreversible de muerte a vida."
            },
            {
                "q": "En el contexto de la invitación relacional que se expone en Apocalipsis 3:20 para concretar la salvación, ¿cuál es el paso final que Cristo solicita?",
                "op": [
                    "Que el individuo escuche Su voz y abra de par en par la puerta de su vida, permitiendo el ingreso soberano del Creador.",
                    "Que se cumplimente de forma exhaustiva una confesión eclesiástica formal ante un ministro ordenado.",
                    "Que se ejecute un ciclo riguroso de oraciones rituales y letanías sacramentales validadas por la tradición."
                ],
                "r": "Que el individuo escuche Su voz y abra de par en par la puerta de su vida, permitiendo el ingreso soberano del Creador."
            },
            {
                "q": "¿Cuál es el resultado inmediato e íntimo prometido por Jesús en Apocalipsis 3:20 para quien decide abrir la puerta a Su llamado?",
                "op": [
                    "Entrará a él, y cenará con él, y él conmigo; inaugurando una comunión, intimidad y mutua comunión eterna en el espíritu.",
                    "Comisionará de manera expedita una hueste o espíritu guardián encargado de custodiar los bienes materiales del hogar terrenal.",
                    "Reescribirá los marcos del destino temporal del individuo, suprimiendo de su historia cualquier libre albedrío posterior."
                ],
                "r": "Entrará a él, y cenará con él, y él conmigo; inaugurando una comunión, intimidad y mutua comunión eterna en el espíritu."
            },
            {
                "q": "Al examinar la mecánica operativa de la fe salvífica planteada en esta quinta ley, ¿cuál es su verdadera naturaleza?",
                "op": [
                    "Una decisión personal e integral de la voluntad que consiste en creer en la veracidad de Dios y recibir a Cristo como Señor y Salvador.",
                    "Un estado emocional transitorio y de efervescencia psicológica estimulado de forma exclusiva por el ambiente litúrgico.",
                    "Una convicción abstracta, puramente racional y especulativa que prescinde del compromiso práctico de la existencia."
                ],
                "r": "Una decisión personal e integral de la voluntad que consiste en creer en la veracidad de Dios y recibir a Cristo como Señor y Salvador."
            },
            {
                "q": "Atendiendo a la afirmación explícita de Juan 5:24, ¿qué seguridad jurídica e histórica recibe el creyente respecto a su condición espiritual anterior?",
                "op": [
                    "Que ha pasado de muerte a vida, sufriendo una traslación de estado legal donde el pasado de condenación queda cancelado ante Dios.",
                    "Que las consecuencias civiles, penales y físicas en la Tierra quedan completamente anuladas por intervención mágica.",
                    "Que sus obras pasadas serán pesadas rigurosamente en una balanza cósmica al final de los tiempos para determinar su estatus."
                ],
                "r": "Que ha pasado de muerte a vida, sufriendo una traslación de estado legal donde el pasado de condenación queda cancelado ante Dios."
            },
            {
                "q": "¿Por qué la teología de esta quinta verdad insiste en catalogar categóricamente a la salvación bajo la rúbrica de una 'dádiva'?",
                "op": [
                    "Porque representa un don inmeritado provisto por el amor de Dios, el cual solo puede ser apropiado mediante la fe en la persona de Cristo Jesús.",
                    "Debido a que constituye una oferta comercial temporal y revocable sujeta a las fluctuaciones del mercado espiritual.",
                    "Porque exige del ser humano un intercambio perfectamente simétrico de devoción y sacrificios equivalentes al valor del regalo."
                ],
                "r": "Porque representa un don inmeritado provisto por el amor de Dios, el cual solo puede ser apropiado mediante la fe en la persona de Cristo Jesús."
            },
            {
                "q": "¿Qué implicación ontológica y relacional conlleva el ser constituido 'hijo de Dios' a través de la instrumentalidad de la fe según Juan 1:12?",
                "op": [
                    "Entrar en una nueva identidad y en un vínculo de paternidad familiar inquebrantable y eterno con el Creador.",
                    "Adquirir inmunidad civil frente a los códigos legislativos y las autoridades jurídicas del plano de la Tierra.",
                    "Lograr una metamorfosis metafísica hacia una condición angelical o espectral superior a la naturaleza humana."
                ],
                "r": "Entrar en una nueva identidad y en un vínculo de paternidad familiar inquebrantable y eterno con el Creador."
            }
        ]
    }
]

preguntas = [
    {"q": "¿Quién era el sumo sacerdote cuando Jesús fue juzgado?", "op": ["Caifás", "Anás", "Gamaliel", "Nicodemo"], "r": "Caifás", "info": "Fue el sumo sacerdote al momento de la crucifixión."},
    {"q": "En qué ciudad predicó Pablo sobre el 'Dios desconocido'?", "op": ["Corinto", "Éfeso", "Atenas", "Filipos"], "r": "Atenas", "info": "Pablo visitó una ciudad famosa por su filosofía."},
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
    {"pista": "Fui la madre que se alejo a la distancia de un tiro de arcopara no ver morir a su hijo, pero este lloró, y Dios escuchó su voz.", "op": ["Agar", "Sara", "Lea", "Raquel"], "r": "Agar"},
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
# --- SECCIÓN: EL RETO DE LAS 5 VERDADES (CON NUEVO BARAJAO DINÁMICO) ---
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
        
        # Mezclamos las opciones dinámicamente en este momento preciso
        ops_barajadas = p['op'][:]
        random.shuffle(ops_barajadas)
        
        # Guardamos en sesión el orden temporal para interpretarlo en /verdades_res
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
            <a href="/menu"><button style="background: #88 snowy-888;">Volver al Menú</button></a>
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
