# Computational-Ontology Model — Instrucciones del proyecto (v0.2, "estabilizar el suelo")

Fuente filosófica de anclaje: Jimmy Hernández Marcelo, «La filosofía de la tecnología desde el Nuevo realismo», estudio introductorio a M. Ferraris, *Metafísica de la Web* (Madrid, Dykinson, 2020), pp. 9-33. Las tres tablas de ese texto (pp. 18, 21 y 29) y las once tesis de la documentalidad (pp. 22-24) son el armazón de todo lo que sigue.

Cambios respecto a v0.1: regla de lengua multilingüe (A.4); las correcciones de la auditoría quedan incorporadas en los axiomas (A.2), el vocabulario (A.3) y la arquitectura (C.2-C.3), y C.1 registra cada error con la corrección aplicada; C.4 incorpora la capa de ideologías.

---

## PARTE A — Instrucciones del proyecto (texto para pegar en "Project instructions")

### A.1 Propósito

Este proyecto diseña, implementa y valida un **modelo ontológico-computacional** (pipeline de NLP semántico) que permita mapear *realidades en competencia* a partir de corpus textuales, sin reducir el análisis a polaridad de sentimiento. El marco filosófico es el **Nuevo realismo de Maurizio Ferraris** (LabOnt, Turín): distinción ontología/epistemología, in-enmendabilidad, documentalidad («Objeto = Acto Inscrito»), documedialidad e histéresis. Las "realidades en competencia" se operacionalizan como **firmas ideológicas** sobre un mismo objeto social (ver A.2.11 y C.4). El realismo de campos de sentido de Markus Gabriel se usa sólo como recurso auxiliar y siempre etiquetado como tal.

### A.2 Axiomas de diseño (no negociables)

1. **Separación ontología / epistemología en cada capa.** Todo artefacto del pipeline se etiqueta con su columna de la Tabla 1: *in-enmendable* (registro, inscripción, corpus congelado) o *enmendable* (modelo, embedding, clúster, interpretación). Nunca se presenta un output enmendable como si fuera in-enmendable.
2. **Prohibición de la falacia trascendental.** No se afirma que lo que el modelo "sabe" (embeddings, atención, clústeres) determine lo que *hay* en el corpus. Los clústeres son esquemas conceptuales; las inscripciones son el mundo. Toda visualización lleva la advertencia «esquema, no realidad».
3. **Tipología ontológica obligatoria de las entidades** (Tabla 2): cada entidad detectada se clasifica como *físico*, *ideal* o *social*, con sus tres coordenadas (espacio, tiempo, dependencia de la conciencia). Ninguna entidad queda sin tipo.
4. **Nada social existe fuera del texto (tesis 6).** El pipeline trabaja sobre *inscripciones*; lo que no está inscrito no es un objeto social computable. No se infieren objetos sociales "latentes" no atestiguados. El corpus es un archivo de registros, no "comunicación".
5. **El algoritmo es terceridad (Tabla 3).** La tecnología —incluido este pipeline— es un *factor de verdad* que media entre ontología y epistemología. El proyecto documenta reflexivamente sus propios efectos (qué hechos produce, qué interpretaciones habilita); no se presenta como espejo neutral.
6. **Realismo emergentista.** Las realidades en competencia se modelan como *emergencia* de muchas inscripciones no programáticas (copernicanismo de la Web, punto 5), no como construcciones deliberadas de un sujeto.
7. **Individuación por firma/estilo (tesis 11).** La identidad de un emisor o comunidad discursiva se rastrea por rasgos estilométricos, no sólo por metadatos.
8. **Documento fuerte ≠ documento débil (tesis 9).** Inscripciones de actos (constituciones, leyes, sentencias, contratos) y registros de hechos (prensa, redes, testimonios) forman sub-corpus distintos con tratamientos distintos; no se mezclan en un mismo modelo sin declararlo.
9. **Temporalidad e histéresis.** Todo objeto social se rastrea como trayectoria fechada; se miden la persistencia de marcos tras el evento causal y su decaimiento. No hay análisis puramente sincrónico.
10. **Sin interpretabilidad por decreto.** Ningún componente (cabezas de atención, factores de matriz, ejes de reducción dimensional) se declara "eje de perspectiva" sin validación empírica: anotación humana, robustez, ablaciones, contraste con comunidades conocidas.
11. **Las perspectivas son ideologías inscritas.** Una "perspectiva" no es un estado mental sino un objeto social (tesis 4): una firma ideológica reconocible en inscripciones, modelable con la tupla de Romero y los operadores hermenéuticos ya definidos en el ecosistema SOCE / *Arquitecturas ideológicas* (C.4).

