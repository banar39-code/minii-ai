import flet as ft
from google import genai
from PIL import Image
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def main(page: ft.Page):
    page.title = "Brain & Eyes A.I"
    page.window.width = 380
    page.window.height = 700

    garchig = ft.Text("Delhiin Brain&Eyes 🧠👁", size=24, weight="bold", color="blue")
    chat_delgets = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    chat_delgets.controls.append(ft.Text("AI: Nadad zurgiinhaa zamiig (C:\\Zurag.jpg) eswel asuultaa ilgeegeerei!", color="green"))

    def zurvas_ilgeeh(e):
        asuult = ug_bichih_hairtsag.value
        if not asuult:
            return

        chat_delgets.controls.append(ft.Text(f"Ta: {asuult}", color="blue", weight="bold", text_align="right"))
        ug_bichih_hairtsag.value = ""

        huleeh_bichig = ft.Text("AI ⏳ Zurgiig unshij baina, tvr hvleene uu...", color="grey", italic=True)
        chat_delgets.controls.append(huleeh_bichig)
        page.update()

        try:
            ilgeeh_zuils = []

            tsever_zam = asuult.strip(' " ').strip(" ' ").strip()

            if os.path.exists(tsever_zam):
                 if tsever_zam.lower().endswith(('.png', '.jpg', '.jpeg', 'webp')):
                    huleeh_bichig.value = "AI 🖼 Zurgiig olloo! Jijigrvvlj shahaad Google-rvv ilgeej baina..."
                    page.update()

                    img = Image.open(tsever_zam)

                    img.thumbnail((800, 800))

                    ilgeeh_zuils.append(img)
                    ilgeeh_zuils.append("Ene zurgan deer yu bna we? Mongoloor tailbarlaj ugnuu?")
                 else:
                    huleeh_bichig.value = "AI: ⚠️ Ene zam zurag bsih baina!"
                    page.update()
                    ilgeeh_zuils.append(asuult)
            else:
                huleeh_bichig.value = "AI 🌐 Engiin text gej vzeed ilgeej baina..."
                page.update()
                ilgeeh_zuils.append(asuult)

            hariult = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=ilgeeh_zuils
            )

            chat_delgets.controls.remove(huleeh_bichig)
            chat_delgets.controls.append(ft.Text(f"AI: {hariult.text}",color="green"))
          
        except Exception as aldaa:
            chat_delgets.controls.append(ft.Text(f"AI: Aldaa garlaa: {aldaa}", color="red"))

        page.update()

    ug_bichih_hairtsag = ft.TextField(hint_text="Asuult eswel zurgiin zam...", expand=True, on_submit=zurvas_ilgeeh)
    ilgeeh_tovch = ft.Button("🚀", on_click=zurvas_ilgeeh, bgcolor="blue", color="white")

    dood_heseg = ft.Row([ug_bichih_hairtsag, ilgeeh_tovch])
    page.add(garchig, chat_delgets, dood_heseg)

port = int(os.environ.get("PORT", 8000))
ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)

            
        
                                            

