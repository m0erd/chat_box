FROM node:16

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ARG REACT_APP_BACKEND_URL
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL

RUN echo "REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL" > .env

RUN npm run build

EXPOSE 3000

CMD sh -c "npx serve -s build -l $PORT"
