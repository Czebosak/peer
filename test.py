from easy_pil import Canvas, Editor, Font

fonts = {
    "poppins": Font("app/assets/fonts/poppins.ttf", size=44),
    "poppins_small": Font("app/assets/fonts/poppins.ttf", size=36)
}

canvas = Canvas((920, 380), color=(34, 47, 53))
pfp = Editor(image="app/assets/img/avatar.png").resize((150, 150)).circle_image()

xp = 200
max_xp = 300

progress = round((xp / max_xp) * 800)
progress_left = (progress * -1) + 800
progress_show = round((xp / max_xp) * 100)

editor = Editor(canvas)
editor.rectangle((20, 20), 880, 340, color=(54, 57, 63))
editor.text(position=(40, 150), text="Czebosak#2281", font=fonts["poppins"], color="white")
editor.text(position=(40, 192), text="Level 10", font=fonts["poppins_small"], color="white")
editor.text(position=(40, 217), text=f"{xp}/{max_xp} XP", font=fonts["poppins_small"], color="white")
editor.text(position=(840, 190), text="20 messsages", font=fonts["poppins"], color="white", align="right")
editor.text(position=(840, 217), text=f"{progress_show}%", font=fonts["poppins"], color="white", align="right")
editor.rectangle((40, 260), 800, 70, (16, 43, 63), radius=35)
editor.rectangle((progress + 40, 260), progress_left, 70, color="white", radius=35)
editor.rectangle((progress + 40, 260), 35, 70, color="white")
editor.paste(image=pfp.image, position=(40, 0))

editor.show()
