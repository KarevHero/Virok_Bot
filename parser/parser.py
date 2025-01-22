import aiohttp
import asyncio
from bs4 import BeautifulSoup
from sale_and_new import sale
from http import cookies
from keyboard import cell_promotion
# async def get_cookies():
#     async with aiohttp.ClientSession().post("https://partners.virok.com.ua/login", data=json.dumps(data), headers=headers) as res:
#         print(res.cookies)
#         print(type(res.cookies))
#         return res.cookies
#
# cookie = asyncio.run(get_cookies())


headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/108.0.0.0 Safari/537.36"}
data = {"email": "aleksandr.shinkarev.1001drib@gmail.com", "password": "Virok1234"}
cookie = cookies.SimpleCookie()
cookie['_identity-site'] = 'aa1a0a62691fd124f575d01d803df8f138ce63bb54628b55caf9097426acbc52a%3A2%3A%7Bi%3A0%3Bs%3A14' \
                           '%3A%22_identity-site%22%3Bi%3A1%3Bs%3A48%3A%22%5B288%2C' \
                           '%22975mkg3UKMt2bWkRpUI5MQ3TDnrIgkAp%22%2C2592000%5D%22%3B%7D'


async def get_info(message):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for art in message.text.split():
            tasks.append(asyncio.create_task(get_data_key(art, session)))
        result = await asyncio.gather(*tasks)

        tasks = []
        for data_key, art in result:
            tasks.append(asyncio.create_task(page(data_key, art, message, session)))

        await asyncio.gather(*tasks)


async def page(data_key, art, message, session):

    if data_key == 'Артикул не найден':
        await message.answer(text=f'Артикул {art} не найден')
    else:
        page_art = await session.get(f"https://partners.virok.com.ua/catalog/{data_key}?name={art}&view=list",
                                     headers=headers, cookies=cookie)
        soup_art = BeautifulSoup(await page_art.text(), 'lxml')
        art_price = soup_art.find('dl', class_='dl-horizontal dl-good-details').find_all('dd')
        product = art_price[0].text
        price = ''.join(art_price[1].text.split())
        leftovers = soup_art.find('table', class_="table manage-u-table table-mini").find_all('tr')
        #leftovers = soup_art.find('table', class_="table table-hover manage-u-table table-mini").find_all('tr')
        #leftovers = [' '.join(i.text.split()) for i in leftovers][1:]
        one = ['🚚Склад', 'Наявність', 'В резерве', 'Доступно']
        lef = []
        for i in leftovers:
            x=0
            for j in i.find_all('td'):
                content = one[x] + j.text
                x+=1
                lef.append(content)
        lef = [' '.join(i.split()) for i in lef]
        lef = '\n'.join(lef)
        # picture = 'https://partners.virok.com.ua' + soup_art.find('img', class_='img-responsive')['ng-init'].split(';')[0][12:-1]
        await message.answer(text=f'Артикул : {product}\nРоздрібна ціна: {price}\n{lef}', reply_markup=cell_promotion.main_keyboard)


async def get_data_key(art, session):
    page = await session.get(f"https://partners.virok.com.ua/catalog?name={art}&view=list", headers=headers,
                             cookies=cookie)
    soup = BeautifulSoup(await page.text(), 'lxml')
    data_base = soup.find('tbody').find_all('tr')
    for d in data_base:
        if len(d.find_all('td')) != 1 and d.find_all('td')[1].text.lower() == art.lower() and d['data-key']:
            return d['data-key'], art

    return 'Артикул не найден', art

# async def sell_part_parser(message):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         star_point = int(message.text.split()[1])
#         for art in sale.sale_list[star_point-1:star_point+9]:
#             tasks.append(asyncio.create_task(get_data_key(art[0], session)))
#         result = await asyncio.gather(*tasks)
#
#         tasks = []
#         for data_key, art in result:
#             tasks.append(asyncio.create_task(page_for_sale(data_key, art, message, session)))
#
#         await asyncio.gather(*tasks)
#
# async def page_for_sale(data_key, art, message, session):
#
#     if data_key == 'Артикул не найден':
#         await message.answer(text=f'Артикул {art} распродан')
#     else:
#         page_art = await session.get(f"https://partners.virok.com.ua/catalog/{data_key}?name={art}&view=list",
#                                      headers=headers, cookies=cookie)
#         soup_art = BeautifulSoup(await page_art.text(), 'lxml')
#         art_price = soup_art.find('dl', class_='dl-horizontal dl-good-details').find_all('dd')
#         product = art_price[0].text
#         price = ''.join(art_price[1].text.split())
#         leftovers = soup_art.find('table', class_='table table-hover manage-u-table table-mini').find_all('tr')
#         leftovers = [' '.join(i.text.split()) for i in leftovers][1:]
#         leftovers = '\n'.join(leftovers)
#         picture = 'https://partners.virok.com.ua' + soup_art.find('img', class_='img-responsive')['ng-init'].split(';')[0][12:-1]
#         await message.answer_photo(photo=picture, caption=f'Артикул : {product}\n{sale.sale[art][0]}\nРоздрібна ціна: {price}\nСкидка{sale.sale[art][1]}\n{leftovers}', reply_markup=cell_promotion.main_keyboard)

async def new_part_parser(message):
    async with aiohttp.ClientSession() as session:
        tasks = []
        star_point = int(message.text.split()[1])
        for art in sale.new_art_list[star_point-1:star_point+9]:
            tasks.append(asyncio.create_task(get_data_key(art[0], session)))
        result = await asyncio.gather(*tasks)
        tasks = []
        for data_key, art in result:
            tasks.append(asyncio.create_task(page_for_new(data_key, art, message, session)))

        await asyncio.gather(*tasks)

async def page_for_new(data_key, art, message, session):
    if data_key == 'Артикул не найден':
        await message.answer(text=f'Артикул {art} не найден')
    else:
        page_art = await session.get(f"https://partners.virok.com.ua/catalog/{data_key}?name={art}&view=list",
                                     headers=headers, cookies=cookie)
        soup_art = BeautifulSoup(await page_art.text(), 'lxml')
        art_price = soup_art.find('dl', class_='dl-horizontal dl-good-details').find_all('dd')
        product = art_price[0].text
        price = ''.join(art_price[1].text.split())
        leftovers = soup_art.find('table', class_="table manage-u-table table-mini").find_all('tr')
        # leftovers = soup_art.find('table', class_="table table-hover manage-u-table table-mini").find_all('tr')
        # leftovers = [' '.join(i.text.split()) for i in leftovers][1:]
        one = ['🚚Склад', 'Наявність', 'В резерве', 'Доступно']
        lef = []
        for i in leftovers:
            x = 0
            for j in i.find_all('td'):
                content = one[x] + j.text
                x += 1
                lef.append(content)
        lef = [' '.join(i.split()) for i in lef]
        lef = '\n'.join(lef)
        picture = 'https://partners.virok.com.ua' + soup_art.find('img', class_='img-responsive')['ng-init'].split(';')[0][12:-1]
        try:
            await message.answer_photo(photo=picture, caption=f'Артикул : {product}\n{sale.new_art[art][0]}\nРоздрібна ціна: {price}\nДата поступления {sale.new_art[art][-1]}\n{lef}', reply_markup=cell_promotion.main_keyboard)
        except:
            await message.answer(text=f'Артикул : {product}\n{sale.new_art[art][0]}\nРоздрібна ціна: {price}\n{lef}, \nДата поступления {sale.new_art[art][-1]}',
                                 reply_markup=cell_promotion.main_keyboard)
