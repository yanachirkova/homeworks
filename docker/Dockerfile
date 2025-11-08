FROM r-base:latest

WORKDIR /home
RUN mkdir -p /home/resources /home/results /home/scripts
COPY script.R /home/scripts
COPY Пациенты.xlsx /home/resources
RUN R -e "install.packages('readxl')"
USER root
CMD ["Rscript", "/home/scripts/script.R"]