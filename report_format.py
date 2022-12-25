COLORS = {
    "black": "#000000",
    "white": "#FFFFFF",
    "red": "#FF0000",
    "yellow": "#FFFF00",
    "gray": "#C0C0C0",
    "pink": "#FF99CC",
    "butter": "#FFFF99",
    "blue": "#3366FF",
    "sky_blue": "#99CCFF",
    "orange": "#FF9900",
    "green": "#A7DE03",
    "sky_green": "#CCFFCC"
}


class Format:
    def __init__(self, workbook):
        self.workbook = workbook

    def set_format(self, bold: bool, font_size: int, bg_color: str, font_color: str, align: str,
                    top: int, bottom: int, left: int, right: int):
        return self.workbook.add_format({
            "bold": bold,
            "font_size": font_size,
            "bg_color": bg_color,
            "font_color": font_color,
            "align": align,
            "valign": "vcenter",
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "text_wrap": True
        })

    def set_format_mb(self, bold: bool, font_size: int, bg_color: str, font_color: str, align: str,
                    top: int, bottom: int, left: int, right: int):
        return self.workbook.add_format({
            "bold": bold,
            "font_size": font_size,
            "bg_color": bg_color,
            "font_color": font_color,
            "align": align,
            "valign": "vcenter",
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "text_wrap": True,
            "num_format": '#,##0 "MB"'
        })

    def set_format_kb(self, bold: bool, font_size: int, bg_color: str, font_color: str, align: str,
                    top: int, bottom: int, left: int, right: int):
        return self.workbook.add_format({
            "bold": bold,
            "font_size": font_size,
            "bg_color": bg_color,
            "font_color": font_color,
            "align": align,
            "valign": "vcenter",
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "text_wrap": True,
            "num_format": '#,##0 "KB"'
        })