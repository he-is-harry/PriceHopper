Apparently according to docker we can start the database server using
`pg_ctl -D /var/lib/postgresql/data -l logfile start`

To run the compose file, we run `docker compose up`

To run the python scripts install the packages as declared in requirements.txt
```
pip install -r requirements.txt
```