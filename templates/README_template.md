# {{brand}} — {{company_name}}

**Fundación:** {{founded}}  
**Sede:** {{hq}}  

## Qué hacemos
{% for a in activities -%}
- {{a}}
{% endfor %}

## Puertos de operación
{% for p in ports -%}
- {{p}}
{% endfor %}

## Flota (selección)
{% for v in fleet_highlights -%}
- **{{v.name}}** — {{v.type}} ({{v.capacity}} pax)
{% endfor %}

## Sostenibilidad
- Bandera Azul: {% if sustainability.blue_flag|length>0 %}{{ sustainability.blue_flag|join(', ') }}{% else %}N/D{% endif %}
- Registro de Huella de Carbono (MITECO): {{ 'Sí' if sustainability.carbon_register else 'No' }}
- Certificación Starlight: {{ 'Sí' if sustainability.starlight else 'No' }}

## Reconocimientos
{% for aw in awards -%}
- {{aw}}
{% endfor %}

## Enlaces
- Web oficial: {{links.website}}
- Repositorio GitHub (documentación): {{links.github_repo}}
- Referencias externas: {{links.references}}
- Logo (Wikimedia Commons): {{links.logo_commons}}

---

### Información legal
- CIF/NIF: {{legal.cif}} · CNAE: {{legal.cnae}} · CEO: {{legal.ceo}}

<!-- Documento generado automáticamente. No editar a mano. -->
