Consistent Environments Across the Universe
====

This directory contains a `patat` presentation on `nix` for consistent environments everywhere.

It also includes a small demo. To run the demo, you'll need:

* to [install `nix`](https://zero-to-nix.com/start/install)
* to [install `direnv`](https://direnv.net/docs/installation.html) (or `nix-env -i direnv` if you have nix already!)

Then you can _do some magic_, like:

```bash
❯ direnv allow .  # 1.
❯ cd postgresql13/  # 2.
direnv: loading ~/gitdirs/patats/2023-07-20-Consistent-Environments-Across-the-Universe/postgresql13/.envrc
direnv: using flake  # 3.
[...]
❯ psql --version  # 4.
psql (PostgreSQL) 13.11
~/g/p/2023-07-20-Consistent-Environments-Across-the-Universe/postgresql13 ❯ cd ../postgresql14/  # 5.
direnv: loading ~/gitdirs/patats/2023-07-20-Consistent-Environments-Across-the-Universe/postgresql14/.envrc
direnv: using flake
[...]
❯ psql --version  # 6.
psql (PostgreSQL) 14.8
```

Those commands, in order:

1. allow `direnv` to load `.envrc` files in this directory. That's important, because if `direnv` can't load the `.envrc` files, nothing will tell your system to use the `flake.nix` file.
2. change to the `postgresql13` repo, where there's a [`flake.nix`](./postgresql13/flake.nix) file defining an environment with `psql` from PostgreSQL 13
3. you'll see a bunch of output about using the flake, and fetching things from the internet
4. check the `psql` version
5. change to the `postgresql14` repo, where there's a `flake.nix` defininng an environment with `psql` from PostgreSQL 14
6. check the `psql` version again -- it's like virtualenv for system dependencies

There are also python directories in `python310a` and `python310b` that show finer-grained environment control than changing `psql` versions. You can inspect those flakes to see
what you can expect of the `python` environments available in each of those directories.
