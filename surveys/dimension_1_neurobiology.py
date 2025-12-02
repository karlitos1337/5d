#!/usr/bin/env python3
"""Dimension 1: Neurobiologische Intelligenz.

Fragenkatalog basierend auf kognitiver Neurowissenschaft,
Flow-Theorie, Neuroplastizität und Aufmerksamkeitsforschung.
"""

NEUROBIOLOGY_QUESTIONS = [
    {
        "id": "neuro_flow_frequency",
        "question": "Wie häufig erleben Sie Flow-Zustände (vollständiges Aufgehen in einer Tätigkeit, Verlust des Zeitgefühls)?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Nie", "Selten", "Manchmal", "Häufig", "Sehr häufig"],
        "required": True,
        "reference": "Csikszentmihalyi, M. (1990). Flow: The Psychology of Optimal Experience.",
        "bibtex_key": "csikszentmihalyi1990flow",
        "sub_dimension": "Flow & Optimal Experience"
    },
    {
        "id": "neuro_attention_span",
        "question": "Wie würden Sie Ihre Fähigkeit einschätzen, sich über längere Zeiträume auf eine Aufgabe zu konzentrieren?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Posner, M. I., & Petersen, S. E. (1990). The attention system of the human brain.",
        "bibtex_key": "posner1990attention",
        "sub_dimension": "Attention & Focus"
    },
    {
        "id": "neuro_neuroplasticity",
        "question": "Wie gut können Sie sich an vollkommen neue Situationen oder Umgebungen anpassen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schwer", "Eher schwer", "Mittelmäßig", "Eher leicht", "Sehr leicht"],
        "required": True,
        "reference": "Kolb, B., & Whishaw, I. Q. (1998). Brain plasticity and behavior.",
        "bibtex_key": "kolb1998plasticity",
        "sub_dimension": "Neuroplasticity & Adaptation"
    },
    {
        "id": "neuro_stress_regulation",
        "question": "Wie gut können Sie in stressigen Situationen ruhig und klar denken?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Eher nicht", "Manchmal", "Meistens", "Immer"],
        "required": True,
        "reference": "Sapolsky, R. M. (2004). Why zebras don't get ulcers.",
        "bibtex_key": "sapolsky2004zebras",
        "sub_dimension": "Stress Regulation"
    },
    {
        "id": "neuro_pattern_recognition",
        "question": "Wie schnell erkennen Sie Muster oder Zusammenhänge in neuen Informationen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr langsam", "Eher langsam", "Normal", "Eher schnell", "Sehr schnell"],
        "required": True,
        "reference": "Hawkins, J., & Blakeslee, S. (2004). On intelligence.",
        "bibtex_key": "hawkins2004intelligence",
        "sub_dimension": "Pattern Recognition"
    },
    {
        "id": "neuro_memory_consolidation",
        "question": "Wie gut können Sie sich an Details von Ereignissen erinnern, die einige Tage zurückliegen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Squire, L. R., & Kandel, E. R. (1999). Memory: From mind to molecules.",
        "bibtex_key": "squire1999memory",
        "sub_dimension": "Memory Consolidation"
    },
    {
        "id": "neuro_cognitive_flexibility",
        "question": "Wie leicht fällt es Ihnen, zwischen unterschiedlichen Denkweisen oder Perspektiven zu wechseln?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schwer", "Eher schwer", "Normal", "Eher leicht", "Sehr leicht"],
        "required": True,
        "reference": "Diamond, A. (2013). Executive functions.",
        "bibtex_key": "diamond2013executive",
        "sub_dimension": "Cognitive Flexibility"
    },
    {
        "id": "neuro_sleep_quality",
        "question": "Wie würden Sie die Qualität Ihres Schlafs in den letzten Wochen einschätzen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Walker, M. (2017). Why we sleep.",
        "bibtex_key": "walker2017sleep",
        "sub_dimension": "Sleep & Recovery"
    },
    {
        "id": "neuro_creativity_moments",
        "question": "Wie häufig haben Sie spontane kreative Einfälle oder 'Aha-Momente'?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Nie", "Selten", "Manchmal", "Häufig", "Sehr häufig"],
        "required": True,
        "reference": "Kounios, J., & Beeman, M. (2015). The eureka factor.",
        "bibtex_key": "kounios2015eureka",
        "sub_dimension": "Creativity & Insight"
    },
    {
        "id": "neuro_dopamine_response",
        "question": "Wie stark motiviert es Sie, wenn Sie Fortschritte bei einer Aufgabe sehen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Mittelmäßig", "Stark", "Sehr stark"],
        "required": True,
        "reference": "Schultz, W. (2015). Neuronal reward and decision signals.",
        "bibtex_key": "schultz2015reward",
        "sub_dimension": "Reward System"
    },
    {
        "id": "neuro_multitasking",
        "question": "Wie gut können Sie mehrere Aufgaben gleichzeitig bewältigen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Monsell, S. (2003). Task switching.",
        "bibtex_key": "monsell2003taskswitching",
        "sub_dimension": "Multitasking & Task Switching",
        "note": "Kritisch diskutiert - moderne Forschung zeigt Grenzen von Multitasking"
    },
    {
        "id": "neuro_default_mode",
        "question": "Wie oft schweifen Ihre Gedanken ab, wenn Sie eigentlich fokussiert sein möchten?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr häufig", "Häufig", "Manchmal", "Selten", "Nie"],
        "reverse_coded": True,
        "required": True,
        "reference": "Raichle, M. E., et al. (2001). A default mode of brain function.",
        "bibtex_key": "raichle2001default",
        "sub_dimension": "Default Mode Network"
    }
]

# Sub-Dimensionen für Auswertung
SUB_DIMENSIONS = [
    "Flow & Optimal Experience",
    "Attention & Focus",
    "Neuroplasticity & Adaptation",
    "Stress Regulation",
    "Pattern Recognition",
    "Memory Consolidation",
    "Cognitive Flexibility",
    "Sleep & Recovery",
    "Creativity & Insight",
    "Reward System",
    "Multitasking & Task Switching",
    "Default Mode Network"
]