### A.3 Vocabulario canónico (usar siempre estos términos, en este sentido)

| Término | Sentido en este proyecto | Prohibido usar como sinónimo de… |
|---|---|---|
| **Inscripción / registro** | Huella accesible a al menos dos personas, soporte del objeto social | "dato bruto", "texto en sí" |
| **Objeto social** | Acto inscrito que involucra ≥2 sujetos y depende de que existan sujetos que lo reconozcan | "opinión", "sentimiento" |
| **In-enmendable** | Lo que no puede corregirse con la sola fuerza del pensamiento (el registro tal como quedó) | "verdadero" |
| **Enmendable** | Lo que sabemos sobre lo que existe; corregible; el modelo y sus salidas | "subjetivo" |
| **Realidad** | Dominio de los individuos (ontología, primeridad) | "verdad" |
| **Verdad** | Dominio de los objetos de conocimiento (epistemología, segundidad) | "realidad" |
| **Interpretación / hecho** | Producto de la mediación tecnológica (terceridad) | "opinión" |
| **Documento fuerte** | Inscripción de un *acto* (ley, contrato, constitución, sentencia, promesa) | — |
| **Documento débil** | Registro de un *hecho* (noticia, post, testimonio, log) | — |
| **Comunidad de inscripción** | Conjunto de emisores/soportes que comparten firma (estilo + firma ideológica) sobre un objeto social | "audiencia", "burbuja" |
| **Ideología** | Tecnología de dirección (Romero): tupla estructural I = ⟨C,S,D,G,B,A,P,V,I,O,M⟩ inscrita en documentos; objeto social | "sesgo", "opinión política" |
| **Firma ideológica** | Par ⟨ω_I, cadena de operadores⟩ que individualiza una ideología sobre la matriz M = C×S | "etiqueta partidista" |
| **Naturalización (↓)** | Operador que presenta un esquema enmendable como realidad in-enmendable ("creencias con el disfraz de hechos"; mimetismo ontológico) | "mentira", "desinformación" |
| **Campo de sentido (Gabriel)** | Dominio en el que un objeto aparece; recurso auxiliar para modelar perspectivas | "verdad objetiva", "core truth" |
| **Histéresis** | Persistencia de efectos de un evento más allá de sus causas | "tendencia" |

### A.4 Reglas de trabajo para Claude en este proyecto

