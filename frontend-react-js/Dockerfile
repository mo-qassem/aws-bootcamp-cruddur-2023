
FROM node:16.18

WORKDIR /frontend-react-js

COPY . /frontend-react-js

RUN npm install

RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache

ENV PORT=3000

EXPOSE ${PORT}

CMD ["npm", "start"]