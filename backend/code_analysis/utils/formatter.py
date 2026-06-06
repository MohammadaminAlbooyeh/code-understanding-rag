import json
import yaml


class Formatter:
    def __init__(self):
        pass

    def format_as_json(self, data: dict) -> str:
        return json.dumps(data, indent=2, default=str)

    def format_as_yaml(self, data: dict) -> str:
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)

    def format_as_markdown(self, data: dict) -> str:
        lines = []
        for key, value in data.items():
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            if isinstance(value, dict):
                for k, v in value.items():
                    lines.append(f"- **{k.replace('_', ' ').title()}**: {v}")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            lines.append(f"- **{k.replace('_', ' ').title()}**: {v}")
                        lines.append("")
                    else:
                        lines.append(f"- {item}")
            else:
                lines.append(str(value))
            lines.append("")
        return "\n".join(lines)

    def format_as_html(self, data: dict) -> str:
        html = ['<div class="code-analysis">']
        for key, value in data.items():
            html.append(f'<section class="{key}">')
            html.append(f'<h2>{key.replace("_", " ").title()}</h2>')
            if isinstance(value, dict):
                html.append('<dl>')
                for k, v in value.items():
                    html.append(f'<dt>{k.replace("_", " ").title()}</dt>')
                    html.append(f'<dd>{v}</dd>')
                html.append('</dl>')
            elif isinstance(value, list):
                html.append('<ul>')
                for item in value:
                    html.append(f'<li>{item}</li>')
                html.append('</ul>')
            else:
                html.append(f'<p>{value}</p>')
            html.append('</section>')
        html.append('</div>')
        return "\n".join(html)