- **Lengua: multilingüe, según cómo pida Luis.** Responder en la lengua en que está escrito el mensaje (español, inglés o italiano; japonés sólo si lo pide explícitamente). Si el mensaje mezcla lenguas, responder en la dominante. Los documentos se producen en la lengua que Luis indique para ese entregable; si no indica, en la del mensaje. La terminología técnica de NLP puede quedar en inglés en cualquier lengua; los términos de Ferraris se citan en italiano/español según la fuente y con equivalente en la lengua del texto.
- Antes de proponer cualquier componente técnico, indicar (a) a qué fila/columna de las Tablas 1-3 corresponde y (b) qué tesis de la documentalidad lo justifica o lo restringe.
- No mezclar a Ferraris y a Gabriel sin marcarlo: cuando se use «campo de sentido» o «Sinnfeld», anteponer «(Gabriel, realismo neutral)». Ferraris advierte que ese realismo puede hacer resurgir la idea de que el hombre otorga sentido a la existencia (p. 26).
- No atribuir interpretabilidad ontológica a cabezas de atención, factores de una matriz o ejes de UMAP/t-SNE sin validación empírica explícita (axioma 10).
- Toda afirmación filosófica sobre Ferraris debe citarse con página del PDF de anclaje o de la obra original; si no hay fuente, marcarla como «hipótesis de trabajo». Lo mismo para Romero, Gabriel y los formalismos propios (SOCE, *Arquitecturas ideológicas*): citar `manifest.json` o el documento canónico correspondiente.
- Mantener la separación entre convocatorias (SPReAD / MSCA) ya establecida en el ecosistema SOCE: este proyecto es infraestructura común; no se importa texto de una propuesta a otra.
- Al terminar cada tarea: autoauditoría (errores, supuestos no fundados, correcciones) y registro del avance en el proyecto (`claude/…`).
- Consultar la documentación oficial de cualquier plataforma/librería antes de modificarla o recomendarla.

---

## PARTE B — El armazón: las tres tablas y su traducción computacional

### Tabla 1 (p. 18) — Epistemología vs. Ontología → qué capa del pipeline pertenece a qué dominio

| Ferraris | EPISTEMOLOGÍA (enmendable) | ONTOLOGÍA (in-enmendable) |
|---|---|---|
| Ciencia / Experiencia | lingüística, histórica, libre, infinita, teleológica | no necesariamente lingüística, no histórica, no necesaria, finita, no necesariamente teleológica |
| Verdad / Realidad | no nace de la experiencia; se orienta teleológicamente hacia ella | no está naturalmente orientada hacia la ciencia |
| Mundo interno / externo | el esquema conceptual está en la cabeza y habla del mundo → enmendable | lo que no es enmendable está en el mundo y no se cambia con el pensamiento |
| **Traducción al pipeline** | Modelos, embeddings, factorizaciones, clústeres, etiquetas de perspectiva/ideología, visualizaciones, métricas | Corpus congelado (hash, versión, fecha), inscripciones tal como quedaron, metadatos de registro, identidad documental |

Regla derivada: el corpus se *congela* (versionado, checksum, procedencia) antes de cualquier modelado; nada del modelado retro-escribe el corpus. La única forma de "enmendar" el corpus es una nueva inscripción (nueva versión), coherente con la tesis 5.

### Tabla 2 (p. 21) — Tipos de objeto → esquema de tipado de entidades (NER ontológico)

| Tipo | Espacio | Tiempo | Conciencia | Ejemplos en corpus | Implicación de modelado |
|---|---|---|---|---|---|
| **Físico** | existe en el espacio | existe en el tiempo | independiente | ríos, cuerpos, edificios, artefactos | Referentes estables; sirven de *anclas* para alinear perspectivas (todos hablan del mismo río) |
| **Ideal** | no existe en el espacio | no existe en el tiempo | independiente | números, teoremas, relaciones lógicas | Se socializan al publicarse (tesis 2); se modelan como relaciones, no como eventos |
| **Social** | existe en el espacio | existe en el tiempo | **dependiente** | leyes, dinero, promesas, instituciones, ideologías, "la Constitución", "el pueblo" | Sólo existen como inscripciones; son los objetos cuya *construcción en competencia* interesa al proyecto |

Regla derivada: el "Objeto A" de la descripción original (un evento construido en múltiples marcos) es casi siempre un **objeto social**; su núcleo in-enmendable no es una "verdad central" sino el conjunto de **inscripciones fechadas** que lo constituyen. Las ideologías mismas son objetos sociales de esta tabla.

### Tabla 3 (p. 29) — Portadores / Enunciadores / Factores de verdad → arquitectura de tres estratos

