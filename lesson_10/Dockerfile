FROM r-base:latest

WORKDIR /home
RUN R -e "if (!require(dplyr)) install.packages('dplyr')"
USER root
CMD ["Rscript", "/home/hw10_Rscript.R"]