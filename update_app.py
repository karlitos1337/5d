import re

with open('web/validation_dashboard/src/App.jsx', 'r') as f:
    content = f.read()

# Desktop Nav
content = content.replace(
    '''                <button
                  key={section.id}
                  onClick={() => scrollToSection(section.id)}
                  className={`text-sm font-medium transition-colors duration-200 ${
                    activeSection === section.id
                      ? (darkMode ? 'text-blue-400' : 'text-blue-600')
                      : (darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-900')
                  }`}
                >''',
    '''                <button
                  key={section.id}
                  onClick={() => scrollToSection(section.id)}
                  className={`text-sm font-medium transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'} rounded-sm ${
                    activeSection === section.id
                      ? (darkMode ? 'text-blue-400' : 'text-blue-600')
                      : (darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-900')
                  }`}
                >'''
)

# Dark Mode
content = content.replace(
    '''              <button
                aria-label={darkMode ? 'Hellen Modus aktivieren' : 'Dunklen Modus aktivieren'}
                onClick={toggleDarkMode}
                className={`p-2 rounded-lg transition-colors duration-200 ${
                  darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                }`}
              >''',
    '''              <button
                aria-label={darkMode ? 'Hellen Modus aktivieren' : 'Dunklen Modus aktivieren'}
                title={darkMode ? 'Hellen Modus aktivieren' : 'Dunklen Modus aktivieren'}
                onClick={toggleDarkMode}
                className={`p-2 rounded-lg transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'} ${
                  darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                }`}
              >'''
)

# Mobile Menu Toggle
content = content.replace(
    '''              <button
                aria-label={mobileMenuOpen ? 'Menü schließen' : 'Menü öffnen'}
                aria-expanded={mobileMenuOpen}
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className={`md:hidden p-2 rounded-lg transition-colors duration-200 ${
                  darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                }`}
              >''',
    '''              <button
                aria-label={mobileMenuOpen ? 'Menü schließen' : 'Menü öffnen'}
                title={mobileMenuOpen ? 'Menü schließen' : 'Menü öffnen'}
                aria-expanded={mobileMenuOpen}
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className={`md:hidden p-2 rounded-lg transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'} ${
                  darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                }`}
              >'''
)

# Mobile Nav
content = content.replace(
    '''                <button
                  key={section.id}
                  onClick={() => scrollToSection(section.id)}
                  className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${
                    activeSection === section.id
                      ? (darkMode ? 'text-blue-400 bg-gray-800' : 'text-blue-600 bg-gray-100')
                      : (darkMode ? 'text-gray-300 hover:text-white hover:bg-gray-800' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100')
                  }`}
                >''',
    '''                <button
                  key={section.id}
                  onClick={() => scrollToSection(section.id)}
                  className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${darkMode ? 'focus-visible:ring-offset-gray-900' : 'focus-visible:ring-offset-white'} ${
                    activeSection === section.id
                      ? (darkMode ? 'text-blue-400 bg-gray-800' : 'text-blue-600 bg-gray-100')
                      : (darkMode ? 'text-gray-300 hover:text-white hover:bg-gray-800' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100')
                  }`}
                >'''
)

with open('web/validation_dashboard/src/App.jsx', 'w') as f:
    f.write(content)
