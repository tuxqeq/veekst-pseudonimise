"""Templates of payment purposes and of questions a person asks.

Written by hand, in the shapes CIS and Polish banks use. No template is copied
from a customer's statement: numbers, contracts, registration codes and names
are slots, and the generator fills them.

Slots:
  {P:<case>}   a private person, Cyrillic, in a Russian grammatical case
  {PL:<case>}  a private person, Polish
  {PLAT}       a private person, Latin letters
  {ORG}        a company, never a person         {BANK} a bank
  {N}          a number    {D} a date    {AMT} an amount    {Y} a year
  {MON} a month, nominative   {MONG} a month, genitive   {MONP} prepositional
  {MEN} a month in English    {MPL} a month in Polish
  {SERV} a service            {CITY} a city      {STREET} a street
  {CUR} a currency code

Each template has a style: "up" (a statement in capitals), "mix" (a
statement in normal case), "q" (a question a person types).
"""

from __future__ import annotations

# (style, language, template)
PURPOSES: list[tuple[str, str, str]] = [
    # ---- Belarus / Russia, capitals
    ("up", "ru", "ПОДОХОДНЫЙ НАЛОГ УДЕРЖАН ИЗ ДИВИДЕНДОВ {P:dat} ОТ СУММЫ {AMT} И ПЕРЕЧИСЛЕН В БЮДЖЕТ ПОЛНОСТЬЮ ПО СРОКУ УПЛАТЫ ДО {D}"),
    ("up", "ru", "ПОДОХОДНЫЙ НАЛОГ С ДОХОДОВ {P:gen} ЗА {MON} {Y} ГОДА"),
    ("up", "ru", "ВЫПЛАТА ДИВИДЕНДОВ {P:dat} ЗА {Y} ГОД СОГЛАСНО РЕШЕНИЮ N {N} ОТ {D}"),
    ("up", "ru", "ПРОФЕССИОНАЛЬНЫЙ ДОХОД ЗА {MON}, {Y} {P:nom} РЕЗИДЕНТ РБ, {SERV}"),
    ("up", "ru", "ЗАРАБОТНАЯ ПЛАТА ЗА {MON} {Y} {P:dat}"),
    ("up", "ru", "ЗАРПЛАТА {P:dat} ЗА {MON} {Y} Г."),
    ("up", "ru", "АВАНС ПО ЗАРАБОТНОЙ ПЛАТЕ ЗА {MON} {Y} {P:dat} НА КАРТСЧЕТ"),
    ("up", "ru", "ОТПУСКНЫЕ {P:dat} ЗА {MON} {Y}"),
    ("up", "ru", "ВОЗВРАТ ПОДОТЧЕТНЫХ СУММ {P:dat} ПО АВАНСОВОМУ ОТЧЕТУ N {N} ОТ {D}"),
    ("up", "ru", "КОМАНДИРОВОЧНЫЕ РАСХОДЫ {P:dat} ПО ПРИКАЗУ N {N} ОТ {D}"),
    ("up", "ru", "ОПЛАТА ПО ДОГОВОРУ ПОДРЯДА N {N} ОТ {D} {P:dat} ЗА {SERV}"),
    ("up", "ru", "ВОЗНАГРАЖДЕНИЕ ПО ДОГОВОРУ ПОДРЯДА С {P:ins} ЗА {MON} {Y}"),
    ("up", "ru", "ОПЛАТА ПО СЧЕТУ N {N} ОТ {D} ИП {P:nom} ЗА {SERV}. БЕЗ НДС"),
    ("up", "ru", "ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ {P:nom} ОПЛАТА ЗА {SERV} ПО ДОГОВОРУ N {N}"),
    ("up", "ru", "ПЕРЕВОД СРЕДСТВ НА КАРТСЧЕТ {P:gen} СОГЛАСНО ЗАЯВЛЕНИЮ ОТ {D}"),
    ("up", "ru", "АЛИМЕНТЫ С {P:gen} ЗА {MON} {Y} ПО ИСПОЛНИТЕЛЬНОМУ ЛИСТУ N {N}"),
    ("up", "ru", "МАТЕРИАЛЬНАЯ ПОМОЩЬ {P:dat} СОГЛАСНО ПРИКАЗУ N {N}"),
    ("up", "ru", "ВОЗВРАТ ЗАЙМА УЧРЕДИТЕЛЮ {P:dat} ПО ДОГОВОРУ ЗАЙМА N {N} ОТ {D}"),
    ("up", "ru", "ВЗНОС В УСТАВНЫЙ ФОНД УЧРЕДИТЕЛЕМ {P:ins}"),
    ("up", "ru", "ОПЛАТА АРЕНДЫ ЗА {MON} {Y} ПО ДОГОВОРУ С {P:ins} N {N}"),
    ("up", "ru", "ВЫПЛАТЫ ПО ДОГОВОРАМ ПОДРЯДА ЗА {MON} {Y} {P:dat} И {P:dat}"),
    ("up", "ru", "ПЕРЕЧИСЛЕНИЕ ЗАРАБОТНОЙ ПЛАТЫ СОТРУДНИКУ {P:dat} ЗА {MON}"),
    ("up", "ru", "ОПЛАТА ЗА ОБУЧЕНИЕ СОТРУДНИКА {P:gen} ПО ДОГОВОРУ N {N} ОТ {D}"),
    ("up", "ru", "ОПЛАТА ПО ДОГОВОРУ N {N} ОТ {D} ЗА {SERV}. ПОЛУЧАТЕЛЬ {P:nom}"),
    ("up", "ru", "ВОЗМЕЩЕНИЕ РАСХОДОВ {P:dat} НА {SERV}"),
    ("up", "ru", "ПРЕМИЯ {P:dat} ПО ИТОГАМ {MONG} {Y}"),
    ("up", "ru", "ОКОНЧАТЕЛЬНЫЙ РАСЧЕТ ПРИ УВОЛЬНЕНИИ {P:gen}"),
    ("up", "ru", "ОТЧИСЛЕНИЯ В ФСЗН ЗА {P:acc} ЗА {MON} {Y}"),
    # ---- the same, in normal case
    ("mix", "ru", "Выплата заработной платы {P:dat} за {MON} {Y} года"),
    ("mix", "ru", "Перевод на карту {P:gen} по заявлению от {D}"),
    ("mix", "ru", "Возврат подотчетных средств {P:dat}"),
    ("mix", "ru", "Оплата по договору оказания услуг № {N} от {D}, исполнитель {P:nom}"),
    ("mix", "ru", "ИПН с доходов {P:gen} за {MON} {Y} года"),
    ("mix", "ru", "Референс {N}; Внутрибанковский перевод с текущего счета, Клиент {P:nom}"),
    ("mix", "ru", "Перевод собственных средств, отправитель {P:nom}"),
    ("mix", "ru", "Выплата дивидендов участнику {P:dat} за {Y} год"),
    ("mix", "ru", "Оплата по счету № {N} от {D} ИП {P:nom} за {SERV}"),
    ("mix", "ru", "Возмещение командировочных расходов {P:dat}, приказ № {N}"),
    ("mix", "ru", "Займ от учредителя {P:gen} по договору № {N} от {D}"),
    ("mix", "ru", "Аренда помещения у физического лица {P:gen} за {MON}"),
    ("mix", "ru", "Социальные отчисления за {P:acc} за {MON} {Y}"),
    ("mix", "ru", "Пенсионные взносы {P:gen} за период {MON} {Y} г."),
    ("mix", "ru", "Оплата услуг по договору ГПХ с {P:ins}"),
    ("mix", "ru", "Премия {P:dat} за {MON} {Y}"),
    # ---- Latin letters (Kazakh and Belarusian currency payments)
    ("up", "en", "SALARY {MEN} {Y} {PLAT}"),
    ("up", "en", "PAYMENT TO {PLAT} FOR CONSULTING SERVICES UNDER CONTRACT {N} DD {D}"),
    ("mix", "en", "Payment for IT services by invoice {N} dd {D}, beneficiary {PLAT}"),
    ("mix", "en", "Transfer from {PLAT} own funds"),
    ("up", "en", "/BNF/{PLAT} /PURPOSE/ SERVICES INV {N}"),
    ("mix", "en", "Dividends {Y} to shareholder {PLAT}"),
    ("up", "en", "REIMBURSEMENT OF EXPENSES {PLAT} {D}"),
    # ---- Poland
    ("up", "pl", "WYNAGRODZENIE ZA {MPL} {Y} {PL:nom}"),
    ("up", "pl", "PRZELEW DLA {PL:gen} FAKTURA {N}"),
    ("mix", "pl", "Zwrot kosztów delegacji dla {PL:gen}"),
    ("mix", "pl", "Wynagrodzenie {PL:nom} umowa zlecenie {MPL} {Y}"),
    ("up", "pl", "FAKTURA {N} {PL:nom} USŁUGI PROGRAMISTYCZNE"),
    ("mix", "pl", "Zaliczka dla {PL:gen} na {MPL}"),
    ("mix", "pl", "Przelew od {PL:gen} tytułem zwrotu pożyczki"),
]

