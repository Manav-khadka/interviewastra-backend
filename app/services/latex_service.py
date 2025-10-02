from jinja2 import Environment
import subprocess
import os
import requests
import re
from typing import Dict, Any, List

class LaTeXService:
    
    @staticmethod
    def _escape_latex(text: str) -> str:
        """
        Escape special LaTeX characters in text.
        Only escape backslash if it's not already part of a LaTeX command.
        """
        if not text:
            return ""
        
        result = str(text)
        
        # Characters that need simple escaping (order matters!)
        # Don't escape backslash if it looks like a LaTeX command
        if not ('\\' in result and any(cmd in result for cmd in ['\\textbf', '\\href', '\\emph', '\\textit'])):
            result = result.replace('\\', r'\textbackslash{}')
        
        # Now escape other special characters
        result = result.replace('&', r'\&')
        result = result.replace('%', r'\%')
        result = result.replace('$', r'\$')
        result = result.replace('#', r'\#')
        result = result.replace('_', r'\_')
        result = result.replace('{', r'\{')
        result = result.replace('}', r'\}')
        result = result.replace('~', r'\textasciitilde{}')
        result = result.replace('^', r'\^{}')
        
        return result
    @staticmethod
    def render_template(template_content: str, data: Dict[str, Any]) -> str:
        """
        Render LaTeX template with data.
        Respects section_order if provided in data.
        Template variables should use {{VARIABLE_NAME}} format.
        """
        # Preprocess template to fix common issues
        processed_template = LaTeXService._preprocess_template(template_content)
        
        # Check if custom section ordering is requested
        if "section_order" in data:
            # Build template with custom section order
            rendered_content = LaTeXService._render_with_custom_order(processed_template, data)
        else:
            # Use default template order
            rendered_content = processed_template
            
            # Map JSON structure to template variables
            template_vars = LaTeXService._map_json_to_template_vars(data)
            
            # Replace all template variables
            for var_name, var_value in template_vars.items():
                placeholder = f"{{{{{var_name}}}}}"
                rendered_content = rendered_content.replace(placeholder, str(var_value))
        
        return rendered_content
    
    @staticmethod
    def _render_with_custom_order(template_content: str, data: Dict[str, Any]) -> str:
        """
        Render template with custom section ordering.
        Completely dynamic - supports any section type.
        """
        # Map JSON to template variables for predefined sections
        template_vars = LaTeXService._map_json_to_template_vars(data)
        
        # Get custom section order
        section_order = data.get("section_order", ["education", "experience", "projects", "skills", "certifications", "leadership"])
        
        # Build ordered sections dynamically
        ordered_sections = ""
        
        for section_name in section_order:
            # Skip non-section fields
            if section_name in ["heading", "section_order"]:
                continue
            
            # Check if section exists in data
            if section_name not in data:
                continue
            
            section_data = data[section_name]
            
            # Skip empty sections
            if not section_data:
                continue
            
            # Render section based on data structure
            section_latex = LaTeXService._render_section_dynamically(section_name, section_data, template_vars)
            
            if section_latex:
                ordered_sections += section_latex + "\n"
        
        # Replace the body sections in template
        import re
        
        # Pattern to match from first section header to end of last section
        pattern = r'%-----------EDUCATION-----------.*?(?=\\end\{document\})'
        
        # Replace heading variables first
        result = template_content
        for var in ["FULL_NAME", "ADDRESS_LINE", "PHONE_NUMBER", "EMAIL_ADDRESS", 
                    "LINKEDIN_URL", "LINKEDIN_USERNAME", "GITHUB_URL", "GITHUB_USERNAME", "ADDITIONAL_LINKS"]:
            placeholder = f"{{{{{var}}}}}"
            result = result.replace(placeholder, str(template_vars.get(var, "")))
        
        # Replace the sections with ordered sections
        def replace_func(match):
            return ordered_sections + "\n"
        
        result = re.sub(pattern, replace_func, result, flags=re.DOTALL)
        
        return result
    
    @staticmethod
    def _render_section_dynamically(section_name: str, section_data: Any, template_vars: Dict[str, str]) -> str:
        """
        Dynamically render any section based on its data structure.
        Supports:
        - String: Text paragraph
        - List of strings: Bulleted list
        - List of dicts: Structured items (education, experience, projects, etc.)
        - Dict with 'categories': Skills-like structure
        """
        # Generate title from section name
        title = section_name.replace("_", " ").title()
        section_latex = f"\n%-----------{title.upper()}-----------\n"
        section_latex += f"\\section{{{title}}}\n"
        
        # Render based on data type
        if isinstance(section_data, str):
            # Simple text section
            escaped_text = LaTeXService._escape_latex(section_data)
            section_latex += f"{escaped_text}\n"
            section_latex += "\\vspace{-8pt}\n"
        
        elif isinstance(section_data, list):
            if not section_data:
                return ""
            
            # Check if it's a list of dicts or list of strings
            if isinstance(section_data[0], dict):
                # Structured list - detect type and render accordingly
                section_latex += LaTeXService._render_structured_list(section_name, section_data)
            else:
                # Simple list of strings
                section_latex += "\\begin{itemize}[leftmargin=0.15in]\n"
                for item in section_data:
                    if isinstance(item, str):
                        escaped_item = LaTeXService._escape_latex(item)
                        section_latex += f"  \\item {escaped_item}\n"
                section_latex += "\\end{itemize}\n"
                section_latex += "\\vspace{-8pt}\n"
        
        elif isinstance(section_data, dict):
            # Check if it's a skills-like structure with categories
            if "categories" in section_data:
                section_latex += " \\begin{itemize}[leftmargin=0.15in, label={}]\n"
                section_latex += "    \\small{\\item{\n"
                for category in section_data["categories"]:
                    name = category.get("name", "")
                    items = category.get("items", [])
                    items_string = ", ".join([LaTeXService._escape_latex(str(i)) for i in items])
                    section_latex += f"     \\textbf{{{name}}}{{: {items_string}}} \\\\\n"
                section_latex += "    }}\n"
                section_latex += " \\end{itemize}\n"
                section_latex += "\\vspace{-16pt}\n"
            else:
                # Generic dict - render key-value pairs
                section_latex += "\\begin{itemize}[leftmargin=0.15in]\n"
                for key, value in section_data.items():
                    escaped_key = LaTeXService._escape_latex(str(key))
                    escaped_value = LaTeXService._escape_latex(str(value))
                    section_latex += f"  \\item \\textbf{{{escaped_key}}}: {escaped_value}\n"
                section_latex += "\\end{itemize}\n"
                section_latex += "\\vspace{-8pt}\n"
        
        return section_latex
    
    @staticmethod
    def _render_structured_list(section_name: str, items: List[Dict[str, Any]]) -> str:
        """
        Render a list of structured items (dicts).
        Auto-detects format based on available keys.
        """
        if not items:
            return ""
        
        # Detect the structure based on keys in first item
        first_item = items[0]
        keys = set(first_item.keys())
        
        result = ""
        
        # Education/Experience-like structure (has institution/company, position/degree, location, date)
        if ("institution" in keys or "company" in keys) and "location" in keys and "date" in keys:
            result += "  \\resumeSubHeadingListStart\n"
            for item in items:
                # Determine if it's education or experience-like
                title1 = LaTeXService._escape_latex(item.get("institution") or item.get("company", ""))
                title2 = LaTeXService._escape_latex(item.get("location", ""))
                subtitle1 = LaTeXService._escape_latex(item.get("degree") or item.get("position", ""))
                subtitle2 = LaTeXService._escape_latex(item.get("date", ""))
                
                result += f"    \\resumeSubheading\n"
                result += f"      {{{title1}}}{{{title2}}}\n"
                result += f"      {{{subtitle1}}}{{{subtitle2}}}\n"
                
                # Add details/responsibilities if present
                details = item.get("details") or item.get("responsibilities") or item.get("description", [])
                if details and isinstance(details, list):
                    result += "      \\resumeItemListStart\n"
                    for detail in details:
                        escaped_detail = LaTeXService._escape_latex(str(detail))
                        result += f"        \\resumeItem{{{escaped_detail}}}\n"
                    result += "      \\resumeItemListEnd\n"
            result += "  \\resumeSubHeadingListEnd\n"
            result += "\\vspace{-16pt}\n"
        
        # Project-like structure (has name, technologies, description)
        elif "name" in keys and ("technologies" in keys or "description" in keys):
            result += "    \\resumeSubHeadingListStart\n"
            for idx, item in enumerate(items):
                name = LaTeXService._escape_latex(item.get("name", ""))
                technologies = item.get("technologies", [])
                date = LaTeXService._escape_latex(item.get("date", ""))
                url = item.get("url", "")
                
                tech_string = ", ".join([LaTeXService._escape_latex(str(t)) for t in technologies]) if technologies else ""
                if url and url.strip():
                    project_title = f"\\textbf{{\\href{{{url}}}{{{name}}}}} $|$ \\emph{{{tech_string}}}"
                else:
                    project_title = f"\\textbf{{{name}}}" + (f" $|$ \\emph{{{tech_string}}}" if tech_string else "")
                
                result += f"      \\resumeProjectHeading\n"
                result += f"          {{{project_title}}}{{{date}}}\n"
                
                # Add description
                description = item.get("description", [])
                if description:
                    if isinstance(description, list):
                        result += "          \\resumeItemListStart\n"
                        for desc in description:
                            escaped_desc = LaTeXService._escape_latex(str(desc))
                            result += f"            \\resumeItem{{{escaped_desc}}}\n"
                        result += "          \\resumeItemListEnd\n"
                    elif isinstance(description, str):
                        result += "          \\resumeItemListStart\n"
                        escaped_desc = LaTeXService._escape_latex(description)
                        result += f"            \\resumeItem{{{escaped_desc}}}\n"
                        result += "          \\resumeItemListEnd\n"
                
                # Add spacing AFTER the entire project entry (between projects only)
                if idx < len(items) - 1:
                    result += "      \\vspace{-16pt}\n"
            
            result += "    \\resumeSubHeadingListEnd\n"
        
        # Certification-like structure (has name, issuer, date)
        elif "name" in keys and "issuer" in keys:
            result += " \\begin{itemize}[leftmargin=0.15in, label={}]\n"
            result += "    \\small{\\item{\n"
            for item in items:
                name = LaTeXService._escape_latex(item.get("name", ""))
                issuer = LaTeXService._escape_latex(item.get("issuer", ""))
                date = LaTeXService._escape_latex(item.get("date", ""))
                url = item.get("url", "")
                
                if url and url.strip():
                    result += f"     \\textbf{{\\href{{{url}}}{{{name}}}}} - {issuer} ({date}) \\\\\n"
                else:
                    result += f"     \\textbf{{{name}}} - {issuer} ({date}) \\\\\n"
            result += "    }}\n"
            result += " \\end{itemize}\n"
            result += " \\vspace{-16pt}\n"
        
        # Leadership/Organization-like structure (has organization/role)
        elif ("organization" in keys or "role" in keys) and "date" in keys:
            result += "    \\resumeSubHeadingListStart\n"
            for item in items:
                org = LaTeXService._escape_latex(item.get("organization", ""))
                role = LaTeXService._escape_latex(item.get("role", ""))
                date = LaTeXService._escape_latex(item.get("date", ""))
                
                result += f"      \\resumeSubheading\n"
                result += f"        {{{org}}}{{}}\n"
                result += f"        {{{role}}}{{{date}}}\n"
                
                # Add description
                description = item.get("description", [])
                if description and isinstance(description, list):
                    result += "        \\resumeItemListStart\n"
                    for desc in description:
                        escaped_desc = LaTeXService._escape_latex(str(desc))
                        result += f"          \\resumeItem{{{escaped_desc}}}\n"
                    result += "        \\resumeItemListEnd\n"
            result += "    \\resumeSubHeadingListEnd\n"
        
        # Generic structured list - render as simple items
        else:
            result += "\\begin{itemize}[leftmargin=0.15in]\n"
            for item in items:
                # Try to create a meaningful representation
                if "name" in item:
                    name = LaTeXService._escape_latex(str(item.get("name", "")))
                    result += f"  \\item \\textbf{{{name}}}"
                    # Add other fields
                    for key, value in item.items():
                        if key != "name" and value:
                            escaped_value = LaTeXService._escape_latex(str(value))
                            result += f" - {escaped_value}"
                    result += "\n"
                else:
                    # Just list all key-value pairs
                    item_text = ", ".join([f"{k}: {v}" for k, v in item.items() if v])
                    escaped_text = LaTeXService._escape_latex(item_text)
                    result += f"  \\item {escaped_text}\n"
            result += "\\end{itemize}\n"
            result += "\\vspace{-8pt}\n"
        
        return result
    
    @staticmethod
    def _preprocess_template(template_content: str) -> str:
        """
        Preprocess template to fix common LaTeX issues and improve spacing.
        Standardizes spacing across all sections to match education/experience.
        Optimizes for ATS-friendly formatting with perfect alignment.
        """
        # Comment out glyphtounicode
        result = template_content.replace(
            '\\input{glyphtounicode}',
            '% \\input{glyphtounicode} % Commented out - file not available'
        )
        
        # Remove extra vspace after Projects section header
        result = result.replace(
            '%-----------PROJECTS-----------\n\\section{Projects}\n    \\vspace{-5pt}',
            '%-----------PROJECTS-----------\n\\section{Projects}'
        )
        
        # Standardize all -15pt spacing to -16pt
        result = result.replace('\\vspace{-15pt}', '\\vspace{-16pt}')
        
        # Ensure ATS-friendly alignment settings
        if '\\raggedright' not in result:
            result = result.replace('\\raggedbottom', '\\raggedbottom\n\\raggedright')
        
        # Fix broken tabular commands that cause LaTeX errors
        # Replace incorrectly split tabular commands with proper single-line versions
        result = result.replace(
            '\\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}\n      \\textbf{#1} & \\textbf{\\small #2} \\\\\n      \\textit{\\small#3} & \\textit{\\small #4} \\\\\n    \\end{tabular*}',
            '\\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}\\textbf{#1} & \\textbf{\\small #2} \\\\\\textit{\\small#3} & \\textit{\\small #4} \\\\ \\end{tabular*}'
        )
        
        result = result.replace(
            '\\begin{tabular*}{1.001\\textwidth}{l@{\\extracolsep{\\fill}}r}\n      \\small#1 & \\textbf{\\small #2}\\\\\n    \\end{tabular*}',
            '\\begin{tabular*}{1.001\\textwidth}{l@{\\extracolsep{\\fill}}r}\\small#1 & \\textbf{\\small #2}\\\\ \\end{tabular*}'
        )
        
        # Ensure proper ATS alignment - no multicol, single column only
        result = result.replace('\\usepackage{multicol}', '% \\usepackage{multicol} % Disabled for ATS compatibility')
        result = result.replace('\\setlength{\\multicolsep}{-3.0pt}', '')
        result = result.replace('\\setlength{\\columnsep}{-1pt}', '')
        
        return result
    
    @staticmethod
    def _map_json_to_template_vars(data: Dict[str, Any]) -> Dict[str, str]:
        """
        Map JSON resume data to LaTeX template variables.
        Converts structured JSON into flat template variable mappings.
        """
        vars_dict = {}
        
        # HEADING SECTION
        if "heading" in data:
            heading = data["heading"]
            vars_dict["FULL_NAME"] = heading.get("full_name", "")
            vars_dict["ADDRESS_LINE"] = heading.get("address", "")
            vars_dict["PHONE_NUMBER"] = heading.get("phone", "")
            vars_dict["EMAIL_ADDRESS"] = heading.get("email", "")
            
            # LinkedIn
            if "linkedin" in heading:
                vars_dict["LINKEDIN_URL"] = heading["linkedin"].get("url", "")
                vars_dict["LINKEDIN_USERNAME"] = heading["linkedin"].get("username", "")
            else:
                vars_dict["LINKEDIN_URL"] = ""
                vars_dict["LINKEDIN_USERNAME"] = ""
            
            # GitHub
            if "github" in heading:
                vars_dict["GITHUB_URL"] = heading["github"].get("url", "")
                vars_dict["GITHUB_USERNAME"] = heading["github"].get("username", "")
            else:
                vars_dict["GITHUB_URL"] = ""
                vars_dict["GITHUB_USERNAME"] = ""
            
            # Additional links
            additional_links = ""
            if "additional_links" in heading and heading["additional_links"]:
                for link in heading["additional_links"]:
                    icon = link.get("icon", "faLink")
                    url = link.get("url", "")
                    display_text = link.get("display_text", url)
                    additional_links += f"~\n    \\href{{{url}}}{{\\raisebox{{-0.2\\height}}\\{icon}\\ \\underline{{{display_text}}}}}"
            vars_dict["ADDITIONAL_LINKS"] = additional_links
        
        # EDUCATION SECTION
        if "education" in data:
            education_section = LaTeXService._build_education_section(data["education"])
            vars_dict["EDUCATION_SECTION"] = education_section
        else:
            vars_dict["EDUCATION_SECTION"] = ""
        
        # EXPERIENCE SECTION
        if "experience" in data:
            experience_section = LaTeXService._build_experience_section(data["experience"])
            vars_dict["EXPERIENCE_SECTION"] = experience_section
        else:
            vars_dict["EXPERIENCE_SECTION"] = ""
        
        # PROJECTS SECTION
        if "projects" in data:
            projects_section = LaTeXService._build_projects_section(data["projects"])
            vars_dict["PROJECTS_SECTION"] = projects_section
        else:
            vars_dict["PROJECTS_SECTION"] = ""
        
        # SKILLS SECTION
        if "skills" in data:
            skills_section = LaTeXService._build_skills_section(data["skills"])
            vars_dict["SKILLS_SECTION"] = skills_section
        else:
            vars_dict["SKILLS_SECTION"] = ""
        
        # CERTIFICATIONS SECTION (Optional)
        if "certifications" in data and data["certifications"]:
            certifications_section = LaTeXService._build_certifications_section(data["certifications"])
            vars_dict["CERTIFICATIONS_SECTION"] = certifications_section
        else:
            vars_dict["CERTIFICATIONS_SECTION"] = ""
        
        # LEADERSHIP SECTION (Optional)
        if "leadership" in data and data["leadership"]:
            leadership_section = LaTeXService._build_leadership_section(data["leadership"])
            vars_dict["LEADERSHIP_SECTION"] = leadership_section
        else:
            vars_dict["LEADERSHIP_SECTION"] = ""
        
        return vars_dict
    
    @staticmethod
    def _build_education_section(education_list: List[Dict[str, Any]]) -> str:
        """Build education section using \\resumeSubheading command."""
        section = ""
        for edu in education_list:
            institution = LaTeXService._escape_latex(edu.get("institution", ""))
            location = LaTeXService._escape_latex(edu.get("location", ""))
            degree = LaTeXService._escape_latex(edu.get("degree", ""))
            date = LaTeXService._escape_latex(edu.get("date", ""))
            
            section += f"    \\resumeSubheading\n"
            section += f"      {{{institution}}}{{{location}}}\n"
            section += f"      {{{degree}}}{{{date}}}\n"
            
            # Add details if present
            if "details" in edu and edu["details"]:
                section += "      \\resumeItemListStart\n"
                for detail in edu["details"]:
                    escaped_detail = LaTeXService._escape_latex(detail)
                    section += f"        \\resumeItem{{{escaped_detail}}}\n"
                section += "      \\resumeItemListEnd\n"
        
        return section
    
    @staticmethod
    def _build_experience_section(experience_list: List[Dict[str, Any]]) -> str:
        """Build experience section using \\resumeSubheading command."""
        section = ""
        for exp in experience_list:
            company = LaTeXService._escape_latex(exp.get("company", ""))
            location = LaTeXService._escape_latex(exp.get("location", ""))
            position = LaTeXService._escape_latex(exp.get("position", ""))
            date = LaTeXService._escape_latex(exp.get("date", ""))
            
            section += f"    \\resumeSubheading\n"
            section += f"      {{{company}}}{{{location}}}\n"
            section += f"      {{{position}}}{{{date}}}\n"
            
            # Add responsibilities
            if "responsibilities" in exp and exp["responsibilities"]:
                section += "      \\resumeItemListStart\n"
                for resp in exp["responsibilities"]:
                    escaped_resp = LaTeXService._escape_latex(resp)
                    section += f"        \\resumeItem{{{escaped_resp}}}\n"
                section += "      \\resumeItemListEnd\n"
        
        return section
    
    @staticmethod
    def _build_projects_section(projects_list: List[Dict[str, Any]]) -> str:
        """Build projects section using \\resumeProjectHeading command."""
        section = ""
        for proj in projects_list:
            name = LaTeXService._escape_latex(proj.get("name", ""))
            technologies = proj.get("technologies", [])
            date = LaTeXService._escape_latex(proj.get("date", ""))
            url = proj.get("url", "")
            
            # Build project heading - don't escape tech names as they're usually simple
            tech_string = ", ".join([LaTeXService._escape_latex(t) for t in technologies]) if technologies else ""
            if url and url.strip():
                # URL itself shouldn't be escaped
                project_title = f"\\textbf{{\\href{{{url}}}{{{name}}}}} $|$ \\emph{{{tech_string}}}"
            else:
                project_title = f"\\textbf{{{name}}} $|$ \\emph{{{tech_string}}}"
            
            section += f"      \\resumeProjectHeading\n"
            section += f"          {{{project_title}}}{{{date}}}\n"
            
            # Add description points
            if "description" in proj and proj["description"]:
                section += "          \\resumeItemListStart\n"
                for desc in proj["description"]:
                    escaped_desc = LaTeXService._escape_latex(desc)
                    section += f"            \\resumeItem{{{escaped_desc}}}\n"
                section += "          \\resumeItemListEnd\n"
            
            # Add consistent vertical spacing between project items (not after last one)
            # This will be handled by the template's end section spacing
        
        return section
    
    @staticmethod
    def _build_skills_section(skills_data: Dict[str, Any]) -> str:
        """Build skills section with categories."""
        section = ""
        if "categories" in skills_data:
            skill_lines = []
            for category in skills_data["categories"]:
                name = category.get("name", "")
                items = category.get("items", [])
                items_string = ", ".join(items) if items else ""
                skill_lines.append(f"     \\textbf{{{name}}}{{: {items_string}}} \\\\")
            section = "\n".join(skill_lines)
        return section
    
    @staticmethod
    def _build_certifications_section(certifications_list: List[Dict[str, Any]]) -> str:
        """Build certifications section (optional)."""
        if not certifications_list:
            return ""
        
        section = "\\section{Certifications}\n"
        section += " \\begin{itemize}[leftmargin=0.15in, label={}]\n"
        section += "    \\small{\\item{\n"
        
        for cert in certifications_list:
            name = cert.get("name", "")
            issuer = cert.get("issuer", "")
            date = cert.get("date", "")
            url = cert.get("url", "")
            
            if url:
                section += f"     \\textbf{{\\href{{{url}}}{{{name}}}}} - {issuer} ({date}) \\\\\n"
            else:
                section += f"     \\textbf{{{name}}} - {issuer} ({date}) \\\\\n"
        
        section += "    }}\n"
        section += " \\end{itemize}\n"
        section += " \\vspace{-16pt}\n"
        
        return section
    
    @staticmethod
    def _build_leadership_section(leadership_list: List[Dict[str, Any]]) -> str:
        """Build leadership/extracurricular section (optional)."""
        if not leadership_list:
            return ""
        
        section = "\\section{Leadership / Extracurricular}\n"
        section += "    \\resumeSubHeadingListStart\n"
        
        for lead in leadership_list:
            organization = lead.get("organization", "")
            role = lead.get("role", "")
            date = lead.get("date", "")
            
            section += f"      \\resumeSubheading\n"
            section += f"        {{{organization}}}{{}}\n"
            section += f"        {{{role}}}{{{date}}}\n"
            
            if "description" in lead and lead["description"]:
                section += "        \\resumeItemListStart\n"
                for desc in lead["description"]:
                    section += f"          \\resumeItem{{{desc}}}\n"
                section += "        \\resumeItemListEnd\n"
        
        section += "    \\resumeSubHeadingListEnd\n"
        
        return section

    @staticmethod
    def generate_pdf(latex_content: str, output_path: str, use_online: bool = True) -> tuple[bool, str]:
        """
        Generate PDF from LaTeX content.
        Args:
            latex_content: The LaTeX source code
            output_path: Where to save the PDF
            use_online: If True, try online compilation first (no LaTeX installation needed)
        Returns:
            tuple of (success: bool, message: str)
        """
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Try online compilation first if enabled
        if use_online:
            print("Attempting online LaTeX compilation...")
            success, message = LaTeXService._compile_online(latex_content, output_path)
            if success:
                print(f"Online compilation succeeded: {message}")
                return True, message
            else:
                print(f"Online compilation failed: {message}")
                # Continue to try local compilation as fallback
        
        # Try local pdflatex as fallback
        if LaTeXService._is_pdflatex_available():
            print("Attempting local pdflatex compilation...")
            return LaTeXService._compile_local(latex_content, output_path)
        
        # Both online and local failed - save tex file
        tex_path = output_path.replace('.pdf', '.tex')
        try:
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(latex_content)
            return False, f"Both online and local compilation failed. LaTeX source saved to {tex_path}"
        except Exception as e:
            return False, f"Failed to save LaTeX file: {str(e)}"
    
    @staticmethod
    def _compile_online(latex_content: str, output_path: str) -> tuple[bool, str]:
        """
        Compile LaTeX using online service.
        No local LaTeX installation required!
        """
        # Service 1: LaTeX.Online (primary)
        try:
            print("Trying LaTeX.Online service...")
            url = "https://latexonline.cc/compile"
            files = {'file': ('resume.tex', latex_content.encode('utf-8'), 'text/plain')}
            
            response = requests.post(url, files=files, timeout=45)
            print(f"LaTeX.Online response: Status={response.status_code}, Content-Length={len(response.content)}")
            
            if response.status_code == 200 and len(response.content) > 1000:  # Valid PDF
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print("PDF successfully generated using LaTeX.Online")
                return True, "Compiled using LaTeX.Online"
            else:
                print(f"LaTeX.Online failed: Status {response.status_code}")
        except requests.exceptions.Timeout:
            print("LaTeX.Online timed out")
        except Exception as e:
            print(f"LaTeX.Online error: {str(e)}")
        
        # Service 2: Alternative - Direct HTTP compile
        try:
            print("Trying alternative online service...")
            url = "https://texlive.net/cgi-bin/latexcgi"
            data = {
                'filecontents': latex_content,
                'filename': 'resume.tex',
                'engine': 'pdflatex'
            }
            response = requests.post(url, data=data, timeout=45)
            print(f"Alternative service response: Status={response.status_code}")
            
            if response.status_code == 200 and len(response.content) > 1000:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print("PDF successfully generated using alternative service")
                return True, "Compiled using TeXLive.net"
        except Exception as e:
            print(f"Alternative service error: {str(e)}")
        
        return False, "All online compilation services failed. The LaTeX syntax may have errors, or the services are unavailable."
    
    @staticmethod
    def _compile_local(latex_content: str, output_path: str) -> tuple[bool, str]:
        """Compile LaTeX using local pdflatex installation."""
        temp_tex = "temp_resume.tex"
        try:
            with open(temp_tex, "w", encoding="utf-8") as f:
                f.write(latex_content)
            
            # Run pdflatex twice for proper rendering
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", temp_tex],
                check=True,
                cwd=os.getcwd(),
                capture_output=True,
                text=True
            )
            
            # Check if PDF was created
            temp_pdf = "temp_resume.pdf"
            if os.path.exists(temp_pdf):
                os.rename(temp_pdf, output_path)
                # Clean up auxiliary files
                for ext in [".aux", ".log", ".tex", ".out"]:
                    temp_file = f"temp_resume{ext}"
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                return True, "PDF generated successfully using local pdflatex"
            else:
                return False, "PDF file was not created"
                
        except subprocess.CalledProcessError as e:
            error_msg = f"pdflatex compilation failed: {e.stderr if e.stderr else str(e)}"
            # Clean up on failure
            for ext in [".aux", ".log", ".tex", ".out", ".pdf"]:
                temp_file = f"temp_resume{ext}"
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            return False, error_msg
        except FileNotFoundError:
            return False, "pdflatex command not found. Please install TeX Live or MiKTeX."
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    @staticmethod
    def _is_pdflatex_available() -> bool:
        """Check if pdflatex is available in the system."""
        try:
            result = subprocess.run(
                ["pdflatex", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False