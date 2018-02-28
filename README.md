# lightning-rest

Rest server for the `lightningd` daemon.

![screenshot](resources/snapshot_2018-02-28_093049.png)

## Setup

Installing lightning-rest is easy, just execute the following in a terminal:


```shell
pip install lightning-rest
```

Run your local app!
```shell
python -m lightning_rest.server 8000 ~/.lightning/lightning-rpc
```

Run as docker container
```shell
docker run -it --rm -p 8000:8000 -v /path/to/lightning-rpc:/tmp/lightning-rpc siriuslabs/lightning-rest 8000 /tmp/lightning-rpc
```

View the lightning-rest app at `localhost:8000`


## License: MIT