def opengamma_template_manager(template_type: str):
    """
    Returns pre-formatted task templates for common sandbox operations.
    Types: ['REFACTOR', 'TEST_FEATURE', 'GENERATE_DOCS', 'DEBUG_LOGS']
    """
    templates = {
        "REFACTOR": """[REFACTOR TASK]
Objective: Refactor the following logic to improve performance/readability:
Source File: ./skills/{filename}
Focus: {specific_logic}
Constraint: Maintain backward compatibility with the existing JSON schema.""",
        
        "TEST_FEATURE": """[TESTING TASK]
Objective: Implement a comprehensive unit test for the '{feature_name}' skill.
Target File: ./skills/{feature_name}.py
Output File: ./test_{feature_name}.py
Requirement: Use standard Python 'unittest' and ensure 100% path coverage.""",
        
        "GENERATE_DOCS": """[DOCUMENTATION TASK]
Objective: Generate detailed docstrings and a README section for the '{skill_name}' tool.
Focus: Input/Output schemas and error handling examples.""",
        
        "DEBUG_LOGS": """[DEBUGGING TASK]
Objective: Analyze the provided execution logs and identify the root cause of the failure.
Logs: {log_snippet}
Requirement: Provide a fix script or a replacement for the failing code block."""
    }
    
    return templates.get(template_type.upper(), "Template type not found. Available: REFACTOR, TEST_FEATURE, GENERATE_DOCS, DEBUG_LOGS")

# Schema for registration
schema = {
    "name": "opengamma_template_manager",
    "description": "Provides standardized task templates for common OpenGamma sandbox operations.",
    "input_schema": {
        "type": "object",
        "properties": {
            "template_type": {"type": "string", "enum": ["REFACTOR", "TEST_FEATURE", "GENERATE_DOCS", "DEBUG_LOGS"]}
        },
        "required": ["template_type"]
    }
}
