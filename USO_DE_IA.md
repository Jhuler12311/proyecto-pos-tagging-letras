Documentación de Uso de Inteligencia Artificial

Estudiante: Brayton (Jhuler12311)
Curso: Técnicas de Minería de Textos y PLN
Proyecto: Análisis Morfosintáctico de Letras Musicales con POS Tagging

Registro de Uso de Inteligencia Artificial

Este documento detalla el uso responsable de herramientas de Inteligencia Artificial durante el desarrollo del proyecto, en concordancia con las directrices de honestidad académica del curso.
La IA fue utilizada como asistente técnico, no como sustituto del trabajo del estudiante.

Herramientas utilizadas

Herramienta principal: Gemini (Google)

Uso secundario: Asistencia puntual para depuración y estructuración de código

Descripción del Uso de IA por Etapas
1. Unificación y optimización del pipeline de procesamiento

Contexto:
El proyecto contaba inicialmente con dos scripts separados:

un análisis básico con spaCy (POS tagging y métricas léxicas)

un pipeline adicional con métricas comparativas

Prompt utilizado:

“Tengo dos scripts en Python: uno con spaCy para POS tagging y métricas (densidad léxica, ratio sust/verb), y otro con NLTK para comparación. Quiero fusionarlos en un solo analyser.py que procese dataset_limpio.csv y genere dataset_master.csv. Incluye detección de idioma y manejo de errores.”

Resultado y modificaciones propias:

La IA propuso una estructura base del pipeline unificado.

Se modificaron manualmente:

rutas de archivos

nombres de columnas

lógica de décadas

integración con el dataset real del proyecto

El resultado final fue adaptado completamente a la estructura del repositorio.

2. Mejora del dashboard interactivo y creación del “ADN Gramatical”

Contexto:
El dashboard inicial solo mostraba gráficos descriptivos, sin interpretación lingüística.

Prompt utilizado:

“Tengo un dashboard Dash con filtros de género, artista y métrica. Quiero agregar un cuadro ‘ADN Gramatical’ que muestre lemas clave, adjetivos representativos y emocionalidad (valence, sadness, romantic). También quiero un filtro ‘Mis Artistas vs Corpus’.”

Resultado y modificaciones propias:

La IA sugirió la idea del cuadro ADN y la estructura del callback.

El estudiante:

ajustó los estilos visuales

tradujo y reformuló textos al español académico

agregó validaciones para casos sin datos

adaptó la lógica a las columnas reales del dataset

3. Creación de interpretación dinámica en el dashboard

Contexto:
Se buscaba que el dashboard no solo mostrara datos, sino que interpretara patrones lingüísticos.

Prompt utilizado:

“Quiero agregar texto interpretativo dinámico en Dash que cambie según género, artista y source. Ejemplo: si selecciono Hip-Hop, indicar que usa más verbos que Baladas.”

Resultado y modificaciones propias:

La IA sugirió lógica condicional básica.

El estudiante:

reformuló los textos para que fueran académicos

incorporó valores reales calculados (promedios, comparaciones)

evitó textos genéricos o fijos

4. Resolución de errores técnicos (entorno y dependencias)

Contexto:
Problemas de compatibilidad entre spaCy, NumPy y Python 3.12 en Windows.

Prompt utilizado:

“Me aparece ImportError: cannot import name randbits al usar spaCy en Windows con Python 3.12. ¿Cómo solucionarlo sin perder el proyecto?”

Resultado y aplicación:

La IA recomendó fijar NumPy en la versión 1.26.4 y recrear el entorno virtual.

El estudiante ejecutó manualmente los pasos y documentó la solución en requirements.txt.

5. Redacción de documentación (README y USO_DE_IA)

Contexto:
Se requería documentar correctamente el uso de IA en el proyecto.

Prompt utilizado:

“Ayúdame a redactar USO_DE_IA.md para un proyecto de POS tagging. Debo mencionar herramientas, prompts, reflexión y modificaciones realizadas.”

Resultado y modificaciones propias:

La IA proporcionó una estructura base.

El estudiante:

ajustó el lenguaje a un tono académico

personalizó los ejemplos

añadió reflexión crítica y honesta

Reflexión sobre el Aprendizaje

El uso de Inteligencia Artificial en este proyecto no reemplazó el aprendizaje, sino que lo potenció.
La IA permitió resolver problemas técnicos complejos (compatibilidad de librerías, estructuración de pipelines, lógica en Dash) de forma más eficiente, lo que permitió dedicar más tiempo a:

analizar resultados lingüísticos

comparar enfoques entre NLTK y spaCy

interpretar patrones por género y evolución temporal

La mayor parte del código generado por IA fue modificado, adaptado y validado manualmente, lo que fortaleció la comprensión del proyecto.
Además, se aprendió que un uso incorrecto de IA (prompts vagos o copia directa) puede generar más errores que soluciones.

Modificaciones realizadas al código sugerido por IA

Reemplazo de rutas absolutas por os.path.abspath para portabilidad

Manejo de columnas faltantes (source, lyric_clean)

Ajuste de nombres y textos al español académico

Inclusión de manejo de errores (try-except) en callbacks

Validación de datos antes de visualización

Reformulación de interpretaciones automáticas

Conclusión

La Inteligencia Artificial fue utilizada como una herramienta de apoyo, no como sustituto del trabajo académico.
El aprendizaje real se produjo al evaluar, corregir y contextualizar las sugerencias de la IA dentro de los objetivos del curso.

Un uso consciente y crítico de la IA puede mejorar significativamente la calidad y eficiencia del desarrollo, siempre que exista comprensión técnica por parte del estudiante.
Para concluir, si bien la IA es un buen asistente, se requiere un estudio previo para poder usarla como se debe.
Ya que si haces un mal pront de lo que quieres o simplemente copias y pegas pues la IA no te ayudara y generaras mas errores 
de los que puedas imaginar.
