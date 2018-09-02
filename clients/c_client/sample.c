#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

enum {
      LEFT,
      RIGHT,
      UP,
      DOWN
};

// TODO: Pass in a nice structured map representation!
int get_move() {
    return DOWN;
}

int main(int argc, char *argv[]) {
    int sock;
    struct sockaddr_in server;
    char *message, server_reply[1024];

    uint16_t port;
    char *host;

    if (argc != 3) {
        printf("Usage: ./sample host port\n");
        return 1;
    }

    host = argv[1];
    port = atoi(argv[2]);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("socket");
        return 1;
    }

    server.sin_addr.s_addr = inet_addr(host);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
 
    // Connect to snake server
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        perror("connect");
        return 1;
    }

    puts("Connected\n");

    while (1) {
        if (recv(sock, server_reply, sizeof(server_reply) , 0) < 0) {
            perror("recv");
            break;
        }

        // TODO: Parse JSON!
        puts(server_reply);

        switch (get_move()) {
        case LEFT:
            message = "left";
        case RIGHT:
            message = "right";
        case UP:
            message = "up";
        case DOWN:
            message = "down";
        }

        if (send(sock, message, strlen(message), 0) < 0) {
            perror("send");
            break;
        }
    }

    close(sock);
    return 0;
}
