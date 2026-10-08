# -*- coding: utf-8 -*-
"""Replace English AI/Economic bodies in module_info_pages.py with Ukrainian, then regen info_pages.txt."""
import ast, io, re, sys

SRC = r"C:\Program Files (x86)\Steam\steamapps\common\MountBlade Warband\Modules\Diplomacy\source\module_info_pages.py"
TXT = r"C:\Program Files (x86)\Steam\steamapps\common\MountBlade Warband\Modules\Diplomacy\info_pages.txt"
VERSION = "4.3+ for Steam"

AI_BODY = ("Низько:^"
" - Бали центрів для розподілу феодів рахуються (села 1 / замки 2 / міста 3) замість (1 / 1 / 2).^"
" - Для квестів порятунку полонених і подарунків перелік можливих родичів розширено (дядьки, тітки, свояки).^"
" - Зміни в розрахунках претендента щодо оцінки центрів.^"
" - Повертаючись у фракцію, лорди частіше обирають свою початкову (крім тієї, з якої їх вигнали). Впливають також відносини з іншими лордами, а не лише з лідерами.^^"
"Середньо:^"
" - Невеликі зміни у відносинах лордів при розподілі феодів.^"
" - Королі рідше скасовують рішення лордів.^"
" - Невеликі зміни для окремих характерів під час вибору кандидата.^"
" - Якщо лорд не знаходить хороших кандидатів, він використовує зважену систему оцінки.^"
" - Іноді використовується альтернативний розрахунок відомості * 3/2.^"
" - Лорди додатково покращують міста та наймають найманців.^^"
"Високо:^"
" - Чинник відомості при залицянні враховує престиж опікуна панянки.^"
" - Якщо є безфеодові лорди та немає вільних феодів — король може перерозподілити власне село.^"
" - При грабуванні сіл добровольці гинуть (і у гравця, і у ШІ).")

GOLD_BODY = ("Низько:^"
" - Політики фракції впливають на податкову неефективність.^"
" - Каравани приносять користь як місту відправлення, так і прибуття.^"
" - При здачі в полон є шанс зберегти частину спорядження залежно від приймача та складності.^"
" - Каравани враховують відстань і дещо частіше відвідують свою фракцію.^"
" - Золото торговців масштабується від добробуту міста (до 40%).^"
" - Ціни на їжу ростуть у містах в облозі 48+ годин.^"
" - Покращено продаж товарів профільним торговцям.^"
" - Їжа може не псуватися залежно від управління інвентарем.^"
" - Грабунок сіл затримує будівництво.^"
" - Торгові партії відвозять полонених у замки.^^"
"Середньо:^"
" - Подружжя і столиця дозволяють утримувати додатковий феод.^"
" - Споживання їжі росте з добробутом і гарнізоном.^"
" - Грабунок сіл більше не дає рівно 30 предметів.^"
" - Грабунок лордів впливає на золото, яке вони забирають у гравця.^"
" - Лідерство лордів знижує платню їх військ, як і у гравця.^"
" - Гравець може втрачати золото, коли грабують його феоди.^"
" - Найманці ростуть разом із прогресом гравця.^"
" - Подружжя отримує частину бонусу сюзерена.^"
" - Центри НІП страждають від нестачі платні.^"
" - Чужинці не можуть купувати підприємства.^"
" - Добробут села впливає на бандитів.^"
" - Староста отримує золото при купівлі худоби.^"
" - Селяни продають надлишки у містах.^^"
"Високо:^"
" - Загальний бонус королів сталий — при вигнанні перерозподіляється.^"
" - Надлишок золота лорда ділиться з гарнізонами.^"
" - Втрата честі залежить від поточної честі.^"
" - Грабунок спершу знімається з незібраних податків.^"
" - Полонені з центрів викуповуються 1:10.^"
" - Можна скасовувати покращення (гроші повертаються, відносини падають).")

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

with io.open(SRC, encoding="utf-8") as f:
    text = f.read()

pat_ai = re.compile(r'\(\"dplmc_ai_changes\".*?\"\),', re.DOTALL)
pat_gold = re.compile(r'\(\"dplmc_gold_changes\".*?\"\),', re.DOTALL)

new_ai = '("dplmc_ai_changes", "Опція: ШІ кампанії", "%s"),' % esc(AI_BODY)
new_gold = '("dplmc_gold_changes", "Опція: Економічний ШІ", "%s"),' % esc(GOLD_BODY)

text2, n_ai = pat_ai.subn(new_ai, text, count=1)
text2, n_gold = pat_gold.subn(new_gold, text2, count=1)
print("replaced ai=%d gold=%d" % (n_ai, n_gold))

with io.open(SRC, "w", encoding="utf-8", newline="") as f:
    f.write(text2)

# ---- regenerate info_pages.txt from the updated source via AST ----
with io.open(SRC, encoding="utf-8") as f:
    src = f.read()
mod = ast.parse(src)
infos = None
for node in mod.body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "info_pages":
        infos = node.value
        break
assert infos is not None, "info_pages not found"

def ev(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, str):
        return n.value
    if isinstance(n, ast.Name) and n.id == "DPLMC_DIPLOMACY_VERSION_STRING":
        return VERSION
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
        return ev(n.left) + ev(n.right)
    raise ValueError("unsupported node %s" % ast.dump(n)[:200])

entries = []
for elt in infos.elts:
    pid, pname, pbody = (ev(e) for e in elt.elts)
    entries.append((pid, pname, pbody))

out = ["infopagesfile version 1", str(len(entries))]
for pid, pname, pbody in entries:
    out.append("ip_%s %s %s" % (pid, pname.replace(" ", "_"), pbody.replace(" ", "_")))
data = "\n".join(out) + "\n"
with io.open(TXT, "w", encoding="utf-8", newline="") as f:
    f.write(data)
print("wrote %d entries, %d chars" % (len(entries), len(data)))
