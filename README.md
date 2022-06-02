# ZiScrap
Using **BeautifulSoup** and **Selenium** to scrap Address, price and link from Zillow and automatically put in Google Sheets.

**Final result:**
![image](https://user-images.githubusercontent.com/88248157/171577665-ece119b6-bd3d-4609-9ce6-7b7256ffdcae.png)


**Overview**

Zillow has protections against scrapping. If we try to scrap only with BeautifulSoup, Zillow will protect against bots. To bypass this first captcha barrier, we can add headers, but we will only be able to scrap the first nine adverts per page because Zillow uses javascript to load the page as demand. Selenium will be used to force the page to load so we can use BeautifulSoup to scrap all the adverts.

The code only scrap the first four pages of Zillow to avoid the next captcha barrier. Using a **VPN** every four pages will scrap all pages without a problem. Maybe if we add more delay between pages, we can bypass this barrier.

My intention is for research only. The code will remain scrapping four pages only.


**header example:**

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
}

Thank you. Any suggestions is appreciated.
