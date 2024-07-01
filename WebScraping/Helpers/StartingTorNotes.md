First, download Tor onto your computer through https://www.torproject.org/download/

Start Tor by running the Tor Browser or by running the `tor` executable file

For example, Harry's tor executable is found at `/Applications/Tor Browser.app/Contents/MacOS/Tor/tor`


If you choose to automatically start the tor server, you may need to kill the tor service through
the command line.

On MacOS, the following command can be used to kill the service using the port 9050
```
kill -15 $(lsof -ti:9050)
```


