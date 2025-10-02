from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class ResumeBase(BaseModel):
    title: str
    content_json: Dict[str, Any]
    ai_enhanced: bool = False

class ResumeCreate(ResumeBase):
    template_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Software Engineer Resume - Jake's Template",
                "template_id": 1,
                "content_json": {
                    "section_order": ["education", "experience", "projects", "skills", "certifications", "leadership"],
                    
                    "heading": {
                        "full_name": "Jake Ryan",
                        "address": "123 Main Street, Anytown, CA 12345",
                        "phone": "123-456-7890",
                        "email": "jake@su.edu",
                        "linkedin": {
                            "url": "https://linkedin.com/in/jake",
                            "username": "jake"
                        },
                        "github": {
                            "url": "https://github.com/jake",
                            "username": "jake"
                        },
                        "additional_links": [
                            {
                                "icon": "faGlobe",
                                "url": "https://jakery.com",
                                "display_text": "jakery.com"
                            }
                        ]
                    },
                    "education": [
                        {
                            "institution": "Southwestern University",
                            "location": "Georgetown, TX",
                            "degree": "Bachelor of Arts in Computer Science, Minor in Business",
                            "date": "Aug. 2018 -- May 2021",
                            "details": []
                        },
                        {
                            "institution": "Blinn College",
                            "location": "Bryan, TX",
                            "degree": "Associate's in Liberal Arts",
                            "date": "Aug. 2014 -- May 2018",
                            "details": []
                        }
                    ],
                    "experience": [
                        {
                            "company": "Undergraduate Research Assistant",
                            "location": "Texas A&M University",
                            "position": "Research Assistant",
                            "date": "June 2020 -- Present",
                            "responsibilities": [
                                "Developed a REST API using FastAPI and PostgreSQL to store data from learning management systems",
                                "Developed a full-stack web application using Flask, React, PostgreSQL and Docker to analyze GitHub data",
                                "Explored ways to visualize GitHub collaboration in a classroom setting"
                            ]
                        },
                        {
                            "company": "Information Technology Support Specialist",
                            "location": "Southwestern University",
                            "position": "IT Support Specialist",
                            "date": "Sep. 2018 -- Present",
                            "responsibilities": [
                                "Communicate with managers to set up campus computers used on campus",
                                "Assess and troubleshoot computer problems brought by students, faculty and staff",
                                "Maintain upkeep of computers, classroom equipment, and 200 printers across campus"
                            ]
                        },
                        {
                            "company": "Artificial Intelligence Research Assistant",
                            "location": "Southwestern University",
                            "position": "AI Research Assistant",
                            "date": "May 2019 -- July 2019",
                            "responsibilities": [
                                "Explored methods to generate video game dungeons based on evolutionary algorithms",
                                "Discovered methods to grade dungeons based on key performance indicators"
                            ]
                        }
                    ],
                    "projects": [
                        {
                            "name": "Gitlytics",
                            "technologies": ["Python", "Flask", "React", "PostgreSQL", "Docker"],
                            "date": "June 2020 -- Present",
                            "url": "https://github.com/jake/gitlytics",
                            "description": [
                                "Developed a full-stack web application using with Flask serving a REST API with React as the frontend",
                                "Implemented GitHub OAuth to get data from user's repositories",
                                "Visualized GitHub data to show collaboration",
                                "Used Celery and Redis for asynchronous tasks"
                            ]
                        },
                        {
                            "name": "Simple Paintball",
                            "technologies": ["Spigot API", "Java", "Maven", "TravisCI", "Git"],
                            "date": "May 2018 -- May 2020",
                            "url": "",
                            "description": [
                                "Developed a Minecraft server plugin to entertain kids during free time for a previous job",
                                "Published plugin to websites gaining 2K+ downloads and an average 4.5/5-star review",
                                "Implemented continuous delivery using TravisCI to build the plugin upon new a release",
                                "Collaborated with Minecraft server administrators to suggest features and get feedback about the plugin"
                            ]
                        }
                    ],
                    "skills": {
                        "categories": [
                            {
                                "name": "Languages",
                                "items": ["Java", "Python", "C/C++", "SQL (Postgres)", "JavaScript", "HTML/CSS", "R"]
                            },
                            {
                                "name": "Frameworks",
                                "items": ["React", "Node.js", "Flask", "JUnit", "WordPress", "Material-UI", "FastAPI"]
                            },
                            {
                                "name": "Developer Tools",
                                "items": ["Git", "Docker", "TravisCI", "Google Cloud Platform", "VS Code", "Visual Studio", "PyCharm", "IntelliJ", "Eclipse"]
                            },
                            {
                                "name": "Libraries",
                                "items": ["pandas", "NumPy", "Matplotlib"]
                            }
                        ]
                    },
                    "certifications": [
                        {
                            "name": "AWS Certified Solutions Architect",
                            "issuer": "Amazon Web Services",
                            "date": "June 2023",
                            "credential_id": "ABC-123-DEF",
                            "url": "https://aws.amazon.com/certification/"
                        }
                    ],
                    "leadership": [
                        {
                            "organization": "Computer Science Club",
                            "role": "President",
                            "date": "Aug 2020 -- Present",
                            "description": [
                                "Organized weekly tech talks with industry professionals",
                                "Led team of 15 students in hackathon competitions"
                            ]
                        }
                    ]
                },
                "ai_enhanced": False
            }
        }

class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    ai_enhanced: Optional[bool] = None

class ResumeResponse(ResumeBase):
    id: uuid.UUID
    user_id: uuid.UUID
    template_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True