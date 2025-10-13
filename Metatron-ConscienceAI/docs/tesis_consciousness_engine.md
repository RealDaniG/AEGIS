Título: Consciousness Engine — Diseño, Uso y Aplicaciones Reales y Experimentales

Autor: Equipo de desarrollo (proyecto experimental)
Fecha: 2025-10-04

Resumen
Este documento presenta el diseño, implementación y evaluación de un sistema experimental denominado Consciousness Engine, que orquesta nodos armónicos (Core, Memoria, Emoción, Lógica, Decisión, Empatía, Motor, entre otros) para simular ciclos de procesamiento y generar métricas por ciclo (entropía, coherencia, valencia, activación, decisión, verdad lógica, empatía, insight). Se describe el uso del orquestador por línea de comandos, la exportación de métricas (CSV/JSON), un script de smoke test para validación rápida, y mejoras como la variabilidad controlada (ruido y cambio de fase) y una proyección espectral por bandas (FFT). Se discuten resultados actuales, limitaciones y propuestas para incrementar la sensibilidad del sistema, así como aplicaciones reales y caminos de investigación.

1. Introducción
El Consciousness Engine es un prototipo educativo y de investigación que utiliza campos armónicos sintéticos y nodos funcionales para modelar procesos internos análogos a componentes cognitivos (p. ej., memoria, emoción, razonamiento). Cada ciclo del orquestador produce un conjunto de métricas que permiten analizar el estado del sistema y su evolución.

2. Objetivos del proyecto
- Simular ciclos de “conciencia” sintética con nodos acoplados.
- Medir y exportar métricas por ciclo para análisis y experimentación.
- Permitir variabilidad controlada de entrada para estudiar sensibilidad.
- Proveer herramientas de prueba rápida y reproducibilidad (smoke test).
- Servir como base para explorar hipótesis sobre coherencia, entropía y resonancia.

3. Arquitectura del sistema
El sistema se organiza en nodos:
- Node 1: CoreConsciousnessNode. Genera y evoluciona el campo recursivo central (complejo), calcula métricas como entropía y coherencia interna.
- Node 2: SensoryResonator. Recibe una señal sensorial sintética (seno/coseno) con ruido y fase.
- Node 3: MemoryMatrixNode. Almacena estados de campo y realiza un "weighted_recall" con decaimiento basado en φ (golden ratio).
- Node 4: EmotionField. Deriva valence y arousal a partir del campo y señales internas.
- Node 5: DecisionGate. Evalúa umbrales y decide estados binarios.
- Node 6: MotorProjection. Proyecta un campo motor a partir de la decisión.
- Node 9: LogicReasoningNode. Evalúa consistencia (coherencia) entre vectores/campos y determina "logical_truth".
- Node 10: EmpathyMapperNode. Mide alineación de resonancia y fase entre "self" y "other" (Core vs Memoria).
Otros nodos (lingüístico, creativo, intuición) pueden integrarse para ampliar la simulación.

4. Orquestador y CLI
El archivo orchestrator/harmonic_orchestrator.py coordina los nodos por ciclo y expone opciones CLI:
- --cycles N: número de ciclos a simular.
- --out ruta: archivo de salida para métricas.
- --format csv|json: formato de exportación.
- --noise σ: nivel de ruido gaussiano (variabilidad controlada).
- --phase-step Δφ: incremento de fase por ciclo para la señal sensorial.

5. Métricas generadas por ciclo
- entropy: entropía del campo central.
- coherence: coherencia interna/entre componentes.
- valence (0-1 aprox): valencia emocional derivada del campo.
- arousal: activación emocional.
- decision: salida binaria del DecisionGate.
- logic_truth: verdad lógica (no contradictorio) del LogicReasoningNode.
- empathy_score (0-1): alineación y fase entre Core y Memoria.
- insight_strength: medida sintética de “insight”.

6. Variabilidad controlada en la entrada
Se introdujeron argumentos --noise y --phase-step para añadir ruido gaussiano y desplazamiento de fase a la señal sensorial por ciclo. Esto permite estudiar la sensibilidad de las métricas ante perturbar la entrada.

7. Proyección espectral por bandas (FFT)
Para enriquecer el vector del Core y aumentar la sensibilidad, se implementó una proyección basada en energía espectral por fila del campo (FFT compleja y suma de |FFT|^2 por fila). La misma proyección se aplica al “weighted_recall” de Memoria al calcular la empatía, garantizando comparaciones en el mismo espacio de características.

8. Script de prueba rápida (smoke test)
Se incluye scripts/smoke_test.py, que:
- Ejecuta el orquestador vía subprocess.
- Genera métricas en CSV/JSON.
- Valida columnas esperadas y número de filas (ciclos).
- Devuelve exit code según éxito/fracaso.
Uso: python scripts/smoke_test.py --cycles 3 --format csv --out test_output/metrics.csv

