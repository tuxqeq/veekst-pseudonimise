"""Names of private people, as they appear in CIS and Polish payment texts.

Every list here is written by hand from common names. Nothing comes from a
customer's statement. The generator draws a name, puts it in the grammatical
case a template needs, and writes it in one of the shapes a bank uses:
"ИВАНОВУ И.И.", "Иванов Иван Иванович", "И.И. Иванову", "IVANOV IVAN".

Two lists are kept apart by `split()` so that the held-out set measures names
the model never saw in training.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

# ---------------------------------------------------------------- Cyrillic

MALE_FIRST = """
Александр Алексей Анатолий Андрей Антон Арсений Артём Артур Богдан Борис Вадим
Валентин Валерий Василий Виктор Виталий Владимир Владислав Всеволод Вячеслав
Геннадий Георгий Глеб Григорий Даниил Денис Дмитрий Евгений Егор Захар Иван
Игорь Илья Кирилл Константин Лев Леонид Максим Матвей Михаил Никита Николай
Олег Павел Пётр Роман Руслан Семён Сергей Станислав Степан Тимофей Тимур
Фёдор Эдуард Юрий Ярослав Нурлан Ерлан Асхат Бауыржан Даурен Ержан Алмас Арман
Серик Мурат Талгат Айдар Санжар Азамат Еркебулан Жандос Дастан Аслан Марат
Рустам Ильдар Самат Канат Болат Алесь Янка Мікалай Уладзімір Сяргей Андрэй
Аляксандр Зміцер
""".split()

FEMALE_FIRST = """
Анна Алина Алла Алёна Анастасия Ангелина Валентина Валерия Вера Вероника
Виктория Галина Дарья Диана Евгения Екатерина Елена Елизавета Жанна Зоя Инна
Ирина Карина Кира Ксения Лариса Лидия Людмила Любовь Маргарита Марина Мария
Милана Надежда Наталья Нина Оксана Олеся Ольга Полина Раиса Светлана София
Таисия Тамара Татьяна Ульяна Юлия Яна Айгерим Айгуль Динара Жанар Гульнара
Асель Мадина Салтанат Алия Камила Аружан Жулдыз Сауле Дана Томирис Алеся
Святлана Вольга Наста
""".split()

# Base (male) surnames. The female form is made by `_female_surname`.
SURNAMES = """
Иванов Петров Сидоров Смирнов Кузнецов Попов Васильев Соколов Михайлов Новиков
Фёдоров Морозов Волков Алексеев Лебедев Семёнов Егоров Павлов Козлов Степанов
Николаев Орлов Андреев Макаров Никитин Захаров Зайцев Соловьёв Борисов Яковлев
Григорьев Романов Воробьёв Сергеев Кузьмин Фролов Александров Дмитриев Королёв
Гусев Киселёв Ильин Максимов Поляков Сорокин Виноградов Ковалёв Белов Медведев
Антонов Тарасов Жуков Баранов Филиппов Комаров Давыдов Беляев Герасимов
Богданов Осипов Бобров Литвинов Мартынов Гаврилов Шубин Карпов Лукин Юдин
Ахметов Жумабаев Абенов Касымов Оспанов Тулегенов Искаков Сулейменов
Кенжебаев Есенов Мухамедов Нурпеисов Байжанов Садыков Омаров Рахимов Галиев
Ковальский Высоцкий Заболоцкий Островский Савицкий Козловский Ковалевский
Гурский Яблонский Вишневский Каминский Левандовский Тарасевич Лукашевич
Богданович Климович Карпович Мицкевич Якубович Война Шевченко Бондаренко
Ткаченко Кравченко Гончаренко Левченко Сидоренко Коваленко Ковальчук Шевчук
Полищук Мельник Новик Жук Сенкевич Пашкевич Котов Чернов Дорофеев Субботин
Тихонов Ершов Блинов Щербаков Голубев Пестов Рыбаков Мухин Голованов Дьячков
""".split()

# ---------------------------------------------------------------- Polish

PL_MALE_FIRST = """
Jan Piotr Krzysztof Andrzej Tomasz Paweł Michał Marcin Grzegorz Łukasz Adam
Marek Kamil Jakub Mateusz Wojciech Rafał Dariusz Bartosz Szymon Filip Robert
Maciej Sebastian Damian Patryk Artur Zbigniew Jerzy Stanisław
""".split()

PL_FEMALE_FIRST = """
Anna Maria Katarzyna Małgorzata Agnieszka Barbara Ewa Magdalena Joanna
Aleksandra Monika Zofia Krystyna Elżbieta Natalia Karolina Paulina Justyna
Beata Dorota Marta Weronika Julia Alicja
""".split()

PL_SURNAMES = """
Nowak Kowalski Wiśniewski Wójcik Kowalczyk Kamiński Lewandowski Zieliński
Szymański Woźniak Dąbrowski Kozłowski Jankowski Mazur Kwiatkowski Krawczyk
Piotrowski Grabowski Nowakowski Pawłowski Michalski Król Wieczorek Jabłoński
Wróbel Nowicki Majewski Olszewski Stępień Malinowski Jaworski Adamczyk Dudek
Zając Pietrzak Górski Rutkowski Sikora Baran Walczak
""".split()

CASES = ("nom", "gen", "dat", "acc", "ins", "pre")


# ------------------------------------------------- Russian declension rules


def _decline_first_male(n: str, case: str) -> str:
    if case == "nom":
        return n
    if n.endswith("й"):
        stem = n[:-1]
        return stem + {"gen": "я", "dat": "ю", "acc": "я", "ins": "ем", "pre": "е"}[case]
    if n.endswith("ь"):
        stem = n[:-1]
        return stem + {"gen": "я", "dat": "ю", "acc": "я", "ins": "ем", "pre": "е"}[case]
    if n.endswith(("а", "я")):
        return _decline_first_female(n, case)
    if n.endswith("о"):
        return n
    if n == "Лев":
        n = "Льв"
    if n == "Пётр":
        n = "Петр"
    return n + {"gen": "а", "dat": "у", "acc": "а", "ins": "ом", "pre": "е"}[case]


def _decline_first_female(n: str, case: str) -> str:
    if case == "nom":
        return n
    if n.endswith("ия"):
        stem = n[:-2]
        return stem + {"gen": "ии", "dat": "ии", "acc": "ию", "ins": "ией", "pre": "ии"}[case]
    if n.endswith("ья"):
        stem = n[:-2]
        return stem + {"gen": "ьи", "dat": "ье", "acc": "ью", "ins": "ьей", "pre": "ье"}[case]
    if n.endswith("я"):
        stem = n[:-1]
        return stem + {"gen": "и", "dat": "е", "acc": "ю", "ins": "ей", "pre": "е"}[case]
    if n.endswith("а"):
        stem = n[:-1]
        soft = stem[-1:] in "гкхжшщч"
        gen = "и" if soft else "ы"
        ins = "ей" if stem[-1:] in "жшщчц" else "ой"
        return stem + {"gen": gen, "dat": "е", "acc": "у", "ins": ins, "pre": "е"}[case]
    if n.endswith("ь"):
        stem = n[:-1]
        return stem + {"gen": "и", "dat": "и", "acc": "ь", "ins": "ью", "pre": "и"}[case]
    return n  # Айгерим, Жанар, Асель-like names stay as written


def patronymic(father: str, female: bool) -> str:
    special = {
        "Илья": ("Ильич", "Ильинична"),
        "Никита": ("Никитич", "Никитична"),
        "Пётр": ("Петрович", "Петровна"),
        "Лев": ("Львович", "Львовна"),
        "Павел": ("Павлович", "Павловна"),
        "Фёдор": ("Фёдорович", "Фёдоровна"),
    }
    if father in special:
        return special[father][int(female)]
    if father.endswith(("ий",)):
        stem = father[:-2]
        return stem + ("ьевна" if female else "ьевич")
    if father.endswith("й"):
        stem = father[:-1]
        return stem + ("евна" if female else "евич")
    if father.endswith(("а", "я")):
        stem = father[:-1]
        return stem + ("ична" if female else "ич")
    return father + ("овна" if female else "ович")


def _decline_patronymic(p: str, case: str) -> str:
    if case == "nom":
        return p
    if p.endswith("на"):
        stem = p[:-1]
        return stem + {"gen": "ы", "dat": "е", "acc": "у", "ins": "ой", "pre": "е"}[case]
    return p + {"gen": "а", "dat": "у", "acc": "а", "ins": "ем", "pre": "е"}[case]


def _female_surname(s: str) -> str:
    if s.endswith(("ов", "ев", "ёв", "ин", "ын")):
        return s + "а"
    if s.endswith("ский"):
        return s[:-4] + "ская"
    if s.endswith("цкий"):
        return s[:-4] + "цкая"
    return s  # -ич, -ко, -ук, -ник and the rest do not change


def _decline_surname(s: str, female: bool, case: str) -> str:
    if case == "nom":
        return s
    if not female:
        if s.endswith(("ов", "ев", "ёв", "ин", "ын")):
            return s + {"gen": "а", "dat": "у", "acc": "а", "ins": "ым", "pre": "е"}[case]
        if s.endswith(("ский", "цкий")):
            stem = s[:-2]
            return stem + {"gen": "ого", "dat": "ому", "acc": "ого", "ins": "им", "pre": "ом"}[case]
        if s.endswith(("ич", "ук", "юк", "ник", "ик", "ок", "ак")) or s[-1] in "бвгджзклмнпрстфхцчшщ":
            ins = "ем" if s[-1] in "жшщчц" else "ом"
            return s + {"gen": "а", "dat": "у", "acc": "а", "ins": ins, "pre": "е"}[case]
        if s.endswith("а"):  # Война
            return _decline_first_female(s, case)
        return s  # -енко, -ко
    if s.endswith(("ова", "ева", "ёва", "ина", "ына")):
        return s[:-1] + {"gen": "ой", "dat": "ой", "acc": "у", "ins": "ой", "pre": "ой"}[case]
    if s.endswith(("ская", "цкая")):
        stem = s[:-2]
        return stem + {"gen": "ой", "dat": "ой", "acc": "ую", "ins": "ой", "pre": "ой"}[case]
    if s.endswith("а"):
        return _decline_first_female(s, case)
    return s


# ----------------------------------------------------------- Transliteration

_TR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu",
    "я": "ya", "і": "i", "ў": "u", "ә": "a", "ғ": "g", "қ": "k", "ң": "n", "ө": "o",
    "ұ": "u", "ү": "u", "һ": "h",
}


def translit(s: str) -> str:
    out = []
    for ch in s:
        low = ch.lower()
        if low in _TR:
            t = _TR[low]
            out.append(t.capitalize() if ch.isupper() and t else t)
        else:
            out.append(ch)
    return "".join(out)


# ------------------------------------------------------------------ People


@dataclass(frozen=True)
class Person:
    first: str
    surname: str  # base, male
    father: str
    female: bool
    lang: str  # "ru" or "pl"

    def surname_in(self, case: str) -> str:
        if self.lang == "pl":
            return _pl_surname(self.surname, self.female, case)
        s = _female_surname(self.surname) if self.female else self.surname
        return _decline_surname(s, self.female, case)

    def first_in(self, case: str) -> str:
        if self.lang == "pl":
            return _pl_first(self.first, self.female, case)
        if self.female:
            return _decline_first_female(self.first, case)
        return _decline_first_male(self.first, case)

    def patronymic_in(self, case: str) -> str:
        return _decline_patronymic(patronymic(self.father, self.female), case)


def _pl_surname(s: str, female: bool, case: str) -> str:
    if s.endswith("ski") or s.endswith("cki"):
        base = s[:-1]
        if female:
            return {"nom": base + "a", "gen": base + "iej", "dat": base + "iej",
                    "acc": base + "ą", "ins": base + "ą", "pre": base + "iej"}[case].replace("kiiej", "kiej").replace("ciiej", "ciej")
        return {"nom": s, "gen": base + "iego", "dat": base + "iemu", "acc": base + "iego",
                "ins": base + "im", "pre": base + "im"}[case]
    if female:
        return s
    return {"nom": s, "gen": s + "a", "dat": s + "owi", "acc": s + "a", "ins": s + "em", "pre": s + "u"}[case]


def _pl_first(n: str, female: bool, case: str) -> str:
    if female and n.endswith("a"):
        stem = n[:-1]
        if stem.endswith("i"):
            return {"nom": n, "gen": stem, "dat": stem, "acc": stem + "ę", "ins": stem + "ą", "pre": stem}[case] if case != "nom" else n
        return {"nom": n, "gen": stem + "y", "dat": stem + "ie", "acc": stem + "ę", "ins": stem + "ą", "pre": stem + "ie"}[case]
    if female:
        return n
    return {"nom": n, "gen": n + "a", "dat": n + "owi", "acc": n + "a", "ins": n + "em", "pre": n + "ie"}[case]


@dataclass
class Pools:
    male_first: list[str]
    female_first: list[str]
    surnames: list[str]
    pl_male_first: list[str]
    pl_female_first: list[str]
    pl_surnames: list[str]


def split(seed: int = 7, held_out: float = 0.2) -> tuple[Pools, Pools]:
    """Train and held-out pools with no name in common."""
    rnd = random.Random(seed)

    def cut(xs: list[str]) -> tuple[list[str], list[str]]:
        xs = sorted(set(xs))
        rnd.shuffle(xs)
        k = max(1, int(len(xs) * held_out))
        return xs[k:], xs[:k]

    parts = [cut(x) for x in (MALE_FIRST, FEMALE_FIRST, SURNAMES, PL_MALE_FIRST, PL_FEMALE_FIRST, PL_SURNAMES)]
    return Pools(*[p[0] for p in parts]), Pools(*[p[1] for p in parts])


def person(rnd: random.Random, pools: Pools, lang: str) -> Person:
    female = rnd.random() < 0.45
    if lang == "pl":
        first = rnd.choice(pools.pl_female_first if female else pools.pl_male_first)
        return Person(first, rnd.choice(pools.pl_surnames), "", female, "pl")
    first = rnd.choice(pools.female_first if female else pools.male_first)
    father = rnd.choice([n for n in pools.male_first if n[-1] not in "аяь"] or ["Иван"])
    return Person(first, rnd.choice(pools.surnames), father, female, "ru")


def initial(word: str) -> str:
    return word[0].upper() + "."


def render(p: Person, case: str, rnd: random.Random, upper: bool | None = None) -> str:
    """One written form of a person's name in a grammatical case."""
    if p.lang == "pl":
        shapes = [
            lambda: f"{p.first_in(case)} {p.surname_in(case)}",
            lambda: f"{p.surname_in(case)} {p.first_in(case)}",
            lambda: f"{initial(p.first)} {p.surname_in(case)}",
            lambda: p.surname_in(case),
        ]
        text = rnd.choices(shapes, weights=[6, 2, 1, 1])[0]()
    else:
        sur, first, pat = p.surname_in(case), p.first_in(case), p.patronymic_in(case)
        shapes = [
            lambda: f"{sur} {initial(p.first)}{initial(patronymic(p.father, p.female))}",
            lambda: f"{sur} {initial(p.first)} {initial(patronymic(p.father, p.female))}",
            lambda: f"{initial(p.first)}{initial(patronymic(p.father, p.female))} {sur}",
            lambda: f"{initial(p.first)} {initial(patronymic(p.father, p.female))} {sur}",
            lambda: f"{sur} {first} {pat}",
            lambda: f"{first} {pat} {sur}",
            lambda: f"{sur} {first}",
            lambda: f"{first} {sur}",
            lambda: f"{sur} {initial(p.first)}",
            lambda: sur,
        ]
        text = rnd.choices(shapes, weights=[8, 3, 4, 2, 8, 2, 4, 3, 2, 1])[0]()
    if upper is None:
        upper = rnd.random() < 0.5
    return text.upper() if upper else text


def render_latin(p: Person, rnd: random.Random) -> str:
    sur, first = translit(p.surname_in("nom")), translit(p.first_in("nom"))
    shapes = [f"{sur} {first}", f"{first} {sur}", f"{sur} {first[0]}.", f"{first[0]}. {sur}"]
    text = rnd.choice(shapes)
    return text.upper() if rnd.random() < 0.6 else text