# Purposes that name no private person. About half of what a bank writes.
NEGATIVES: list[tuple[str, str, str]] = [
    ("up", "ru", "ПОДОХОДНЫЙ НАЛОГ УДЕРЖАН ИЗ ОКОНЧАТЕЛЬНОГО РАСЧЕТА ЗА {MON} {Y} ГОДА И ПЕРЕЧИСЛЕН В БЮДЖЕТ ПОЛНОСТЬЮ ПО СРОКУ УПЛАТЫ {D}"),
    ("up", "ru", "ОТЧИСЛЕНИЯ В ФСЗН ИЗ ОТПУСКНЫХ ЗА {MON} {Y} ГОДА. РЕГИСТРАЦИОННЫЙ НОМЕР {N}"),
    ("up", "ru", "ОПЛАТА ПО ДОГОВОРУ АРЕНДЫ {N} ОТ {D} ЗА {MON} {Y} Г. СТАВКА НДС 20%, СУММА НДС {AMT}"),
    ("up", "ru", "{ORG} ОПЛАТА ЗА {SERV} СОГЛАСНО ДОГОВОРУ N {N} ОТ {D}"),
    ("up", "ru", "ОПЛАТА ЗА {SERV} ПО СЧЕТУ N {N} ОТ {D}. В Т.Ч. НДС {AMT}"),
    ("up", "ru", "ВЫПЛАТЫ ПО ДОГОВОРАМ ПОДРЯДА ЗА {MON}, {Y} СОГЛ. СПИСКУ N {N} ОТ {D} Г."),
    ("up", "ru", "ЗАРАБОТНАЯ ПЛАТА ЗА {MON} {Y} СОГЛАСНО ВЕДОМОСТИ N {N}"),
    ("up", "ru", "ПЕРЕЧИСЛЕНИЕ НА КАРТСЧЕТА СОТРУДНИКОВ СОГЛАСНО СПИСКУ N {N}"),
    ("up", "ru", "ВОЗВРАТ ОШИБОЧНО ПЕРЕЧИСЛЕННЫХ СРЕДСТВ ПО П/П N {N} ОТ {D}"),
    ("up", "ru", "ОПЛАТА ЗА ТОВАР ПО ТТН N {N} ОТ {D} {ORG}"),
    ("up", "ru", "ПЛАТА ЗА ОБСЛУЖИВАНИЕ СЧЕТА {BANK} ЗА {MON} {Y}"),
    ("up", "ru", "АРЕНДА ОФИСА ПО АДРЕСУ Г. {CITY}, {STREET} ЗА {MON}"),
    ("up", "ru", "ДОСТАВКА ПОЧТЫ НА ЭТАЖ СОГЛАСНО ДОГОВОРУ {N}"),
    ("up", "ru", "ПРОДАЖА ВАЛЮТЫ {CUR} ПО КУРСУ {AMT}"),
    ("up", "ru", "ОБЯЗАТЕЛЬНОЕ СТРАХОВАНИЕ ОТ НЕСЧАСТНЫХ СЛУЧАЕВ НА ПРОИЗВОДСТВЕ ЗА {MON} {Y}"),
    ("mix", "ru", "Комиссия за перевод в {BANK}"),
    ("mix", "ru", "Оплата по счету № {N} от {D} за {SERV}. Сумма {AMT} без НДС"),
    ("mix", "ru", "Взносы на ОСМС за {MON} {Y} года согласно прилагаемого списка"),
    ("mix", "ru", "Заработная плата за {MON} для зачисления на картсчета сотрудникам согласно спискам {AMT} тенге"),
    ("mix", "ru", "Аренда облака за {MON} {Y} года по договору № {N} от {D}"),
    ("mix", "ru", "Оплата услуг связи {ORG} за {MON}"),
    ("mix", "ru", "Перевод между своими счетами в {BANK}"),
    ("mix", "ru", "Возврат по договору № {N}, {ORG}"),
    ("mix", "ru", "Оплата за {SERV} на сайте {ORG}"),
    ("up", "en", "PAYMENT FOR SOFTWARE DEVELOPMENT ACCORDING TO CONTRACT {N} DD {D}"),
    ("mix", "en", "Payment for {SERV} by invoice {N} dd {D}. Money transfer is not connected with business activity"),
    ("mix", "en", "Commission for {Y} on account No. {N} dated {D}"),
    ("up", "en", "{ORG} INVOICE {N} {CUR}"),
    ("up", "pl", "WARTOŚĆ PIT-4R {MPL} {Y}"),
    ("up", "pl", "PROWIZJA ZA PRZELEW WALUTOWY"),
    ("up", "pl", "ZUS {MPL} {Y}"),
    ("mix", "pl", "Faktura {N} {ORG} usługi hostingowe"),
    ("up", "pl", "WYNAGRODZENIE ZA {MPL} {Y}"),
    ("mix", "pl", "Opłata za prowadzenie rachunku {BANK}"),
]

