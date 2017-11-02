FROM alpine

# Setup demo environment variables
ENV HOME=/root \
        DEBIAN_FRONTEND=noninteractive \
        LANG=en_US.UTF-8 \
        LANGUAGE=en_US.UTF-8 \
        LC_ALL=C.UTF-8 \
        DISPLAY=:0.0 \
        DISPLAY_WIDTH=1024 \
        DISPLAY_HEIGHT=768

# x11vnc is in testing repo
RUN echo "http://dl-3.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

# Install git, supervisor, VNC, & X11 packages
RUN apk --update --upgrade add --no-cache firefox-esr \
        openrc \
        dbus \
        bash \
        openssh \
        fluxbox \
        git \
        socat \
        supervisor \
        x11vnc \
        xterm \
        xvfb \
        python \
        py-pip \
        py-setuptools \
        libx11 \
        python2-dev \
        mysql-client \
        py-mysqldb \
        py-lxml \
        py-dateutil \
        python py-pip curl unzip libexif udev chromium chromium-chromedriver xvfb && \
        pip install selenium && \
        pip install pyvirtualdisplay \
        requests \
        boto3 \
        awscli \
        tendo \
        bottlenose \
 && sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
  && echo "root:root" | chpasswd \
  && rm -rf /var/cache/apk/*
RUN sed -ie 's/#Port 22/Port 22/g' /etc/ssh/sshd_config
RUN sed -ri 's/#HostKey \/etc\/ssh\/ssh_host_key/HostKey \/etc\/ssh\/ssh_host_key/g' /etc/ssh/sshd_config
RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_rsa_key/HostKey \/etc\/ssh\/ssh_host_rsa_key/g' /etc/ssh/sshd_config
RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_dsa_key/HostKey \/etc\/ssh\/ssh_host_dsa_key/g' /etc/ssh/sshd_config
RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ecdsa_key/HostKey \/etc\/ssh\/ssh_host_ecdsa_key/g' /etc/ssh/sshd_config
RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ed25519_key/HostKey \/etc\/ssh\/ssh_host_ed25519_key/g' /etc/ssh/sshd_config
RUN /usr/bin/ssh-keygen -A
RUN ssh-keygen -t rsa -b 4096 -f  /etc/ssh/ssh_host_key
RUN rc-update add sshd && \
    rc-status          && \
    touch /run/openrc/softlevel  && \
    rc-service sshd start
# Clone noVNC from github
RUN git clone https://github.com/kanaka/noVNC.git /root/noVNC \
        && git clone https://github.com/kanaka/websockify /root/noVNC/utils/websockify \
        && rm -rf /root/noVNC/.git \
        && rm -rf /root/noVNC/utils/websockify/.git \
        && apk del git

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ebay /
COPY geckodriver /
COPY password /
# Modify the launch script 'ps -p'
RUN sed -i -- "s/ps -p/ps -o pid | grep/g" /root/noVNC/utils/launch.sh
RUN chmod +x geckodriver

EXPOSE 8080

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


