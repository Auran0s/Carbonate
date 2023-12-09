FROM python:alpine3.16

ENV DATABASE_URL=postgresql://clkpatiys000y9ypdei4v6ip6:5jhSgd6ReMmCwv5PVn9BMy87@49.12.226.12:9000/clkpatiyu00109ypdfa9wfi03

RUN apk update && apk add nodejs npm

WORKDIR /Carbonate

COPY package*.json ./
RUN npm install

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./
RUN npx tailwindcss -i ./static/src/main.css -o ./static/dist/main.css

RUN prisma db push

CMD ["waitress-serve", "--port=5067", "app:app"]