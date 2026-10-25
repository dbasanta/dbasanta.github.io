#!/usr/bin/env python3
"""Remove metadata (EXIF incl. GPS location, XMP, IPTC, comments, appended data) from JPEG and PNG files.

Phone photos record where they were taken. Run this on every photo before committing it:

    python3 _tools/image_metadata.py assets/images/team/new-photo.jpg     # strip in place
    python3 _tools/image_metadata.py --check assets/images/**/*.jpg       # report only; exit 1 if any would change

Stripping is lossless: the compressed image data is copied byte for byte, nothing is re-encoded. Kept, because
they change how the image is displayed: JPEG JFIF/ICC/Adobe segments, PNG colour chunks (iCCP, cICP, sRGB, gAMA,
cHRM), pHYs and bKGD. A JPEG whose EXIF Orientation is not 1 keeps a minimal EXIF block holding only that tag,
so it still displays the right way up. Requires Pillow (pip install pillow).
"""
import io, shlex, struct, sys
from PIL import Image

PNG_SIG = b"\x89PNG\r\n\x1a\n"
PNG_DROP = {b"eXIf", b"iTXt", b"tEXt", b"zTXt", b"tIME"}


def strip_jpeg(data):
    orientation = Image.open(io.BytesIO(data)).getexif().get(0x0112)
    out, i = bytearray(data[:2]), 2
    assert data[:2] == b"\xff\xd8", "not a JPEG"
    while True:
        marker = data[i + 1]
        if marker == 0xD9:                                   # end of image: drop anything appended after it
            out += data[i:i + 2]
            break
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        seg, body = data[i:i + 2 + length], data[i + 4:i + 2 + length]
        i += 2 + length
        keep = not (0xE0 <= marker <= 0xEF or marker == 0xFE)   # all non-APP, non-comment segments are image data
        keep |= marker == 0xE0 and body.startswith(b"JFIF")
        keep |= marker == 0xE2 and body.startswith(b"ICC_PROFILE")
        keep |= marker == 0xEE and body.startswith(b"Adobe")    # colour-transform flag affects decoding
        if keep:
            out += seg
        if marker == 0xDA:                                   # copy entropy-coded data up to the next real marker
            j = i
            while not (data[j] == 0xFF and data[j + 1] != 0x00 and not 0xD0 <= data[j + 1] <= 0xD7):
                j += 1
            out += data[i:j]; i = j
    if orientation not in (None, 1):
        exif = Image.Exif(); exif[0x0112] = orientation
        payload = exif.tobytes()
        if not payload.startswith(b"Exif\x00\x00"):
            payload = b"Exif\x00\x00" + payload
        app1 = b"\xff\xe1" + struct.pack(">H", len(payload) + 2) + payload
        pos = 2 + (struct.unpack(">H", out[4:6])[0] + 2 if out[2:4] == b"\xff\xe0" else 0)   # after JFIF if present
        out[pos:pos] = app1
    return bytes(out)


def strip_png(data):
    assert data[:8] == PNG_SIG, "not a PNG"
    orientation = Image.open(io.BytesIO(data)).getexif().get(0x0112)
    assert orientation in (None, 1), "PNG with a non-default EXIF orientation: handle by hand"
    out, i = bytearray(PNG_SIG), 8
    while i < len(data):
        length, ctype = struct.unpack(">I4s", data[i:i + 8])
        chunk = data[i:i + 12 + length]; i += 12 + length
        if ctype not in PNG_DROP:
            out += chunk
        if ctype == b"IEND":
            break                                            # drop anything appended after IEND
    return bytes(out)


def stripped(data):
    if data[:2] == b"\xff\xd8":
        return strip_jpeg(data)
    if data[:8] == PNG_SIG:
        return strip_png(data)
    return None


if __name__ == "__main__":
    check = "--check" in sys.argv
    dirty = []
    for path in [a for a in sys.argv[1:] if a != "--check"]:
        data = open(path, "rb").read()
        new = stripped(data)
        if new is None or new == data:
            continue
        if check:
            dirty.append(path)
            print(f"has metadata: {path}")
        else:
            open(path, "wb").write(new)
            print(f"stripped {path}: {len(data):,} -> {len(new):,} B")
    if dirty:
        print(f"\nFix with: python3 _tools/image_metadata.py {' '.join(shlex.quote(p) for p in dirty)}")
        sys.exit(1)
