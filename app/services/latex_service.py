from jinja2 import Template
import subprocess
import os
from typing import Dict, Any

class LaTeXService:
    @staticmethod
    def render_template(template_content: str, data: Dict[str, Any]) -> str:
        template = Template(template_content)
        return template.render(**data)

    @staticmethod
    def generate_pdf(latex_content: str, output_path: str) -> bool:
        with open("temp.tex", "w") as f:
            f.write(latex_content)
        
        try:
            subprocess.run(["pdflatex", "temp.tex"], check=True, cwd=os.getcwd())
            os.rename("temp.pdf", output_path)
            # Clean up
            for ext in [".aux", ".log", ".tex"]:
                if os.path.exists(f"temp{ext}"):
                    os.remove(f"temp{ext}")
            return True
        except subprocess.CalledProcessError:
            return False