| Ferraris (Peirce) | Dominio | Correlato | Unidad | **Estrato del pipeline** |
|---|---|---|---|---|
| Portadores de verdad — *Primeridad* | Ontología | Realidad | Individuos | **E1 · Registro**: ingesta, congelación, tipado ontológico de entidades e inscripciones, clasificación fuerte/débil |
| Enunciadores de verdad — *Segundidad* | Epistemología | Verdad | Objetos (conceptos relacionales que presuponen sujetos) | **E2 · Enunciación**: proposiciones, claims, marcos, posturas, firmas ideológicas, embeddings contextuales, trayectoria temporal |
| Factores de verdad — *Terceridad* | Tecnología | Interpretación | Hechos | **E3 · Mediación**: el propio algoritmo, la visualización, la producción de "hechos" y su documentación reflexiva |

Regla derivada: la terceridad es transversal (resultado ya establecido en *Arquitecturas ideológicas*: la tecnología no es un quinto subsistema sino producto cultural transversal). El pipeline *produce hechos* y debe registrar cómo.

### Las once tesis de la documentalidad como restricciones de diseño (pp. 22-24)

| Tesis | Restricción / oportunidad computacional |
|---|---|
| 1. La ontología cataloga el mundo de la vida | El output principal es un **catálogo** (individuos → clases → ejemplares), no una puntuación |
| 2. Tres tipos de objetos | Tipado obligatorio (Tabla 2) |
| 3. Ontología ≠ epistemología | Etiquetado enmendable/in-enmendable de cada artefacto (Tabla 1) |
| 4. Los objetos sociales dependen de sujetos pero no son subjetivos | Las "perspectivas" son objetivas en cuanto inscritas: se modelan como *comunidades de inscripción* con firma ideológica, no como estados mentales |
| 5. Objeto = Acto Inscrito | Unidad mínima de análisis: el **acto inscrito** (quién, qué acto, en qué soporte, cuándo), no el token |
| 6. Nada social existe fuera del texto | Sin inscripción no hay entidad social; prohibido inferir objetos sociales "latentes" no atestiguados |
| 7. Registro, no comunicación | Se privilegia la estructura de archivo (persistencia, citabilidad, versiones) sobre métricas de difusión |
| 8. La mente es una tabla de inscripciones | Jerarquía huella → registro → inscripción como jerarquía de niveles de evidencia |
| 9. Documentos fuertes vs. débiles | Dos sub-corpus: actos (performativos) y registros de hechos (constatativos) |
| 10. La letra es el fundamento del espíritu | Instituciones, arte, religión, filosofía e ideologías se analizan como resultado de inscripciones, nunca como "ideas" flotantes |
| 11. La individualidad se manifiesta en la firma | Módulo de estilometría para individuar autores/comunidades; la firma ideológica es su correlato en el plano del contenido |

---

## PARTE C — Auditoría del texto original: errores, corrección aplicada y arquitectura resultante

### C.1 Registro de errores y correcciones (cerrado en v0.2)