QUESTIONS: list[tuple[str, str, str]] = [
    ("q", "ru", "Сколько мы заплатили {P:dat} в {MONP}?"),
    ("q", "ru", "сколько ушло {P:dat} за {Y} год"),
    ("q", "ru", "Почему платёж {P:dat} попал в маркетинг?"),
    ("q", "ru", "Покажи все выплаты {P:dat}"),
    ("q", "ru", "Что за платеж от {P:gen} в {MONP}?"),
    ("q", "ru", "{P:nom} — это наш подрядчик, поставь его в разработку"),
    ("q", "ru", "Кто такой {P:nom} в выписке?"),
    ("q", "ru", "переводы {P:dat} это зарплата"),
    ("q", "ru", "Платежи {P:dat} и {P:dat} это аренда?"),
    ("q", "ru", "Найди платежи с {P:ins}"),
    ("q", "ru", "Сколько дивидендов получил {P:nom}?"),
    ("q", "en", "How much did we pay {PLAT} in {MEN}?"),
    ("q", "en", "Why is the payment to {PLAT} in marketing?"),
    ("q", "en", "{PLAT} is our contractor"),
    ("q", "pl", "Ile zapłaciliśmy {PL:dat} w {MPL}?"),
    ("q", "pl", "Dlaczego przelew dla {PL:gen} jest w marketingu?"),
]

