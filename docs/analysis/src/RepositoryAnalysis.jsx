import React, { useState, useEffect } from 'react';
import { motion, useScroll, useSpring } from 'framer-motion';
import { Sun, Moon, Menu, X, ChevronDown } from 'lucide-react';

const RepositoryAnalysis = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('');
  const [expandedSections, setExpandedSections] = useState({});
  
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

  const toggleSection = (sectionId) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  const navItems = [
    { id: 'overview', label: 'Übersicht' },
    { id: 'methodology', label: 'Methodik' },
    { id: 'findings', label: 'Ergebnisse' },
    { id: 'improvements', label: 'Verbesserungen' },
    { id: 'architecture', label: 'Architektur' },
    { id: 'conclusion', label: 'Fazit' }
  ];

  useEffect(() => {
    // ⚡ Bolt: Cache DOM elements to avoid getElementById during scroll
    const cachedSections = navItems.map(item => ({
      id: item.id,
      element: document.getElementById(item.id)
    })).filter(item => item.element);

    // ⚡ Bolt: Optimize scroll performance by using requestAnimationFrame and a ticking flag
    // to throttle expensive DOM queries (offsetTop) and state updates, preventing main-thread
    // blocking during continuous scrolling.
    let ticking = false;

    const handleScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const scrollPosition = window.scrollY + 100;

          for (const sectionObj of cachedSections) {
            const section = sectionObj.element;
            const offsetTop = section.offsetTop;
            const height = section.offsetHeight;
            if (scrollPosition >= offsetTop && scrollPosition < offsetTop + height) {
              setActiveSection(sectionObj.id);
              break;
            }
          }
          ticking = false;
        });
        ticking = true;
      }
    };

    // ⚡ Bolt: Add { passive: true } to allow the browser to scroll immediately without waiting for JS execution.
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setMobileMenuOpen(false);
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900 text-gray-100' : 'bg-white text-gray-900'}`}>
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:top-0 focus:left-0 focus:p-4 focus:bg-blue-600 focus:text-white focus:font-bold">
        Zum Hauptinhalt springen
      </a>
      <motion.div
        className="fixed top-0 left-0 right-0 h-1 bg-blue-500 transform-origin-left z-50"
        style={{ scaleX }}
      />
      
      <header className={`fixed top-0 left-0 right-0 z-40 backdrop-blur-md transition-all duration-300 ${
        darkMode ? 'bg-gray-900/80 border-b border-gray-700' : 'bg-white/80 border-b border-gray-200'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                5D Repository Analyse
              </h1>
            </div>
            
            <nav className="hidden md:flex space-x-8">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => scrollToSection(item.id)}
                  className={`text-sm font-medium transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded-sm ${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'} ${
                    activeSection === item.id 
                      ? (darkMode ? 'text-blue-400' : 'text-blue-600')
                      : (darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-900')
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </nav>
            
            <div className="flex items-center space-x-4">
              <button
                aria-label={darkMode ? 'Hellen Modus aktivieren' : 'Dunklen Modus aktivieren'}
                title={darkMode ? 'Hellen Modus aktivieren' : 'Dunklen Modus aktivieren'}
                onClick={toggleDarkMode}
                className={`p-2 rounded-lg transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${
                  darkMode ? 'bg-gray-700 text-yellow-400 hover:bg-gray-600 focus-visible:ring-offset-gray-900' : 'bg-gray-200 text-gray-700 hover:bg-gray-300 focus-visible:ring-offset-white'
                }`}
              >
                {darkMode ? <Sun size={20} /> : <Moon size={20} />}
              </button>
              
              <button
                aria-label={mobileMenuOpen ? 'Menü schließen' : 'Menü öffnen'}
                title={mobileMenuOpen ? 'Menü schließen' : 'Menü öffnen'}
                aria-expanded={mobileMenuOpen}
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className={`md:hidden p-2 rounded-lg transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${
                  darkMode ? 'bg-gray-700 text-white hover:bg-gray-600 focus-visible:ring-offset-gray-900' : 'bg-gray-200 text-gray-700 hover:bg-gray-300 focus-visible:ring-offset-white'
                }`}
              >
                {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            </div>
          </div>
        </div>
        
        {mobileMenuOpen && (
          <div className={`md:hidden border-t ${darkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-200 bg-gray-50'}`}>
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => scrollToSection(item.id)}
                  className={`block px-3 py-2 text-base font-medium w-full text-left rounded-md transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'} ${
                    activeSection === item.id 
                      ? (darkMode ? 'text-blue-400 bg-gray-700' : 'text-blue-600 bg-gray-200')
                      : (darkMode ? 'text-gray-300 hover:text-white hover:bg-gray-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-200')
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </header>

      <main id="main-content" tabIndex="-1" className="pt-16 outline-none">
        {/* Part 1 of Component - First sections */}
        {/* Continue in next file... */}
      </main>
    </div>
  );
};

export default RepositoryAnalysis;
