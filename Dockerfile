FROM bxwill/nirvana-base-img:svc
MAINTAINER min.xu@daocloud.io
WORKDIR /workspace

COPY . .
RUN pip install -r requirements.txt && /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

CMD ./launch.sh
EXPOSE 9090
