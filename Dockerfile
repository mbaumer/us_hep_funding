FROM python:3.10
RUN pip install --upgrade pip

## Cartopy dependencies
# Install GEOS + PROJ
RUN apt-get update && apt-get install -y \
    libgeos++-dev \
    libgeos-3.9.0 \
    libgeos-c1v5 \
    libgeos-dev \
    libgeos-doc \
    proj-bin \
    libproj-dev \
 && rm -rf /var/lib/apt/lists/*
RUN pip install pyshp==2.2.0 pyproj==3.3.0 scipy==1.8.0
# From https://scitools.org.uk/cartopy/docs/latest/installing.html
# shapely needs to be built from source to link to geos. If it is already
# installed, uninstall it by: pip3 uninstall shapely
RUN pip install --no-cache-dir shapely --no-binary shapely
RUN pip install --no-cache-dir Cartopy==0.19.0.post1

# Install remaining requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Included in lieu of better packaging
ENV PYTHONPATH /workspaces/us_hep_funding