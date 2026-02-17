# Documentación de Uso de IA
**Estudiante:** Jhuler12311

# Herramientas de IA usadas:
## Gemini
Registro de Uso de Inteligencia Artificial
Este documento detalla la colaboración con herramientas de IA para el desarrollo del proyecto de Análisis Morfosintáctico, siguiendo las directrices de honestidad académica.

1. Unificación y Optimización del Pipeline de Procesamiento
Contexto: Se contaba con un script de análisis básico (analyser.py) y un pipeline avanzado de procesamiento (pipeline.py).

Intervención de la IA: Se utilizó la IA para fusionar ambos archivos en un único motor de ejecución.

Resultado Técnico: La IA permitió integrar la eficiencia de nlp.pipe de spaCy (para procesamiento masivo) con tareas complejas de PLN como el Reconocimiento de Entidades Nombradas (NER), la Lematización y el filtrado de StopWords. Esto aseguró la generación de un archivo dataset_master.csv consistente para el dashboard.

2. Mejora del Dashboard e Interpretación de Emocionalidad
Contexto: El dashboard inicial solo presentaba frecuencias gramaticales simples.

Intervención de la IA: Se solicitó a la IA rediseñar la lógica de visualización para incluir un "Perfil Gramatical" o "ADN Musical" por artista.

Resultado Técnico: Se implementó un cuadro de hallazgos dinámico que extrae automáticamente lemas y adjetivos específicos (ej. "fiel", "ciego", "corazón") para justificar la temática emocional de las canciones. Además, se optimizaron las métricas de "Personalización" mediante el análisis temporal de pronombres para cumplir con los objetivos de evolución lingüística del proyecto.

Reflexión sobre el aprendizaje
El uso de IA en este proyecto no sustituyó el desarrollo, sino que actuó como un consultor técnico para la resolución de conflictos entre scripts y la optimización de algoritmos de etiquetado. Esto permitió centrar el esfuerzo humano en la interpretación de los hallazgos morfosintácticos y la comparación de modelos entre NLTK y spaCy.

