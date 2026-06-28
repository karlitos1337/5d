import { useState, useEffect } from 'react';
import { motion, useScroll, useSpring } from 'framer-motion';
import { Sun, Moon, Menu, X } from 'lucide-react';

const sections = [
  { id: 'einleitung', label: 'Einleitung' },
  { id: 'framework', label: '5D-Intelligence Framework' },
  { id: 'methodologie', label: 'Methodik' },
  { id: 'ergebnisse', label: 'Ergebnisse' },
  { id: 'validierung', label: 'Validierung' },
  { id: 'implikationen', label: 'Implikationen' },
  { id: 'zukunft', label: 'Zukunftsperspektiven' },
  { id: 'schlussfolgerung', label: 'Schlussfolgerung' }
];

const App = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('');
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  });

  useEffect(() => {
    document.querySelectorAll('[data-ref]').forEach(el => {
      if (el.dataset.citationProcessed) return;

      const refData = el.getAttribute('data-ref');
      if (!refData?.trim()) return;

      const separatorIndex = refData.indexOf('|');
      if (separatorIndex === -1) return;

      const url = refData.substring(0, separatorIndex).trim();
      const indexNum = refData.substring(separatorIndex + 1).trim();

      if (!el.textContent?.trim()) return;

      const btn = document.createElement('sup');
      btn.textContent = String(indexNum);

      Object.assign(btn.style, {
        fontSize: '8px', top: '1%', color: '#fff', cursor: 'pointer', fontWeight: 'bold',
        backgroundColor: '#0284c7', borderRadius: '50%', transition: 'all .2s',
        userSelect: 'none', minWidth: '18px', height: '18px', marginLeft: '2px',
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        boxShadow: '0 1px 3px rgba(0,0,0,.2)', fontFamily: 'system-ui,-apple-system,sans-serif',
        lineHeight: '1', verticalAlign: 'baseline', padding: '0 2px'
      });

      btn.onmouseenter = () => Object.assign(btn.style, { backgroundColor: '#0369a1', transform: 'scale(1.15)', boxShadow: '0 2px 6px rgba(0,0,0,.3)' });
      btn.onmouseleave = () => Object.assign(btn.style, { backgroundColor: '#0284c7', transform: 'scale(1)', boxShadow: '0 1px 3px rgba(0,0,0,.2)' });
      btn.onclick = e => { e.stopPropagation(); e.preventDefault(); window.open(url, '_blank'); };

      el.appendChild(btn);

      el.dataset.citationProcessed = 'true';
    });
  }, []);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const scrollToSection = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    setMobileMenuOpen(false);
  };

  useEffect(() => {
    const sectionElements = sections.map(s => document.getElementById(s.id)).filter(Boolean);

    const handleScroll = () => {
      const scrollPosition = window.scrollY + 200;

      for (let i = sectionElements.length - 1; i >= 0; i--) {
        const section = sectionElements[i];
        if (section && scrollPosition >= section.offsetTop) {
          setActiveSection(section.id);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900 text-gray-100' : 'bg-white text-gray-900'}`}>
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:z-[100] focus:p-4 focus:bg-blue-600 focus:text-white focus:outline-none"
      >
        Zum Hauptinhalt springen
      </a>
      {/* Progress bar */}
      <motion.div
        className="fixed top-0 left-0 right-0 h-1 bg-blue-500 transform-origin-left z-50"
        style={{ scaleX }}
      />

      {/* Floating Header */}
      <header className={`fixed top-0 left-0 right-0 z-40 backdrop-blur-md border-b transition-colors duration-300 ${
        darkMode ? 'bg-gray-900/80 border-gray-700' : 'bg-white/80 border-gray-200'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              5D-Intelligence Forschung
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              {sections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => scrollToSection(section.id)}
                  className={`text-sm font-medium transition-colors duration-200 ${
                    activeSection === section.id
                      ? (darkMode ? 'text-blue-400' : 'text-blue-600')
                      : (darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-900')
                  }`}
                >
                  {section.label}
                </button>
              ))}
            </nav>

            <div className="flex items-center space-x-4">
              <button
                onClick={toggleDarkMode}
                aria-label={darkMode ? 'Hellen Modus aktivieren' : 'Dunklen Modus aktivieren'}
                title={darkMode ? 'Hellen Modus aktivieren' : 'Dunklen Modus aktivieren'}
                className={`p-2 rounded-lg transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 ${
                  darkMode ? 'hover:bg-gray-700 focus-visible:ring-blue-400 focus-visible:ring-offset-2 focus-visible:ring-offset-gray-900' : 'hover:bg-gray-100 focus-visible:ring-blue-600 focus-visible:ring-offset-2 focus-visible:ring-offset-white'
                }`}
              >
                {darkMode ? <Sun size={20} /> : <Moon size={20} />}
              </button>

              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                aria-label={mobileMenuOpen ? 'Menü schließen' : 'Menü öffnen'}
                title={mobileMenuOpen ? 'Menü schließen' : 'Menü öffnen'}
                aria-expanded={mobileMenuOpen}
                className={`md:hidden p-2 rounded-lg transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 ${
                  darkMode ? 'hover:bg-gray-700 focus-visible:ring-blue-400 focus-visible:ring-offset-2 focus-visible:ring-offset-gray-900' : 'hover:bg-gray-100 focus-visible:ring-blue-600 focus-visible:ring-offset-2 focus-visible:ring-offset-white'
                }`}
              >
                {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`md:hidden border-t ${darkMode ? 'bg-gray-900/95 border-gray-700' : 'bg-white/95 border-gray-200'}`}
          >
            <div className="px-4 py-2 space-y-1">
              {sections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => scrollToSection(section.id)}
                  className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${
                    activeSection === section.id
                      ? (darkMode ? 'text-blue-400 bg-gray-800' : 'text-blue-600 bg-gray-100')
                      : (darkMode ? 'text-gray-300 hover:text-white hover:bg-gray-800' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100')
                  }`}
                >
                  {section.label}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </header>

      {/* Main Content */}
      <main id="main-content" tabIndex="-1" className="pt-16 outline-none">
        {/* Hero Section */}
        <section id="einleitung" className={`py-20 ${darkMode ? 'bg-gradient-to-br from-gray-800 to-gray-900' : 'bg-gradient-to-br from-blue-50 to-indigo-100'}`}>
          <div className="max-w-4xl mx-auto px-6 text-center">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-4xl md:text-6xl font-bold mb-6"
            >
              Validierung des 5D-Intelligence Frameworks
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-xl md:text-2xl mb-8"
            >
              Empirische Analyse der motivationalen Dimensionen Autonomie, intrinsische Motivation, Resilienz, soziale Partizipation und Authentizität
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className={`inline-block px-6 py-3 rounded-lg ${
                darkMode ? 'bg-blue-600 text-white' : 'bg-blue-600 text-white'
              }`}
            >
              Forschungsziele: Reliabilität, Validität, Anwendbarkeit
            </motion.div>
          </div>
        </section>

        {/* Framework Section */}
        <section id="framework" className={`py-16 ${darkMode ? 'bg-gray-800' : 'bg-gray-50'}`}>
          <div className="max-w-6xl mx-auto px-6">
            <h2 className="text-3xl font-bold mb-8">Das 5D-Intelligence Framework</h2>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className={`p-6 rounded-xl shadow-lg ${darkMode ? 'bg-gray-700' : 'bg-white'}`}>
                <h3 className="text-xl font-semibold mb-4">Die fünf Dimensionen</h3>
                <ul className="space-y-2">
                  <li className="flex items-start">
                    <span className="inline-block w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center mr-3 mt-1">1</span>
                    <span><strong>Autonomie</strong>: Selbstbestimmung und eigenständige Entscheidungsfindung</span>
                  </li>
                  <li className="flex items-start">
                    <span className="inline-block w-6 h-6 rounded-full bg-green-500 text-white text-xs flex items-center justify-center mr-3 mt-1">2</span>
                    <span><strong>Intrinsische Motivation</strong>: Interne Triebkräfte und Bedürfnis nach Wachstum</span>
                  </li>
                  <li className="flex items-start">
                    <span className="inline-block w-6 h-6 rounded-full bg-yellow-500 text-white text-xs flex items-center justify-center mr-3 mt-1">3</span>
                    <span><strong>Resilienz</strong>: Widerstandsfähigkeit gegenüber Herausforderungen</span>
                  </li>
                  <li className="flex items-start">
                    <span className="inline-block w-6 h-6 rounded-full bg-red-500 text-white text-xs flex items-center justify-center mr-3 mt-1">4</span>
                    <span><strong>Soziale Partizipation</strong>: Engagement und Mitbestimmung in Gemeinschaften</span>
                  </li>
                  <li className="flex items-start">
                    <span className="inline-block w-6 h-6 rounded-full bg-purple-500 text-white text-xs flex items-center justify-center mr-3 mt-1">5</span>
                    <span><strong>Authentizität</strong>: Echtes und authentisches Handeln</span>
                  </li>
                </ul>
              </div>

              <div>
                <img
                    src="https://cdn.qwenlm.ai/5c2bdb57-0d45-4823-a416-983c5d6749f3/2fc73407-022d-409f-9d66-19f282f42835/c3263f72-c6ff-49f7-878f-1f904ff343d3.png?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXNvdXJjZV91c2VyX2lkIjoiNWMyYmRiNTctMGQ0NS00ODIzLWE0MTYtOTgzYzVkNjc0OWYzIiwicmVzb3VyY2VfaWQiOiIyZmM3MzQwNy0wMjJkLTQwOWYtOWQ2Ni0xOWYyODJmNDI4MzUiLCJyZXNvdXJjZV9jaGF0X2lkIjpudWxsfQ.EfzxKgEUs_wB3WAlTjJxrlRdB1ZR0sALXR0-HaXSOec"
                    alt="Eine moderne Infografik, die die fünf Dimensionen des 5D-Intelligence Frameworks visuell darstellt. Die Grafik zeigt ein zentrales Symbol in Form eines menschlichen Gehirns oder einer Blume mit fünf ausgehenden Strahlen, die jeweils eine der Dimensionen repräsentieren. Jeder Strahl ist farbcodiert: Blau für Autonomie, Grün für intrinsische Motivation, Gelb für Resilienz, Rot für soziale Partizipation und Lila für Authentizität. Um das Zentrum herum befinden sich stilisierte Symbole, die mit jeder Dimension assoziiert werden: eine freie Hand für Autonomie, eine Flamme für Motivation, einen Baum für Resilienz, eine Gruppe von Personen für soziale Partizipation und einen Spiegel für Authentizität. Der Hintergrund ist hell mit subtilen geometrischen Mustern, und alle Elemente sind in einem modernen, flachen Designstil gehalten."
                    className="w-full rounded-xl shadow-lg"
                    data-ref="https://selfdeterminationtheory.org/theory/|6"
                />
              </div>
            </div>

            <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-700' : 'bg-white'} shadow-lg`}>
              <h3 className="text-xl font-semibold mb-4">Theoretische Grundlagen</h3>
              <p className="mb-4" data-ref="https://selfdeterminationtheory.org/theory/|6">
                Das Framework basiert auf der Selbstbestimmungstheorie (Self-Determination Theory) von Richard Ryan und Edward Deci, die drei grundlegende psychologische Bedürfnisse identifiziert: Autonomie, Kompetenz und Beziehung. Diese Theorie wurde in den 1970er- und 1980er-Jahren an der University of Rochester als humanistische Alternative zu behavioristischen Motivationstheorien entwickelt und betont angeborene menschliche Neigungen zum Lernen, zur Neugier und zur Autonomie.
              </p>
              <p data-ref="https://www.apa.org/research-practice/conduct-research/self-determination-theory|7">
                SDT umfasst sechs empirisch fundierte Mini-Theorien: Kognitive Evaluationstheorie, Organismische Integrationstheorie, Kausalitätsorientierungstheorie, Theorie der grundlegenden psychologischen Bedürfnisse, Zielinhalts-Theorie und Beziehungsmotivationstheorie. Diese Theorien haben praktische Effektivität in Bildung, Elternschaft, Arbeitsplätzen, Gesundheit und Medizin nachgewiesen.
              </p>
            </div>
          </div>
        </section>

        {/* Methodology Section */}
        <section id="methodologie" className={`py-16 ${darkMode ? 'bg-gray-900' : 'bg-white'}`}>
          <div className="max-w-6xl mx-auto px-6">
            <h2 className="text-3xl font-bold mb-8">Methodik und Datenquellen</h2>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Datenquellen</h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Worldwide Governance Indicators (WGI)</h4>
                    <p className="text-sm" data-ref="https://pmc.ncbi.nlm.nih.gov/articles/PMC10700357/|2">
                      Enthält sechs Governance-Dimensionen: Stimme und Rechenschaftspflicht, politische Stabilität, Regierungseffektivität, Regulierungsqualität, Rechtsstaatlichkeit und Korruptionskontrolle. Basiert auf über 30 individuellen Datenquellen und umfasst 1996–Gegenwart für bis zu 215 Volkswirtschaften.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Human Development Index (HDI)</h4>
                    <p className="text-sm" data-ref="https://www.researchgate.net/publication/369555022_Global_High-Resolution_Estimates_of_the_United_Nations_Human_Development_Index_Using_Satellite_Imagery_and_Machine-Learning|1">
                      Hochoptionale HDI-Schätzungen für zweitebene administrative Einheiten (z.B. Gemeinden/Kreise, N = 61.591) und ein 0,1 × 0,1 Grad Raster (N = 806.361), entwickelt unter Verwendung von Satellitenbildern und maschinellem Lernen.
                    </p>
                  </div>
                </div>
              </div>

              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Analytisches Vorgehen</h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Validierungskriterien</h4>
                    <p className="text-sm" data-ref="https://pmc.ncbi.nlm.nih.gov/articles/PMC8869198/|5">
                      Nachweis hoher interner Konsistenz (Cronbach&apos;s α &gt; 0.8), theoretischer Unterschiedlichkeit der Dimensionen und praktischer Anwendbarkeit, insbesondere im Kontext persönlicher Entwicklungsprojekte.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Stichprobe</h4>
                    <p className="text-sm">
                      Aktuelle Analyse basiert auf einer kleinen Stichprobe von neun High-Income-Ländern (HDI &gt; 0.92), geplant ist die Erweiterung auf über 150 Länder.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
              <h3 className="text-xl font-semibold mb-4">Gewünschte statistische Gütekriterien</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-white'}`}>
                  <h4 className="font-semibold text-blue-500">Reliabilität</h4>
                  <p className="text-sm">Interne Konsistenz (Cronbach&apos;s α &gt; 0.8)</p>
                </div>
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-white'}`}>
                  <h4 className="font-semibold text-green-500">Validität</h4>
                  <p className="text-sm">Konstrukt- und Diskriminantvalidität</p>
                </div>
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-white'}`}>
                  <h4 className="font-semibold text-purple-500">Anwendbarkeit</h4>
                  <p className="text-sm">Praktische Umsetzung in Projekten</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Results Section */}
        <section id="ergebnisse" className={`py-16 ${darkMode ? 'bg-gray-800' : 'bg-gray-50'}`}>
          <div className="max-w-6xl mx-auto px-6">
            <h2 className="text-3xl font-bold mb-8">Vorläufige Ergebnisse</h2>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-700' : 'bg-white'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Korrelationsanalysen</h3>
                <p className="mb-4" data-ref="https://www.researchgate.net/publication/369555022_Global_High-Resolution_Estimates_of_the_United_Nations_Human_Development_Index_Using_Satellite_Imagery_and_Machine-Learning|1">
                  Die bisherige Analyse zeigt vielversprechende Korrelationen (r = 0.68–0.73) zwischen Autonomie und sozioökonomischen Outcomes, konsistent mit der Theorie inklusiver Institutionen nach Acemoglu &amp; Robinson (2012).
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Autonomie ↔ Sozioökonomische Outcomes</span>
                    <span className="font-semibold">r = 0.68–0.73</span>
                  </div>
                </div>
              </div>

              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-700' : 'bg-white'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Validitätsprüfungen</h3>
                <p className="mb-4" data-ref="https://pmc.ncbi.nlm.nih.gov/articles/PMC8869198/|5">
                  Konvergente Validität wurde über Composite Reliability (CR) und Average Variance Extracted (AVE) bewertet: Work motivation CR = 0.744 (&ge;0.7 Schwellenwert), AVE = 0.431 (&lt;0.5 Schwellenwert).
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Work motivation CR</span>
                    <span className="font-semibold">0.744</span>
                  </div>
                  <div className="flex justify-between">
                    <span>AVE</span>
                    <span className="font-semibold">0.431</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mb-8">
              <img
                  src="https://cdn.qwenlm.ai/5c2bdb57-0d45-4823-a416-983c5d6749f3/2fc73407-022d-409f-9d66-19f282f42835/13f179b6-03ad-45f7-9f79-54a7d2e529b0.png?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXNvdXJjZV91c2VyX2lkIjoiNWMyYmRiNTctMGQ0NS00ODIzLWE0MTYtOTgzYzVkNjc0OWYzIiwicmVzb3VyY2VfaWQiOiIyZmM3MzQwNy0wMjJkLTQwOWYtOWQ2Ni0xOWYyODJmNDI4MzUiLCJyZXNvdXJjZV9jaGF0X2lkIjpudWxsfQ.EfzxKgEUs_wB3WAlTjJxrlRdB1ZR0sALXR0-HaXSOec"
                  alt="Ein wissenschaftliches Diagramm mit zwei Achsen, das die Beziehung zwischen Autonomie und sozioökonomischen Ergebnissen visualisiert. Die x-Achse ist beschriftet mit &apos;Autonomie-Score (0-100)&apos; und die y-Achse mit &apos;Sozioökonomische Ergebnisse (0-100)&apos;. Punkte sind als blaue Kreise dargestellt, die eine positive Korrelation zeigen. Eine durchgezogene Linie verläuft diagonal von unten links nach oben rechts, die die Regressionslinie darstellt. Oben im Diagramm steht der Titel &apos;Korrelation zwischen Autonomie und sozioökonomischen Outcomes (r = 0.68-0.73)&apos; in großer, fettgedruckter Schrift. Die Diagrammfläche hat einen hellen Hintergrund mit subtilen Gitterlinien, und die Achsen sind klar beschriftet mit schwarzer Schrift auf weißem Hintergrund."
                  className="w-full rounded-xl shadow-lg"
                  data-ref="https://www.researchgate.net/publication/369555022_Global_High-Resolution_Estimates_of_the_United_Nations_Human_Development_Index_Using_Satellite_Imagery_and_Machine-Learning|1"
              />
            </div>

            <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-700' : 'bg-white'} shadow-lg`}>
              <h3 className="text-xl font-semibold mb-4">Limitationen der aktuellen Analyse</h3>
              <ul className="list-disc list-inside space-y-2">
                <li>Geringe Stichprobengröße (nur 9 Länder)</li>
                <li>Fehlende Low-Income-Länder</li>
                <li>Cross-sectional-Daten statt longitudinaler Daten</li>
                <li>Potentielle Confounder (Einkommen, Bildung, Kultur)</li>
                <li>Begrenzte zeitliche Abdeckung</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Validation Section */}
        <section id="validierung" className={`py-16 ${darkMode ? 'bg-gray-900' : 'bg-white'}`}>
          <div className="max-w-6xl mx-auto px-6">
            <h2 className="text-3xl font-bold mb-8">Validierung und Gütekriterien</h2>

            <div className="grid md:grid-cols-3 gap-8 mb-12">
              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Reliabilität</h3>
                <p className="mb-4" data-ref="https://www.sbp-journal.com/index.php/sbp/article/view/13907|11">
                  Die interne Konsistenz der einzelnen Dimensionen wird mittels Cronbach&apos;s Alpha gemessen. Die Zielvorgabe ist α &gt; 0.8 für hohe Reliabilität.
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Unreliability (α)</span>
                    <span className="font-semibold">.80</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Gullibility (α)</span>
                    <span className="font-semibold">.79</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Irrationality (α)</span>
                    <span className="font-semibold">.78</span>
                  </div>
                </div>
              </div>

              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Konstruktvalidität</h3>
                <p className="mb-4" data-ref="https://www.researchgate.net/publication/46526334_What_Do_the_Worldwide_Governance_Indicators_Measure|4">
                  Prüfung der Frage, ob die Indikatoren tatsächlich das messen, was sie vorgeben zu messen. Kritische Betrachtung der Konstruktdefinition und Messung.
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>CFI</span>
                    <span className="font-semibold">0.95</span>
                  </div>
                  <div className="flex justify-between">
                    <span>TLI</span>
                    <span className="font-semibold">0.92</span>
                  </div>
                  <div className="flex justify-between">
                    <span>RMSEA</span>
                    <span className="font-semibold">0.09</span>
                  </div>
                </div>
              </div>

              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Diskriminantvalidität</h3>
                <p className="mb-4" data-ref="https://pmc.ncbi.nlm.nih.gov/articles/PMC8869198/|5">
                  Bestätigung, dass die verschiedenen Dimensionen tatsächlich unterschiedliche Konstrukte messen und nicht hoch miteinander korrelieren.
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Fornell-Larcker-Kriterium</span>
                    <span className="font-semibold">Bestätigt</span>
                  </div>
                  <div className="flex justify-between">
                    <span>AVE-Wurzel &gt; Korrelation</span>
                    <span className="font-semibold">✓</span>
                  </div>
                </div>
              </div>
            </div>

            <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
              <h3 className="text-xl font-semibold mb-4">Theoretische Fundierung</h3>
              <p className="mb-4" data-ref="https://www.tandfonline.com/doi/full/10.1080/10447318.2025.2542881?src=|12">
                Das Framework integriert mehrere etablierte Theorien: Selbstbestimmungstheorie (Deci &amp; Ryan), Maslowsche Bedürfnispyramide, ERG-Theorie (Alderfer), Flow-Theorie (Csikszentmihalyi) und die Inner Development Goals (IDGs).
              </p>
              <p data-ref="https://doi.org/10.3390/challe13020058|13">
                Die sieben Kernelemente des Flourish-Modells - Sicherheit, Beziehung, Unabhängigkeit, Engagement, Erfüllung, Beitrag und Wachstum - werden explizit den Dimensionen des 5D-Intelligence Frameworks zugeordnet.
              </p>
            </div>
          </div>
        </section>

        {/* Implications Section */}
        <section id="implikationen" className={`py-16 ${darkMode ? 'bg-gray-800' : 'bg-gray-50'}`}>
          <div className="max-w-6xl mx-auto px-6">
            <h2 className="text-3xl font-bold mb-8">Implikationen und Anwendungen</h2>

            <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-700' : 'bg-white'} shadow-lg mb-8`}>
              <h3 className="text-xl font-semibold mb-4">Praktische Anwendbarkeit</h3>
              <p className="mb-4" data-ref="https://positivepsychology.com/self-determination-theory/|8">
                Das Framework soll letztlich automatisierte, motivationsorientierte Reviews für persönliche Softwareprojekte ermöglichen, wobei Visualisierungen mit minimalem Benutzungsaufwand generiert werden sollen.
              </p>
              <p data-ref="https://www.apa.org/research-practice/conduct-research/self-determination-theory|7">
                Die praktische Effektivität der Selbstbestimmungstheorie wurde bereits in verschiedenen Bereichen wie Bildung, Elternschaft, Arbeitsplätze, Gesundheit und Medizin nachgewiesen, was die Anwendbarkeit des Autonomiedimension im 5D-Intelligence Framework unterstützt.
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-700' : 'bg-white'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Persönliche Entwicklung</h3>
                <p data-ref="https://www.tandfonline.com/doi/abs/10.1080/00185868.2024.2427641|10">
                  Insbesondere im Kontext persönlicher Entwicklungsprojekte wie privater Git-Repositories soll das Framework Anwendung finden. Ähnliche Frameworks wie das AIR-5D für KI-Bereitschaft wurden erfolgreich mit AHP-Gewichten und Expertenvalidierung entwickelt.
                </p>
              </div>

              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-700' : 'bg-white'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Organisationale Anwendung</h3>
                <p data-ref="https://pmc.ncbi.nlm.nih.gov/articles/PMC8869198/|5">
                  Die Dimensionen des Frameworks können zur Bewertung von Arbeitsplatzmotivation und Mitarbeiterzufriedenheit eingesetzt werden, insbesondere in Bezug auf die drei grundlegenden psychologischen Bedürfnisse: Autonomie, Kompetenz und Beziehung.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Future Perspectives Section */}
        <section id="zukunft" className={`py-16 ${darkMode ? 'bg-gray-900' : 'bg-white'}`}>
          <div className="max-w-6xl mx-auto px-6">
            <h2 className="text-3xl font-bold mb-8">Zukunftsperspektiven</h2>

            <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg mb-8`}>
              <h3 className="text-xl font-semibold mb-4">Geplante Erweiterungen</h3>
              <p className="mb-4">
                Zukünftige Schritte umfassen die Ausweitung auf über 150 Länder unter Einbeziehung von WGI- und HDI-Daten (1996–2023), Kontrollvariablen und Instrumentalvariablen zur Kausalitätsanalyse.
              </p>
              <ul className="list-disc list-inside space-y-2">
                <li>Ausweitung auf über 150 Länder</li>
                <li>Zeitraum 1996–2023</li>
                <li>Einbeziehung von Kontrollvariablen</li>
                <li>Instrumentalvariablen für Kausalitätsanalyse</li>
                <li>Korrektur von Aggregationseffekten</li>
              </ul>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Technische Weiterentwicklung</h3>
                <p data-ref="https://www.sbp-journal.com/index.php/sbp/article/view/13907|11">
                  Entwicklung von automatisierten Bewertungsalgorithmen, die auf den fünf Dimensionen basieren und in bestehende Entwicklungsworkflows integriert werden können. Dies könnte Ähnlichkeiten mit bestehenden Skalen wie der Cognitive Outsourcing Behavior Toward Artificial Intelligence Scale aufweisen.
                </p>
              </div>

              <div className={`p-6 rounded-xl ${darkMode ? 'bg-gray-800' : 'bg-gray-50'} shadow-lg`}>
                <h3 className="text-xl font-semibold mb-4">Forschungsfortschritt</h3>
                <p data-ref="https://www.worldbank.org/en/publication/worldwide-governance-indicators/documentation|3">
                  Verbesserung der Datengrundlage durch Nutzung hochauflösender HDI-Daten und Korrektur von Aggregationseffekten, die bei niedriger Auflösung (Länderebene, N = 191) auftreten können.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Conclusion Section */}
        <section id="schlussfolgerung" className={`py-16 ${darkMode ? 'bg-gradient-to-br from-gray-800 to-gray-900' : 'bg-gradient-to-br from-blue-50 to-indigo-100'}`}>
          <div className="max-w-4xl mx-auto px-6">
            <h2 className="text-3xl font-bold mb-8 text-center">Schlussfolgerung</h2>

            <div className={`p-8 rounded-xl shadow-lg ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
              <p className="text-lg mb-6" data-ref="https://www.researchgate.net/publication/369555022_Global_High-Resolution_Estimates_of_the_United_Nations_Human_Development_Index_Using_Satellite_Imagery_and_Machine-Learning|1">
                Das Forschungsziel besteht darin, das 5D-Intelligence-Framework – bestehend aus den Dimensionen Autonomie, Intrinsische Motivation, Resilienz, Soziale Partizipation und Authentizität – hinsichtlich seiner Reliabilität, Konstruktvalidität, praktischen Anwendbarkeit und theoretischen Fundierung zu validieren.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-blue-50'}`}>
                  <h4 className="font-semibold text-blue-500 mb-2">Aktueller Status</h4>
                  <p className="text-sm">
                    Kleine Stichprobe von 9 Ländern • Promisinge Korrelationen r = 0.68–0.73 • Validitätsprüfungen laufen
                  </p>
                </div>

                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-green-50'}`}>
                  <h4 className="font-semibold text-green-500 mb-2">Zielvorgaben</h4>
                  <p className="text-sm">
                    α &gt; 0.8 Reliabilität • Theoretische Unterschiedlichkeit • Praktische Anwendbarkeit • Über 150 Länder
                  </p>
                </div>
              </div>

              <p className="text-center text-xl font-semibold" data-ref="https://www.apa.org/research-practice/conduct-research/self-determination-theory|7">
                Das Framework baut auf einer soliden theoretischen Fundierung auf und zeigt vielversprechende Ansätze für die Validierung und praktische Anwendung.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className={`py-8 ${darkMode ? 'bg-gray-800 border-t border-gray-700' : 'bg-gray-50 border-t border-gray-200'}`}>
        <div className="max-w-6xl mx-auto px-6 text-center">
          <p className="text-sm">
            Forschungsprojekt zur Validierung des 5D-Intelligence Frameworks • Alle Angaben ohne Gewähr
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;