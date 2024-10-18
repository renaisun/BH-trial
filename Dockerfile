FROM continuumio/miniconda3

WORKDIR /app

# copy environment.yml for caching
COPY environment.yml /app/environment.yml

RUN conda env create -f environment.yml
# activate deisred environment when shell starts
RUN echo "source activate blockhouse" > ~/.bashrc
ENV PATH /opt/conda/envs/blockhouse/bin:$PATH
# activate shell
SHELL ["conda", "run", "-n", "blockhouse", "/bin/bash", "-c"]
# copy source code
COPY . /app

EXPOSE 8123

CMD ["bash", "./entrypoint.sh"]