QUESTION_NEGATIVES: list[tuple[str, str, str]] = [
    ("q", "ru", "Сколько мы потратили на аренду в {MONP}?"),
    ("q", "ru", "Почему выручка упала в {MONP}?"),
    ("q", "ru", "Покажи топ пять расходов за {Y} год"),
    ("q", "ru", "Где загрузить выписку?"),
    ("q", "ru", "Что такое проводка?"),
    ("q", "ru", "Сколько мы заплатили {ORG} в {MONP}?"),
    ("q", "ru", "платежи в {BANK} это комиссия?"),
    ("q", "ru", "Почему такси в маркетинге?"),
    ("q", "ru", "Сравни март и апрель"),
    ("q", "ru", "Какие вопросы остались в проверке?"),
    ("q", "en", "Why is March lower than February?"),
    ("q", "en", "How much did we pay {ORG} in {MEN}?"),
    ("q", "pl", "Ile wydaliśmy na {SERV} w {MPL}?"),
]

ORGS = """
ООО «Ромашка»|ОДО "ТЕХНОСТРОЙ"|ЧУП «БЕЛСЕРВИС»|УП "МИНСКВОДОКАНАЛ"|ИООО "ДПД БЕЛ"|
РУП "БЕЛПОЧТА"|ЗАО "АЛЬФА-СОФТ"|ОАО "МИНСКИЙ ТРАКТОРНЫЙ ЗАВОД"|ТОО "KAZ LOGISTICS"|
ТОО «Алматы Сервис»|АО "Казахтелеком"|LLP NOMAD SOFT|ООО "Яндекс.Такси"|
GOOGLE IRELAND LTD|AMAZON WEB SERVICES EMEA SARL|ATLASSIAN PTY LTD|JETBRAINS S.R.O.|
DIGITALOCEAN LLC|OVH SP. Z O.O.|ORANGE POLSKA S.A.|ALLEGRO SP. Z O.O.|
МТС|А1|ЕВРООПТ|ГИППО|БЕЛАВИА|ВЕЛКОМ|KASPI.KZ|WOLT|BOLT|GLOVO|SPOTIFY|ZOOM VIDEO
""".replace("\n", "").split("|")

