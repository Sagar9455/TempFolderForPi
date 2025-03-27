# Compiler
CC = gcc

# Compiler Flags
CFLAGS = -Wall -Wextra -g

# Source Files
SRCS = main.c can_utils.c display_utils.c

# Object Files
OBJS = $(SRCS:.c=.o)

# Executable Name
TARGET = rpi_app

# Build the project
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(TARGET)

# Compile individual .c files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean Build
clean:
	rm -f $(OBJS) $(TARGET)
