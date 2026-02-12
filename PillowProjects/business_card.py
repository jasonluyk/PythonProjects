from PIL import Image, ImageDraw, ImageOps
import os

from font_selection import choose_pil_font_with_wx
from color_selection import choose_color_wx
from image_selection import open_image_dialog_wx
from export_pdf import export_pdf_with_link
from vcard import write_vcard



def multiline_bbox(draw: ImageDraw.ImageDraw, xy, text: str, font, spacing: int = 6):
    """
    Returns bbox (l,t,r,b) for multiline text. Uses multiline_textbbox if available.
    """
    if hasattr(draw, "multiline_textbbox"):
        return draw.multiline_textbbox(xy, text, font=font, spacing=spacing)

    x, y = xy
    lines = text.splitlines() or [""]
    widths = []
    heights = []

    for line in lines:
        l, t, r, b = draw.textbbox((0, 0), line, font=font)
        widths.append(r - l)
        heights.append(b - t)

    w = max(widths) if widths else 0
    h = sum(heights) + spacing * (len(lines) - 1)
    return (x, y, x + w, y + h)


def main():
    # --- card setup ---
    W, H = 800, 400
    padding = 20
    border_width = 2
    inset = border_width + 2  # keep content away from border stroke

    image = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # --- border (reference frame) ---
    border_rect = (padding, padding, W - padding, H - padding)
    border_color = (0, 0, 0)
    draw.rectangle(border_rect, outline=border_color, width=border_width)

    L, T, R, B = border_rect
    SL, ST, SR, SB = (L + inset, T + inset, R - inset, B - inset)  # safe content box

    # --- select images ---
    logo_src = open_image_dialog_wx()
    photo_src = open_image_dialog_wx()

    if logo_src is None or photo_src is None:
        print("Image selection cancelled.")
        return

    # normalize sizes (locked)
    logo_img = ImageOps.contain(logo_src, size=(100, 100))
    photo_img = ImageOps.contain(photo_src, size=(300, 300))

    # --- user inputs ---
    name = input("What is your name? ").strip()
    name_color = choose_color_wx()
    name_font = choose_pil_font_with_wx()

    job = input("What are your job titles (separate by commas)? ").strip()
    jobs = [j.strip() for j in job.split(",") if j.strip()]
    jobs_color = choose_color_wx()
    jobs_font = choose_pil_font_with_wx()

    company = input("What is your company name? ").strip()
    company_color = choose_color_wx()
    company_font = choose_pil_font_with_wx()


    # defaults so they always exist
    linkedin_url = ""
    personal_website = ""
    phone = ""
    email = ""

    contact_info = input("Would you like to add contact info?(yes or no): ")
    if contact_info.lower() == "yes":
        linkedin_url = input("LinkedIn URL (include https://, or blank): ").strip()
        personal_website = input("Personal Webpage (include https://, or blank): ").strip()
        phone = input("Phone (optional): ").strip()
        email = input("Email (optional): ").strip()

    contact_font = choose_pil_font_with_wx()
    contact_color = choose_color_wx()

    # --- place photo (top-right inside border) ---
    photo_x = SR - photo_img.size[0]
    photo_y = ST
    image.paste(photo_img, (photo_x, photo_y))

    # --- place logo (bottom-left inside border) ---
    logo_x = SL
    logo_y = SB - logo_img.size[1]
    image.paste(logo_img, (logo_x, logo_y))

    # --- name at top-left inside safe box ---
    name_x = SL
    name_y = ST
    draw.text((name_x + 5, name_y), name, font=name_font, fill=name_color)

    # underline name with measured width
    nl, nt, nr, nb = draw.textbbox((name_x, name_y), name, font=name_font)
    draw.line(((name_x + 5, nb + 5), (nr, nb + 5)), fill=name_color, width=5)

    # --- jobs under name ---
    jobs_x = SL
    jobs_y = nb + padding  # space under underline
    if jobs:
        draw.multiline_text((jobs_x, jobs_y), "\n".join(jobs), font=jobs_font, fill=jobs_color, spacing=15)
        jl, jt, jr, jb = draw.multiline_textbbox((jobs_x, jobs_y), "\n".join(jobs), font=jobs_font, spacing=15)
    else:
        jb = jobs_y

    # --- company aligned to bottom, just right of logo ---
    company_x = logo_x + logo_img.size[0] + 8
    # Your “simple” bottom alignment method (works well with your fonts)
    company_y = SB - company_font.size
    draw.text((company_x, company_y), company, font=company_font, fill=company_color)

    # --- contact block aligned to bottom (same baseline as company) ---
    # Build contact lines with LinkedIn first (display text uses NAME, not URL)

    my_page = "My Page"

    contact_lines = []
    if linkedin_url:
        contact_lines.append(f"LinkedIn: {name}")
    if personal_website:
        contact_lines.append(f"Personal Site: {my_page}")
    if phone:
        contact_lines.append(f"Phone: {phone}")
    if email:
        contact_lines.append(f"Email: {email}")

    linkedin_bbox = None
    if contact_lines:
        # Contact block sits in the right column; align its bottom to company_y
        contact_text = "\n".join(contact_lines)

        # measure block height (starting at y=0 for measurement convenience)
        ml, mt, mr, mb = multiline_bbox(draw, (0, 0), contact_text, font=contact_font, spacing=6)
        block_h = mb - mt

        contact_x = photo_x  # align left edge with the photo
        contact_y = company_y - (block_h - contact_font.size)  # baseline-ish alignment

        # Draw LinkedIn line as "link style" if provided
        cursor_y = contact_y

        if linkedin_url:
            linkedin_label = "LinkedIn: "
            linkedin_name = name

            # label
            draw.text((contact_x, cursor_y), linkedin_label, font=contact_font, fill=contact_color)

            # measure label to place name right after it
            lab_l, lab_t, lab_r, lab_b = draw.textbbox((contact_x, cursor_y), linkedin_label, font=contact_font)
            name_x = lab_r

            # name in link style
            link_color = (0, 102, 204)
            draw.text((name_x, cursor_y), linkedin_name, font=contact_font, fill=link_color)

            # underline name
            n_l, n_t, n_r, n_b = draw.textbbox((name_x, cursor_y), linkedin_name, font=contact_font)
            underline_y = n_b + 1
            draw.line(((n_l, underline_y), (n_r, underline_y)), fill=link_color, width=2)

            # clickable bbox is NAME only
            linkedin_bbox = (n_l, n_t, n_r, n_b)

            cursor_y += (n_b - n_t) + 6

        if personal_website:
            personal_label = "Personal Site: "
            personal_name = my_page

            # label
            draw.text((contact_x, cursor_y), personal_label, font=contact_font, fill=contact_color)

            # measure label to place name right after it
            lab_l, lab_t, lab_r, lab_b = draw.textbbox((contact_x, cursor_y), personal_label, font=contact_font)
            name_x = lab_r

            # name in link style
            link_color = (0, 102, 204)
            draw.text((name_x, cursor_y), personal_name, font=contact_font, fill=link_color)

            # underline name
            n_l, n_t, n_r, n_b = draw.textbbox((name_x, cursor_y), personal_name, font=contact_font)
            underline_y = n_b + 1
            draw.line(((n_l, underline_y), (n_r, underline_y)), fill=link_color, width=2)

            # clickable bbox is NAME only
            personal_bbox = (n_l, n_t, n_r, n_b)

            cursor_y += (n_b - n_t) + 6

        # remaining lines (phone/email)
        rest_lines = []
        if phone:
            rest_lines.append(f"Phone: {phone}")
        if email:
            rest_lines.append(f"Email: {email}")

        if rest_lines:
            draw.multiline_text((contact_x, cursor_y), "\n".join(rest_lines),
                                font=contact_font, fill=contact_color, spacing=6)

    # --- save outputs ---
    png_path = os.path.abspath("business_card.png")
    pdf_path = os.path.abspath("business_card.pdf")

    # IMPORTANT: save final PNG right before exporting PDF
    image.save(png_path)
    print("Saved PNG:", png_path)

    if (linkedin_url and linkedin_bbox) or (personal_website and personal_bbox):
        export_pdf_with_link(png_path, pdf_path, linkedin_bbox, linkedin_url, personal_bbox, personal_website, page_w=W, page_h=H)
        print("Saved clickable PDF:", pdf_path)
    else:
        print("No LinkedIn URL provided; PDF not generated.")

    vcf_path = os.path.abspath("business_card.vcf")
    write_vcard(
        vcf_path,
        full_name=name,
        company=company,
        phone=phone,
        email=email,
        linkedin_url=linkedin_url,
        website=personal_website,
    )
    print("Saved vCard:", vcf_path)


    # Show the in-memory final (and you can also open saved file if you prefer)
    image.show()


if __name__ == "__main__":
    main()
