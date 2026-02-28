from jinja2 import Environment


class ResumeGenerator:
    def __init__(self):
        self.env = Environment()

    def generate_html(self, resume_data, template_path, style_path):
        try:
            with open(style_path, encoding="utf-8") as f:
                style_css = f.read()
        except FileNotFoundError as e:
            raise ValueError(
                f"Il file di stile non è stato trovato nel percorso: {style_path}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Errore durante la lettura del file CSS: {e}") from e

        # Genera l'HTML del resume
        return style_css
