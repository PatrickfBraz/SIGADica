FROM ubuntu:18.04

# Prerequisites
RUN apt-get update && \
    apt-get install -y curl git unzip xz-utils zip libglu1-mesa openjdk-8-jdk wget

#COPY ./* ./
#RUN find ./ -type d -exec chmod 755 {} \;

# Set up new user
#RUN useradd -ms /bin/bash developer
#USER developer
WORKDIR /home/developer

RUN mkdir -p Android/sdk
ENV ANDROID_SDK_ROOT /home/developer/Android/sdk
RUN mkdir -p .android && touch .android/repositories.cfg

RUN wget -O sdk-tools.zip https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
RUN unzip sdk-tools.zip && rm sdk-tools.zip
RUN mv tools Android/sdk/tools
RUN cd Android/sdk/tools/bin && yes | ./sdkmanager --licenses
RUN cd Android/sdk/tools/bin && ./sdkmanager "build-tools;29.0.2" "patcher;v4" "platform-tools" "platforms;android-29" "sources;android-29"
ENV PATH "$PATH:/home/developer/Android/sdk/platform-tools"

RUN git clone https://github.com/flutter/flutter.git
ENV PATH "$PATH:/home/developer/flutter/bin"


COPY ./* ./
COPY ./lib/ ./lib/
COPY ./android/ ./android/
COPY ./assets/ ./assets/
COPY ./ios/ ./ios/
COPY ./test/ ./test/
COPY ./web/ ./web/

## change files permission
#RUN find ./ -type d -exec chmod 755 {} \;
#RUN chmod -R 755 pubspec.lock
#RUN chmod -R 755 pubspec.yaml

RUN ls -all

RUN flutter doctor
RUN flutter pub get
RUN flutter build web

CMD ["flutter", "pub", "global", "run", "webdev", "serve", "0.0.0.0:5001"]