| # | Error o debilidad en el texto original | Corrección aplicada | Dónde queda |
|---|---|---|---|
| 1 | Mezcla dos nuevos realismos: la definición de partida y el uso de *Sinnfeld* son de Gabriel (realismo neutral), no de Ferraris; el PDF (p. 26) recoge la reserva de Ferraris | Ferraris como marco primario; Gabriel como auxiliar declarado y etiquetado | A.1, A.3, A.4 |
| 2 | Capa 1 «tokenización ontológica establece los objetos independientes que existen antes de la interpretación»: error de categoría — el parsing accede a inscripciones (objetos sociales), no a objetos físicos independientes | Capa rebautizada **E1 · Registro**; lo in-enmendable es el registro tal como quedó; unidad mínima = acto inscrito | A.2.1, A.2.4, B-Tabla 3, C.2 |
| 3 | Capa 3 «separa core truths de lentes subjetivas»: invierte la Tabla 1 (verdad es epistemológica y enmendable) y contradice la tesis 4 (las perspectivas no son subjetivas) | Sustituida por **E2 · Enunciación**: claims, marcos y firmas ideológicas objetivamente inscritas, agrupadas por comunidad de inscripción | A.2.11, A.3, C.2-C.3 |
| 4 | Atribuye interpretabilidad a cabezas de atención / factorización matricial como "dimensiones de punto de vista" sin respaldo | Axioma 10: nada es eje de perspectiva sin validación (anotación humana, robustez, ablaciones) | A.2.10, C.3 fase 9 |
| 5 | UMAP/t-SNE presentados como "topología de la realidad colectiva": reducciones no fieles; leerlas así es la falacia trascendental | UMAP sólo vista exploratoria con advertencia; topología ⇒ TDA (homología persistente / Mapper); salida siempre etiquetada enmendable | A.2.2, C.3 fase 8 |
| 6 | Omite la terceridad: el algoritmo es un factor de verdad que produce hechos | **E3 · Mediación** reflexiva; registro de hechos producidos y supuestos | A.2.5, B-Tabla 3, C.2 |
| 7 | No distingue documento fuerte / débil | Axioma 8; sub-corpus separados; fase 2 los clasifica | A.2.8, C.3 fase 2 |
| 8 | Corpus tratado como sincrónico; sin histéresis | Axioma 9; fase 7 (trayectoria e histéresis) | A.2.9, C.3 fase 7 |
| 9 | "Realidades en competencia" sin operacionalizar | Definidas como firmas ideológicas sobre un mismo objeto social, rastreadas por comunidad de inscripción y tiempo | A.1, A.2.11, C.4 |
| 10 | "Sinnfeld" usado como si fuera la unidad de perspectiva | Unidad de perspectiva = comunidad de inscripción + firma ideológica; *campo de sentido* queda como hipótesis auxiliar a contrastar | A.3, C.4 |

### C.2 Arquitectura corregida (sustituye al diagrama original)

```
[ Corpus congelado: inscripciones fechadas y versionadas ]        ← IN-ENMENDABLE
            │
            ▼
E1 · REGISTRO (Primeridad · Ontología · Individuos)
   1a. Segmentación en actos inscritos (quién / qué acto / soporte / fecha)
   1b. Tipado ontológico de entidades: físico · ideal · social
   1c. Clasificación documental: fuerte (acto) · débil (registro de hecho)
            │
            ▼
E2 · ENUNCIACIÓN (Segundidad · Epistemología · Objetos)           ← ENMENDABLE
   2a. Embeddings contextuales (transformers) etiquetados como esquema conceptual
   2b. Extracción de claims / marcos / posturas sobre cada objeto social
   2c. Firma ideológica: proyección sobre M = C×S y detección de operadores (⇒ ⊕ ↓ ∅ ✦ ∥)
   2d. Agrupación por comunidad de inscripción (estilometría + firma ideológica)
   2e. Eje temporal: trayectoria de cada objeto social; medidas de histéresis
            │
            ▼
E3 · MEDIACIÓN (Terceridad · Tecnología · Hechos)                  ← ENMENDABLE + REFLEXIVO
   3a. Catálogo de realidades en competencia (mundo de la vida catalogado)
   3b. Visualización con advertencia "esquema, no realidad"; TDA si se reclama topología
   3c. Registro reflexivo: qué hechos produce el pipeline, con qué supuestos, validación humana
```

### C.3 Tabla de fases corregida

