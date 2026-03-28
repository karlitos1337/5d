// Part 1: Imports, State Management, and Effects
import { useState, useEffect } from 'react';
import { motion, useScroll, useSpring } from 'framer-motion';
import { Sun, Moon, Menu, X, ChevronDown, ChevronUp } from 'lucide-react';

const AppComponent = () => {
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

  // Citation effect
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

  const sections = [
    { id: 'einleitung', title: 'Einleitung' },
    { id: 'architektur', title: 'Architektur-Analyse' },
    { id: 'domains', title: 'Domain-Struktur' },
    { id: 'schwachstellen', title: 'Identifizierte Schwächen' },
    { id: 'verbesserungen', title: 'Verbesserungsvorschläge' },
    { id: 'feedback', title: 'Feedback-Schleifen' },
    { id: 'fazit', title: 'Fazit' }
  ];

  useEffect(() => {
    // ⚡ Bolt: Optimize scroll performance by using requestAnimationFrame and a ticking flag
    // to throttle expensive DOM queries (offsetTop) and state updates, preventing main-thread
    // blocking during continuous scrolling.
    let ticking = false;

    const handleScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const scrollPosition = window.scrollY + 200;
          
          for (const section of sections) {
            const element = document.getElementById(section.id);
            if (element) {
              const offsetTop = element.offsetTop;
              const height = element.offsetHeight;

              if (scrollPosition >= offsetTop && scrollPosition < offsetTop + height) {
                setActiveSection(section.id);
                break;
              }
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

  return { darkMode, setDarkMode, mobileMenuOpen, setMobileMenuOpen, activeSection, expandedSections, toggleDarkMode, toggleSection, sections, scaleX };
};

export default AppComponent;
