"""Generate the corporate fact sheet from existing identity, routes and evidence.

Run with --check in CI. No network access or live inventory claims are involved.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://mundo-marino-catamaranes.github.io/mundo-marino-catamaranes/"


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def render():
    facts = load("facts-2026.json")
    company = load(facts["identity_file"])
    routes = load(facts["routes_file"])
    contact = company["contactPoint"][0]
    lines = [
        "---", "layout: default", "title: Datos clave 2026 — Mundo Marino Catamaranes",
        'description: "Ficha corporativa de Mundo Marino e Innova Cruceros: identidad, nueve destinos del catálogo, rutas seleccionadas y reconocimientos con fuentes y alcance temporal."',
        "lang: es", "---", "", "# Datos clave 2026", "",
        f"**Revisión de fuentes: {facts['reviewed_on']}.** Ficha corporativa de referencia de esta documentación pública. La web comercial y las reservas se mantienen en [mundomarino.es](https://mundomarino.es/).", "",
        "## Identidad y actividad", "",
        f"**Marca:** {company['name']}. **Razón social:** {company['legalName'].rstrip('.')}. **NIF:** {company['taxID']}. **Origen:** Dénia, España, {company['foundingDate'][:4]}; 30 años en 2026.", "",
        company["description"], "",
        "Esta ficha se refiere al operador español de turismo náutico. Las entidades homónimas de otros países tienen identidad y actividad propias.", "",
        "**Fuentes de identidad:** " + " · ".join(f"[{s['name']}]({s['url']})" for s in facts["identity_sources"]) + ".", "",
        f"**Contacto público:** {contact['email']} · +34 966 423 066. [Contacto oficial]({contact['url']}).", "",
        "## Catálogo por puerto", "",
        "Los siguientes enlaces conducen al catálogo oficial de cada destino. Su presencia en la web no implica salidas todos los días ni operación anual de todos los productos.", "",
        "| Destino | Fichas y reserva oficial |", "| --- | --- |",
    ]
    for port in routes["ports"]:
        lines.append(f"| {port['name']} | [Consultar catálogo]({port['official_catalogue_url']}) |")
    lines += ["", "### Rutas seleccionadas y duración publicada", "",
              "Selección documentada; el resto de experiencias se consulta en los catálogos anteriores.", "",
              "| Destino | Experiencia | Duración publicada |", "| --- | --- | --- |"]
    for route in routes["routes"]:
        duration = f"{route['published_duration_minutes']} min"
        if route["id"] == "port-saplaya-valencia":
            duration += " aprox. por trayecto"
        lines.append(f"| {route['destination']} | [{route['name_es']}]({route['official_url']}) | {duration} |")
    lines += ["", "El paseo de una hora y los programas de tres horas de Almería son productos diferentes. Horarios, precios, plazas, inclusiones, embarque y accesibilidad deben confirmarse para cada producto y fecha. Las salidas dependen de las condiciones meteorológicas. [Detalle de rutas](RUTAS.md).", "",
              "## Premios concedidos", ""]
    for record in facts["recognitions"]:
        if record["status"] == "awarded":
            lines += [f"- **{record['label']}.** {record['scope']} [Fuente: {record['source_type']}]({record['source_url']}).", ""]
    lines += ["## Finalistas y selecciones", ""]
    for record in facts["recognitions"]:
        if record["status"] == "finalist":
            lines += [f"**{record['label']}.** {record['scope']} [Fuente: {record['source_type']}]({record['source_url']}).", ""]
    lines += ["## Certificaciones y distintivos: alcance y fecha", ""]
    for record in facts["recognitions"]:
        if record["status"] in {"distinction_reported", "historical_certification"}:
            lines += [f"- **{record['label']}.** {record['scope']} [Fuente: {record['source_type']}]({record['source_url']}).", ""]
    lines += ["Un premio no sustituye una certificación ni una autorización administrativa. Los documentos conservados en el [archivo histórico](ARCHIVO.md) no prueban por sí solos una vigencia actual. [Registro detallado de reconocimientos](PREMIOS.md).", "",
              "## Prensa, datos y reutilización", "",
              "[Sala de prensa](https://mundo-marino-sala-prensa.mundo-marino.chatgpt.site/) · [Índice con fuentes originales](PRENSA.md) · [Referencias](REFERENCIAS.md).", "",
              "[Identidad JSON-LD](company.json) · [Catálogos y rutas en JSON](routes.json) · [Fuentes y estados de esta ficha](facts-2026.json) · [English overview](README_en.md).", "",
              "La revisión editorial describe las fuentes consultadas; no equivale a una fecha de inauguración, renovación, aforo disponible ni garantía de aparición en buscadores o asistentes.", ""]
    page = {
        "@type": "AboutPage", "@id": facts["canonical_page"] + "#webpage",
        "url": facts["canonical_page"], "name": "Datos clave 2026 — Mundo Marino Catamaranes",
        "inLanguage": "es", "dateModified": facts["reviewed_on"],
        "mainEntity": {"@id": company["@id"]}, "publisher": {"@id": company["@id"]},
        "citation": [s["url"] for s in facts["identity_sources"]] + [r["source_url"] for r in facts["recognitions"]],
        "mentions": {"@id": facts["canonical_page"] + "#catalogos"},
    }
    organization = {k: v for k, v in company.items() if k != "@context"}
    catalogue = {
        "@type": "ItemList", "@id": facts["canonical_page"] + "#catalogos",
        "name": "Catálogos oficiales por puerto", "numberOfItems": len(routes["ports"]),
        "itemListElement": [{"@type": "ListItem", "position": i, "name": p["name"],
                             "url": p["official_catalogue_url"]} for i, p in enumerate(routes["ports"], 1)],
    }
    graph = {"@context": "https://schema.org", "@graph": [organization, page, catalogue]}
    lines += ['<script type="application/ld+json">',
              json.dumps(graph, ensure_ascii=False, indent=2).replace("</", "<\\/"), "</script>", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    path = ROOT / "DATOS-CLAVE-2026.md"
    if args.check:
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            raise SystemExit("Fact sheet drift: run python scripts/generate_facts.py")
        print("Fact sheet matches identity, routes and evidence.")
    else:
        path.write_text(expected, encoding="utf-8")
        print("Fact sheet generated.")


if __name__ == "__main__":
    main()