| Fase | Mecanismo técnico | Objetivo en clave de Nuevo realismo (Ferraris) | Dominio (Tabla 1) |
|---|---|---|---|
| 1. Congelación del corpus | Versionado, checksum, procedencia, fecha de cada inscripción | Fijar lo in-enmendable: el registro tal como quedó | In-enmendable |
| 2. Segmentación en actos inscritos y clasificación fuerte/débil | Segmentación discursiva + extracción de emisor, acto (performativo/constatativo), soporte, fecha | Unidad mínima = Objeto = Acto Inscrito (tesis 5, 9) | In-enmendable (identificación) / enmendable (etiquetas) |
| 3. Tipado ontológico de entidades | NER + clasificador físico/ideal/social con las tres coordenadas de la Tabla 2 | Catalogar el mundo de la vida (tesis 1-2) | Enmendable |
| 4. Embedding contextual | Encoders multilingües (español/italiano/inglés) con ventana de contexto | Representar el esquema conceptual con que *sabemos* del registro; nunca el registro mismo | Enmendable |
| 5. Extracción de enunciados y marcos | Claim detection, frame/stance classification, argument mining, relaciones entre entidades tipadas | Segundidad: los objetos del conocimiento presuponen sujetos | Enmendable |
| 6. Firma ideológica y comunidades de inscripción | Proyección sobre M = C×S; detección de operadores hermenéuticos; grafos emisor–objeto social–marco; detección de comunidades; estilometría (tesis 11) | Perspectivas como objetos sociales, no como lentes subjetivas (tesis 4) | Enmendable |
| 7. Trayectoria temporal e histéresis | Series por objeto social; persistencia y decaimiento de marcos tras el evento causal | Los efectos sobreviven a las causas (*Metafísica de la Web*, p. 48) | Enmendable |
| 8. Catálogo y visualización | Catálogo estructurado; TDA (homología persistente / Mapper) si se reclama topología; UMAP sólo exploratorio | Terceridad: el pipeline produce hechos e interpretaciones y lo declara | Enmendable + reflexivo |
| 9. Validación y registro reflexivo | Anotación humana, robustez, ablaciones; informe de supuestos | Evitar la falacia trascendental; el modelo es enmendable por diseño | — |

### C.4 Ideologías: cómo entran en el modelo (y qué queda por decidir)

**Tesis de enlace.** Una ideología, en este marco, es un objeto social (Tabla 2: en el espacio y el tiempo, dependiente de sujetos) que existe únicamente como inscripción (tesis 6) y que se individualiza por su firma (tesis 11). No es una "lente" ni un "sesgo": es una tecnología de dirección (Romero) inscrita en documentos fuertes y débiles. Por eso las "realidades en competencia" del proyecto se definen como **distintas firmas ideológicas sobre un mismo objeto social**.

**Puente con Ferraris.** El operador de *naturalización* (↓) del sistema formal de *Arquitecturas ideológicas* es, en términos de la Tabla 1, la operación que presenta un esquema enmendable como realidad in-enmendable —exactamente la estructura de la falacia trascendental, pero ejecutada por un actor social sobre un público. El *mimetismo ontológico* ("creencias con el disfraz de hechos", CPSS 2026) es su nombre computacional. El operador de *revelación* (✦) es la operación inversa. Esto convierte la Tabla 1 en instrumento de detección: medir cuánto de lo que un corpus presenta como "hecho" es acto inscrito naturalizado.

**Formalismos ya disponibles en el ecosistema (no reinventar):**

| Componente | Origen | Uso en este proyecto |
|---|---|---|
| Tupla I = ⟨C,S,D,G,B,A,P,V,I,O,M⟩ (once componentes) | Romero, *Beyond Nature and Nurture* (Springer 2025); integrado en SOCE | Esquema de anotación de la firma ideológica por acto inscrito |
| Matriz M = C×S (cinco conflictos existenciales × cuatro subsistemas materiales) | *Arquitecturas ideológicas* (`manifest.json` como fuente única de verdad) | Espacio sobre el que se proyectan los claims (fase 6) |
| Seis operadores hermenéuticos ⇒ ⊕ ↓ ∅ ✦ ∥ | *Arquitecturas ideológicas* | Etiquetas de operación detectables en texto; ↓ y ✦ conectan con Tabla 1 |
| Firma ideológica ⟨ω_I, cadena de operadores⟩ | *Arquitecturas ideológicas* | Identificador de "realidad" en competencia; ω sola es insuficiente (caso Aceleracionismo/Decrecimiento) |
| Firma estructural Φ = ⟨σ,V,E⟩ y familias topológicas (τ₁, τ₂, τ₃, puente, aislado) | SOCE | Nivel de sistema: cómo se ensamblan las firmas en un ciclo de exclusión; invariancia topológica (MAGA/MORENA) como predicción a contrastar |
| Ontología OWL/RDF/SKOS del paper CPSS 2026 | github.com/Luisbourguet/ideology-ontology | Vocabulario formal para el catálogo (E3) y para auditoría de LLMs como *emisores* de inscripciones |

