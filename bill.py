from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.color.color import HexColor, X11Color
from datetime import datetime
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.table import TableCell
import random

pdf = Document()
page = Page()
pdf.add_page(page)

page_layout = SingleColumnLayout(page)
page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)


def _build_itemized_description_table(items):
    table_001 = Table(number_of_rows=len(items)+1, number_of_columns=5)
    for h in ["NAME", "BRAND", "QTY", "UNIT PRICE", "AMOUNT"]:
        table_001.add(
            TableCell(
                Paragraph(h, font_color=X11Color("White")),
                background_color=HexColor("016934"),
            ))

    odd_color = HexColor("BBBBBB")
    even_color = HexColor("FFFFFF")
    product_tuple = []
    for item in items:
        product_tuple.append(
            (item["product"]["name"],
             item["product"]["brand"], item["qty"], item["product"]["price"],
             int(item["qty"]) * float(item["product"]["price"])))

    for row_number, item in enumerate(product_tuple):
        c = even_color if row_number % 2 == 0 else odd_color
        table_001.add(TableCell(Paragraph(item[0] + "      "), background_color=c))
        table_001.add(TableCell(Paragraph(item[1]), background_color=c))
        table_001.add(TableCell(Paragraph(str(item[2])), background_color=c))
        table_001.add(
            TableCell(Paragraph("$ " + str(item[3])), background_color=c))
        table_001.add(
            TableCell(Paragraph("$ " + str(item[4]).split(".")[0] +
                                "." + str(item[4]).split(".")[1][0]),
                      background_color=c))

    table_001.no_borders()
    return table_001


def _build_billing_and_shipping_information():
    table_001 = Table(number_of_rows=6, number_of_columns=2)
    table_001.add(
        Paragraph(
            "BILL TO",
            background_color=HexColor("263238"),
            font_color=X11Color("White"),
        ))
    table_001.add(
        Paragraph(
            "SHIP TO",
            background_color=HexColor("263238"),
            font_color=X11Color("White"),
        ))
    table_001.add(Paragraph("[Recipient Name]"))  # BILLING
    table_001.add(Paragraph("[Recipient Name]"))  # SHIPPING
    table_001.add(Paragraph("[Company Name]"))  # BILLING
    table_001.add(Paragraph("[Company Name]"))  # SHIPPING
    table_001.add(Paragraph("[Street Address]"))  # BILLING
    table_001.add(Paragraph("[Street Address]"))  # SHIPPING
    table_001.add(Paragraph("[City, State, ZIP Code]"))  # BILLING
    table_001.add(Paragraph("[City, State, ZIP Code]"))  # SHIPPING
    table_001.add(Paragraph("[Phone]"))  # BILLING
    table_001.add(Paragraph("[Phone]"))  # SHIPPING
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2),
                                       Decimal(2))
    table_001.no_borders()
    return table_001


def _build_invoice_information():
    table_001 = Table(number_of_rows=5, number_of_columns=3)

    table_001.add(Paragraph("[Street Address]"))
    table_001.add(
        Paragraph("Date",
                  font="Helvetica-Bold",
                  horizontal_alignment=Alignment.RIGHT))
    now = datetime.now()
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))

    table_001.add(Paragraph("[City, State, ZIP Code]"))
    table_001.add(
        Paragraph("Invoice #",
                  font="Helvetica-Bold",
                  horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d" % random.randint(1000, 10000)))

    table_001.add(Paragraph("[Phone]"))
    table_001.add(
        Paragraph("Due Date",
                  font="Helvetica-Bold",
                  horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))

    table_001.add(Paragraph("[Email Address]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.add(Paragraph("[Company Website]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2),
                                       Decimal(2))
    table_001.no_borders()
    return table_001


page_layout.add(_build_invoice_information())
page_layout.add(Paragraph(" "))
page_layout.add(_build_billing_and_shipping_information())
page_layout.add(Paragraph(" "))
page_layout.add(
    _build_itemized_description_table([{
        "product": {
            "id": "c045b87f-e524-46f7-8ee5-10b696712d00",
            "name": "Felt Texture Coat",
            "price": "60.8",
            "img": "/static/assets/products/Image.png",
            "qty": "100",
            "description":
            "Open coat with a lapel collar and long sleeves. One of the best-selling products in the world, this innovative coat by Zara is made of 100% felt, which has a wonderful texture. It is a timeless, versatile piece that is perfect for all seasons.",
            "brand": "Zara"
        },
        "qty": "3"
    }]))
with open("output.pdf", "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, pdf)