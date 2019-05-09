# vim:set ft=dockerfile:
FROM continuumio/miniconda3
MAINTAINER https://github.com/maartenplieger/climexp_numerical_wps
LABEL Description="Climate Explorer WPS service WPS" Vendor="Birdhouse" Version="0.1.0"

# Update Debian system
RUN apt-get update && apt-get install -y \
 build-essential \
&& rm -rf /var/lib/apt/lists/*

# Update conda
RUN conda update -n base conda

# Copy WPS project
COPY . /opt/wps

WORKDIR /opt/wps

# Create conda environment
RUN conda env create -n wps -f environment.yml
WORKDIR /src
ENV MY_CONDA_ENV /opt/conda/envs/wps
ENV gsl_CFLAGS "-I${MY_CONDA_ENV}/include"
ENV gsl_LIBS   "-L${MY_CONDA_ENV}/lib"

# Climate explorer expects libblas, not libopenblas
RUN ln -s /opt/conda/envs/wps/lib/libopenblas.so /opt/conda/envs/wps/lib/libblas.so

# Compile fortran gsl
WORKDIR /src
RUN curl -L "https://doku.lrz.de/download/attachments/28051060/fgsl-1.2.0.tar.gz" > fgsl.tar.gz && tar -xzvf fgsl.tar.gz 
RUN ["/bin/bash", "-c", "source activate wps && cd /src/fgsl-1.2.0 && ./configure --prefix ${MY_CONDA_ENV}/ && make && make install" ]

# Compile fortran lapack, ensures that same fortran compiler is used as used to compile climate explorer
WORKDIR /src
RUN curl -L "http://www.netlib.org/lapack/lapack-3.8.0.tar.gz" > lapack-3.8.0.tar.gz && tar -xzvf lapack-3.8.0.tar.gz 
RUN ["/bin/bash", "-c", "source activate wps && cd /src/lapack-3.8.0 && cp make.inc.example make.inc && make lapacklib && cp liblapack.a ${MY_CONDA_ENV}/lib " ]

# Install climate explorer from source, no conda package available
WORKDIR /src
RUN git clone https://github.com/c3s-magic/climexp_numerical
ENV CPPFLAGS      "-I${MY_CONDA_ENV}/include -I${MY_CONDA_ENV}/include/fgsl ${CPPFLAGS}"
ENV LDFLAGS       "-L${MY_CONDA_ENV}/lib ${LDFLAGS}"
ENV FORTRAN_FLAGS ${CPPFLAGS} ${LDFLAGS}
ENV PVM_ARCH build
ENV LD_LIBRARY_PATH ${MY_CONDA_ENV}:${LD_LIBRARY_PATH}
WORKDIR /src/climexp_numerical/${PVM_ARCH}
RUN cp /src/climexp_numerical/Docker/Makefile.docker /src/climexp_numerical/${PVM_ARCH}/Makefile
RUN ["/bin/bash", "-c", "source activate wps && make" ]
ENV CLIMATE_EXPLORER_BUILD /src/climexp_numerical/build/

# Install python wrapper
WORKDIR /src/climexp_numerical/python
RUN ["/bin/bash", "-c", "source activate wps && python setup.py install"]

# Install WPS
WORKDIR /opt/wps
RUN ["/bin/bash", "-c", "source activate wps && python setup.py develop"]

COPY . /opt/wps

# Start WPS service on port 5000 on 0.0.0.0
EXPOSE 5000
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["source activate wps && exec climexp_numerical_wps start --hostname ${HOSTNAME} -b 0.0.0.0 -c /opt/wps/etc/demo.cfg"]

# docker build -t climexp_numerical_wps .
# docker run -p 5000:5000 climexp_numerical_wps
