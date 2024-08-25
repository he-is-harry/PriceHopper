# PriceHopper

Author: Harry He

## Project Description

The PriceHopper app allows users to compare grocery store prices and shopping carts between different companies. The backend scrapes grocery prices off the internet into the database, allowing users to use to app to run queries on the best prices and value.

### Development Tools Used
- **React Native**: Mobile / web framework used to develop the frontend app
- **Spring Boot**: Backend Java framework used to create the REST API backend
- **Python Web Scraping Libraries** (*requests*, *BeautifulSoup*, *Selenium*, ...): Python libraries used to scrape grocery prices off the web
- **PostgreSQL**: Database used to store prices for queries
- **Docker**: Development tool to package and build parts of the project

### Challenges Faced
#### Problem
The major challenge when creating this project was figuring out the scraping of prices. The issue is that basically all major companies who have a website will use some DDOS protection and captcha service like Cloudflare.

To bypass this issue, an initial approach was to use public proxies and / or Tor network routing to simulate many IP's loading the site for only a few times (maybe like once every 5ish seconds). In this scenario, it would seem that there was just a bunch of regular computers connecting at once. However, there was some issues with using both of these methods.
1. **Public proxies are unreliable**\
Most public proxies listed on sites such as [ProxyScrape](https://proxyscrape.com/free-proxy-list) do not work, you cannot establish a network connection. Even when they do connect, most do not run JavaScript which is predominantly used in web development, basically preventing you from loading a site without it. To avoid this issue, you can filter only *good* public proxies, which is done in the `WebScraping/Source/PublicProxies` folder. However, these proxies endpoints will eventually stop being hosted after a few minutes as there is essentially zero benefit of running a public proxy (since you attract cyber crime).
2. **Tor exit nodes are sketchy**\
Tor exit nodes are all publically released and with Tor being known for its anonymity, I have found that some sites seem to put captchas when they recieve a request from those IPs, at least more than usual. As a result, it makes it difficult to scrape anything because you essentially have to figure out a way to solve captchas.
3. **Grocery prices are localized**\
The most important consideration that stopped me from using this initial approach was that most of the prices I would get would be very inconsistent. It is impossible to set cookies on every public proxy to set store locations, so websites will default to the IP address to get the closest store and their prices. As a result, these prices are from vastly different locations and are inaccurate for any user region's use.

#### Solution
To solve this issue, it was necessary that I use my own IP address. However, it is inevitable that after sending too many requests that look like robots, a company will ban your IP from their site. (In fact, I got banned from TNT Supermarket's website for a few days!) To make all your requests legit, one of the best ways is to actually make them legit, so I settled on a solution that simulated real human actions using keyboard macros. Using a regular web browser, I simulated keyboard strokes to visit websites and this worked! I could parse many pages without captchas and allow me to run the scraper for long periods of time to get all the products I needed. The keyboard macro scrapers are contained in `WebScraping/ManualParseAutomater.py` and `WebScraping/ManualParallelParseAutomater.py`

> **Note**: Many sites that are potentials for scraping only need to be visited once, so these workarounds aren't normally necessary. Futhermore, this solution is really only necessary for sites strongly protected from DDOS attacks. Some sites like [Wikipedia](https://en.wikipedia.org/wiki/Main_Page) where you may also want to retrieve data might not be so defensive.


## Installation and Running
1. Clone this repository and enter the folder
    ```
    git clone https://github.com/he-is-harry/PriceHopper.git
    cd PriceHopper
    ```

2. Ensure that you have Docker installed on your computer. If not, you can install it [here](https://www.docker.com/).
We will need the official Postgres Docker image, which is the Postgres database where all the products are stored.
However, your database will be empty, so refer to the `WebScraping/ScriptingNotes.md` file for more information on retrieving
the data yourself (or you can ask me for the data).
    ```
    docker pull postgres
    ```

3. Start the database
    ```
    cd Database
    docker compose up
    ```

4. To start the backend for development, there are a few more prerequisites. You will need Java 17+ and Maven. For MacOS users, these can be installed using Homebrew using `brew install openjdk` and `brew install maven`. From there, you can start the backend using the following command.
    ```
    cd ../Backend
    mvn spring-boot:run
    ```

5. To start the frontend, first install the necessary packages. Then we run the app using Expo, the framework used to develop the app.
    ```
    cd ../Frontend
    npm install
    npx expo start
    ```

6. If you have an iOS simulator, you can press `i` to open the app there. Alternatively, you can open it in your web browser by pressing `w`. In addition, you can also use your phone by scanning the QR code that should be displayed in the terminal (you may need to install the Expo Go app).

From there you should be finished! However, if you don't have any data, you can access `WebScraping/ScriptingNotes.md` file for more information on how to get the data.

