import csv

kassa_data = {}
with open('Kassa.csv', "r", newline='') as kassa_file:
    kassa_reader = csv.reader(kassa_file, delimiter=";")
    for row2 in kassa_reader:
        if len(row2) >= 2:
            barcode = row2[0].strip().strip('"')
            item_name = row2[1].strip().strip('"')
            kassa_data[barcode] = item_name

with open('Barcodes.csv', "r", newline='') as barcode_file:
    barcode_reader = csv.reader(barcode_file, delimiter=";")
    current_article_barcode = None
    for row in barcode_reader:
        scanned_barcode = row[0].strip().strip('"')
        if scanned_barcode == "000000000017":
            if current_article_barcode is not None:
                if current_article_barcode in kassa_data:
                    print(kassa_data[current_article_barcode])
                else:
                    print("Artikel bestaat niet in het kassa systeem")
                current_article_barcode = None
        else:
            current_article_barcode = scanned_barcode