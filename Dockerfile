FROM rasa/rasa:2.8.23-full
WORKDIR /app
COPY . /app
USER root
RUN useradd -m myuser
USER myuser
ENTRYPOINT ["/bin/bash","-l","-c"]
CMD ["/opt/venv/bin/rasa run -p $PORT"]