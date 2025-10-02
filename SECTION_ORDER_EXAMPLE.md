# Resume Section Ordering Guide

## Overview
You can now control the order of sections in your resume by including a `section_order` array in your `content_json`.

## Default Section Order
If you don't specify `section_order`, sections appear in this default order:
1. Education
2. Experience
3. Projects
4. Technical Skills
5. Certifications (if present)
6. Leadership (if present)

## Custom Section Ordering

### Example 1: Experience First (Most Common for Professionals)
```json
{
  "title": "Senior Software Engineer Resume",
  "template_id": 1,
  "content_json": {
    "section_order": ["experience", "skills", "projects", "education", "certifications", "leadership"],
    "heading": { ... },
    "experience": [ ... ],
    "skills": { ... },
    "projects": [ ... ],
    "education": [ ... ]
  }
}
```

### Example 2: Skills First (Good for Career Changers)
```json
{
  "section_order": ["skills", "projects", "experience", "education"],
  ...
}
```

### Example 3: Projects First (Good for Students/Bootcamp Grads)
```json
{
  "section_order": ["education", "projects", "skills", "experience"],
  ...
}
```

### Example 4: Education First (Good for Recent Graduates)
```json
{
  "section_order": ["education", "skills", "projects", "experience", "leadership"],
  ...
}
```

## Available Section Names
- `"education"` - Education Section
- `"experience"` - Work Experience Section
- `"projects"` - Projects Section
- `"skills"` - Technical Skills Section
- `"certifications"` - Certifications Section (optional)
- `"leadership"` - Leadership/Extracurricular Section (optional)

## Important Notes

1. **Order Matters**: The sections will appear in the exact order you specify in the array
2. **Skip Sections**: Only include section names you want to appear. Omitted sections won't be rendered
3. **Empty Sections**: Empty sections are automatically skipped even if listed in `section_order`
4. **Heading Always First**: The heading (name, contact info) always appears first, regardless of `section_order`

## Complete Example with Custom Order

```json
{
  "title": "Full Stack Developer Resume - Experience First",
  "template_id": 1,
  "ai_enhanced": false,
  "content_json": {
    "section_order": ["experience", "skills", "projects", "education", "certifications"],
    
    "heading": {
      "full_name": "Jane Developer",
      "address": "San Francisco, CA",
      "phone": "555-123-4567",
      "email": "jane@example.com",
      "linkedin": {
        "url": "https://linkedin.com/in/janedev",
        "username": "janedev"
      },
      "github": {
        "url": "https://github.com/janedev",
        "username": "janedev"
      }
    },
    
    "experience": [
      {
        "company": "Tech Corp",
        "location": "San Francisco, CA",
        "position": "Senior Full Stack Developer",
        "date": "Jan 2020 -- Present",
        "responsibilities": [
          "Led team of 5 developers building scalable web applications",
          "Reduced page load time by 60% through optimization"
        ]
      }
    ],
    
    "skills": {
      "categories": [
        {
          "name": "Languages",
          "items": ["Python", "JavaScript", "TypeScript", "Go"]
        },
        {
          "name": "Frameworks",
          "items": ["React", "Node.js", "FastAPI", "Django"]
        }
      ]
    },
    
    "projects": [ ... ],
    "education": [ ... ],
    "certifications": [ ... ]
  }
}
```

## Testing Section Order

1. **Create resume with custom order**:
   ```bash
   POST /resumes/
   # Include section_order in content_json
   ```

2. **Generate LaTeX**:
   ```bash
   POST /resumes/{resume_id}/generate-pdf
   ```

3. **Verify order** in the generated `.tex` file

## Use Cases by Career Stage

### 🎓 Recent Graduate / Student
```json
"section_order": ["education", "projects", "skills", "experience", "leadership"]
```
*Highlights education and academic projects*

### 💼 Mid-Level Professional (2-5 years)
```json
"section_order": ["experience", "skills", "projects", "education"]
```
*Emphasizes professional experience*

### 🚀 Senior Professional (5+ years)
```json
"section_order": ["experience", "skills", "certifications", "education"]
```
*Focus on experience and credentials, may omit projects*

### 🔄 Career Changer
```json
"section_order": ["skills", "projects", "experience", "education"]
```
*Leads with transferable skills and relevant projects*

### 🏗️ Project-Heavy Role (Consultant, Freelancer)
```json
"section_order": ["projects", "skills", "experience", "education"]
```
*Showcases portfolio of work*
