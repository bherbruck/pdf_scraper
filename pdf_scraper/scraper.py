import pdfquery


def _load_pdf(path):
    pdf = pdfquery.PDFQuery(path)
    pdf.load()
    return pdf


def scrape(path: str, fields: dict, table_bbox=None, ignore_headers=[]) -> list:
    pdf = _load_pdf(path)
    # format the table bbox for the query
    str_table_bbox = ", ".join([str(i)
                                for i in table_bbox
                                or (0, 0, 0, 0)])  # default value if no bbox
    rows = []
    # query each page
    for page in range(pdf.doc.catalog['Pages'].resolve()['Count']):
        page += 1
        query = [
            ('with_parent', f'LTPage[pageid="{page}"]'),
            ('with_formatter', None),
            ('table', f'LTTextLineHorizontal:in_bbox("{str_table_bbox}")')
        ] + [(k, f'LTTextLineHorizontal:contains("{v}")')
             for k, v in fields.items()]
        # run the query
        result = pdf.extract(query)
        # prep the dat
        metadata = {k: v.text().replace(fields.get(k), '').strip()
                    for k, v in result.items() if k in fields.keys()}

        if table_bbox is not None:
            # get the table
            table = get_table(result['table'], ignore_headers=ignore_headers)
            rows += [{**metadata, **row} for row in table]
        else:
            rows.append(metadata)

    return rows


def get_table(boxes, ignore_headers=[]):
    from itertools import groupby

    # prep the table data using just the first coordinate
    table_all = [{'text': box[0].text.strip(),
                  'x0': float(box.attrib['x0']),
                  'y0': float(box.attrib['y0'])}
                 for box in boxes]

    # get each row grouped by the y-coord (sort results by x-coord)
    def key(x): return int(x['y0'])
    table_rows = {k: [i['text'] for i in sorted(list(g), key=lambda x: x['x0'])]
                  for k, g in groupby(sorted(table_all, key=key), key=key)}
    # pop the headers off the list (row with the max y value)
    table_headers = [i.lower().replace(' ', '_') for i in table_rows.pop(max(table_rows))
                     if i not in ignore_headers]

    # zip it all up
    table_data = [dict(zip(table_headers, v))
                  for v in table_rows.values()]

    return table_data