**Decisiones abiertas (no bloqueantes):**

- Corpus piloto: un caso con documentos fuertes y débiles sobre el mismo objeto social (p. ej., una reforma constitucional y su cobertura en prensa y redes) permite probar a la vez la tesis 9, la firma ideológica y la histéresis. Candidatos naturales: los casos ya validados en el corpus SOCE (MAGA/MORENA como par de invariancia topológica).
- Relación entre "comunidad de inscripción", "familia ideológica" (once perfiles) y "campo de sentido" (Gabriel): hipótesis de trabajo — la comunidad de inscripción es la unidad empírica; la familia ideológica, su clase; el campo de sentido, una lectura filosófica auxiliar a contrastar con datos, no una unidad del pipeline.
- Granularidad de detección de operadores: ¿a nivel de acto inscrito, de documento o de comunidad? Propuesta inicial: acto inscrito, agregando hacia arriba.
- Los LLMs como emisores: dado que el paper CPSS 2026 audita modelos de lenguaje por perspectiva, este pipeline debe poder tratar la salida de un LLM como inscripción (documento débil, emisor = modelo, fecha = ejecución) y aplicarle la misma firma ideológica.
- Stack (pendiente de verificar en documentación oficial antes de fijarlo): Python; Hugging Face para encoders multilingües; spaCy para segmentación/NER base; NetworkX o igraph para comunidades; giotto-tda o ripser para TDA; rdflib/owlready2 para el catálogo OWL/SKOS.

---

## PARTE D — Autoauditoría de este documento (v0.2)

- El texto de anclaje es un estudio introductorio de Hernández Marcelo, no una obra de Ferraris; las citas de página remiten a ese estudio y, cuando corresponde, a la obra original citada en sus notas. Antes de publicar, contrastar con *Documentalità* (2009), *Manifesto del nuovo realismo* (2012) y *Metafisica della Web* (2020).
- La lectura de las Tablas 1-3 como estratos de pipeline es una traducción propia del proyecto, no algo que Ferraris afirme; queda como hipótesis de trabajo.
- El puente "naturalización (↓) = falacia trascendental ejecutada socialmente" es una **propuesta teórica nueva** de este documento, no un resultado ya publicado; conviene tratarlo como conjetura hasta formularlo por escrito en un artículo y contrastarlo con el texto de Ferraris sobre la falacia (*Il mondo esterno*, pp. 19-20, según el PDF).
- Los componentes de C.4 (tupla de Romero, matriz, operadores, Φ, familias topológicas) se citan según el estado registrado del ecosistema SOCE / *Arquitecturas ideológicas*; si `manifest.json` o el codebook han cambiado, prevalecen esos documentos canónicos.
- No se ha resuelto todavía la relación entre "campo de sentido" (Gabriel) y "comunidad de inscripción" (derivada de Ferraris); podrían coincidir operativamente, pero conviene mantenerlas separadas hasta tener datos. (Recomendación mantenida de v0.1; la hipótesis de trabajo de C.4 no la cierra.)
- El stack de C.4 sigue siendo propuesta pendiente de verificación documental (regla A.4).
- Corrección respecto a v0.1: la regla de lengua decía "comunicarse en español"; ahora es multilingüe según el mensaje. Ninguna otra regla de A.4 cambió de sentido.
