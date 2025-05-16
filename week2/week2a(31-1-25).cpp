#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


char keywords[100][100];
char operators[100][100];
char specialChars[100][100];
int keyword_count = 0, operator_count = 0, special_count = 0;

// Function to load tokens from a file
void loadTokens(char *filename, char tokens[][100], int *count) {
    FILE *file = fopen(filename, "r");

    while (fgets(tokens[*count], 100, file)) {
        tokens[*count][strlen(tokens[*count]) - 1] = '\0'; // Remove newline
        (*count)++;
    }
    fclose(file);
}

// Function to check if a word is a keyword
int isKeyword(char *word) {
    for (int i = 0; i < keyword_count; i++) {
        if (strcmp(word, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

// Function to check if a word is an operator
int isOperator(char *word) {
    for (int i = 0; i < operator_count; i++) {
        if (strcmp(word, operators[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

// Function to check if a word is a special character
int isSpecialCharacter(char ch) {
    for (int i = 0; i < special_count; i++) {
        if (ch == specialChars[i][0]) {
            return 1;
        }
    }
    return 0;
}

// Function to check if a string is an identifier
int isIdentifier(char *word) {
    if (!isalpha(word[0]) && word[0] != '_') {
        return 0;
    }
    for (int i = 1; word[i] != '\0'; i++) {
        if (!isalnum(word[i]) && word[i] != '_') {
            return 0;
        }
    }
    return 1;
}

// Function to process a line and extract tokens
void processLine(char *line) {
    char *token = strtok(line, " \t\n");
    while (token != NULL) {
        if (isKeyword(token)) {
            printf("Keyword: %s\n", token);
        } else if (isOperator(token)) {
            printf("Operator: %s\n", token);
        } else if (isIdentifier(token)) {
            printf("Identifier: %s\n", token);
        } else if (strlen(token) == 1 && isSpecialCharacter(token[0])) {
            printf("Special Character: %s\n", token);
        } else {
            printf("Lexeme: %s\n", token);
        }
        token = strtok(NULL, " \t\n");
    }
} 

// Function to process comments
void processComments(FILE *file) {
    char line[100];
    while (fgets(line, 100, file)) {
        if (strstr(line, "//")) {
            printf("Comment: %s", line);
        } else if (strstr(line, "/*")) {
            printf("Multiline Comment Start: %s", line);
            while (fgets(line, 100, file) && !strstr(line, "*/")) {
                printf("%s", line);
            }
            printf("Multiline Comment End\n");
        }
    }
}

// Main function
int main() {
    // Load keywords, operators, and special characters
    loadTokens("keywords.txt", keywords, &keyword_count);
    loadTokens("operators.txt", operators, &operator_count);
    loadTokens("special.txt", specialChars, &special_count);

    FILE *file = fopen("example.txt", "r");

    char line[100];
    printf("Processing tokens in example.txt:\n");

    while (fgets(line, 100, file)) {
        processLine(line);
    }

    // Reopen file to check for comments separately
    fclose(file);
    file = fopen("example.txt", "r");
    printf("\nProcessing comments in example.txt:\n");
    processComments(file);

    fclose(file);
    return 0;
}