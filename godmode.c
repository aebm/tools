#include <stdio.h>
#include <signal.h>
#include <unistd.h>

void handler(int sig)
{
    printf("U can't touch this. Break it down. Stop Hammer time!\n");
    if (fflush(NULL) != 0) {
        perror("Ouch! (^_^')");
    }
}

int main(void)
{
    unsigned int t = 999999999;
    struct sigaction new;
    struct sigaction old;
    new.sa_handler = &handler;
    int i;
    printf("Become a politician!\n");
    for (i = 1; i < 50; i++) {
        if (sigaction(i, &new, &old) != 0) {
            perror("Cannot ignore signal T_T!");
            fprintf(stderr, "Signal %d\n", i);
        }
    }
    while (t > 0) {
        t = sleep(t);
    }
    printf("This should never runs\n");
    return 0;
}
