#!/usr/bin/env python3
"""Dimension 3: Philosophische Intelligenz.

Fragenkatalog basierend auf kritischem Denken,
epistemologischer Pluralität und reflexivem Bewusstsein.
"""

PHILOSOPHY_QUESTIONS = [
    {
        "id": "philo_critical_thinking",
        "question": "Wie wichtig ist es Ihnen, etablierte Wahrheiten und Annahmen zu hinterfragen?",  # noqa: E501
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": [
            "Überhaupt nicht wichtig",
            "Wenig wichtig",
            "Mäßig wichtig",
            "Wichtig",
            "Sehr wichtig",
        ],
        "required": True,
        "reference": "Paul, R., & Elder, L. (2006). Critical thinking: The nature of critical and creative thought.",  # noqa: E501
        "bibtex_key": "paul2006critical",
        "sub_dimension": "Critical Thinking",
    },
    {
        "id": "philo_epistemic_pluralism",
        "question": "Wie offen sind Sie gegenüber unterschiedlichen Formen von Wissen (wissenschaftlich, kulturell, intuitiv, spirituell)?",  # noqa: E501
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": [
            "Überhaupt nicht offen",
            "Wenig offen",
            "Mäßig offen",
            "Sehr offen",
            "Völlig offen",
        ],
        "required": True,
        "reference": "Santos, B. d. S. (2014). Epistemologies of the South: Justice against epistemicide.",  # noqa: E501
        "bibtex_key": "santos2014epistemologies",
        "sub_dimension": "Epistemic Pluralism",
    },
    {
        "id": "philo_uncertainty_tolerance",
        "question": "Wie gut können Sie mit Unsicherheit und mehrdeutigen Situationen umgehen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Keats, J. (1817). Negative capability concept.",
        "bibtex_key": "keats1817negative",
        "sub_dimension": "Ambiguity Tolerance",
    },
    {
        "id": "philo_dialectical_thinking",
        "question": "Wie häufig betrachten Sie Probleme aus mehreren, auch widersprüchlichen Perspektiven?",  # noqa: E501
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Nie", "Selten", "Manchmal", "Häufig", "Immer"],
        "required": True,
        "reference": "Hegel, G. W. F. (1807). Phänomenologie des Geistes.",
        "bibtex_key": "hegel1807phenomenology",
        "sub_dimension": "Dialectical Thinking",
    },
    {
        "id": "philo_ethical_reflection",
        "question": "Wie intensiv setzen Sie sich mit ethischen Fragen und moralischen Dilemmata auseinander?",  # noqa: E501
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Mäßig", "Intensiv", "Sehr intensiv"],
        "required": True,
        "reference": "Kohlberg, L. (1981). The philosophy of moral development.",
        "bibtex_key": "kohlberg1981moral",
        "sub_dimension": "Ethical Reasoning",
    },
    {
        "id": "philo_existential_awareness",
        "question": "Wie häufig denken Sie über existenzielle Fragen nach (Sinn des Lebens, Tod, Freiheit, Verantwortung)?",  # noqa: E501
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Nie", "Selten", "Manchmal", "Häufig", "Sehr häufig"],
        "required": True,
        "reference": "Sartre, J.-P. (1943). L'Être et le néant.",
        "bibtex_key": "sartre1943being",
        "sub_dimension": "Existential Awareness",
    },
    {
        "id": "philo_socratic_method",
        "question": "Wie sehr schätzen Sie die Praxis des nicht-wissenden Fragens (Sokrates: 'Ich weiß, dass ich nichts weiß')?",  # noqa: E501
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Mäßig", "Sehr", "Extrem"],
        "required": True,
        "reference": "Plato (380 BC). Apology of Socrates.",
        "bibtex_key": "plato380apology",
        "sub_dimension": "Socratic Inquiry",
    },
    {
        "id": "philo_power_critique",
        "question": "Wie wichtig ist es Ihnen, Machtstrukturen und deren Einfluss auf Wissen zu analysieren?",  # noqa: E501
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": [
            "Überhaupt nicht wichtig",
            "Wenig wichtig",
            "Mäßig wichtig",
            "Wichtig",
            "Sehr wichtig",
        ],
        "required": True,
        "reference": "Foucault, M. (1980). Power/Knowledge.",
        "bibtex_key": "foucault1980power",
        "sub_dimension": "Power-Knowledge Critique",
    },
    {
        "id": "philo_holistic_thinking",
        "question": "Inwieweit denken Sie in ganzheitlichen Zusammenhängen statt in isolierten Teilen?",  # noqa: E501
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Mäßig", "Stark", "Sehr stark"],
        "required": True,
        "reference": "Capra, F. (1996). The web of life.",
        "bibtex_key": "capra1996web",
        "sub_dimension": "Systems & Holistic Thinking",
    },
    {
        "id": "philo_paradox_embrace",
        "question": "Wie gut können Sie Paradoxien und Widersprüche als produktiv betrachten?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Gödel, K. (1931). Über formal unentscheidbare Sätze.",
        "bibtex_key": "goedel1931incompleteness",
        "sub_dimension": "Paradox & Incompleteness",
    },
]

SUB_DIMENSIONS = [
    "Critical Thinking",
    "Epistemic Pluralism",
    "Ambiguity Tolerance",
    "Dialectical Thinking",
    "Ethical Reasoning",
    "Existential Awareness",
    "Socratic Inquiry",
    "Power-Knowledge Critique",
    "Systems & Holistic Thinking",
    "Paradox & Incompleteness",
]
