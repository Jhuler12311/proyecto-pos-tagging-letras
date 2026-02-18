# Documentación de Uso de Inteligencia Artificial
**Estudiante:** Jhuler12311  
**Herramienta principal:** Gemini (Google)

## Registro de Uso de Inteligencia Artificial

Este documento detalla la colaboración con herramientas de IA para el desarrollo del proyecto "Análisis Morfosintáctico de Letras Musicales", siguiendo las directrices de honestidad académica del curso.

### Herramientas utilizadas y tareas específicas

1. **Unificación y optimización del pipeline de procesamiento**  
   **Contexto:** Tenía dos scripts separados (analyser.py básico y pipeline avanzado).  
   **Prompt usado:**  
   "Tengo dos scripts en Python: uno con spaCy para POS tagging y métricas (densidad léxica, ratio sust/verb), y otro con NLTK para comparación. Quiero fusionarlos en un solo analyser.py que procese todo el dataset_limpio.csv y genere dataset_master.csv con columnas adicionales como 'source' para distinguir mis artistas. Incluye detección de idioma y manejo de errores."  
   **Resultado:** La IA generó la estructura base del pipeline unificado. Modifiqué rutas, agregué columnas 'source' y 'lyric_clean', y ajusté el manejo de décadas.

2. **Mejora del dashboard interactivo y ADN gramatical**  
   **Contexto:** El dashboard inicial solo mostraba gráficos básicos sin interpretación.  
   **Prompt usado:**  
   "Tengo un dashboard Dash con filtros de género, artista y métrica. Quiero agregar un cuadro 'ADN Gramatical' que muestre lemas clave, adjetivos representativos y emocionalidad (valence, sadness, romantic) del artista seleccionado. También quiero un filtro 'Mis Artistas vs Corpus' usando columna 'source'."  
   **Resultado:** La IA propuso el layout del ADN box y el callback dinámico. Ajusté estilos, agregué robustez para casos vacíos y cambié títulos a español.

3. **Creación de sección de interpretación dinámica**  
   **Contexto:** Quería que el dashboard no solo muestre gráficos, sino que interprete patrones (ej. verbos por género).  
   **Prompt usado:**  
   "En mi dashboard Dash quiero agregar un div con texto interpretativo que cambie según los filtros (género, artista, source). Ejemplo: si selecciono Hip-Hop, diga que tiene más verbos que Baladas. El texto debe ser dinámico según los datos filtrados."  
   **Resultado:** La IA sugirió lógica condicional con if/elif. Modifiqué los textos para que sean más académicos y agregué valores dinámicos (e.g., promedio real de verbos).

4. **Corrección de errores de venv y dependencias**  
   **Contexto:** Tenía errores constantes de NumPy (randbits) y spaCy no cargaba.  
   **Prompt usado:**  
   "Me sale ImportError: cannot import name randbits al importar spaCy en Windows con Python 3.12. ¿Cómo arreglo el venv sin perder mi proyecto?"  
   **Resultado:** La IA recomendó bajar NumPy a 1.26.4 y recrear venv. Lo implementé manualmente en PyCharm.

5. **Estructuración de USO_DE_IA.md**  
   **Contexto:** Necesitaba redactar este documento.  
   **Prompt usado:**  
   "Ayúdame a redactar USO_DE_IA.md para mi proyecto de POS tagging. Debo mencionar herramientas, prompts, reflexión y modificaciones hechas al código generado por IA."  
   **Resultado:** La IA dio estructura base. Modifiqué ejemplos de prompts, agregué reflexión personal y ajusté lenguaje a académico.

### Reflexión sobre el aprendizaje

El uso de IA en este proyecto no sustituyó mi trabajo, sino que actuó como un asistente técnico avanzado. Me permitió resolver problemas complejos (compatibilidad NumPy, fusión de scripts, lógica dinámica en Dash) en mucho menos tiempo, lo que me dejó espacio para enfocarme en lo más importante: interpretar los patrones morfosintácticos, comparar NLTK vs spaCy y redactar conclusiones académicas. Aprendí que la IA es una herramienta poderosa cuando se combina con comprensión humana (modifiqué casi todo el código generado para adaptarlo a mis rutas, columnas y objetivos). También entendí mejor las limitaciones técnicas (e.g., bugs de dependencias en Windows) y cómo depurarlas. En resumen, la IA aceleró el desarrollo, pero el aprendizaje real vino de validar, ajustar y contextualizar sus sugerencias.

### Modificaciones realizadas al código generado por IA

- Cambié rutas absolutas por os.path.abspath para portabilidad.
- Agregué manejo de columnas faltantes (e.g., 'source', 'lyric_clean').
- Ajusté títulos y etiquetas a español para consistencia.
- Incluí try-except en callbacks del dashboard para evitar crashes.
- Modifiqué textos interpretativos para que sean académicos y no genéricos.
- Vi que el uso de la IA puede ser beneficiosa si se usa bien.

Con esto, el documento es completo, honesto y cumple con los requisitos de la rúbrica (uso documentado, reflexión, ejemplos de prompts, modificaciones).