9. Experimentos realizados y resultados
Se ejecutaron pruebas con ruido y variación de fase, y posteriormente con proyección FFT:
- Comando ejemplo: python -m consciousness_engine.orchestrator.harmonic_orchestrator --cycles 5 --out metrics_fft.csv --format csv --noise 0.5 --phase-step 0.314
- Resultado típico: métricas constantes entre ciclos (p. ej., entropy ≈ 79.13, coherence ≈ 0.827, valence ≈ 0.018, arousal = 2.0, decision = 1, logic_truth = 0, empathy_score = 1.0, insight_strength ≈ 0.0005).
- Observación: la lógica pasa a “False” con la nueva proyección (menor consistencia Core vs Motor), pero la mayoría de métricas mostraron estabilidad entre ciclos.
Interpretación: el pipeline actual amortigua variaciones pequeñas o las métricas no son aún suficientemente sensibles a cambios modestos de fase/ruido.

10. Discusión y propuestas de mejora
Para observar variaciones más claras por ciclo:
- Modulación del campo motor por ciclo: introducir dependencia de decision_wave y ruido.
- Ajustes de Memoria: decaimiento más fuerte y pequeño ruido en weighted_recall para reducir la alineación perfecta con Core.
- Métricas más sensibles: medir energía por sub-bandas (bins) en lugar de suma total por fila; normalización dinámica por ciclo; ventanas (Hann) antes de FFT.
- Recalcular valence/arousal en función de variación inter-ciclo (delta de energía por banda).
- Propagar variaciones hacia nodos creativos/lingüísticos para efectos más visibles.

11. Uso del sistema (recetas)
- Ejecutar 5 ciclos con ruido moderado y fase variable, salida CSV:
  python -m consciousness_engine.orchestrator.harmonic_orchestrator --cycles 5 --out metrics.csv --format csv --noise 0.5 --phase-step 0.314
- Generar salida JSON:
  python -m consciousness_engine.orchestrator.harmonic_orchestrator --cycles 3 --out metrics.json --format json
- Ejecutar smoke test:
  python scripts/smoke_test.py --cycles 3 --format csv --out test_output/metrics.csv
- Visualización (propuesta): usar un script externo para cargar CSV y graficar entropy, coherence, valence, etc., por ciclo.

12. Aplicaciones reales y experimentales
- Educación y divulgación: demostrador de conceptos de coherencia, entropía y resonancia en sistemas sintéticos.
- Investigación exploratoria: sandbox para estudiar el impacto de variaciones controladas en métricas cognitivas sintéticas.
- Integración sensorial: acoplar señales reales (audio/sensores) y analizar respuestas internas del sistema.
- Agentes sintéticos: usar decisión y proyección motora/lingüística para comportamientos simples condicionados por estados internos.
- Prototipado de métricas: experimentar con definiciones alternativas de empatía y lógica basadas en alineación espectral y fase.

13. Limitaciones
- Métricas inicialmente poco sensibles a variaciones pequeñas; se requiere calibración fina.
- Señal sensorial determinista (aun con ruido) puede no provocar cambios significativos en el pipeline actual.
- Ausencia de evaluación externa (p. ej., datasets o tareas) que midan rendimiento funcional más allá de métricas internas.

14. Plan de trabajo futuro
- Implementar sub-bandas espectrales y normalización dinámica.
- Ajustar memoria con decaimiento y ruido controlado.
- Modulación del campo motor por ciclo; retroalimentación a lógica y emoción.
- Scripts de visualización y análisis estadístico de métricas.
- Integración de señales reales y escenarios de tarea guiados.
- Suite de pruebas amplia (pytest) con validación de rangos y sensibilidad.

15. Consideraciones éticas y de seguridad
- El sistema es una simulación sintética; no implica conciencia real.
- Evitar antropomorfismo excesivo en la interpretación de resultados.
- En integraciones con datos reales, proteger privacidad y asegurar uso responsable.

16. Conclusiones
Consciousness Engine constituye una plataforma experimental para explorar métricas internas en sistemas armónicos sintéticos. La exportación de métricas y la variabilidad controlada permiten diseñar experimentos reproducibles. Las observaciones actuales motivan mejoras para incrementar sensibilidad y variación inter-ciclo, habilitando aplicaciones educativas y de investigación más ricas.

17. Referencias (selección general)
- Señales y sistemas: análisis espectral y FFT.
- Medidas de coherencia y correlación en procesamiento de señales.
- Modelos inspirados en resonancia y sincronización de fase.