# Inventory Manager

Inventory Manager je aplikace postavená na Django frameworku pro správu skladových zásob. Je navržena tak, aby usnadnila sledování produktů, jejich umístění a stav. Nabízí jednoduché rozhraní a široké možnosti filtrování a vyhledávání produktů.

## Funkcionality

- Správa produktů: Možnost přidávat, upravovat a mazat produkty.

- Vyhledávání: Fulltextové vyhledávání.

- Filtrování: Filtrování produktů podle lokality a jiných parametrů.

- Stránkování: Optimalizované zobrazení velkého množství dat s možností stránkování.

- Integrace: Podpora integrace s XML daty pro import a export produktů.

- Správa lokalit: Produkty jsou propojeny s lokacemi pomocí vztahu many-to-many.

## Požadavky
- Python 3.9+

- Django 5.1.1

- Další knihovny specifikované v requirements.txt

## Instalace

1. Naklonujte repozitář:

``` git clone https://github.com/uzivatel/inventory-manager.git ```

2. Přejděte do adresáře projektu:

``` cd inventory-manager ```

3. Vytvořte a aktivujte virtuální prostředí:

``` python -m venv venv ```
``` source venv/bin/activate ``` # na Windows: venv\Scripts\activate 

4. Nainstalujte požadované balíčky:

``` pip install -r requirements.txt ```

5. Proveďte migrace:

``` python manage.py migrate ```

6. Vytvořte superusera pro přístup do administračního rozhraní:

```python manage.py createsuperuser ```

8. Spusťte server:

``` python manage.py runserver ```

## Používání

Otevřete webový prohlížeč a přejděte na http://127.0.0.1:8000/.

Přihlaste se pomocí administrátorského účtu nebo vytvořte nový účet.

Pro správu produktů a lokalit použijte administrační rozhraní nebo zákaznické zóny aplikace.


### Plánované funkce

- Generátor reportů pro export dat o produktech.

- Notifikace pro sledování skladových hladin.

- Integrace s API pro další systémy správy zásob.