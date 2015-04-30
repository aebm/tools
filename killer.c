#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>


void kill_it(void) {
    char *command = "hdparm --direct -t /dev/sda";
    fclose(stdout);
    while (1) {
      system(command);
    }
}

int main(int argc, char *argv[]) {
    int i;
    int num_procs = atoi(argv[1]);
    if (num_procs < 1) {
        fprintf(stderr, "Give me a number from 1 to max int\n");
        exit(1);
    }
    for (i = 0; i < num_procs; i++) {
        pid_t pid;
        pid = fork();
        if (pid < 0) {
            fprintf(stderr, "Could not create process %d\n", i + 1);
        }
        if (pid == 0) {
           kill_it();
        }
    }
    for (i = 0; i < num_procs; i++) {
        wait(NULL);
    }
    return 0;
}
