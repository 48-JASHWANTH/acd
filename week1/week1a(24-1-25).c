#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void wri(char *fname) {
    FILE *fileptr = fopen(fname, "w");
    char data[100];
    printf("Enter data : ");
    fgets(data, sizeof(data), stdin);
    
    fprintf(fileptr, "%s", data);
    fclose(fileptr);
    printf("Data written successfully.\n");
}

void rea(char *fname) {
    FILE *fileptr = fopen(fname, "r");
    char ch;
    printf("Contents of %s:\n", fname);
    while ((ch = fgetc(fileptr)) != EOF) {
        putchar(ch);
    }
    fclose(fileptr);
}

int main() {
    char *fname = "output.txt"; 

    clock_t start = clock();
    wri(fname);
    clock_t end = clock();
    double writeTime = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken to write: %f seconds\n", writeTime);
    
    start = clock();
    rea(fname);
    end = clock();
    double readTime= ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken to read: %f seconds\n", readTime);
    
    return 0;
}
