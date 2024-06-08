# Use the official MySQL image from Docker Hub
FROM mysql:8.0

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=URWa0qovwu2hhPdOLKSh
ENV MYSQL_DATABASE=resto-db
ENV MYSQL_USER=betulioo
ENV MYSQL_PASSWORD=client12tri

# Expose the default MySQL port
EXPOSE 3307
