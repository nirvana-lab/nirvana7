FROM bxwill/nirvana-base-img:svc
MAINTAINER min.xu@daocloud.io
WORKDIR /workspace

COPY . .
RUN pip install -r requirements.txt
CMD ./launch.sh
EXPOSE 9090
