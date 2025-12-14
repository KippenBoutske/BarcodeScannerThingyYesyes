import flet as ft


def main(page: ft.Page):
    ## Page settings
    page.title = "Barcode App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    ###
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)

    page.add(
        ft.Row(
            [
                ft.Text("Barcode Bestand:"),
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                ),
                selected_files,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ft.Row(
        [
            ft.Text("Kassa systeem bestand:"),
            ft.ElevatedButton(
                "Pick files",
                icon=ft.Icons.UPLOAD_FILE,
                on_click=lambda _: pick_files_dialog.pick_files(
                    allow_multiple=False
                ),
            ),
            selected_files,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    ),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Start verwerking",
                    icon=ft.Icons.START,
                    )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    )


ft.app(main)