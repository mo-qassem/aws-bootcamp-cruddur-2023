FROM node:16.18 AS builder
WORKDIR /frontend-react-js
COPY ./frontend-react-js/ /frontend-react-js
RUN npm install

FROM node:alpine
WORKDIR /frontend-app
COPY --from=builder /frontend-react-js /frontend-app
ENV PORT=3000
EXPOSE ${PORT}
CMD ["npm", "start"]