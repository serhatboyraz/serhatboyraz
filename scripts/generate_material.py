"""Generate Material Design assets for the GitHub profile README."""

from __future__ import annotations

from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

DARK = {
    "page": "#0d1117",
    "card": "#211F26",
    "outline": "#49454F",
    "primary": "#A8C7FA",
    "on_card": "#E6E1E5",
    "on_variant": "#CAC4D0",
    "chip": "#36343B",
    "chip_text": "#E6E1E5",
    "overline": "#A8C7FA",
    "shadow": "#010409",
}

LIGHT = {
    "page": "#ffffff",
    "card": "#FFFBFE",
    "outline": "#CAC4D0",
    "primary": "#1565C0",
    "on_card": "#1C1B1F",
    "on_variant": "#49454F",
    "chip": "#E7E0EC",
    "chip_text": "#1C1B1F",
    "overline": "#1565C0",
    "shadow": "#D0D7DE",
}

FONT = "Segoe UI, Helvetica, Arial, sans-serif"
W = 888


def card(
    x: float,
    y: float,
    w: float,
    h: float,
    t: dict,
    overline: str,
    title: str,
    chips: list[str],
    body_lines: list[str],
) -> str:
    shadow = (
        f'<rect x="{x + 3}" y="{y + 7}" width="{w}" height="{h}" rx="16" fill="{t["shadow"]}"/>'
    )
    surface = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" '
        f'fill="{t["card"]}" stroke="{t["outline"]}" stroke-width="1"/>'
    )
    accent = f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{t["primary"]}"/>'
    texts = [
        f'<text x="{x + 28}" y="{y + 36}" fill="{t["overline"]}" font-family="{FONT}" '
        f'font-size="11" font-weight="600" letter-spacing="1.8">{overline}</text>',
        f'<text x="{x + 28}" y="{y + 68}" fill="{t["on_card"]}" font-family="{FONT}" '
        f'font-size="22" font-weight="700">{title}</text>',
    ]
    for i, line in enumerate(body_lines):
        texts.append(
            f'<text x="{x + 28}" y="{y + 100 + i * 20}" fill="{t["on_variant"]}" '
            f'font-family="{FONT}" font-size="13">{line}</text>'
        )
    chip_y = y + h - 48
    chip_x = x + 28
    chip_svgs: list[str] = []
    for label in chips:
        cw = 12 + len(label) * 7.2
        chip_svgs.append(
            f'<rect x="{chip_x}" y="{chip_y}" width="{cw:.1f}" height="28" rx="14" fill="{t["chip"]}"/>'
            f'<text x="{chip_x + cw / 2:.1f}" y="{chip_y + 18}" text-anchor="middle" '
            f'fill="{t["chip_text"]}" font-family="{FONT}" font-size="11" font-weight="600">{label}</text>'
        )
        chip_x += cw + 8
    return shadow + surface + accent + "".join(texts) + "".join(chip_svgs)


def projects_svg(t: dict) -> str:
    h = 268
    gap = 20
    cw = (W - gap) / 2
    agent = card(
        0,
        2,
        cw,
        h,
        t,
        "FEATURED PROJECT",
        "AI Development Agent",
        ["GitLab", "Jira", "Tests", "Code Review"],
        [
            "AI-powered software development workflow that",
            "takes work from the backlog to a reviewed merge",
            "request.",
            "",
            "GitLab   →   Jira   →   Agent   →   Dev   →   MR",
        ],
    )
    esign = card(
        cw + gap,
        2,
        cw,
        h,
        t,
        "FEATURED PROJECT",
        "E-Signature Platform",
        [".NET", "HSM", "Esya", "e-Invoice"],
        [
            "Enterprise electronic signature platform built",
            "with .NET. Integrates TÜBİTAK Esya with smart",
            "cards and HSM devices for legally compliant",
            "signing in e-invoice and e-dispatch flows.",
        ],
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h + 16}" '
        f'viewBox="0 0 {W} {h + 16}">'
        f'<rect width="{W}" height="{h + 16}" fill="{t["page"]}"/>'
        f"{agent}{esign}</svg>"
    )


def chips_svg(t: dict) -> str:
    groups = [
        ("BACKEND", ["C#", ".NET", "Java"]),
        ("CLOUD AND PLATFORM", ["Azure", "Docker", "Kubernetes", "GitLab CI"]),
        ("DATA AND MESSAGING", ["Kafka", "RabbitMQ", "PostgreSQL", "Redis", "Elasticsearch"]),
        ("ARCHITECTURE", ["Microservices", "Event-Driven", "DDD", "Modular Monolith"]),
    ]
    inner_h = 4 * 72 + 16
    h = inner_h + 36
    shadow = f'<rect x="3" y="7" width="{W - 3}" height="{h}" rx="16" fill="{t["shadow"]}"/>'
    surface = (
        f'<rect x="0" y="0" width="{W}" height="{h}" rx="16" '
        f'fill="{t["card"]}" stroke="{t["outline"]}" stroke-width="1"/>'
    )
    accent = f'<rect x="0" y="0" width="6" height="{h}" rx="3" fill="{t["primary"]}"/>'
    parts = [shadow, surface, accent]
    y = 28
    for title, labels in groups:
        parts.append(
            f'<text x="28" y="{y + 12}" fill="{t["overline"]}" font-family="{FONT}" '
            f'font-size="11" font-weight="600" letter-spacing="1.6">{title}</text>'
        )
        x = 28
        cy = y + 24
        for label in labels:
            cw = 20 + len(label) * 7.2
            parts.append(
                f'<rect x="{x}" y="{cy}" width="{cw:.1f}" height="30" rx="15" fill="{t["chip"]}"/>'
                f'<text x="{x + cw / 2:.1f}" y="{cy + 20}" text-anchor="middle" '
                f'fill="{t["chip_text"]}" font-family="{FONT}" font-size="13" font-weight="600">{label}</text>'
            )
            x += cw + 8
        y += 72
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h + 12}" '
        f'viewBox="0 0 {W} {h + 12}">'
        f'<rect width="{W}" height="{h + 12}" fill="{t["page"]}"/>'
        f"{''.join(parts)}</svg>"
    )


def bar_svg(t: dict) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="8" viewBox="0 0 {W} 8">'
        f'<rect width="{W}" height="8" fill="{t["page"]}"/>'
        f'<rect width="{W}" height="4" rx="2" fill="{t["primary"]}"/></svg>'
    )


def write_svg_png(name: str, svg: str) -> None:
    svg_path = ASSETS / f"{name}.svg"
    png_path = ASSETS / f"{name}.png"
    svg_path.write_text(svg, encoding="utf-8")
    doc = pymupdf.open(svg_path)
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=True)
    pix.save(png_path)
    print(f"wrote {png_path.name} ({pix.width}x{pix.height})")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    write_svg_png("projects-dark", projects_svg(DARK))
    write_svg_png("projects-light", projects_svg(LIGHT))
    write_svg_png("tech-dark", chips_svg(DARK))
    write_svg_png("tech-light", chips_svg(LIGHT))
    write_svg_png("bar-dark", bar_svg(DARK))
    write_svg_png("bar-light", bar_svg(LIGHT))


if __name__ == "__main__":
    main()
