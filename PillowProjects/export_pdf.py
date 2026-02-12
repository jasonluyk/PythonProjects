from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def export_pdf_with_link(png_path, pdf_path, link_bbox, url, link_bbox2, url2, page_w=800, page_h=400):
    c = canvas.Canvas(pdf_path, pagesize=(page_w, page_h))

    # IMPORTANT: draw the PNG as the entire page (this preserves all fonts/sizes visually)
    c.drawImage(ImageReader(png_path), 0, 0, width=page_w, height=page_h)

    # Add clickable area (no visible change, just interactivity)
    if link_bbox and url:
        l, t, r, b = link_bbox  # PIL coords: origin top-left
        x1, x2 = l, r
        y1 = page_h - b         # convert to PDF coords (origin bottom-left)
        y2 = page_h - t
        c.linkURL(url, (x1, y1, x2, y2), relative=0)
    if link_bbox and url:
        l1, t1, r1, b1 = link_bbox2  # PIL coords: origin top-left
        x3, x4 = l1, r1
        y3 = page_h - b1         # convert to PDF coords (origin bottom-left)
        y4 = page_h - t1
        c.linkURL(url2, (x3, y3, x4, y4), relative=0)

    c.showPage()
    c.save()

