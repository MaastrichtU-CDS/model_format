# Specify the base image for the environment
FROM python:3.11

# Authors of the image
# LABEL authors="lnuernberg@bwh.harvard.edu,dbontempi@bwh.harvard.edu"

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY main.py /usr/src/app/
COPY requirements.txt /usr/src/app/

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# specify the port number (from the flask app - 5000)
EXPOSE 5000


# FIXME: pass it as a command to the container in Slicer
CMD ["python", "./app.py"]
