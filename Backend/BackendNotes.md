The backend contains a configuration file called `env.properties` that is not included in the git repository. The file contains the database connection strings for the project.

To run the project, set up your own `env.properties` file with the layout as shown below.
```
PRICE_SCRAPING_DATASOURCE_URL=jdbc:postgresql://{WEB HOST}:{PORT}/{DATABASE NAME}
PRICE_SCRAPING_DATABASE_USERNAME={DATABASE USER}
PRICE_SCRAPING_DATABASE_PASSWORD={DATABASE USER PASSWORD}
```