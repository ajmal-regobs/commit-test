FROM eclipse-temurin:11-jdk

ARG JAR_FILE
ARG PROFILE

ENV profile=$PROFILE
ENV APP_HOME=/usr/app/

WORKDIR $APP_HOME

COPY ${JAR_FILE} /app.jar
RUN chmod 755 /app.jar

ENV JAVA_TOOL_OPTIONS="-Xms5m -Xmx5m -Dlogging.level.root=info"

ENTRYPOINT ["sh", "-c", "java -jar /app.jar --spring.profiles.active=${profile}"]
