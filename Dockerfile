FROM python:3.7-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends \
    wget cpio sudo git zip unzip curl xterm vim bzip2 ca-certificates lsb-release && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN useradd -m -s /bin/bash ubuntu
RUN gpasswd -a ubuntu sudo


ENV USER_NAME ubuntu
RUN chown ${USER_NAME} -R /usr/local/

USER ${USER_NAME}
RUN export PATH="${HOME}/.local/bin:$PATH"

WORKDIR /project/
COPY . .
RUN python -m pip install --upgrade pip==22.0.3
RUN pip install .[dev]
