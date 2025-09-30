# FROM node:20-alpine

# WORKDIR /app
# COPY package*.json ./
# RUN npm install

# COPY . .
# RUN npm run build

# EXPOSE 80
# CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "80"] 
# CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"] # toto pre local, hore pre docker

# Use the official Node.js 20-alpine image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

# Build the frontend application
RUN npm run build

# Expose the port the frontend will run on
EXPOSE 80

# Command to run the app
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "80"]
