import flet as ft
import csv
import os.path
from pathlib import Path

from flet.core.theme import Theme


def main(page: ft.Page):
    page.title = "Barcode App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme = Theme(color_scheme_seed=ft.Colors.GREEN)

    selected_file_kassa_path = None
    selected_file_barcode_path = None

    def barcode_csv_picker(e: ft.FilePickerResultEvent):
       selected_file_barcode.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
       nonlocal selected_file_barcode_path
       selected_file_barcode_path = e.files[0].path

       selected_file_barcode.update()

    def kassa_csv_picker(e: ft.FilePickerResultEvent):
        selected_file_kassa.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        nonlocal selected_file_kassa_path
        selected_file_kassa_path = e.files[0].path
        selected_file_kassa.update()

    progress_bar = ft.ProgressBar(width=400, color=ft.Colors.GREEN, bgcolor="#eeeeee")
    progress_bar.visible = False
    kassa_csv_picker_dialog = ft.FilePicker(on_result=kassa_csv_picker)
    barcode_csv_picker_dialog = ft.FilePicker(on_result=barcode_csv_picker)
    selected_file_kassa = ft.Text()
    selected_file_barcode = ft.Text()

    page.overlay.append(kassa_csv_picker_dialog)
    page.overlay.append(barcode_csv_picker_dialog)

    dlg = ft.AlertDialog(
        title=ft.Text("Nog niet alle bestanden zijn gekozen..."),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25),
    )

    console = ft.TextField(
                    label="Console",
                    multiline=True,
                    read_only=True,
                    min_lines=1,
                    max_lines=10,
                    expand=True
                )

    def barcode_scanner_start(e: ft.ElevatedButton):
        if selected_file_barcode.value == "Cancelled!" or \
                selected_file_kassa.value == "Cancelled!" or \
                selected_file_barcode.value is None or \
                selected_file_kassa.value is None:
            page.open(dlg)
        else:

            progress_bar.visible = True
            page.update()

            directory = Path(selected_file_kassa_path).parent

            console.value = "BARCODE SCANNER \n-----------------------------------\n"

            try:
                if not os.path.isfile(directory / "result.csv"):
                    console.value = console.value + "*result.csv* Bestand bestaat niet... \n-----------------------------------\n"
                    page.update()
                    f = open(directory / "result.csv", "x")
                else:
                    console.value = console.value + "*result.csv* Bestand bestond en is gewist... \n-----------------------------------\n"
                    page.update()
                    f = open(directory / "result.csv", "w")
                    f.truncate()
                    f.close()

            except PermissionError:
                console.value = (
                    "'result.csv' kan niet geopend worden. Sluit Excel aub af."
                )
                progress_bar.visible = False
                page.update()

            with open(directory / "result.csv", 'w', newline='') as file:
                writer = csv.writer(file, delimiter=";")
                field = ["Artikel", "Omschrijving1", "Groep Code", "Groep tekst", "Inkoop", "Verkoop prijs", "BTW", "Aantal", "Verkoop prijs * Aantal"]

                writer.writerow(field)

            kassa_data = {}
            with open(selected_file_kassa_path, "r", newline='', encoding="utf-8") as kassa_file:
                kassa_reader = csv.reader(kassa_file, delimiter=",")

                try:
                    next(kassa_reader)
                except StopIteration:
                    pass

                for row2 in kassa_reader:
                    if len(row2) >= 2:
                        barcode = row2[0].replace('"', '').strip()
                        omschrijving1 = row2[1].strip().strip('"')
                        groepcode = row2[2].strip().strip('"')
                        groeptekst = row2[3].strip().strip('"')
                        inkoop = row2[4].strip().strip('"')
                        verkoopprijs = row2[5].strip().strip('"')
                        btw = row2[6].strip().strip('"')
                        kassa_data[barcode] = [omschrijving1, groepcode, groeptekst, inkoop, verkoopprijs, btw]

            with open(selected_file_barcode_path, "r", newline='') as barcode_file:
                barcode_reader = csv.reader(barcode_file, delimiter=";")
                current_article_barcode = None
                for row in barcode_reader:
                    if not row: continue
                    scanned_barcode = row[0].replace('"', '').strip()
                    if int(scanned_barcode.lstrip("0")) <= 50:
                        if current_article_barcode is not None:
                            if current_article_barcode in kassa_data:

                                omschrijving1, groepcode, groeptekst, inkoop, verkoopprijs, btw = kassa_data[current_article_barcode]

                                console.value = console.value + current_article_barcode + " - " + omschrijving1 + " | Aantal: " + scanned_barcode.lstrip("0") + "\n"
                                page.update()
                                with open(directory / "result.csv", 'a', newline='') as file:
                                    writer = csv.writer(file, delimiter=";")
                                    writer.writerow([current_article_barcode, omschrijving1, groepcode, groeptekst, inkoop, verkoopprijs, btw, scanned_barcode.lstrip("0"), "€" + str(round(int(scanned_barcode.lstrip("0"))*float(verkoopprijs), 2))])
                            else:
                                console.value = console.value + "Artikel bestaat niet in het kassa systeem\n"

                                page.update()
                            current_article_barcode = None
                    else:
                        current_article_barcode = scanned_barcode
            console.value = console.value + f"-----------------------------------\nSuccesvol gelukt! Locatie bestand: {directory / 'result.csv'}"
            progress_bar.visible = False
            page.update()



    page.add(
        ft.Row(
            [
                ft.Text("Barcode Bestand:"),
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: barcode_csv_picker_dialog.pick_files(
                        allow_multiple=False,
                        allowed_extensions=["csv"]
                    ),
                ),
                selected_file_barcode,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ft.Row(
        [
            ft.Text("Kassa systeem bestand:"),
            ft.ElevatedButton(
                "Pick files",
                icon=ft.Icons.UPLOAD_FILE,
                on_click=lambda _: kassa_csv_picker_dialog.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["csv"]
                ),
            ),
            selected_file_kassa,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    ),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Start verwerking",
                    icon=ft.Icons.START,
                    on_click=barcode_scanner_start,
                    ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [
                progress_bar
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),

        ft.Row(
            [
                console
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),



    )


ft.app(main)