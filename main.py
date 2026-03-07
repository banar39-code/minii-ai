import flet as ft
import os
from google import genai
from PIL import Image


os.makedirs("uploads", exist_ok=True)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def main(page: ft.Page):
    page.title = "Eyes AI - Cloud Хувилбар"
    page.window.width = 380
    page.window.height = 700
    
    garchig = ft.Text("Hi!!!! ene bol A.i 🧠👁️", size=24, weight="bold", color="blue")
    chat_delgets = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    chat_delgets.controls.append(ft.Text("AI: Сайн уу! Утаснаасаа 📷 товчийг дараад зургаа оруулаарай!", color="green"))

    songoson_zurag = [None] 

    
    def zurag_huulagdsan(e: ft.FilePickerUploadEvent):
        if not e.error:
            songoson_zurag[0] = os.path.join("uploads", e.file_name)
            chat_delgets.controls.append(ft.Text("📷 Зураг серверт амжилттай орж ирлээ! Одоо асуултаа бичээд 🚀 дарна уу.", color="orange"))
            page.update()

   
    def zurag_songoson(e: ft.FilePickerResultEvent):
        if e.files:
            f = e.files[0]
            chat_delgets.controls.append(ft.Text(f"⏳ Зургийг утаснаас сервер рүү татаж байна...", color="grey", italic=True))
            page.update()
       
            upload_url = page.get_upload_url(f.name, 60)
            file_picker.upload([ft.FilePickerUploadFile(f.name, upload_url=upload_url)])

    
    
    file_picker = ft.FilePicker()
    file_picker.on_result = zurag_songoson
    file_picker.on_upload = zurag_huulagdsan
    page.overlay.append(file_picker)

    
    def zurvas_ilgeeh(e):
        asuult = ug_bichih_hairtsag.value
        if not asuult and not songoson_zurag[0]: 
            return
            
        chat_delgets.controls.append(ft.Text(f"Та: {asuult if asuult else '(Зураг илгээв)'}", color="blue", weight="bold", text_align="right"))
        ug_bichih_hairtsag.value = ""
        
        huleeh_bichig = ft.Text("AI: ⏳ Тархи ажиллаж байна...", color="grey", italic=True)
        chat_delgets.controls.append(huleeh_bichig)
        page.update()

        try:
            ilgeeh_zuils = []
            
            if songoson_zurag[0]:
                img = Image.open(songoson_zurag[0])
                img.thumbnail((800, 800))
                ilgeeh_zuils.append(img)
                if not asuult: 
                    asuult = "Энэ зурган дээр юу байна вэ? Тайлбарлаж өгнө үү."
                    
            if asuult:
                ilgeeh_zuils.append(asuult) 

            hariult = client.models.generate_content(
                model='gemini-3.0-flash', 
                contents=ilgeeh_zuils
            )
            
            chat_delgets.controls.remove(huleeh_bichig)
            chat_delgets.controls.append(ft.Text(f"AI: {hariult.text}", color="green"))
            songoson_zurag[0] = None 
            
        except Exception as aldaa:
            chat_delgets.controls.remove(huleeh_bichig)
            chat_delgets.controls.append(ft.Text(f"AI: Алдаа гарлаа: {aldaa}", color="red"))

        page.update()

    ug_bichih_hairtsag = ft.TextField(hint_text="Асуух зүйлээ бичнэ үү...", expand=True, on_submit=zurvas_ilgeeh)
    zurag_tovch = ft.Button("📷", on_click=lambda _: file_picker.pick_files(allow_multiple=False))
    ilgeeh_tovch = ft.Button("🚀", on_click=zurvas_ilgeeh, bgcolor="blue", color="white")
    
    dood_hesed = ft.Row([zurag_tovch, ug_bichih_hairtsag, ilgeeh_tovch])
    page.add(garchig, chat_delgets, dood_hesed)


port = int(os.environ.get("PORT", 8000))
ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port, upload_dir="uploads")

            
        
                                            
