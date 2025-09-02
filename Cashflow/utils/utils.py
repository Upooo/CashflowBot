def rupiah(n:int):
    try:
        return "Rp " + "{:,}".format(int(n)).replace(",", ".")
    except:
        return f"Rp {n}"

def safe_int(text:str):
    try:
        return int(text.replace(",", "").replace(".", "").strip())
    except Exception:
        raise ValueError("Tidak bisa konversi ke angka")

def format_note_doc(doc):
    t = doc.get("created_at")
    when = t.strftime("%Y-%m-%d %H:%M") if hasattr(t, "strftime") else str(t)
    return f"[{str(doc.get('_id'))[:6]}] {doc.get('type').upper()} {rupiah(doc.get('amount'))} — {doc.get('desc')} ({when})"

