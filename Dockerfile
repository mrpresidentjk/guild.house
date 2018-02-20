# Build / run:
# docker build --tag="${PWD##*/}" .
# docker run --tty --interactive --volume "${PWD}":/opt/project --publish=8000:8000 "${PWD##*/}"
# Cleanup:
# docker rm $(docker ps --all --quiet)
# docker rmi $(docker images --quiet --filter "dangling=true")


FROM ubuntu:14.04


MAINTAINER Matt Austin


# Install required packages
RUN apt-get update --quiet --yes  # 2016-01-14
RUN apt-get install --quiet --yes --force-yes dictionaries-common language-pack-en
RUN apt-get install --quiet --yes --force-yes build-essential fabric gettext git graphicsmagick imagemagick libffi-dev libgdal1-dev libgeos-dev libgraphicsmagick++-dev libjpeg-dev libmagickwand-dev libssl-dev libpng-dev libpq-dev libproj-dev libspatialite-dev libsqlite3-dev libxslt1-dev libyaml-dev python3-dev python3-pip python3-setuptools wbritish zlib1g-dev
RUN apt-get install --quiet --yes --force-yes ipython3


# Install required packages
ADD requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt


# Configure environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONWARNINGS d


# Entrypoint
EXPOSE 8000
ENTRYPOINT ["python3", "/opt/project/manage.py"]
CMD ["check"]
