with open('web/validation_dashboard/src/App.jsx', 'r') as f:
    content = f.read()

old_str = "    const handleScroll = () => {\n"
new_str = """    // Handle scroll events with requestAnimationFrame for better performance
    const handleScroll = () => {
"""
content = content.replace(old_str, new_str)

old_str2 = "    window.addEventListener('scroll', handleScroll, { passive: true });\n"
new_str2 = """    // Use passive listener to avoid blocking the main thread
    window.addEventListener('scroll', handleScroll, { passive: true });
"""
content = content.replace(old_str2, new_str2)

with open('web/validation_dashboard/src/App.jsx', 'w') as f:
    f.write(content)
