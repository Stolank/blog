FROM ruby:3.2
RUN apt-get update -y && \
    apt-get install -y build-essential libpq-dev nodejs

WORKDIR /app


COPY Gemfile Gemfile.lock ./
RUN bundle install

COPY . .

EXPOSE 3000

CMD ["rails", "s", "-b", "0.0.0.0"]
