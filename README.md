# TransIP updater
This container will check and compare your external IP with all A-records on the specified domain. If they're different, it will automatically update the A-records with the correct external IP.  This way you don't have to deal with a dynamic dns solution if you don't have a static IP.  

Make sure to enable the API, create a keyfile and put that in the container under /keyfile/key. See [this](https://www.transip.nl/knowledgebase/artikel/77-de-transip-rest-api-gebruiken/) page for more info on how to do so. Also add 0.0.0.0/0 to your IP whitelist, else the script won't be able to update once the IP has changed.

## Usage
```shell
docker run larsstoker/transip-updater:latest
```

#### Environment Variables

* `username` - Your TransIP username
* `domain` - The domain you wish to monitor
