

from PIL import Image, ImageDraw
import svgwrite
import itertools
import os

# Configuración general
width, height = 600, 400  # Relación 3:2
colors = {
    'red': '#FF0000',
    'blue': '#0000FF',
    'green': '#008000',
    'pink': '#FF00FF',
    'yellow': '#FFFF00',
    'black': '#000000',
    'white': '#FFFFFF'
}

output_dir = "banderas_generadas"
os.makedirs(output_dir, exist_ok=True)

def has_valid_repetition(combo):
    """
    Permite:
    - Todas las combinaciones sin repeticiones adyacentes
    - Una única repetición adyacente de 2 colores iguales
    No permite:
    - Más de una repetición adyacente
    - Repeticiones triples o más (A-A-A)
    """
    if len(combo) == 1:
        return True
    if len(combo) == 2:
        return combo[0] != combo[1]  # Sin repetición
    repetition_found = False
    i = 0
    while i < len(combo) - 1:
        if combo[i] == combo[i + 1]:
            if repetition_found:
                return False  # ya había una repetición
            # Verificamos que no sea triple (o más)
            if i + 2 < len(combo) and combo[i] == combo[i + 2]:
                return False  # triple repetición
            repetition_found = True
            i += 2  # saltamos la pareja
        else:
            i += 1
    return True

def draw_png_flag(stripes, orientation, filename):
    flag = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(flag)

    if orientation == "horizontal":
        stripe_height = height // len(stripes)
        for i, color in enumerate(stripes):
            draw.rectangle(
                [(0, i * stripe_height), (width, (i + 1) * stripe_height)],
                fill=colors[color]
            )
    elif orientation == "vertical":
        stripe_width = width // len(stripes)
        for i, color in enumerate(stripes):
            draw.rectangle(
                [(i * stripe_width, 0), ((i + 1) * stripe_width, height)],
                fill=colors[color]
            )
    elif orientation == "diagonal":
        stripe_width = width / len(stripes)
        for i, color in enumerate(stripes):
            draw.polygon(
                [
                    (i * stripe_width, 0),
                    ((i + 1) * stripe_width, 0),
                    ((i + 1) * stripe_width - width, height),
                    (i * stripe_width - width, height)
                ],
                fill=colors[color]
            )

    flag.save(os.path.join(output_dir, filename + ".png"))

def draw_svg_flag(stripes, orientation, filename):
    if orientation == "diagonal":
        return  # SVG omitido para diagonales
    dwg = svgwrite.Drawing(os.path.join(output_dir, filename + ".svg"), size=(f"{width}px", f"{height}px"))
    
    if orientation == "horizontal":
        stripe_height = height / len(stripes)
        for i, color in enumerate(stripes):
            dwg.add(dwg.rect(insert=(0, i * stripe_height), size=(width, stripe_height), fill=colors[color]))
    elif orientation == "vertical":
        stripe_width = width / len(stripes)
        for i, color in enumerate(stripes):
            dwg.add(dwg.rect(insert=(i * stripe_width, 0), size=(stripe_width, height), fill=colors[color]))

    dwg.save()

def generate_flags():
    for num_stripes in [1, 2, 3, 4]:
        combos = itertools.product(colors.keys(), repeat=num_stripes)
        for combo in combos:
            if has_valid_repetition(combo):
                name = f"{'-'.join(combo)}_{num_stripes}stripes"

                # Horizontal
                draw_png_flag(combo, "horizontal", name + "_horizontal")
                draw_svg_flag(combo, "horizontal", name + "_horizontal")

                # Vertical
                if num_stripes >= 2:
                    draw_png_flag(combo, "vertical", name + "_vertical")
                    draw_svg_flag(combo, "vertical", name + "_vertical")

                # Diagonal
                if num_stripes >= 2:
                    draw_png_flag(combo, "diagonal", name + "_diagonal")
                
                print("✅ " + name)

generate_flags()
print(f"✅ Banderas PNG+SVG generadas (1–4 franjas, horizontal, vertical y diagonal) en: {output_dir}")
