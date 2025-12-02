#!/usr/bin/env python3
"""Dimension 2: Psychologische Intelligenz.

Fragenkatalog basierend auf Self-Determination Theory,
Growth Mindset, Selbstwirksamkeit und positiver Psychologie.
"""

PSYCHOLOGY_QUESTIONS = [
    {
        "id": "psych_intrinsic_motivation",
        "question": "Wie stark fühlen Sie sich von innen heraus motiviert bei Ihren Haupttätigkeiten (Arbeit, Studium, Hobbys)?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Mittelmäßig", "Stark", "Sehr stark"],
        "required": True,
        "reference": "Deci, E. L., & Ryan, R. M. (2000). The 'what' and 'why' of goal pursuits: Human needs and the self-determination of behavior.",
        "bibtex_key": "deci2000sdt",
        "sub_dimension": "Autonomy (SDT)"
    },
    {
        "id": "psych_growth_mindset",
        "question": "Inwieweit glauben Sie, dass Sie durch Anstrengung und Übung Ihre Fähigkeiten grundlegend verbessern können?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Teilweise", "Weitgehend", "Vollständig"],
        "required": True,
        "reference": "Dweck, C. S. (2006). Mindset: The new psychology of success.",
        "bibtex_key": "dweck2006mindset",
        "sub_dimension": "Growth vs. Fixed Mindset"
    },
    {
        "id": "psych_self_efficacy",
        "question": "Wie zuversichtlich sind Sie, dass Sie auch schwierige Aufgaben erfolgreich bewältigen können?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht zuversichtlich", "Wenig zuversichtlich", "Mäßig zuversichtlich", "Ziemlich zuversichtlich", "Sehr zuversichtlich"],
        "required": True,
        "reference": "Bandura, A. (1997). Self-efficacy: The exercise of control.",
        "bibtex_key": "bandura1997selfefficacy",
        "sub_dimension": "Self-Efficacy"
    },
    {
        "id": "psych_social_relatedness",
        "question": "Wie stark fühlen Sie sich mit anderen Menschen verbunden und in Ihrer Gemeinschaft eingebunden?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Mittelmäßig", "Stark", "Sehr stark"],
        "required": True,
        "reference": "Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being.",
        "bibtex_key": "ryan2000sdt",
        "sub_dimension": "Relatedness (SDT)"
    },
    {
        "id": "psych_emotional_regulation",
        "question": "Wie gut können Sie negative Emotionen regulieren und konstruktiv damit umgehen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Gross, J. J. (2015). Emotion regulation: Current status and future prospects.",
        "bibtex_key": "gross2015emotion",
        "sub_dimension": "Emotional Intelligence"
    },
    {
        "id": "psych_resilience",
        "question": "Wie gut erholen Sie sich von Rückschlägen oder schwierigen Lebensereignissen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Masten, A. S. (2001). Ordinary magic: Resilience processes in development.",
        "bibtex_key": "masten2001resilience",
        "sub_dimension": "Resilience"
    },
    {
        "id": "psych_meaning_purpose",
        "question": "Wie stark empfinden Sie Sinn und Zweck in Ihrem Leben?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Teilweise", "Stark", "Sehr stark"],
        "required": True,
        "reference": "Frankl, V. E. (1959). Man's search for meaning.",
        "bibtex_key": "frankl1959meaning",
        "sub_dimension": "Meaning & Purpose"
    },
    {
        "id": "psych_positive_affect",
        "question": "Wie häufig erleben Sie positive Emotionen wie Freude, Dankbarkeit oder Begeisterung?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Nie", "Selten", "Manchmal", "Häufig", "Sehr häufig"],
        "required": True,
        "reference": "Fredrickson, B. L. (2001). The role of positive emotions in positive psychology.",
        "bibtex_key": "fredrickson2001positive",
        "sub_dimension": "Positive Psychology"
    },
    {
        "id": "psych_empathy",
        "question": "Wie gut können Sie sich in die Gefühle und Perspektiven anderer Menschen hineinversetzen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr schlecht", "Eher schlecht", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Decety, J., & Jackson, P. L. (2004). The functional architecture of human empathy.",
        "bibtex_key": "decety2004empathy",
        "sub_dimension": "Empathy & Social Cognition"
    },
    {
        "id": "psych_metacognition",
        "question": "Wie häufig reflektieren Sie bewusst über Ihre eigenen Denkprozesse und Lernstrategien?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Nie", "Selten", "Manchmal", "Häufig", "Sehr häufig"],
        "required": True,
        "reference": "Flavell, J. H. (1979). Metacognition and cognitive monitoring.",
        "bibtex_key": "flavell1979metacognition",
        "sub_dimension": "Metacognition"
    }
]

SUB_DIMENSIONS = [
    "Autonomy (SDT)",
    "Growth vs. Fixed Mindset",
    "Self-Efficacy",
    "Relatedness (SDT)",
    "Emotional Intelligence",
    "Resilience",
    "Meaning & Purpose",
    "Positive Psychology",
    "Empathy & Social Cognition",
    "Metacognition"
]
