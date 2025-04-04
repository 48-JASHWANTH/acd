#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_KEYWORDS 50
#define MAX_OPERATORS 50
#define MAX_LENGTH 100

int main() {
    char keywords[MAX_KEYWORDS][MAX_LENGTH];
    char operators[MAX_OPERATORS][MAX_LENGTH];
    int keyword_count = 0, operator_count = 0;
    FILE *file = fopen("keywords.txt", "r");
    if (file == NULL) {
        printf("Error: Unable to open keywords.txt\n");
        return 1;
    }

    while (fgets(keywords[keyword_count], MAX_LENGTH, file)) {
        keywords[keyword_count][strlen(keywords[keyword_count]) - 1] = '\0';
        keyword_count++;
    }
    fclose(file);
    file = fopen("operators.txt", "r");
    if (file == NULL) {
        printf("Error: Unable to open operators.txt\n");
        return 1;
    }

    while (fgets(operators[operator_count], MAX_LENGTH, file)) {
        operators[operator_count][strlen(operators[operator_count]) - 1] = '\0'; 
        operator_count++;
    }
    fclose(file);
    file = fopen("example.txt", "r");
    if (file == NULL) {
        printf("Error: Unable to open example.txt\n");
        return 1;
    }

    char line[MAX_LENGTH];
    printf("Keywords and operators found in example.txt:\n");

    while (fgets(line, MAX_LENGTH, file)) {
        int i;
        for (i = 0; i < keyword_count; i++) {
            if (strstr(line, keywords[i])) {
                printf("Keyword: %s\n", keywords[i]);
            }
        }
        for (i = 0; i < operator_count; i++) {
            if (strstr(line, operators[i])) {
                printf("Operator: %s\n", operators[i]);
            }
        }
    }
    fclose(file);
    return 0;
}