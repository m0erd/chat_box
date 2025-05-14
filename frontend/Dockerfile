FROM node:16

WORKDIR /app

ARG REACT_APP_BACKEND_URL
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL

COPY package*.json ./

RUN npm install

COPY . .

RUN echo "REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL" > .env

RUN npm run build

EXPOSE $PORT

CMD ["npx", "serve", "-s", "build", "-l", "$PORT"]
