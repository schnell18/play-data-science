# R development enviroment setup

## install
Overall install instructions is [described here][1].

The ubuntu specific instructions:

- Add CRAN repository:
```bash
# update indices
sudo apt update -qq
# install two helper packages we need
sudo apt install --no-install-recommends software-properties-common dirmngr
# add the signing key (by Michael Rutter) for these repos
# To verify key, run gpg --show-keys /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
# Fingerprint: E298A3A825C0D65DFD57CBB651716619E084DAB9
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
# add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
```

- Install r-base package:
```bash
sudo apt install --no-install-recommends r-base
```

## start rstudio on Ubuntu 24.04
Due to [#14336][2], the rstudio 2024.04.2 Build 764 doesn't launch properly.
We need start it in a non-sandbox mode like:

```bash
rstudio --no-sandbox
```

## install development dependencies

We need tidyverse, ggplot2 etc to transform and visualize data.
There are some native packages to be installed on Ubuntu 24.04:

```bash
sudo apt-get install -y \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libharfbuzz-dev \
    libfribidi-dev
```

```r
install.packages(
  c(
    "tidyverse", "ggplot2", "arrow", "babynames", "curl", "duckdb",
    "gapminder", "ggrepel", "ggridges", "ggthemes", "hexbin", "janitor",
    "Lahman", "leaflet", "maps", "nycflights13", "openxlsx",
    "palmerpenguins", "repurrrsive", "tidymodels", "writexl"
  )
)
```

## rayrender

```bash
sudo apt-get install -y \
    liblapack-dev \
    libblas-dev \
    libgdal-dev \
    libgfortran-13-dev
```


[1]: https://cran.rstudio.com/
[2]: https://github.com/rstudio/rstudio/issues/14336
