import fitz  # PyMuPDF
import os

def vurgulanan_kelimeler_alti_cizili_ve_yorumlar_al_ve_kaydet(pdf_dosyasi, cikti_dosyasi):
    doc = fitz.open(pdf_dosyasi)
    with open(cikti_dosyasi, 'w', encoding='utf-8') as f:
        for sayfa_no in range(len(doc)):
            sayfa = doc[sayfa_no]
            annotasyonlar = sayfa.annots()
            if annotasyonlar:
                for annot in annotasyonlar:
                    # Vurgu ve altı çizili kontrolü
                    if annot.type[0] in (8, 9):  # Highlight ve Underline tipleri
                        rect = annot.rect  # Annotasyonun dikdörtgenini al
                        vurgulanan_metin = sayfa.get_textbox(rect)  # Dikdörtgen içindeki metni çıkar
                        vurgulanan_metin = vurgulanan_metin.replace('\xad', '').replace('\n', ' ').strip()
                        
                        yorum = annot.info.get("content", "")  # Yorumu al, eğer yoksa boş string kullan
                        cikti_metni = f"Sayfa {sayfa_no + 1}: {vurgulanan_metin}"
                        if yorum:  # Yorum varsa cikti_metni'ne ekle
                            cikti_metni += f" {{Yorum: {yorum}}}"
                        cikti_metni += "\n"  # Her annotasyon için yeni bir satıra geç
                        f.write(cikti_metni)
    doc.close()
    return cikti_dosyasi

pdf_dosyasi = 'Hegel - Terry Pinkard.pdf'  # PDF dosyasının yolu
pdf_dosyasi_ismi = os.path.basename(pdf_dosyasi)
txt_dosyasi_ismi = os.path.splitext(pdf_dosyasi_ismi)[0] + '.txt'
cikti_dosyasi = os.path.join('', txt_dosyasi_ismi)

vurgulanan_metinler_dosyasi = vurgulanan_kelimeler_alti_cizili_ve_yorumlar_al_ve_kaydet(pdf_dosyasi, cikti_dosyasi)
print(vurgulanan_metinler_dosyasi)
