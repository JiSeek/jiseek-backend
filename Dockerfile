# base image  
FROM python:3.9
# set environment variables  
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# install dependencies  
RUN pip install --no-cache-dir --upgrade pip  
# copy whole project to your docker home directory. COPY . $DockerHOME  
COPY requirements.txt .

ADD . /home
ADD requirements.txt /home

WORKDIR /home

# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 8000  
# start server  
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]