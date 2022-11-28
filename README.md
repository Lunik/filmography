# Filmography

Simple Application to search Persons/Movies/TvShows

[Screenshots](./resources/screenshots)

## Demo

https://filmography.tiwabbit.fr

## Usage

### Standalone

```shell
make install

TMDB_API_KEY=<API_KEY> make run-dev
```

### Docker

```shell
make build-docker

docker run -d -e TMDB_API_KEY=<API_KEY> -p 8080:8080 filmography:<COMMIT_HASH>
```

## Resources

- [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction)
- [TMDB stats](https://www.themoviedb.org/settings/api)

## TODO

- Open/Close categories
- TMDB rating

## Other

### Patches

> https://github.com/celiao/tmdbsimple/pull/93

```bash
patch -u venv/lib/python3.10/site-packages/tmdbsimple/tv.py patches/tv_watch_providers.patch
```