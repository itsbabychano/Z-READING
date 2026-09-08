from pathlib import Path


def _pdf_text(value):
    """Escape text for a PDF literal string."""
    value = value.encode("latin-1", errors="replace").decode("latin-1")
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def create_combined_pdf(
    folder,
    output_name="combined_reading_reports.pdf",
    output_folder=None,
):
    """Create one monospaced PDF containing every TXT file in folder."""
    folder = Path(folder)
    paths = sorted(folder.glob("*.txt"))
    if not paths:
        raise FileNotFoundError(f"No .txt files found in {folder}")
    output_folder = Path(output_folder) if output_folder else folder
    output_folder.mkdir(parents=True, exist_ok=True)

    page_width, page_height = 612, 792  # US Letter, in points
    left_margin, right_margin = 72, 72
    top_margin, bottom_margin = 720, 72
    line_height = 9
    font_size = 8
    column_count = 2
    column_gap = 14
    column_width = (
        page_width - left_margin - right_margin - column_gap
    ) / column_count
    max_lines_per_column = int((top_margin - bottom_margin) // line_height) + 1
    pages = []

    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        lines = [f"--- {path.name} ---"] + lines
        if len(lines) > max_lines_per_column * column_count:
            raise ValueError(
                f"{path.name} has too many lines to fit in two columns on one page"
            )

        lines_per_column = (len(lines) + column_count - 1) // column_count
        commands = []
        for column in range(column_count):
            start = column * lines_per_column
            column_lines = lines[start:start + lines_per_column]
            if not column_lines:
                continue
            x_position = left_margin + column * (column_width + column_gap)
            commands.extend([
                "BT",
                f"/F1 {font_size} Tf",
                "90 Tz",
                f"{x_position:.2f} {top_margin} Td",
            ])
            for index, line in enumerate(column_lines):
                if index:
                    commands.append(f"0 -{line_height} Td")
                commands.append(f"({_pdf_text(line)}) Tj")
            commands.append("ET")
        pages.append("\n".join(commands).encode("latin-1"))

    objects = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    page_references = " ".join(
        f"{index + 4} 0 R" for index in range(len(pages))
    )
    objects.append(
        f"<< /Type /Pages /Kids [{page_references}] /Count {len(pages)} >>".encode(
            "ascii"
        )
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

    for index, content in enumerate(pages):
        content_object_number = 4 + len(pages) + index
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width} {page_height}] "
                f"/Resources << /Font << /F1 3 0 R >> >> "
                f"/Contents {content_object_number} 0 R >>"
            ).encode("ascii")
        )

    for content in pages:
        objects.append(
            f"<< /Length {len(content)} >>\nstream\n".encode("ascii")
            + content
            + b"\nendstream"
        )

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )

    requested_path = output_folder / output_name
    output_path = requested_path
    for attempt in range(100):
        try:
            output_path.write_bytes(pdf)
            break
        except PermissionError as error:
            if attempt == 99:
                raise PermissionError(
                    f"Cannot write {requested_path}. Close the PDF if it is open, "
                    "then run the script again."
                ) from error
            suffix = "_new" if attempt == 0 else f"_new_{attempt + 1}"
            output_path = requested_path.with_name(
                f"{requested_path.stem}{suffix}{requested_path.suffix}"
            )
    return output_path, len(paths), len(pages)


def create_year_month_pdfs(source_folder, output_folder):
    """Create one PDF for each year/month folder containing text files."""
    source_folder = Path(source_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    results = []

    for year_folder in sorted(source_folder.iterdir()):
        if not year_folder.is_dir() or not year_folder.name.isdigit():
            continue
        for month_folder in sorted(year_folder.iterdir()):
            if not month_folder.is_dir() or not list(month_folder.glob("*.txt")):
                continue
            output_name = f"{month_folder.name.title()}_{year_folder.name}.pdf"
            result = create_combined_pdf(
                month_folder,
                output_name=output_name,
                output_folder=output_folder,
            )
            results.append((year_folder.name, month_folder.name, *result))
    return results


if __name__ == "__main__":
    source_folder = r"E:\PROJECTS\Z READING BIR"
    output_folder = r"E:\PROJECTS\COVERTED"
    results = create_year_month_pdfs(source_folder, output_folder)
    for year, month, output_path, file_count, page_count in results:
        print(f"Created {output_path}")
        print(
            f"{month} {year}: combined {file_count} text files "
            f"into {page_count} PDF pages."
        )
    print(f"Created {len(results)} monthly PDF files.")