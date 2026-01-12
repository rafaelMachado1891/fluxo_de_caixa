FROM astrocrpublic.azurecr.io/runtime:3.1-9


USER root
RUN mkdir -p /home/astro/.dbt

COPY .dbt/profiles.yml /home/astro/.dbt/profiles.yml

USER astro