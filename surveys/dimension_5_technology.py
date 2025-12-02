#!/usr/bin/env python3
"""Dimension 5: Technologische Intelligenz.

Fragenkatalog basierend auf Open-Source-Philosophie,
digitaler Autonomie und resonanter Technologie.
"""

TECHNOLOGY_QUESTIONS = [
    {
        "id": "tech_open_source",
        "question": "Wie wichtig ist Ihnen Open-Source-Software (freier Zugang zu Quellcode)?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht wichtig", "Wenig wichtig", "Mäßig wichtig", "Wichtig", "Sehr wichtig"],
        "required": True,
        "reference": "Raymond, E. S. (1999). The cathedral and the bazaar.",
        "bibtex_key": "raymond1999cathedral",
        "sub_dimension": "Open Source Philosophy"
    },
    {
        "id": "tech_digital_autonomy",
        "question": "Wie wichtig ist Ihnen die Kontrolle über Ihre eigenen digitalen Daten?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht wichtig", "Wenig wichtig", "Mäßig wichtig", "Wichtig", "Sehr wichtig"],
        "required": True,
        "reference": "Zuboff, S. (2019). The age of surveillance capitalism.",
        "bibtex_key": "zuboff2019surveillance",
        "sub_dimension": "Digital Autonomy"
    },
    {
        "id": "tech_ai_ethics",
        "question": "Wie wichtig ist Ihnen die ethische Gestaltung künstlicher Intelligenz?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht wichtig", "Wenig wichtig", "Mäßig wichtig", "Wichtig", "Sehr wichtig"],
        "required": True,
        "reference": "Floridi, L., et al. (2018). AI4People—An ethical framework for a good AI society.",
        "bibtex_key": "floridi2018ai4people",
        "sub_dimension": "AI Ethics"
    },
    {
        "id": "tech_decentralization",
        "question": "Wie wichtig ist Ihnen dezentrale (statt zentralisierter) Technologie-Infrastruktur?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht wichtig", "Wenig wichtig", "Mäßig wichtig", "Wichtig", "Sehr wichtig"],
        "required": True,
        "reference": "Baran, P. (1964). On distributed communications.",
        "bibtex_key": "baran1964distributed",
        "sub_dimension": "Decentralization"
    },
    {
        "id": "tech_digital_literacy",
        "question": "Wie würden Sie Ihre eigenen digitalen Kompetenzen einschätzen?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Sehr gering", "Eher gering", "Mittelmäßig", "Gut", "Sehr gut"],
        "required": True,
        "reference": "Eshet-Alkalai, Y. (2004). Digital literacy: A conceptual framework for survival skills in the digital era.",
        "bibtex_key": "eshet2004digital",
        "sub_dimension": "Digital Literacy"
    },
    {
        "id": "tech_appropriate_technology",
        "question": "Wie wichtig ist Ihnen angepasste Technologie (einfach, reparierbar, lokal wartbar)?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht wichtig", "Wenig wichtig", "Mäßig wichtig", "Wichtig", "Sehr wichtig"],
        "required": True,
        "reference": "Schumacher, E. F. (1973). Small is beautiful.",
        "bibtex_key": "schumacher1973small",
        "sub_dimension": "Appropriate Technology"
    },
    {
        "id": "tech_privacy_awareness",
        "question": "Wie häufig machen Sie sich Gedanken über Ihre digitale Privatsphäre?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Nie", "Selten", "Manchmal", "Häufig", "Sehr häufig"],
        "required": True,
        "reference": "Solove, D. J. (2008). Understanding privacy.",
        "bibtex_key": "solove2008privacy",
        "sub_dimension": "Privacy Awareness"
    },
    {
        "id": "tech_interoperability",
        "question": "Wie wichtig ist Ihnen Interoperabilität (Kompatibilität zwischen verschiedenen Systemen)?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht wichtig", "Wenig wichtig", "Mäßig wichtig", "Wichtig", "Sehr wichtig"],
        "required": True,
        "reference": "Berners-Lee, T. (1989). Information management: A proposal.",
        "bibtex_key": "bernerslee1989web",
        "sub_dimension": "Interoperability"
    },
    {
        "id": "tech_energy_efficiency",
        "question": "Wie wichtig ist Ihnen die Energieeffizienz digitaler Technologien?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht wichtig", "Wenig wichtig", "Mäßig wichtig", "Wichtig", "Sehr wichtig"],
        "required": True,
        "reference": "Belkhir, L., & Elmeligi, A. (2018). Assessing ICT global emissions footprint.",
        "bibtex_key": "belkhir2018ict",
        "sub_dimension": "Energy Efficiency"
    },
    {
        "id": "tech_resonance_theory",
        "question": "Wie sehr interessiert Sie die Idee, dass Technologie harmonisch mit natürlichen Systemen resonieren sollte?",
        "type": "likert",
        "scale": [1, 2, 3, 4, 5],
        "labels": ["Überhaupt nicht", "Wenig", "Mäßig", "Stark", "Sehr stark"],
        "required": True,
        "reference": "László, E. (2004). Science and the akashic field.",
        "bibtex_key": "laszlo2004akashic",
        "sub_dimension": "Resonance Theory",
        "note": "Inspiriert von Tesla, László, und Systemtheorie"
    }
]

SUB_DIMENSIONS = [
    "Open Source Philosophy",
    "Digital Autonomy",
    "AI Ethics",
    "Decentralization",
    "Digital Literacy",
    "Appropriate Technology",
    "Privacy Awareness",
    "Interoperability",
    "Energy Efficiency",
    "Resonance Theory"
]
