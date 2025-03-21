from color_model import HEXColor, HEXColorFactory

def main_task() -> None:
    factory = HEXColorFactory()
    color_list = factory.create_list_hex_colors(["#000000", "#FFFFFF"])
    max_color = max(color_list, key=lambda i: i.brightness)
    name = max_color.get_color_name()
    R,G,B = max_color.HEXtoRGBAdapter()
    print(f"The brightest color is: {max_color.value} (r={R}, g={G}, b={B}){", called " + name.lower() if name else ""}")

def main():
    """Hauptarbeitsmethode mit Aufgabe"""
    # factory = HEXColorFactory()
    # c = HEXColor("#FFFFFF")
    # q = factory.create_hex_color("#FFFFFF")
    # print(q.value, c.value)
    # print(q.brightness, c.brightness)
    main_task()

if __name__ == "__main__":
    main()