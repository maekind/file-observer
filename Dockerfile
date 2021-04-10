# File-observer program
FROM python:slim
LABEL maekind.webplayer.name="file-observer" \
      maekind.webplayer.maintainer="Marco Espinosa" \
      maekind.webplayer.version="1.0" \
      maekind.webplayer.description="Monitoring music folder changes" \
      maekind.webplayer.email="hi@marcoespinosa.es"

# Change working dir to app and copy requirements
WORKDIR /app
COPY requirements.txt requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt

# Copy application into app dir
COPY ./src/*.* .

# Set working dir to path
ENV PATH="/app:${PATH}"

# Entry command for docker image
ENTRYPOINT [ "file-observer.py" ]







      