BANKS = ["ПРИОРБАНК ОАО", "ОАО «Приорбанк»", "Альфа-Банк", "БЕЛАРУСБАНК", "ОАО АСБ БЕЛАРУСБАНК",
         "Kaspi Bank", "АО «Bank RBK»", "Halyk Bank", "PKO BP", "mBank", "BNY MELLON"]

SERVICES = ["ТЕХНИЧЕСКОЕ ОБСЛУЖИВАНИЕ", "УСЛУГИ СВЯЗИ", "РАЗРАБОТКУ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ",
            "КОНСУЛЬТАЦИОННЫЕ УСЛУГИ", "РЕПЕТИТОРСТВО ПО АНГЛИЙСКОМУ ЯЗЫКУ", "УБОРКУ ПОМЕЩЕНИЙ",
            "ДИЗАЙН ЛОГОТИПА", "ПЕРЕВОД ДОКУМЕНТОВ", "РЕМОНТ ОРГТЕХНИКИ", "ХОСТИНГ",
            "рекламные услуги", "бухгалтерские услуги", "аренду оборудования", "подписку на сервис",
            "обучение по онлайн курсу", "услуги такси", "доставку"]

CITIES = ["МИНСК", "ГРОДНО", "БРЕСТ", "АЛМАТЫ", "АСТАНА", "ВАРШАВА", "Минск", "Алматы"]

# Streets carry a famous person's name. That is not a private person, and the
# detector must leave it alone.
STREETS = ["УЛ. ЛЕНИНА, {N}", "ПР-Т НЕЗАВИСИМОСТИ, {N}", "УЛ. ПУШКИНА, Д. {N}", "УЛ. АБАЯ {N}",
           "ул. Гагарина, д. {N}", "УЛ. КАЛИНОВСКОГО {N}", "ул. Сурганова {N}"]

MONTHS = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь",
          "октябрь", "ноябрь", "декабрь"]
MONTHS_GEN = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа",
              "сентября", "октября", "ноября", "декабря"]
MONTHS_PRE = ["январе", "феврале", "марте", "апреле", "мае", "июне", "июле", "августе",
              "сентябре", "октябре", "ноябре", "декабре"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December"]
MONTHS_PL = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień",
             "wrzesień", "październik", "listopad", "grudzień"]
CURRENCIES = ["USD", "EUR", "RUB", "KZT", "BYN", "PLN"]
