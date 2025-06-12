from liquid import Template

def validate_liquid_template(template_str: str, payloads: list[dict]) -> list[str]:
    errors = []
    template = Template(template_str)
    for i, data in enumerate(payloads):
        try:
            template.render(data)
        except Exception as e:
            errors.append(f"Payload #{i} error: {str(e)}")
    return errors