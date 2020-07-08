# Yemeksepeti API
This repository containst the code for Yemeksepeti unofficial API. It has been reverse enginereed from the mobile client. You can search provinces, areas, restaurants and get reviews for restaurants using this code.

 
# Quickstart

```
git clone https://github.com/e4c6/yemeksepeti_api && cd yemeksepeti_api

pip install -r requirements
```
At this point, you're ready to use the script.
```python
import yemeksepeti_api
import random
```
All you need to do is import the api, but we import random for demonstration purposes.
```python
api = YemeksepetiApi()
catalogs = api.get_catalogs()
random_city = random.choice(catalogs)

print(random_city['CatalogName'])
>> TR_VAN
```
Catalogs are provinces, they store various information regarding the province. We need the catalog name to search areas belonging to the province. Their ids correspond to the license plate numbers.

```python
van_areas = api.get_catalog_areas("TR_VAN")
random_area = random.choice(van_areas)

print(random_area['Name'])
>> Edremit (Eminpaşa Mah. - Havalimanı) 
print(random_area['Id'])
>> 717c73d8-5748-4a2b-a467-3af94d9e3ddc
```

Each area has it's unique id and it's city id. We need the unique id to search for restaurants belonging to an area.

```python
edremit_restaurants = api.search_restaurants(catalog="TR_VAN", 
                                            area_id="717c73d8-5748-4a2b-a467-3af94d9e3ddc")

random_restaurant = random.choice(edremit_restaurants)
print(random_restaurant['DisplayName'])
>> Akdeniz Tantuni, Çarşı
print(random_restaurant['MainCuisineName'])
>> Kebap & Türk Mutfağı
print(random_restaurant['CategoryName'])
>> bea5c4cf-d779-48bb-9c12-25ce1da5dc46
```
Restaurants too have their unique ids under the "CategoryName" key. We need this id if we'd like to see their reviews.
```python
akdeniz_tantuni_reviews = api.get_restaurant_reviews(catalog="TR_VAN", 
                                                    area_id="717c73d8-5748-4a2b-a467-3af94d9e3ddc",
                                                    category_name="bea5c4cf-d779-48bb-9c12-25ce1da5dc46")
random_review = random.choice(akdeniz_tantuni_reviews)
print(random_review['Comment'])
>> Abi asiri hizliydi ya vanin en hizli restorani olabilir.
print(random_review['CommentDate'])
>> 2020-03-26 19:05:26.717000
print(random_review['Flavour'], random_review['Serving'], random_review['Speed'])
>> 7 9 10
```
Reviews include their scores, date and comment text and various other information.

# Data Dump

* **3,536,968** records
* Raw **1.6GB**
* New line delimited JSON dump
    * [Link 1](https://mega.nz/file/xiA3FYoR#PPsE10Rkpw5P5CZ6EhxOp1GJStkVgEfTiCvyzPf62uQ): Compressed with zstd (**191.5MB**)


**Parsed Sample**: 

| Comment                                              | CommentDate                 | Flavour | RestaurantDisplayName       | Serving | Speed | Status    | CommentType | AreaName              | AvgRestaurantScore | CatalogName |
|------------------------------------------------------|-----------------------------|---------|-----------------------------|---------|-------|-----------|-------------|-----------------------|--------------------|-------------|
| Gayet güzeldi, memnunuyetle sipariş verebilirsiniz\. | 2020\-03\-15T16:49:07\.570Z | 9       | Değer Kebap, Kurtuluş Mah\. | 9       | 10    | Onaylandı | UserComment | Uşak \(Ünalan Mah\.\) | 9,0                | TR\_USAK    |

**Raw Sample**:

```json
{"Comment":"Gayet güzeldi, memnunuyetle sipariş verebilirsiniz.","CommentDate":"2020-03-15T16:49:07.570Z","Flavour":"9","RestaurantDisplayName":"Değer Kebap, Kurtuluş Mah.","Serving":"9","Speed":"10","Status":"Onaylandı","CommentType":"UserComment","AreaName":"Uşak (Ünalan Mah.)","AvgRestaurantScore":"9,0","CatalogName":"TR_USAK"}
```