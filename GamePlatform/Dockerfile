
FROM python:3.10

RUN apt-get update && apt install -y netcat-traditional

 
MAINTAINER HOWARD 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



ENV APP_HOME=/www/html/GamePlatform
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY . $APP_HOME

RUN chown -R www-data:www-data $APP_HOME/media \
&& chmod -R 775 $APP_HOME/media \
&& chown -R www-data:www-data $APP_HOME/staticfiles \
&& chmod -R 775 $APP_HOME/staticfiles 

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN sed -i 's/\r//' ./init.sh

RUN chmod +x ./init.sh

ENTRYPOINT /bin/bash ./init.sh 
