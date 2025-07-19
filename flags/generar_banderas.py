from PIL import Image, ImageDraw
import svgwrite
import itertools
import os

# Configuración general
width, height = 7500, 5000  # Relación 3:2
colors = {
    'red': '#FF0000',
    'blue': '#0000FF',
    'green': '#008000',
    'yellow': '#FFFF00',
    'black': '#000000',
    'white': '#FFFFFF'
}

output_dir = "banderas_generadas"
os.makedirs(output_dir, exist_ok=True)

def draw_png_flag(stripes, orientation, filename):
    flag = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(flag)

    if orientation == "horizontal":
        stripe_size = height // len(stripes)
        for i, color in enumerate(stripes):
            draw.rectangle(
                [(0, i * stripe_size), (width, (i + 1) * stripe_size)],
                fill=colors[color]
            )
    elif orientation == "vertical":
        stripe_size = width // len(stripes)
        for i, color in enumerate(stripes):
            draw.rectangle(
                [(i * stripe_size, 0), ((i + 1) * stripe_size, height)],
                fill=colors[color]
            )
    flag.save(os.path.join(output_dir, filename + ".png"))

def draw_svg_flag(stripes, orientation, filename):
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
    for num_stripes in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        for combo in itertools.product(colors.keys(), repeat=num_stripes):
            if all(combo[i] != combo[i + 1] for i in range(len(combo) - 1)):  # evitar repetidos adyacentes
                name = f"{'-'.join(combo)}_{num_stripes}stripes"

                # Horizontal
                draw_png_flag(combo, "horizontal", name + "_horizontal")
                draw_svg_flag(combo, "horizontal", name + "_horizontal")
                print(name + "_horizontal drawn")

                # Vertical
                if num_stripes>1:  # solo si tiene mas de una franja, crear ambas versiones
                    draw_png_flag(combo, "vertical", name + "_vertical")
                    draw_svg_flag(combo, "vertical", name + "_vertical")
                print(name + "_vertical drawn")

generate_flags()
print(f"✅ Banderas PNG y SVG generadas en la carpeta: {output_dir}")
